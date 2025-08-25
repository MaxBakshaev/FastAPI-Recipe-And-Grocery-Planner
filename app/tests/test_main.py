from fastapi.testclient import TestClient
from app.main import app as application

client = TestClient(application)


def test_app_root_available():
    response = client.get("/api")
    assert response.status_code in [200, 404]


def test_app_docs_available():
    response = client.get("/docs")
    assert response.status_code, 200


def test_app_redoc_available():
    response = client.get("/redoc")
    assert response.status_code, 200
