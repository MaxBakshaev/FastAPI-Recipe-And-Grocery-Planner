from unittest.mock import patch
from fastapi.testclient import TestClient

from main import application, run
from core import settings


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


def test_default_prefix_available():
    response = client.get(settings.api.prefix)
    assert response.status_code, 200


@patch("uvicorn.run")
def test_run_with_default_args(mock_uvicorn_run):
    """
    Проверяет, что сервер запускается с параметрами,
    совпадающими с настройками из конфига settings
    """
    run()
    args, kwargs = mock_uvicorn_run.call_args
    assert args[0] == "main:application"
    assert kwargs["host"] == settings.run.host
    assert kwargs["port"] == settings.run.port
