from fastapi.testclient import TestClient

from app.main import app
from app.services.auth import create_access_token

client = TestClient(app)


def test_get_all_users_success():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.get("/api/v1/admin/users",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


def test_get_all_users_fail():
    access_token = create_access_token(data={"sub": "user"})
    response = client.get("/api/v1/admin/users",
                          headers={"Authorization": f"Bearer {access_token}"}
                          )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}


def test_get_user_success():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.get("/api/v1/admin/users/1",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


def test_get_user_fail():
    access_token = create_access_token(data={"sub": "user"})
    response = client.get("/api/v1/admin/users/1",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}


def test_get_user_fail_not_found():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.get("/api/v1/admin/users/100",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404


def test_create_user_success():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.post("/api/v1/admin/users",
                           headers={"Authorization": f"Bearer {access_token}"},
                           json={"username": "testuser",
                                 "email": "testuser@test.com",
                                 "password": "password",
                                 "is_admin": False,
                                 "name": "Test",
                                 "surname": "User",
                                 "year": 1,
                                 "section": "A",
                                 "specialisation_id": 1})
    assert response.status_code == 200


def test_create_user_fail():
    access_token = create_access_token(data={"sub": "user"})
    response = client.post("/api/v1/admin/users",
                           headers={"Authorization": f"Bearer {access_token}"},
                           json={"username": "testuser1",
                                 "email": "testuser1@test.com",
                                 "password": "password",
                                 "is_admin": False,
                                 "name": "Test",
                                 "surname": "User",
                                 "year": 1,
                                 "section": "A",
                                 "specialisation_id": 1})
    assert response.status_code == 403


def test_update_user_success():
    from app.database import get_db
    from app.models.user import User

    db = next(get_db())
    user = db.query(User).filter(User.username == "testuser").first()
    access_token = create_access_token(data={"sub": "admin"})
    response = client.put(f"/api/v1/admin/users/{user.id}",
                          headers={"Authorization": f"Bearer {access_token}"},
                          json={"username": "testuser",
                                "email": "test@test.com",
                                "password": "password",
                                "is_admin": False,
                                "name": "NewName",
                                "surname": "NewUsername",
                                "year": 1,
                                "section": "A",
                                "specialisation_id": 1})
    assert response.status_code == 200


def test_update_user_fail():
    access_token = create_access_token(data={"sub": "user"})
    response = client.put("/api/v1/admin/users/1",
                          headers={"Authorization": f"Bearer {access_token}"},
                          json={"username": "testuser1",
                                "email": "testuser1@test.com",
                                "password": "password",
                                "is_admin": False,
                                "name": "NewName",
                                "surname": "NewUsername",
                                "year": 1,
                                "section": "A",
                                "specialisation_id": 1})
    assert response.status_code == 403


def test_update_user_fail_not_found():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.put("/api/v1/admin/users/100",
                          headers={"Authorization": f"Bearer {access_token}"},
                          json={"username": "testuser",
                                "email": "test@test.com",
                                "password": "password",
                                "is_admin": False,
                                "name": "NewName",
                                "surname": "NewUsername",
                                "year": 1,
                                "section": "A",
                                "specialisation_id": 1})
    assert response.status_code == 404


def test_delete_user_fail():
    from app.database import get_db
    from app.models.user import User

    db = next(get_db())
    user = db.query(User).filter(User.username == "testuser").first()

    access_token = create_access_token(data={"sub": "user"})
    response = client.delete(f"/api/v1/admin/users/{user.id}",
                             headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user_fail_not_found():
    access_token = create_access_token(data={"sub": "admin"})
    response = client.delete("/api/v1/admin/users/100",
                             headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_success():
    from app.database import get_db
    from app.models.user import User

    db = next(get_db())
    user = db.query(User).filter(User.username == "testuser").first()

    access_token = create_access_token(data={"sub": "admin"})
    response = client.delete(f"/api/v1/admin/users/{user.id}",
                             headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
