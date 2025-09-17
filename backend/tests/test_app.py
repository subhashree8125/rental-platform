import pytest
from backend.app import create_app


@pytest.fixture
def app():
    """Create a Flask app instance for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,  # disable CSRF for testing forms
    })
    return app


@pytest.fixture
def client(app):
    """Test client for simulating requests."""
    return app.test_client()


# ---------------------------
# ROUTE TESTS
# ---------------------------

def test_ping(client):
    """Check if backend is alive."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert "BrokLink backend is running" in response.json["message"]


def test_index(client):
    """Test home page renders."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data  # HTML page content


def test_signup_page(client):
    """Test GET signup page loads."""
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Signup" in response.data or b"signup" in response.data


def test_login_page(client):
    """Test GET login page loads."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data or b"login" in response.data


def test_explore_page(client):
    """Test explore page is accessible without login."""
    response = client.get("/explore")
    assert response.status_code == 200
    assert b"Explore" in response.data or b"explore" in response.data
