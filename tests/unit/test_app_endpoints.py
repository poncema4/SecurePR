from app.app import app


def client():
    return app.test_client()


def test_home_endpoint():
    response = client().get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "service": "SecurePR sample application",
        "status": "running",
    }


def test_valid_login_returns_authenticated_response():
    response = client().post(
        "/login",
        json={"username": "demo", "password": "securepr-demo-password"},
    )
    assert response.status_code == 200
    assert response.get_json() == {"authenticated": True, "username": "demo"}


def test_admin_login_returns_authenticated_response():
    response = client().post(
        "/login",
        json={"username": "admin", "password": "securepr-admin-password"},
    )
    assert response.status_code == 200
    assert response.get_json()["username"] == "admin"


def test_login_rejects_wrong_password():
    response = client().post(
        "/login",
        json={"username": "demo", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.get_json() == {"error": "invalid credentials"}


def test_login_rejects_unknown_user():
    response = client().post(
        "/login",
        json={"username": "unknown", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_login_rejects_non_string_username():
    response = client().post(
        "/login",
        json={"username": 123, "password": "securepr-demo-password"},
    )
    assert response.status_code == 400


def test_login_rejects_non_string_password():
    response = client().post(
        "/login",
        json={"username": "demo", "password": 123},
    )
    assert response.status_code == 400


def test_login_rejects_empty_json_body():
    response = client().post("/login", json={})
    assert response.status_code == 401


def test_profile_returns_existing_user():
    response = client().get("/users/demo")
    assert response.status_code == 200
    assert response.get_json() == {"username": "demo", "role": "user"}


def test_profile_returns_admin_role():
    response = client().get("/users/admin")
    assert response.status_code == 200
    assert response.get_json()["role"] == "admin"


def test_profile_returns_not_found_for_unknown_user():
    response = client().get("/users/not-a-user")
    assert response.status_code == 404


def test_search_accepts_normal_input():
    response = client().get("/search?q=security")
    assert response.status_code == 200
    assert response.get_json() == {"query": "security", "results": []}


def test_search_accepts_empty_input():
    response = client().get("/search")
    assert response.status_code == 200
    assert response.get_json()["query"] == ""


def test_search_rejects_oversized_input():
    response = client().get("/search?q=" + ("A" * 101))
    assert response.status_code == 400
    assert response.get_json() == {"error": "query too long"}


def test_search_accepts_maximum_allowed_input():
    response = client().get("/search?q=" + ("A" * 100))
    assert response.status_code == 200
