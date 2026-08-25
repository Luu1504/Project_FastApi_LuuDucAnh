from datetime import datetime, timedelta, timezone
from app.db.database import SessionLocal
from app.core.security import hash_password
from app.models import User, Club, ClubMember, ClubActivity


def seed_data():
    db = SessionLocal()
    try:
        # Xoa du lieu cu de seed moi
        db.query(ClubActivity).delete()
        db.query(ClubMember).delete()
        db.query(Club).delete()
        db.query(User).delete()
        db.commit()

        # 1. Tai khoan ADMIN (1 user)
        admin = User(
            email="admin@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Admin He Thong",
            role="ADMIN",
            is_active=True,
        )

        # 2. Tai khoan OWNER (2 chu nhiem CLB)
        owner1 = User(
            email="owner1@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Nguyen Van Chu Nhiem 1",
            role="USER",
            is_active=True,
        )
        owner2 = User(
            email="owner2@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Tran Thi Chu Nhiem 2",
            role="USER",
            is_active=True,
        )

        # 3. Tai khoan MEMBER (3 thanh vien da vao CLB)
        member1 = User(
            email="member1@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Le Van Member 1",
            role="USER",
            is_active=True,
        )
        member2 = User(
            email="member2@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Pham Thi Member 2",
            role="USER",
            is_active=True,
        )
        member3 = User(
            email="member3@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Hoang Van Member 3",
            role="USER",
            is_active=True,
        )

        # 4. Tai khoan TU DO (2 sinh vien chua tham gia CLB nao)
        free_user1 = User(
            email="student1@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Do Van Sinh Vien Tu Do 1",
            role="USER",
            is_active=True,
        )
        free_user2 = User(
            email="student2@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Vu Thi Sinh Vien Tu Do 2",
            role="USER",
            is_active=True,
        )

        db.add_all([admin, owner1, owner2, member1, member2, member3, free_user1, free_user2])
        db.commit()
        for u in [owner1, owner2, member1, member2, member3]:
            db.refresh(u)

        # 5. Tao 2 Cau lac bo
        club_code = Club(
            name="CLB Lap Trinh PTIT",
            description="CLB nghien cuu va phat trien phan mem",
            owner_id=owner1.id,
        )
        club_media = Club(
            name="CLB Truyen Thong PTIT",
            description="CLB to chuc su kien va truyen thong",
            owner_id=owner2.id,
        )
        db.add_all([club_code, club_media])
        db.commit()
        db.refresh(club_code)
        db.refresh(club_media)

        # 6. Gan thanh vien vao CLB (Bang ClubMember)
        # CLB Lap Trinh: owner1 (OWNER), member1 (MEMBER), member2 (MEMBER)
        cm1 = ClubMember(club_id=club_code.id, user_id=owner1.id, role="OWNER")
        cm2 = ClubMember(club_id=club_code.id, user_id=member1.id, role="MEMBER")
        cm3 = ClubMember(club_id=club_code.id, user_id=member2.id, role="MEMBER")

        # CLB Truyen Thong: owner2 (OWNER), member2 (MEMBER), member3 (MEMBER)
        cm4 = ClubMember(club_id=club_media.id, user_id=owner2.id, role="OWNER")
        cm5 = ClubMember(club_id=club_media.id, user_id=member2.id, role="MEMBER")
        cm6 = ClubMember(club_id=club_media.id, user_id=member3.id, role="MEMBER")

        db.add_all([cm1, cm2, cm3, cm4, cm5, cm6])
        db.commit()

        # 7. Tao Hoat dong / Cong viec mau (ClubActivity)
        now = datetime.now(timezone.utc)
        act1 = ClubActivity(
            club_id=club_code.id,
            title="Lap trinh Backend FastAPI",
            description="Xay dung he thong quan ly CLB",
            assignee_id=member1.id,
            status="IN_PROGRESS",
            priority="HIGH",
            due_date=now + timedelta(days=7),
        )
        act2 = ClubActivity(
            club_id=club_media.id,
            title="Thiet ke poster su kien",
            description="Lam truyen thong cho chuong trinh chao tan sinh vien",
            assignee_id=member3.id,
            status="TODO",
            priority="MEDIUM",
            due_date=now + timedelta(days=14),
        )
        db.add_all([act1, act2])
        db.commit()

        print("Seed data successfully: 1 Admin, 2 Owners, 3 Members, 2 Free Users, 2 Clubs!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
