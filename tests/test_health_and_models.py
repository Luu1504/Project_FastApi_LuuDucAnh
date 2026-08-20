from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.models import User, Club, ClubMember, ClubActivity


def test_health_check_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_api_v1_health_check_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["docs"] == "/docs"


def test_password_hash_and_verify():
    plain = "secret123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_create_and_decode():
    user_id = 99
    token = create_access_token(user_id=user_id)
    payload = decode_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"
    assert "exp" in payload


def test_models_relationships(db_session):
    user = User(
        email="test@ptit.edu.vn",
        password_hash=hash_password("123456"),
        full_name="Nguyen Van Test",
        role="USER",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.id is not None

    club = Club(
        name="CLB Test PTIT",
        description="Mo ta test",
        owner_id=user.id,
    )
    db_session.add(club)
    db_session.commit()
    db_session.refresh(club)
    assert club.id is not None
    assert club.owner.id == user.id

    member = ClubMember(
        club_id=club.id,
        user_id=user.id,
        role="OWNER",
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)
    assert member.id is not None
    assert member.user.id == user.id
    assert member.club.id == club.id

    activity = ClubActivity(
        club_id=club.id,
        title="Hoat dong test",
        description="Mo ta hoat dong",
        assignee_id=user.id,
        status="TODO",
        priority="HIGH",
    )
    db_session.add(activity)
    db_session.commit()
    db_session.refresh(activity)
    assert activity.id is not None
    assert activity.assignee.id == user.id
    assert activity.club.id == club.id
