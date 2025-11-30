"""add the tables

Revision ID: e55a57ba42cc
Revises: 
Create Date: 2025-11-29 14:37:30.029600

"""

import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel  # added

from alembic import op

# revision identifiers, used by Alembic.
revision = "e55a57ba42cc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # --------------------------
    # Topic table
    # --------------------------
    op.create_table(
        "Topic",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Topic_name"), "Topic", ["name"], unique=True)
    op.create_index(op.f("ix_Topic_id"), "Topic", ["id"], unique=True)

    # --------------------------
    # Subscriber table
    # --------------------------
    op.create_table(
        "Subscriber",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Subscriber_email"), "Subscriber", ["email"], unique=True)
    op.create_index(op.f("ix_Subscriber_id"), "Subscriber", ["id"], unique=True)

    # --------------------------
    # Subscription table
    # --------------------------
    op.create_table(
        "Subscription",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("subscriber_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("topic_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["subscriber_id"], ["Subscriber.id"]),
        sa.ForeignKeyConstraint(["topic_id"], ["Topic.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Subscription_id"), "Subscription", ["id"], unique=True)
    op.create_index(
        op.f("ix_Subscription_subscriber_id"),
        "Subscription",
        ["subscriber_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_Subscription_topic_id"),
        "Subscription",
        ["topic_id"],
        unique=False,
    )

    # --------------------------
    # Content table
    # --------------------------
    op.create_table(
        "Content",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("topic_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("subject", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("body", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("scheduled_time", sa.DateTime(), nullable=False),
        sa.Column("sent", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["Topic.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Content_id"), "Content", ["id"], unique=True)
    op.create_index(
        op.f("ix_Content_topic_id"),
        "Content",
        ["topic_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_Content_scheduled_time"),
        "Content",
        ["scheduled_time"],
        unique=False,
    )

    # --------------------------
    # DeliveryLog table
    # --------------------------
    op.create_table(
        "DeliveryLog",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("content_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("subscriber_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("error", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["content_id"], ["Content.id"]),
        sa.ForeignKeyConstraint(["subscriber_id"], ["Subscriber.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_DeliveryLog_id"), "DeliveryLog", ["id"], unique=True)
    op.create_index(
        op.f("ix_DeliveryLog_content_id"),
        "DeliveryLog",
        ["content_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_DeliveryLog_subscriber_id"),
        "DeliveryLog",
        ["subscriber_id"],
        unique=False,
    )


def downgrade() -> None:
    # Drop order matters due to FKs
    op.drop_table("DeliveryLog")
    op.drop_table("Content")
    op.drop_table("Subscription")
    op.drop_table("Subscriber")
    op.drop_table("Topic")
