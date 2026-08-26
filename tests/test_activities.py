def test_create_activity_and_pagination(client):
    # 1. Register Owner & Create Club
    client.post("/api/v1/auth/register", json={
        "email": "act_owner@ptit.edu.vn",
        "password": "password123",
        "full_name": "Activity Owner"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "act_owner@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    club_id = client.post("/api/v1/clubs", json={
        "name": "CLB Test Activity",
        "description": "Desc"
    }, headers=headers).json()["id"]

    # 2. Create 3 Activities
    for i in range(1, 4):
        res = client.post(f"/api/v1/clubs/{club_id}/activities", json={
            "title": f"Activity {i}",
            "description": f"Desc {i}",
            "priority": "HIGH" if i == 1 else "MEDIUM"
        }, headers=headers)
        assert res.status_code == 201

    # 3. Get Paginated Activities (page 1, page_size 2)
    paginated_res = client.get(f"/api/v1/clubs/{club_id}/activities?page=1&page_size=2", headers=headers)
    assert paginated_res.status_code == 200
    data = paginated_res.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2

    # 4. Search Activity by title
    search_res = client.get(f"/api/v1/clubs/{club_id}/activities?search=Activity 1", headers=headers)
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["total"] == 1
    assert search_data["items"][0]["title"] == "Activity 1"

    # 5. Filter Activity by priority
    filter_res = client.get(f"/api/v1/clubs/{club_id}/activities?priority=HIGH", headers=headers)
    assert filter_res.status_code == 200
    filter_data = filter_res.json()
    assert filter_data["total"] == 1


def test_update_and_delete_activity(client):
    # 1. Register Owner & Create Club
    client.post("/api/v1/auth/register", json={
        "email": "owner_up@ptit.edu.vn",
        "password": "password123",
        "full_name": "Owner Up"
    })
    token = client.post("/api/v1/auth/login", json={
        "email": "owner_up@ptit.edu.vn",
        "password": "password123"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    club_id = client.post("/api/v1/clubs", json={
        "name": "CLB Update Test",
        "description": "Desc"
    }, headers=headers).json()["id"]

    # 2. Create Activity
    act_id = client.post(f"/api/v1/clubs/{club_id}/activities", json={
        "title": "Task To Update",
        "description": "Before update"
    }, headers=headers).json()["id"]

    # 3. Update Activity Status to DONE
    up_res = client.put(f"/api/v1/activities/{act_id}", json={
        "status": "DONE",
        "title": "Task Done"
    }, headers=headers)
    assert up_res.status_code == 200
    assert up_res.json()["status"] == "DONE"
    assert up_res.json()["title"] == "Task Done"

    # 4. Delete Activity
    del_res = client.delete(f"/api/v1/activities/{act_id}", headers=headers)
    assert del_res.status_code == 200
