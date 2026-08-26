# Đồ Án: Hệ Thống Quản Lý Câu Lạc Bộ Sinh Viên (FastAPI Backend)

Hệ thống Backend RESTful API phục vụ quản lý hoạt động câu lạc bộ sinh viên, phân quyền người dùng (Admin, Chủ nhiệm CLB, Thành viên) và theo dõi công việc.

---

## 🛠️ Công Nghệ Sử Dụng

- **Ngôn ngữ:** Python 3.10+
- **Framework:** FastAPI
- **Cơ sở dữ liệu:** SQLite / SQLAlchemy ORM
- **Xác thực & Bảo mật:** Bcrypt (băm mật khẩu) & PyJWT (JWT Bearer Token)
- **Kiểm tra dữ liệu:** Pydantic v2
- **Kiểm thử:** Pytest

---

## 📁 Cấu Trúc Thư Mục

```text
Project/
├── app/
│   ├── main.py                     # Khởi tạo FastAPI app, CORS, Exception handler
│   ├── core/
│   │   ├── config.py               # Đọc cấu hình từ file .env
│   │   └── security.py             # Băm mật khẩu bcrypt và mã hóa/giải mã JWT
│   ├── db/
│   │   ├── database.py             # Kết nối Database và session SQLAlchemy (get_db)
│   │   ├── init_db.py              # Script khởi tạo bảng CSDL
│   │   └── seed.py                 # Script nạp dữ liệu mẫu ban đầu
│   ├── models/
│   │   ├── user.py                 # Bảng User
│   │   ├── club.py                 # Bảng Club và ClubMember
│   │   └── activity.py             # Bảng ClubActivity
│   ├── schemas/
│   │   ├── user.py                 # Pydantic Schemas cho User & Auth
│   │   ├── club.py                 # Pydantic Schemas cho Club & Member
│   │   └── activity.py             # Pydantic Schemas cho Activity
│   ├── dependencies/
│   │   └── auth.py                 # Dependency get_current_user và require_admin
│   └── routers/
│       ├── health.py               # API kiểm tra kết nối hệ thống
│       ├── auth.py                 # API Đăng ký, Đăng nhập
│       ├── users.py                # API Profile cá nhân, Quản lý tài khoản (Admin)
│       ├── club.py                 # API Quản lý CLB & Thành viên
│       └── activity.py             # API Quản lý công việc CLB
├── tests/
│   ├── conftest.py                 # Cấu hình test database SQLite in-memory
│   ├── test_health_and_models.py   # Test kết nối & model
│   ├── test_auth_and_users.py      # Test xác thực & phân quyền
│   ├── test_clubs.py               # Test chức năng CLB & Thành viên
│   └── test_activities.py          # Test chức năng hoạt động & phân trang
├── .env                            # Biến môi trường
├── requirements.txt                # Danh sách thư viện
└── README.md                       # Tài liệu hướng dẫn
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Kích hoạt môi trường ảo (.venv)
- **PowerShell:**
  ```powershell
  ..\.venv\Scripts\Activate.ps1
  ```
- **Command Prompt (CMD):**
  ```cmd
  ..\.venv\Scripts\activate.bat
  ```

### 2. Cài đặt thư viện (nếu cần)
```bash
pip install -r requirements.txt
```

### 3. Khởi tạo Database & Nạp dữ liệu mẫu
```bash
python -m app.db.init_db
python -m app.db.seed
```

### 4. Khởi chạy Server
```bash
uvicorn app.main:app --reload
```

Sau khi chạy, truy cập tài liệu Swagger UI tại: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 👥 Danh Sách Tài Khoản Mẫu (Mật khẩu chung: `123456`)

| STT | Nhóm Tài Khoản | Họ và Tên | Email | Vai trò trong hệ thống |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **ADMIN (1 user)** | Admin Hệ Thống | `admin@ptit.edu.vn` | Quản trị viên toàn trường (Xem mọi User & CLB) |
| 2 | **OWNER 1 (Chủ nhiệm)** | Nguyễn Văn Chủ Nhiệm 1 | `owner1@ptit.edu.vn` | Chủ nhiệm **CLB Lập Trình** |
| 3 | **OWNER 2 (Chủ nhiệm)** | Trần Thị Chủ Nhiệm 2 | `owner2@ptit.edu.vn` | Chủ nhiệm **CLB Truyền Thông** |
| 4 | **MEMBER 1 (Thành viên)** | Lê Văn Member 1 | `member1@ptit.edu.vn` | Thành viên CLB Lập Trình |
| 5 | **MEMBER 2 (Thành viên)** | Phạm Thị Member 2 | `member2@ptit.edu.vn` | Thành viên cả 2 CLB |
| 6 | **MEMBER 3 (Thành viên)** | Hoàng Văn Member 3 | `member3@ptit.edu.vn` | Thành viên CLB Truyền Thông |
| 7 | **TỰ DO 1 (Chưa vào CLB)** | Đỗ Văn Sinh Viên Tự Do 1 | `student1@ptit.edu.vn` | Sinh viên tự do (Chưa tham gia CLB nào) |
| 8 | **TỰ DO 2 (Chưa vào CLB)** | Vũ Thị Sinh Viên Tự Do 2 | `student2@ptit.edu.vn` | Sinh viên tự do (Chưa tham gia CLB nào) |

---

## 📌 Các Nhóm Chức Năng Chính (Chuẩn Cốt Lõi)

1. **Authentication & User:**
   - Đăng ký tài khoản mới (`POST /auth/register`)
   - Đăng nhập lấy Bearer Token (`POST /auth/login`)
   - Xem thông tin cá nhân (`GET /users/me`)
   - Xem danh sách người dùng (`GET /users` - Admin)
   - Xem chi tiết người dùng (`GET /users/{id}`)
   - Cập nhật thông tin người dùng (`PUT /users/{id}`)
   - Xóa tài khoản (`DELETE /users/{id}` - Admin)

2. **Quản lý Câu Lạc Bộ & Thành Viên:**
   - Tạo CLB mới (`POST /clubs`) - Người tạo tự động thành `OWNER`
   - Xem danh sách CLB (`GET /clubs`)
   - Xem chi tiết CLB & danh sách thành viên (`GET /clubs/{id}`)
   - Xem danh sách thành viên trong CLB (`GET /clubs/{id}/members`)
   - Cập nhật thông tin CLB (`PUT /clubs/{id}` - Chỉ Owner/Admin)
   - Xóa CLB (`DELETE /clubs/{id}` - Chỉ Owner/Admin)
   - Thêm thành viên vào CLB (`POST /clubs/{id}/members`)
   - Xóa thành viên khỏi CLB (`DELETE /clubs/{id}/members/{user_id}`)

3. **Quản lý Hoạt Động (Activities):**
   - Tạo hoạt động trong CLB (`POST /clubs/{club_id}/activities`)
   - Xem danh sách hoạt động có Tìm kiếm, Lọc trạng thái/ưu tiên & Phân trang (`GET /clubs/{club_id}/activities`)
   - Xem chi tiết hoạt động (`GET /activities/{id}`)
   - Cập nhật hoạt động (`PUT /activities/{id}`)
   - Xóa hoạt động (`DELETE /activities/{id}`)

4. **Hệ Thống:**
   - Kiểm tra kết nối Server & Database (`GET /health`)

---

## 🧪 Kiểm Thử Tự Động (Tests)

Chạy bộ kiểm thử tự động bằng lệnh:
```bash
pytest -v
```
