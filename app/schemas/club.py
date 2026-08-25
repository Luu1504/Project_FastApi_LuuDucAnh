from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserResponse


class ClubCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ClubMemberCreate(BaseModel):
    user_id: int
    role: Optional[str] = "MEMBER"


class ClubMemberResponse(BaseModel):
    id: int
    club_id: int
    user_id: int
    role: str
    joined_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ClubResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime
    owner: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ClubDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime
    owner: Optional[UserResponse] = None
    members: List[ClubMemberResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TransferOwnerRequest(BaseModel):
    new_owner_id: int
