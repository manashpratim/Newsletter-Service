"""make scheduled_time column in Content table time zone aware

Revision ID: a37befc37752
Revises: e55a57ba42cc
Create Date: 2025-11-30 10:59:02.983527

"""

import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel  # added

from alembic import op

# revision identifiers, used by Alembic.
revision = "a37befc37752"
down_revision = "e55a57ba42cc"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "Content",
        "scheduled_time",
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "Content",
        "scheduled_time",
        type_=sa.DateTime(timezone=False),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
