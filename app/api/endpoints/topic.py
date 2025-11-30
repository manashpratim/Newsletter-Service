from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

from app import crud
from app.models.topic_model import Topic
from app.schemas.response_schema import (IDeleteResponseBase, IGetResponseBase,
                                         IPostResponseBase, IPutResponseBase,
                                         create_response)
from app.schemas.topic_schema import TopicCreate, TopicRead, TopicUpdate
from app.utils.exceptions.common_exceptions import (CustomException,
                                                    DataValidationError,
                                                    IdNotFoundException)

router = APIRouter()


@router.get("/list")
async def list_topics(
    params: Params = Depends(),
) -> IGetResponseBase[List[TopicRead]]:

    topics = await crud.topic.get_all()
    return create_response(data=topics)


@router.get("/get-by-id/{topic_id}")
async def get_topic_by_id(
    topic_id: UUID,
) -> IGetResponseBase[TopicRead]:
    topic = await crud.topic.get_by_id(id=topic_id)
    if not topic:
        return IdNotFoundException(Topic, topic_id).get_response()
    return create_response(data=topic)


@router.get("/get-by-name")
async def get_topic_by_name(
    name: str,
) -> IGetResponseBase[TopicRead]:
    topic = await crud.topic.get_by_name(name=name)
    if not topic:
        return CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Topic with name '{name}' not found.",
        ).get_response()
    return create_response(data=topic)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_topic(payload: TopicCreate) -> IPostResponseBase[TopicRead]:
    existing = await crud.topic.get_by_name(name=payload.name)
    if existing:
        return CustomException(
            status_code=status.HTTP_409_CONFLICT,
            message=f"Topic with name '{payload.name}' already exists.",
        ).get_response()

    created = await crud.topic.create(obj_in=payload)
    return create_response(data=created)


@router.put("/update/{topic_id}", status_code=status.HTTP_200_OK)
async def update_topic(
    topic_id: UUID,
    payload: TopicUpdate,
) -> IPutResponseBase[TopicRead]:
    current = await crud.topic.get_by_id(id=topic_id)
    if not current:
        return IdNotFoundException(Topic, topic_id).get_response()

    if getattr(payload, "name", None) and payload.name != current.name:
        conflict = await crud.topic.get_by_name(name=payload.name)
        if conflict:
            return CustomException(
                status_code=status.HTTP_409_CONFLICT,
                message=f"Another topic already uses the name '{payload.name}'.",
            ).get_response()

    updated = await crud.topic.update(obj_current=current, obj_new=payload)
    return create_response(data=updated)


@router.delete("/delete/{topic_id}", status_code=status.HTTP_200_OK)
async def delete_topic(
    topic_id: UUID,
) -> IDeleteResponseBase:
    current = await crud.topic.get_by_id(id=topic_id)
    if not current:
        return IdNotFoundException(Topic, topic_id).get_response()

    contents = await crud.content.get_by_topic_id(topic_id=topic_id)
    subs = await crud.subscription.get_for_topic(topic_id=topic_id)
    if contents:
        return DataValidationError(
            message="Topic has content items. Delete contents first or archive topic."
        ).get_response()
    if subs:
        return DataValidationError(
            message="Topic has active subscribers. Unsubscribe users before deleting."
        ).get_response()

    deleted_topic = await crud.topic.remove(obj_current=current)

    return create_response(data={"deleted": True, "topic_id": str(topic_id)})
