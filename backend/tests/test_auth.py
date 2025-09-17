import pytest
from backend.app import create_app, db
from backend.models.users import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # in-memory DB for testing

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_signup(client):
    response = client.post("/signup", json={
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "1234",
        "mobile_number": "9876543210"
    })

    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"


def test_login_success(client):
    # First create a user
    client.post("/signup", json={
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "1234",
        "mobile_number": "9999999999"
    })

    # Now login
    response = client.post("/login", json={
        "email": "login@example.com",
        "password": "1234"
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"


def test_login_failure(client):
    response = client.post("/login", json={
        "email": "notfound@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"



