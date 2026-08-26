from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserResponse


class ActivityCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    priority: Optional[str] = "MEDIUM"
    due_date: Optional[datetime] = None


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class ActivityStatusUpdate(BaseModel):
    status: str


class ActivityResponse(BaseModel):
    id: int
    club_id: int
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    created_at: datetime
    assignee: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ActivityStatsResponse(BaseModel):
    total: int
    todo: int
    in_progress: int
    done: int
    completion_rate: float


class PaginatedActivityResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ActivityResponse]
