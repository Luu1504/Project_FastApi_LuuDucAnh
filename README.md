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
│   ├── main.py                     # Khởi tạo ứng dụng FastAPI, CORS và xử lý lỗi tập trung
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
│       ├── health.py               # API kiểm tra trạng thái hệ thống
│       ├── auth.py                 # API Đăng ký, Đăng nhập
│       ├── users.py                # API Profile cá nhân, Quản lý tài khoản (Admin)
│       ├── club.py                 # API Quản lý CLB & Thành viên
│       └── activity.py             # API Quản lý công việc CLB
├── tests/
│   ├── conftest.py                 # Cấu hình test database SQLite in-memory
│   ├── test_health_and_models.py   # Test kết nối & model
│   ├── test_auth_and_users.py      # Test xác thực & phân quyền
│   └── test_clubs.py               # Test chức năng CLB & Thành viên
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

## 📌 Các Nhóm Chức Năng Chính

1. **Authentication & User:**
   - Đăng ký tài khoản mới (`POST /api/v1/auth/register`)
   - Đăng nhập lấy Bearer Token (`POST /api/v1/auth/login`)
   - Xem thông tin cá nhân (`GET /api/v1/users/me`)
   - Xem danh sách người dùng, tìm kiếm & lọc trạng thái (`GET /api/v1/users` - Admin)

2. **Quản lý Câu Lạc Bộ & Thành Viên:**
   - Tạo CLB mới (`POST /api/v1/clubs`) - Người tạo tự động thành `OWNER`
   - Xem danh sách CLB (`GET /api/v1/clubs`)
   - Xem chi tiết CLB & danh sách thành viên (`GET /api/v1/clubs/{id}`)
   - Cập nhật thông tin CLB (`PUT /api/v1/clubs/{id}` - Chỉ Owner/Admin)
   - Xóa CLB (`DELETE /api/v1/clubs/{id}` - Chỉ Owner/Admin)
   - Thêm thành viên vào CLB (`POST /api/v1/clubs/{id}/members`)
   - Xóa thành viên khỏi CLB (`DELETE /api/v1/clubs/{id}/members/{user_id}`)
   - Tự rời CLB (`POST /api/v1/clubs/{id}/leave`)
   - Chuyển quyền Chủ nhiệm (`POST /api/v1/clubs/{id}/transfer-owner`)

3. **Hệ Thống:**
   - Kiểm tra kết nối Server & Database (`GET /api/v1/health`)

---

## 🧪 Kiểm Thử Tự Động (Tests)

Chạy bộ kiểm thử tự động bằng lệnh:
```bash
pytest -v
```
