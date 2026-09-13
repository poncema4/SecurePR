from app.app import app


def test_login_rejects_missing_json_body():
    response = app.test_client().post("/login", data="not-json", content_type="text/plain")
    assert response.status_code == 401


def test_login_rejects_null_username():
    response = app.test_client().post(
        "/login",
        json={"username": None, "password": "securepr-demo-password"},
    )
    assert response.status_code == 400


def test_login_rejects_null_password():
    response = app.test_client().post(
        "/login",
        json={"username": "demo", "password": None},
    )
    assert response.status_code == 400


def test_search_rejects_101_character_query():
    response = app.test_client().get("/search?q=" + ("x" * 101))
    assert response.status_code == 400


def test_search_boundary_at_100_characters_is_allowed():
    response = app.test_client().get("/search?q=" + ("x" * 100))
    assert response.status_code == 200
