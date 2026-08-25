from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.club import Club, ClubMember
from app.models.user import User
from app.schemas.club import (
    ClubCreate,
    ClubUpdate,
    ClubResponse,
    ClubDetailResponse,
    ClubMemberCreate,
    ClubMemberResponse,
    TransferOwnerRequest,
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/clubs", tags=["Clubs"])


@router.post("", response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
def create_club(
    data: ClubCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(Club).filter(Club.name == data.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ten CLB da ton tai")

    new_club = Club(
        name=data.name,
        description=data.description,
        owner_id=current_user.id,
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club)

    owner_member = ClubMember(
        club_id=new_club.id,
        user_id=current_user.id,
        role="OWNER",
    )
    db.add(owner_member)
    db.commit()

    return new_club


@router.get("", response_model=List[ClubResponse], status_code=status.HTTP_200_OK)
def get_clubs(
    search: Optional[str] = Query(None, description="Tim kiem theo ten CLB"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == "ADMIN":
        query = db.query(Club)
    else:
        user_club_ids = [
            cm.club_id for cm in db.query(ClubMember.club_id).filter(ClubMember.user_id == current_user.id).all()
        ]
        query = db.query(Club).filter(Club.id.in_(user_club_ids))

    if search:
        query = query.filter(Club.name.ilike(f"%{search}%"))

    return query.all()


@router.get("/{club_id}", response_model=ClubDetailResponse, status_code=status.HTTP_200_OK)
def get_club_detail(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    is_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == current_user.id,
    ).first()

    if current_user.role != "ADMIN" and not is_member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Ban khong phai thanh vien cua CLB nay")

    return club


@router.put("/{club_id}", response_model=ClubResponse, status_code=status.HTTP_200_OK)
def update_club(
    club_id: int,
    data: ClubUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Chi OWNER moi co quyen chinh sua CLB")

    if data.name is not None:
        existing = db.query(Club).filter(
            Club.name == data.name, Club.id != club_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Ten CLB da ton tai")
        club.name = data.name

    if data.description is not None:
        club.description = data.description

    db.commit()
    db.refresh(club)
    return club


@router.delete("/{club_id}", status_code=status.HTTP_200_OK)
def delete_club(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Chi OWNER moi co quyen xoa CLB")

    db.delete(club)
    db.commit()
    return {"message": "Xoa CLB thanh cong"}


@router.post("/{club_id}/members", response_model=ClubMemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(
    club_id: int,
    data: ClubMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Chi OWNER moi co quyen them thanh vien")

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User khong ton tai")

    existing_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == data.user_id,
    ).first()
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Nguoi dung da la thanh vien CLB")

    new_member = ClubMember(
        club_id=club_id,
        user_id=data.user_id,
        role=data.role or "MEMBER",
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.delete("/{club_id}/members/{user_id}", status_code=status.HTTP_200_OK)
def remove_member(
    club_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Chi OWNER moi co quyen xoa thanh vien")

    if user_id == club.owner_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Khong the xoa OWNER khoi CLB")

    member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == user_id,
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Thanh vien khong ton tai trong CLB")

    db.delete(member)
    db.commit()
    return {"message": "Da xoa thanh vien khoi CLB"}


@router.post("/{club_id}/leave", status_code=status.HTTP_200_OK)
def leave_club(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if club.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OWNER khong the roi CLB, vui long chuyen quyen hoac giai tan CLB",
        )

    member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == current_user.id,
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Ban khong phai thanh vien cua CLB nay")

    db.delete(member)
    db.commit()
    return {"message": "Ban da roi CLB thanh cong"}


@router.post("/{club_id}/transfer-owner", status_code=status.HTTP_200_OK)
def transfer_owner(
    club_id: int,
    data: TransferOwnerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="CLB khong ton tai")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Chi OWNER moi co quyen chuyen nhuong")

    new_owner_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == data.new_owner_id,
    ).first()
    if not new_owner_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nguoi duoc chuyen quyen phai la thanh vien trong CLB",
        )

    old_owner_member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == club.owner_id,
    ).first()
    if old_owner_member:
        old_owner_member.role = "MEMBER"

    club.owner_id = data.new_owner_id
    new_owner_member.role = "OWNER"

    db.commit()
    return {"message": f"Da chuyen quyen OWNER sang user_id = {data.new_owner_id}"}
