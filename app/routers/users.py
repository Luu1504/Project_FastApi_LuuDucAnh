from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(
    search: Optional[str] = Query(None, description="Tim kiem theo ten hoac email"),
    is_active: Optional[bool] = Query(None, description="Loc theo trang thai"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    if search:
        query = query.filter((User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()
