import pytest
from ..app import create_app
from typing import Any

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app: Any):
    return app.test_client()

def test_ping(client: Any):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["message"] == "BrokLink backend is running 🚀"