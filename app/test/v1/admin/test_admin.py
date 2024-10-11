from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_admin_root():
    response = client.get("/api/v1/admin/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the admin root path"}
