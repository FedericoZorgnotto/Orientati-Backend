from fastapi.testclient import TestClient

from app.main import app
from app.services.auth import create_access_token, create_refresh_token

client = TestClient(app)


def test_auth_login_success():
    # curl - X
    # 'POST' \
    # 'http://127.0.0.1:8000/api/v1/login' \
    # - H
    # 'accept: application/json' \
    # - H
    # 'Content-Type: application/x-www-form-urlencoded' \
    # - d
    # 'grant_type=password&username=user&password=user&scope=&client_id=string&client_secret=string'
    response = client.post(
        "/api/v1/login",
        data={
            "grant_type": "password",
            "username": "user",
            "password": "user",
            "scope": "",
            "client_id": "string",
            "client_secret": "string",
        },
    )

    assert response.status_code == 200

    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_auth_login_fail():
    response = client.post(
        "/api/v1/login",
        data={
            "grant_type": "password",
            "username": "user",
            "password": "wrong_password",
            "scope": "",
            "client_id": "string",
            "client_secret": "string",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_auth_login_empty():
    response = client.post(
        "/api/v1/login",
        data={
            "grant_type": "password",
            "username": "",
            "password": "",
            "scope": "",
            "client_id": "string",
            "client_secret": "string",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_auth_login_nodata():
    response = client.post(
        "/api/v1/login",
        data={},
    )

    assert response.status_code == 422


def test_auth_refresh_token_fail():
    response = client.post(
        "/api/v1/token/refresh",
        json={"refresh_token": "wrong_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_auth_refresh_token_empty():
    response = client.post(
        "/api/v1/token/refresh",
        json={},
    )

    assert response.status_code == 422


def test_auth_refresh_token_success():
    refresh_token = create_refresh_token(data={"sub": "user"})

    response = client.post(
        "/api/v1/token/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_auth_users_me_fail():
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer wrong_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_auth_users_me_success():
    access_token = create_access_token(data={"sub": "user"})

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert "username" in response.json()
    assert "admin" in response.json()
    assert "temporaneo" in response.json()
    assert "connessoAGruppo" in response.json()


def test_change_password_success():
    access_token = create_access_token(data={"sub": "user"})

    response = client.post(
        "/api/v1/users/me/change_password",
        json={"old_password": "user", "new_password": "new_password"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/users/me/change_password",
        json={"old_password": "new_password", "new_password": "user"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200


def test_change_password_fail_no_token():
    response = client.post(
        "/api/v1/users/me/change_password",
        json={"old_password": "user", "new_password": "new_password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_change_password_fail_wrong_token():
    response = client.post(
        "/api/v1/users/me/change_password",
        json={"old_password": "user", "new_password": "new_password"},
        headers={"Authorization": "Bearer wrong_token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_change_password_fail_wrong_password():
    access_token = create_access_token(data={"sub": "user"})

    response = client.post(
        "/api/v1/users/me/change_password",
        json={"old_password": "wrong_password",
              "new_password": "new_password"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Old password is incorrect"}
