from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from app.schemas.response_schema import ErrorDetail, IResponseBase

ModelType = TypeVar("ModelType", bound=SQLModel)


class IdNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        id: Optional[Union[UUID, str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Generate a detailed error message
        detail_message = (
            f"Unable to find the {model.__name__} with id {id}."
            if id
            else f"{model.__name__} id not found."
        )

        # Call parent constructor
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_message,
            headers=headers,
        )

        # Additional attributes for the exception
        self.model = model
        self.object_id = id

    def get_response(self) -> JSONResponse:
        """
        Returns a JSONResponse that conforms to the IResponseBase structure.
        """
        return JSONResponse(
            status_code=self.status_code,
            content=IResponseBase(
                message="Resource not found",
                data=None,
                error=ErrorDetail(
                    code=self.status_code,
                    message=self.detail,
                ),
            ).dict(),
        )


class NameNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__name__} named {name}.",
                headers=headers,
            )
        else:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__name__} name not found.",
                headers=headers,
            )


class NameExistException(HTTPException, Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        name: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The {model.__name__} name {name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The {model.__name__} name already exists.",
            headers=headers,
        )


class CustomException(HTTPException):
    def __init__(self, message="An error occurred", status_code=400):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.status_code = status_code

    def get_response(self) -> JSONResponse:
        """
        Returns a JSONResponse with a structured error message.
        """
        return JSONResponse(
            status_code=self.status_code,
            content=IResponseBase(
                message="An error occurred",
                data=None,
                error=ErrorDetail(
                    code=self.status_code,
                    message=self.message,
                ),
            ).dict(),
        )


class DatabaseConnectionError(CustomException):
    """Raised when the database connection fails"""

    def __init__(self, message="Could not connect to the database", status_code=500):
        super().__init__(message, status_code)


class DataValidationError(CustomException):
    """Raised when data validation fails"""

    def __init__(self, message="Data validation error", status_code=422):
        super().__init__(message, status_code)


class ProcessError(CustomException):
    """Raised when a process fails or any service breaks"""

    def __init__(self, message="Process failure error", status_code=500):
        # Call the parent constructor with message and status_code
        super().__init__(message, status_code)


class EntityNotFoundError(CustomException):
    """Raised when an entity is not found"""

    def __init__(self, message="Entity Not Found error", status_code=404):
        super().__init__(message, status_code)


class AuthorizationError(CustomException):
    """Raised when unauthorized request is made"""

    def __init__(self, message="Unauthorized request", status_code=401):
        super().__init__(message, status_code)
