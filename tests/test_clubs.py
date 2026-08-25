def test_create_club_and_owner_membership(client):
    # 1. Register & Login User
    client.post("/api/v1/auth/register", json={
        "email": "clubowner@ptit.edu.vn",
        "password": "password123",
        "full_name": "Club Owner"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "clubowner@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Club
    res = client.post("/api/v1/clubs", json={
        "name": "CLB Robot PTIT",
        "description": "Nghien cuu robotics"
    }, headers=headers)
    assert res.status_code == 201
    club_id = res.json()["id"]

    # 3. Get Club Detail
    detail_res = client.get(f"/api/v1/clubs/{club_id}", headers=headers)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["name"] == "CLB Robot PTIT"
    assert len(detail["members"]) == 1
    assert detail["members"][0]["role"] == "OWNER"


def test_add_and_remove_member_in_club(client):
    # 1. Register & Login President
    client.post("/api/v1/auth/register", json={
        "email": "pres_test@ptit.edu.vn",
        "password": "password123",
        "full_name": "President Test"
    })
    pres_token = client.post("/api/v1/auth/login", json={
        "email": "pres_test@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]
    pres_headers = {"Authorization": f"Bearer {pres_token}"}

    # 2. Create New User to add
    new_user = client.post("/api/v1/auth/register", json={
        "email": "member_to_add@ptit.edu.vn",
        "password": "password123",
        "full_name": "Member To Add"
    }).json()
    new_user_id = new_user["id"]

    # 3. President creates club
    club_id = client.post("/api/v1/clubs", json={
        "name": "CLB AI PTIT",
        "description": "CLB AI"
    }, headers=pres_headers).json()["id"]

    # 4. President adds member
    add_res = client.post(f"/api/v1/clubs/{club_id}/members", json={
        "user_id": new_user_id,
        "role": "MEMBER"
    }, headers=pres_headers)
    assert add_res.status_code == 201

    # 5. President removes member
    del_res = client.delete(f"/api/v1/clubs/{club_id}/members/{new_user_id}", headers=pres_headers)
    assert del_res.status_code == 200


def test_non_owner_cannot_update_or_delete_club(client):
    # 1. Register & Login President, Create Club
    client.post("/api/v1/auth/register", json={
        "email": "pres_owner@ptit.edu.vn",
        "password": "password123",
        "full_name": "President Owner"
    })
    pres_token = client.post("/api/v1/auth/login", json={
        "email": "pres_owner@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]
    club_id = client.post("/api/v1/clubs", json={
        "name": "CLB Private PTIT",
        "description": "Private"
    }, headers={"Authorization": f"Bearer {pres_token}"}).json()["id"]

    # 2. Register & Login Member 1
    client.post("/api/v1/auth/register", json={
        "email": "member_attacker@ptit.edu.vn",
        "password": "password123",
        "full_name": "Attacker"
    })
    m1_token = client.post("/api/v1/auth/login", json={
        "email": "member_attacker@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]
    m1_headers = {"Authorization": f"Bearer {m1_token}"}

    # 3. Member 1 tries to delete club -> 403 Forbidden
    del_res = client.delete(f"/api/v1/clubs/{club_id}", headers=m1_headers)
    assert del_res.status_code == 403

    # 4. Member 1 tries to update club -> 403 Forbidden
    up_res = client.put(f"/api/v1/clubs/{club_id}", json={"name": "Hacked Name"}, headers=m1_headers)
    assert up_res.status_code == 403
