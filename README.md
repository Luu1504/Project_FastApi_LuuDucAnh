# Student Club Management API (FastAPI Backend)

Hệ thống RESTful API Quản lý Câu lạc bộ Sinh viên (Student Club Management API) được xây dựng bằng **FastAPI**, **SQLAlchemy** và **MySQL / SQLite**, tuân thủ cấu trúc module hóa chuẩn công nghiệp theo đặc tả phân rã công việc.

---

## 📁 1. Cấu trúc thư mục dự án

```text
Project/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Khởi tạo FastAPI app, lifespan, CORS, middleware, routers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic Settings đọc cấu hình từ .env
│   │   ├── security.py             # Hash mật khẩu (bcrypt) và mã hóa/giải mã JWT token
│   │   └── exceptions.py           # Custom exceptions & handlers format JSON error chuẩn
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py             # SQLAlchemy engine, SessionLocal, Base, get_db dependency
│   │   ├── init_db.py              # Script khởi tạo bảng cơ sở dữ liệu
│   │   └── seed.py                 # Script seed dữ liệu mẫu (User, Club, Member, Activity)
│   ├── models/
│   │   ├── __init__.py             # Export toàn bộ models
│   │   ├── user.py                 # Model User & Enum UserRole (USER, ADMIN)
│   │   ├── club.py                 # Model Club, ClubMember & Enum ClubRole (OWNER, MEMBER)
│   │   └── activity.py             # Model ClubActivity & Enums ActivityStatus, ActivityPriority
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                 # Pydantic schemas cho User (Base, Create, Update, Response)
│   │   ├── club.py                 # Pydantic schemas cho Club & ClubMember
│   │   ├── activity.py             # Pydantic schemas cho ClubActivity
│   │   └── common.py               # StandardResponse, ErrorResponse, HealthCheckResponse
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py               # Health check endpoints (/health, /api/v1/health)
│   │   ├── auth.py                 # Router Auth (chuẩn bị cho Tiết 2)
│   │   ├── users.py                # Router Users (chuẩn bị cho Tiết 2)
│   │   ├── club.py                 # Router Club (chuẩn bị cho Tiết 3)
│   │   └── activity.py             # Router Activity (chuẩn bị cho Tiết 4)
│   ├── services/
│   │   └── __init__.py             # Business logic layer
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── db.py                   # get_db dependency
│   │   └── auth.py                 # get_current_user & role guard dependencies
│   └── utils/
│       └── __init__.py             # Utilities & helper functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Test fixtures & in-memory SQLite setup
│   └── test_health_and_models.py   # Test suite kiểm thử toàn diện Tiết 1
├── .env                            # Biến môi trường hiện tại
├── .env.example                    # Mẫu biến môi trường
├── requirements.txt                # Danh sách thư viện phụ thuộc
└── README.md                       # Tài liệu hướng dẫn dự án
```

---

## ⚙️ 2. Cài đặt & Cấu hình môi trường

### Bước 1: Kích hoạt môi trường ảo (.venv)
Môi trường ảo đã được tạo sẵn trong thư mục gốc. Để kích hoạt:
* **Trên PowerShell (Windows):**
  ```powershell
  ..\.venv\Scripts\Activate.ps1
  ```
* **Hoặc Command Prompt (CMD):**
  ```cmd
  ..\.venv\Scripts\activate.bat
  ```

### Bước 2: Cài đặt thư viện (nếu cần cập nhật thêm)
```bash
python -m pip install -r requirements.txt
```

### Bước 3: Cấu hình biến môi trường (`.env`)
File `.env` mặc định sử dụng SQLite để chạy ngay không cần cài đặt MySQL:
```env
DATABASE_URL=sqlite:///./club_management.db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_STR=/api/v1
PROJECT_NAME=Student Club Management API
```

---

## 🗄️ 3. Khởi tạo Database & Seed Dữ Liệu Mẫu

### 1. Khởi tạo các bảng Database
Đứng tại thư mục `Project`:
```bash
python -m app.db.init_db
```

### 2. Nạp dữ liệu mẫu (Seed Data)
```bash
python -m app.db.seed
```

> **Tài khoản mẫu sau khi seed:**
> - **Admin**: `admin@ptit.edu.vn` | Password: `123456` (Role: ADMIN)
> - **Chủ nhiệm**: `president@ptit.edu.vn` | Password: `123456` (Role: USER / Club OWNER)
> - **Thành viên 1**: `member1@ptit.edu.vn` | Password: `123456` (Role: USER / Club MEMBER)
> - **Thành viên 2**: `member2@ptit.edu.vn` | Password: `123456` (Role: USER / Club MEMBER)

---

## 🚀 4. Khởi chạy Server FastAPI

Chạy lệnh sau tại thư mục `Project`:
```bash
python -m uvicorn app.main:app --reload --port 8000
```

Sau khi server chạy, bạn truy cập:
* **Swagger UI API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Health Check API**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 5. Chạy Test Tự Động (Pytest)

Chạy lệnh sau tại thư mục `Project`:
```bash
python -m pytest -v
```

---

## 📊 Bảng tiến độ Task Tiết 1 (Day 1) theo File Sheet

| STT | Nhóm Task | Nhiệm vụ chi tiết | Mức độ | Điểm | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Khởi tạo dự án | Cấu trúc source module hóa: routers, models, schemas, services, dependencies, core, db | Bắt buộc | 2 | ✅ Hoàn thành |
| 2 | Khởi tạo dự án | Cấu hình môi trường `.env`, `.env.example`, Pydantic Settings đọc config | Bắt buộc | 2 | ✅ Hoàn thành |
| 3 | Database | Kết nối MySQL/SQLite bằng SQLAlchemy, `engine`, `SessionLocal`, dependency `get_db` | Bắt buộc | 2 | ✅ Hoàn thành |
| 4 | Database | Thiết kế model `User`, `Club`, `ClubMember`, `ClubActivity` với đầy đủ quan hệ, khóa ngoại | Bắt buộc | 3 | ✅ Hoàn thành |
| 5 | Database | Pydantic schemas (Base, Create, Update, Response) với `from_attributes = True` | Bắt buộc | 2 | ✅ Hoàn thành |
| 6 | Database | Khởi tạo bảng tự động qua SQLAlchemy metadata (`init_db.py`) | Bắt buộc | 2 | ✅ Hoàn thành |
| 7 | Core | Custom Exception handling (400, 403, 404, 422, 500) format chuẩn và endpoint `/health` | Bắt buộc | 2 | ✅ Hoàn thành |
| 8 | Nâng cao | Script seed dữ liệu mẫu (`seed.py`) | Không bắt buộc | 5 (Bonus) | ✅ Hoàn thành |
| **Tổng** | | | | **20 / 20** | **100% Hoàn thành** |
