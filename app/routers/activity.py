from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.activity import ClubActivity
from app.models.club import Club, ClubMember
from app.models.user import User
from app.schemas.activity import (
    ActivityCreate,
    ActivityUpdate,
    ActivityStatusUpdate,
    ActivityResponse,
    ActivityStatsResponse,
    PaginatedActivityResponse,
)
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Activities"])


@router.post("/clubs/{club_id}/activities", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    club_id: int,
    data: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    is_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == current_user.id,
    ).first()

    if current_user.role != "ADMIN" and not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong phai thanh vien cua CLB nay")

    if data.assignee_id:
        assignee_member = db.query(ClubMember).filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == data.assignee_id,
        ).first()
        if not assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nguoi duoc giao viec phai la thanh vien cua CLB",
            )

    new_activity = ClubActivity(
        club_id=club_id,
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        priority=data.priority or "MEDIUM",
        due_date=data.due_date,
        status="TODO",
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


@router.get("/clubs/{club_id}/activities", response_model=PaginatedActivityResponse, status_code=status.HTTP_200_OK)
def get_club_activities(
    club_id: int,
    search: Optional[str] = Query(None, description="Tim kiem theo tieu de hoat dong"),
    status_filter: Optional[str] = Query(None, alias="status", description="Loc theo trang thai (TODO, IN_PROGRESS, DONE)"),
    priority_filter: Optional[str] = Query(None, alias="priority", description="Loc theo muc do uu tien (LOW, MEDIUM, HIGH)"),
    page: int = Query(1, ge=1, description="So trang (bat dau tu 1)"),
    page_size: int = Query(10, ge=1, le=100, description="So luong moi trang"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    is_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == current_user.id,
    ).first()

    if current_user.role != "ADMIN" and not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong phai thanh vien cua CLB nay")

    query = db.query(ClubActivity).filter(ClubActivity.club_id == club_id)

    if search:
        query = query.filter(ClubActivity.title.ilike(f"%{search}%"))

    if status_filter:
        query = query.filter(ClubActivity.status == status_filter.upper())

    if priority_filter:
        query = query.filter(ClubActivity.priority == priority_filter.upper())

    total = query.count()
    skip = (page - 1) * page_size
    items = query.offset(skip).limit(page_size).all()

    return PaginatedActivityResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get("/clubs/{club_id}/activities/stats", response_model=ActivityStatsResponse, status_code=status.HTTP_200_OK)
def get_club_activity_stats(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    is_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == current_user.id,
    ).first()

    if current_user.role != "ADMIN" and not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong phai thanh vien cua CLB nay")

    total = db.query(ClubActivity).filter(ClubActivity.club_id == club_id).count()
    todo = db.query(ClubActivity).filter(ClubActivity.club_id == club_id, ClubActivity.status == "TODO").count()
    in_progress = db.query(ClubActivity).filter(ClubActivity.club_id == club_id, ClubActivity.status == "IN_PROGRESS").count()
    done = db.query(ClubActivity).filter(ClubActivity.club_id == club_id, ClubActivity.status == "DONE").count()

    completion_rate = round((done / total * 100), 2) if total > 0 else 0.0

    return ActivityStatsResponse(
        total=total,
        todo=todo,
        in_progress=in_progress,
        done=done,
        completion_rate=completion_rate,
    )


@router.get("/activities/my-activities", response_model=List[ActivityResponse], status_code=status.HTTP_200_OK)
def get_my_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activities = db.query(ClubActivity).filter(ClubActivity.assignee_id == current_user.id).all()
    return activities


@router.get("/activities/{activity_id}", response_model=ActivityResponse, status_code=status.HTTP_200_OK)
def get_activity_detail(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoat dong khong ton tai")

    is_member = db.query(ClubMember).filter(
        ClubMember.club_id == activity.club_id,
        ClubMember.user_id == current_user.id,
    ).first()

    if current_user.role != "ADMIN" and not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ban khong co quyen xem hoat dong nay")

    return activity


@router.put("/activities/{activity_id}", response_model=ActivityResponse, status_code=status.HTTP_200_OK)
def update_activity(
    activity_id: int,
    data: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoat dong khong ton tai")

    club = db.query(Club).filter(Club.id == activity.club_id).first()
    is_owner = club and club.owner_id == current_user.id
    is_assignee = activity.assignee_id == current_user.id

    if current_user.role != "ADMIN" and not is_owner and not is_assignee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chi OWNER, nguoi duoc giao viec hoac ADMIN moi co quyen sua hoat dong")

    if data.title is not None:
        activity.title = data.title
    if data.description is not None:
        activity.description = data.description
    if data.status is not None:
        activity.status = data.status.upper()
    if data.priority is not None:
        activity.priority = data.priority.upper()
    if data.due_date is not None:
        activity.due_date = data.due_date
    if data.assignee_id is not None:
        if data.assignee_id > 0:
            assignee_member = db.query(ClubMember).filter(
                ClubMember.club_id == activity.club_id,
                ClubMember.user_id == data.assignee_id,
            ).first()
            if not assignee_member:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nguoi duoc giao viec phai la thanh vien cua CLB")
            activity.assignee_id = data.assignee_id
        else:
            activity.assignee_id = None

    db.commit()
    db.refresh(activity)
    return activity


@router.patch("/activities/{activity_id}/status", response_model=ActivityResponse, status_code=status.HTTP_200_OK)
def update_activity_status(
    activity_id: int,
    data: ActivityStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoat dong khong ton tai")

    club = db.query(Club).filter(Club.id == activity.club_id).first()
    is_owner = club and club.owner_id == current_user.id
    is_assignee = activity.assignee_id == current_user.id

    if current_user.role != "ADMIN" and not is_owner and not is_assignee:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chi OWNER, nguoi duoc giao viec hoac ADMIN moi co quyen sua trang thai")

    activity.status = data.status.upper()
    db.commit()
    db.refresh(activity)
    return activity


@router.delete("/activities/{activity_id}", status_code=status.HTTP_200_OK)
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    activity = db.query(ClubActivity).filter(ClubActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hoat dong khong ton tai")

    club = db.query(Club).filter(Club.id == activity.club_id).first()
    is_owner = club and club.owner_id == current_user.id

    if current_user.role != "ADMIN" and not is_owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chi OWNER cua CLB hoac ADMIN moi co quyen xoa hoat dong")

    db.delete(activity)
    db.commit()
    return {"message": "Xoa hoat dong thanh cong"}
