from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status
from fastapi_pagination import Params

from app import crud
from app.models.content_model import Content
from app.models.topic_model import Topic
from app.schemas.content_schema import (ContentCreate, ContentRead,
                                        ContentUpdate)
from app.schemas.response_schema import (IDeleteResponseBase, IGetResponseBase,
                                         IPostResponseBase, IPutResponseBase,
                                         create_response)
from app.utils.exceptions.common_exceptions import (CustomException,
                                                    DataValidationError,
                                                    IdNotFoundException)

router = APIRouter()


@router.get("/list")
async def list_contents(
    topic_id: Optional[UUID] = None,
    params: Params = Depends(),
) -> IGetResponseBase[List[ContentRead]]:

    if topic_id:
        items = await crud.content.get_by_topic_id(topic_id=topic_id)
    else:
        items = await crud.content.get_all()
    return create_response(data=items)


@router.get("/get-by-id/{content_id}")
async def get_content_by_id(
    content_id: UUID,
) -> IGetResponseBase[ContentRead]:
    content = await crud.content.get_by_id(id=content_id)
    if not content:
        return IdNotFoundException(Content, content_id).get_response()
    return create_response(data=content)


@router.get("/list/by-topic/{topic_id}")
async def list_by_topic(
    topic_id: UUID,
) -> IGetResponseBase[List[ContentRead]]:
    topic = await crud.topic.get_by_id(id=topic_id)
    if not topic:
        return IdNotFoundException(Topic, topic_id).get_response()
    contents = await crud.content.get_by_topic_id(topic_id=topic_id)
    return create_response(data=contents)


@router.get("/list/pending")
async def list_pending_contents(
    as_of: Optional[datetime] = None,
) -> IGetResponseBase[List[ContentRead]]:
    """
    Return contents scheduled to be sent <= as_of (default now UTC) and not marked sent.
    """
    as_of = as_of or datetime.now(timezone.utc)
    pending = await crud.content.get_pending_to_send(as_of=as_of)
    return create_response(data=pending)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_content(
    payload: ContentCreate,
) -> IPostResponseBase[ContentRead]:

    topic = await crud.topic.get_by_id(id=payload.topic_id)
    if not topic:
        return CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Topic with id {payload.topic_id} not found.",
        ).get_response()

    created = await crud.content.create(obj_in=payload)

    run_time = payload.scheduled_time

    if run_time.tzinfo is None:
        run_time = run_time.replace(tzinfo=timezone.utc)

    return create_response(data=created)


@router.put("/update/{content_id}", status_code=status.HTTP_200_OK)
async def update_content(
    content_id: UUID,
    payload: ContentUpdate,
) -> IPutResponseBase[ContentRead]:
    current = await crud.content.get_by_id(id=content_id)
    if not current:
        return IdNotFoundException(Content, content_id).get_response()

    if getattr(current, "sent", False):
        return DataValidationError(
            message="Cannot modify content that is already sent"
        ).get_response()

    original_run_time = getattr(current, "scheduled_time", None)
    updated = await crud.content.update(obj_current=current, obj_new=payload)

    return create_response(data=updated)


@router.delete("/delete/{content_id}", status_code=status.HTTP_200_OK)
async def delete_content(
    content_id: UUID,
) -> IDeleteResponseBase:
    current = await crud.content.get_by_id(id=content_id)
    if not current:
        return IdNotFoundException(Content, content_id).get_response()

    if getattr(current, "sent", False):
        return DataValidationError(
            message="Cannot delete content that has already been sent"
        ).get_response()

    delete_c = crud.content.remove(obj_current=current)

    return create_response(data={"deleted": True, "content_id": str(content_id)})
