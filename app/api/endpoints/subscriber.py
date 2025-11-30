from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Params
from sqlmodel import select

from app import crud
from app.models.subscriber_model import Subscriber
from app.schemas.response_schema import (IDeleteResponseBase, IGetResponseBase,
                                         IPostResponseBase, IPutResponseBase,
                                         create_response)
from app.schemas.subscriber_schema import (SubscriberCreate, SubscriberRead,
                                           SubscriberUpdate)
from app.schemas.subscription_schema import (SubscriptionCreate,
                                             SubscriptionRead)
from app.utils.exceptions.common_exceptions import (CustomException,
                                                    DataValidationError,
                                                    IdNotFoundException)

router = APIRouter()


@router.get("/list")
async def list_subscribers(
    params: Params = Depends(),
) -> IGetResponseBase[List[SubscriberRead]]:

    subscribers = await crud.subscriber.get_all()
    return create_response(data=subscribers)


@router.get("/get-by-id/{subscriber_id}")
async def get_subscriber_by_id(
    subscriber_id: UUID,
) -> IGetResponseBase[SubscriberRead]:
    subscriber = await crud.subscriber.get_by_id(id=subscriber_id)
    if not subscriber:
        return IdNotFoundException(Subscriber, subscriber_id).get_response()
    return create_response(data=subscriber)


@router.get("/get-by-email")
async def get_subscriber_by_email(
    email: str,
) -> IGetResponseBase[SubscriberRead]:
    subscriber = await crud.subscriber.get_by_email(email=email)
    if not subscriber:
        return CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Subscriber with email '{email}' not found.",
        ).get_response()
    return create_response(data=subscriber)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_subscriber(
    payload: SubscriberCreate,
) -> IPostResponseBase[SubscriberRead]:

    existing = await crud.subscriber.get_by_email(email=payload.email)
    if existing:
        return CustomException(
            status_code=status.HTTP_409_CONFLICT,
            message="Subscriber already exists with this email.",
        ).get_response()

    created = await crud.subscriber.create(obj_in=payload)
    return create_response(data=created)


@router.put("/update/{subscriber_id}", status_code=status.HTTP_200_OK)
async def update_subscriber(
    subscriber_id: UUID,
    payload: SubscriberUpdate,
) -> IPutResponseBase[SubscriberRead]:
    current = await crud.subscriber.get_by_id(id=subscriber_id)
    if not current:
        return IdNotFoundException(Subscriber, subscriber_id).get_response()

    if getattr(payload, "email", None) and payload.email != current.email:
        conflict = await crud.subscriber.get_by_email(email=payload.email)
        if conflict:
            return CustomException(
                status_code=status.HTTP_409_CONFLICT,
                message="Another subscriber already uses this email.",
            ).get_response()

    updated = await crud.subscriber.update(obj_current=current, obj_new=payload)
    return create_response(data=updated)


@router.post("/subscribe/{subscriber_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_to_topic(
    subscriber_id: UUID,
    payload: SubscriptionCreate,
) -> IPostResponseBase[SubscriptionRead]:

    subscriber = await crud.subscriber.get_by_id(id=subscriber_id)
    if not subscriber:
        return IdNotFoundException(Subscriber, subscriber_id).get_response()

    topic = await crud.topic.get_by_id(id=payload.topic_id)
    if not topic:
        return CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Topic with id {payload.topic_id} not found.",
        ).get_response()

    existing = await crud.subscription.get_for_subscriber(subscriber_id=subscriber_id)
    if any(s.topic_id == payload.topic_id for s in existing):
        return CustomException(
            status_code=status.HTTP_409_CONFLICT,
            message="Subscriber is already subscribed to this topic.",
        ).get_response()

    created = await crud.subscription.create(
        obj_in=(
            payload
            if getattr(payload, "subscriber_id", None)
            else SubscriptionCreate(
                subscriber_id=subscriber_id, topic_id=payload.topic_id
            )
        )
    )
    return create_response(data=created)


@router.delete("/unsubscribe/{subscription_id}", status_code=status.HTTP_200_OK)
async def unsubscribe_by_subscription_id(
    subscription_id: UUID,
) -> IDeleteResponseBase:
    subscription = await crud.subscription.get_by_id(id=subscription_id)
    if not subscription:
        return CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Subscription with id {subscription_id} not found.",
        ).get_response()

    delete_sub = await crud.subscription.remove(obj_current=subscription)

    return create_response(
        data={"deleted": True, "subscription_id": str(subscription.id)}
    )
