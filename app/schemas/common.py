from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any, List

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "Thành công"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    status: str = "error"
    code: int
    message: str
    details: Optional[Any] = None


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    version: str
    database: str
    timestamp: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
