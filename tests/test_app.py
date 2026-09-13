from app.app import app, authenticate


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_valid_login():
    assert authenticate("demo", "securepr-demo-password") is True


def test_invalid_login():
    assert authenticate("demo", "wrong-password") is False


def test_login_endpoint_rejects_invalid_credentials():
    client = app.test_client()
    response = client.post(
        "/login",
        json={"username": "demo", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_profile_returns_existing_user():
    client = app.test_client()
    response = client.get("/users/demo")
    assert response.status_code == 200
    assert response.get_json()["username"] == "demo"


def test_profile_returns_not_found_for_unknown_user():
    client = app.test_client()
    response = client.get("/users/not-a-user")
    assert response.status_code == 404


def test_search_rejects_oversized_input():
    client = app.test_client()
    response = client.get("/search?q=" + ("A" * 101))
    assert response.status_code == 400


def test_search_accepts_normal_input():
    client = app.test_client()
    response = client.get("/search?q=security")
    assert response.status_code == 200
    assert response.get_json()["query"] == "security"
