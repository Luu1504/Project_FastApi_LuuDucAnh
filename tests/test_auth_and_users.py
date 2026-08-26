from app.models.user import User


def test_register_user_success(client):
    payload = {
        "email": "newuser@ptit.edu.vn",
        "password": "password123",
        "full_name": "Nguyen Van New",
        "role": "USER"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@ptit.edu.vn"
    assert data["full_name"] == "Nguyen Van New"
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    payload = {
        "email": "dup@ptit.edu.vn",
        "password": "password123",
        "full_name": "Nguyen Van Dup"
    }
    r1 = client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 400


def test_login_success_and_get_profile(client):
    # 1. Register
    client.post("/api/v1/auth/register", json={
        "email": "loginuser@ptit.edu.vn",
        "password": "password123",
        "full_name": "Login User"
    })

    # 2. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "loginuser@ptit.edu.vn",
        "password": "password123"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 3. Get /users/me with token
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/users/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "loginuser@ptit.edu.vn"


def test_get_profile_without_token(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_admin_get_users_list_and_user_crud(client):
    # 1. Register Admin
    client.post("/api/v1/auth/register", json={
        "email": "admin1@ptit.edu.vn",
        "password": "password123",
        "full_name": "Admin User",
        "role": "ADMIN"
    })
    login_admin = client.post("/api/v1/auth/login", json={
        "email": "admin1@ptit.edu.vn",
        "password": "password123"
    }).json()
    admin_token = login_admin["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Register Regular User
    user_res = client.post("/api/v1/auth/register", json={
        "email": "regular@ptit.edu.vn",
        "password": "password123",
        "full_name": "Regular User",
        "role": "USER"
    }).json()
    user_id = user_res["id"]
    login_user = client.post("/api/v1/auth/login", json={
        "email": "regular@ptit.edu.vn",
        "password": "password123"
    }).json()
    user_token = login_user["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 3. Regular user calling /users -> 403 Forbidden
    r_forbidden = client.get("/api/v1/users", headers=user_headers)
    assert r_forbidden.status_code == 403

    # 4. Admin calling /users -> 200 OK
    r_admin = client.get("/api/v1/users", headers=admin_headers)
    assert r_admin.status_code == 200
    users_list = r_admin.json()
    assert len(users_list) >= 2

    # 5. User detail
    u_detail = client.get(f"/api/v1/users/{user_id}", headers=user_headers)
    assert u_detail.status_code == 200
    assert u_detail.json()["full_name"] == "Regular User"

    # 6. Update user
    u_update = client.put(f"/api/v1/users/{user_id}", json={"full_name": "Updated Regular"}, headers=user_headers)
    assert u_update.status_code == 200
    assert u_update.json()["full_name"] == "Updated Regular"

    # 7. Admin lock user status
    status_res = client.patch(f"/api/v1/users/{user_id}/status", json={"is_active": False}, headers=admin_headers)
    assert status_res.status_code == 200
    assert status_res.json()["is_active"] is False

    # 8. Locked user cannot login
    locked_login = client.post("/api/v1/auth/login", json={"email": "regular@ptit.edu.vn", "password": "password123"})
    assert locked_login.status_code == 403
