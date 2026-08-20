from datetime import datetime, timedelta, timezone
from app.db.database import SessionLocal
from app.core.security import hash_password
from app.models import User, Club, ClubMember, ClubActivity


def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).first():
            return

        admin = User(
            email="admin@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Admin",
            role="ADMIN",
            is_active=True,
        )
        president = User(
            email="president@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Nguyen Van President",
            role="USER",
            is_active=True,
        )
        member1 = User(
            email="member1@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Tran Thi Member 1",
            role="USER",
            is_active=True,
        )
        member2 = User(
            email="member2@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Le Van Member 2",
            role="USER",
            is_active=True,
        )
        db.add_all([admin, president, member1, member2])
        db.commit()
        db.refresh(president)
        db.refresh(member1)
        db.refresh(member2)

        club_it = Club(
            name="CLB Tin Hoc PTIT",
            description="CLB hoc thuat lap trinh",
            owner_id=president.id,
        )
        club_media = Club(
            name="CLB Truyen Thong PTIT",
            description="CLB truyen thong",
            owner_id=president.id,
        )
        db.add_all([club_it, club_media])
        db.commit()
        db.refresh(club_it)
        db.refresh(club_media)

        cm1 = ClubMember(club_id=club_it.id, user_id=president.id, role="OWNER")
        cm2 = ClubMember(club_id=club_it.id, user_id=member1.id, role="MEMBER")
        cm3 = ClubMember(club_id=club_it.id, user_id=member2.id, role="MEMBER")
        cm4 = ClubMember(club_id=club_media.id, user_id=president.id, role="OWNER")
        cm5 = ClubMember(club_id=club_media.id, user_id=member1.id, role="MEMBER")
        db.add_all([cm1, cm2, cm3, cm4, cm5])
        db.commit()

        now = datetime.now(timezone.utc)
        act1 = ClubActivity(
            club_id=club_it.id,
            title="Hackathon 2026",
            description="Cuoc thi lap trinh",
            assignee_id=member1.id,
            status="IN_PROGRESS",
            priority="HIGH",
            due_date=now + timedelta(days=7),
        )
        act2 = ClubActivity(
            club_id=club_it.id,
            title="Workshop FastAPI",
            description="Chia se kien thuc backend",
            assignee_id=member2.id,
            status="TODO",
            priority="MEDIUM",
            due_date=now + timedelta(days=14),
        )
        db.add_all([act1, act2])
        db.commit()
        print("Seed data completed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
