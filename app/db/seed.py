from datetime import datetime, timedelta, timezone
from app.db.database import SessionLocal
from app.core.security import hash_password
from app.models import User, Club, ClubMember, ClubActivity


def seed_data():
    db = SessionLocal()
    try:
        # 0. Xoa sach du lieu cu
        db.query(ClubActivity).delete()
        db.query(ClubMember).delete()
        db.query(Club).delete()
        db.query(User).delete()
        db.commit()

        # =====================================================================
        # 1. TAI KHOAN NGUOI DUNG (USERS) - PASS CHUNG: "123456"
        # =====================================================================
        # Admin he thong (xem moi thu, xoa moi thu)
        admin = User(
            email="admin@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Admin He Thong",
            role="ADMIN",
            is_active=True,
        )

        # Manager (dung de test Cau 7 De 1: ca Admin va Manager xem /users)
        manager = User(
            email="manager@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Quan Ly Manager",
            role="MANAGER",
            is_active=True,
        )

        # Chu nhiem CLB (Owner)
        owner = User(
            email="owner@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Nguyen Chu Nhiem",
            role="USER",
            is_active=True,
        )

        # Thanh vien CLB (Member)
        member = User(
            email="member@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Le Thanh Vien",
            role="USER",
            is_active=True,
        )

        # Nguoi xem trong CLB (Viewer)
        viewer = User(
            email="viewer@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Pham Nguoi Xem",
            role="USER",
            is_active=True,
        )

        # Tai khoan BI KHOA (dung test Cau 15 De 1: chan user is_active=False)
        locked_user = User(
            email="locked@ptit.edu.vn",
            password_hash=hash_password("123456"),
            full_name="Tai Khoan Bi Khoa",
            role="USER",
            is_active=False,
        )

        # Sinh vien tu do (chua vao CLB nao - dung test them thanh vien)
        free_student = User(
            email="student@gmail.com",
            password_hash=hash_password("123456"),
            full_name="Tran Sinh Vien Tu Do",
            role="USER",
            is_active=True,
        )

        db.add_all([admin, manager, owner, member,
                   viewer, locked_user, free_student])
        db.commit()

        for u in [admin, manager, owner, member, viewer, locked_user, free_student]:
            db.refresh(u)

        # =====================================================================
        # 2. CAU LAC BO / CHIEN DICH (CLUBS / CAMPAIGNS)
        # =====================================================================
        club1 = Club(
            name="CLB Lap Trinh PTIT",
            description="CLB nghien cuu va phat trien ung dung phan mem cho sinh vien",
            owner_id=owner.id,
        )
        db.add(club1)
        db.commit()
        db.refresh(club1)

        # =====================================================================
        # 3. THANH VIEN TRONG CLB (CLUB MEMBERS)
        # =====================================================================
        cm_owner = ClubMember(club_id=club1.id, user_id=owner.id, role="OWNER")
        cm_member = ClubMember(
            club_id=club1.id, user_id=member.id, role="MEMBER")
        cm_viewer = ClubMember(
            club_id=club1.id, user_id=viewer.id, role="VIEWER")

        db.add_all([cm_owner, cm_member, cm_viewer])
        db.commit()

        # =====================================================================
        # 4. CONG VIEC / HOAT DONG (TASKS / ACTIVITIES)
        # =====================================================================
        now = datetime.now(timezone.utc)

        # Task 1: TODO, MEDIUM - co the xoa (test Cau 14 De 3)
        task_todo = ClubActivity(
            club_id=club1.id,
            title="Lap ke hoach su kien moi",
            description="Soan thao noi dung ke hoach to chuc buoi gap mat dau nam",
            assignee_id=member.id,
            status="TODO",
            priority="MEDIUM",
            due_date=now + timedelta(days=5),
        )

        # Task 2: IN_PROGRESS, HIGH - khong the xoa (test Cau 14 De 3)
        task_doing = ClubActivity(
            club_id=club1.id,
            title="Xay dung API Backend FastAPI",
            description="Lap trinh cac chuc nang xac thuc va phan quyen",
            assignee_id=member.id,
            status="IN_PROGRESS",
            priority="HIGH",
            due_date=now + timedelta(days=3),
        )

        # Task 3: DONE, URGENT - da hoan thanh (test completed_at, dem task done)
        task_done = ClubActivity(
            club_id=club1.id,
            title="Thiet ke co so du lieu PostgreSQL",
            description="Ve so do thuc the ERD va tao migrations",
            assignee_id=owner.id,
            status="DONE",
            priority="URGENT",
            due_date=now - timedelta(days=2),
            completed_at=now - timedelta(days=1),
        )

        # Task 4: TODO, LOW - TRE HAN (test Cau 12 De 3: is_overdue)
        task_overdue = ClubActivity(
            club_id=club1.id,
            title="Tong hop danh sach thanh vien cu",
            description="Kiem tra va doi soat so lieu sinh vien khoa truoc",
            assignee_id=viewer.id,
            status="TODO",
            priority="LOW",
            due_date=now - timedelta(days=1),  # Han chot o qua khu -> Qua han
        )

        db.add_all([task_todo, task_doing, task_done, task_overdue])
        db.commit()

        print("=" * 65)
        print("🎉 NAP DU LIEU MAU THANH CONG 100%! BANG TRA CUU KHI THI:")
        print("=" * 65)
        print("🔑 TAI KHOAN (PASS CHUNG: 123456):")
        print(
            f"  • ADMIN      : admin@ptit.edu.vn    (ID={admin.id}, Role=ADMIN)")
        print(
            f"  • MANAGER    : manager@ptit.edu.vn  (ID={manager.id}, Role=MANAGER)")
        print(
            f"  • OWNER CLB  : owner@ptit.edu.vn    (ID={owner.id}, Role=USER)")
        print(
            f"  • MEMBER     : member@ptit.edu.vn   (ID={member.id}, Role=USER)")
        print(
            f"  • VIEWER     : viewer@ptit.edu.vn   (ID={viewer.id}, Role=USER)")
        print(
            f"  • BI KHOA    : locked@ptit.edu.vn   (ID={locked_user.id}, is_active=False)")
        print(
            f"  • TU DO      : student@gmail.com    (ID={free_student.id}, domain=gmail.com)")
        print("-" * 65)
        print(
            f"🏢 CLB MAU     : ID={club1.id} (Owner ID={owner.id}, 3 Members)")
        print("📋 TASKS MAU   : 4 tasks (TODO, IN_PROGRESS, DONE, OVERDUE)")
        print("=" * 65)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
