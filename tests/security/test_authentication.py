from werkzeug.security import check_password_hash

from app.app import USERS, authenticate


def test_demo_password_authenticates():
    assert authenticate("demo", "securepr-demo-password") is True


def test_admin_password_authenticates():
    assert authenticate("admin", "securepr-admin-password") is True


def test_wrong_password_does_not_authenticate():
    assert authenticate("demo", "wrong-password") is False


def test_unknown_user_does_not_authenticate():
    assert authenticate("does-not-exist", "securepr-demo-password") is False


def test_passwords_are_stored_as_hashes_not_plaintext():
    assert USERS["demo"]["password_hash"] != "securepr-demo-password"
    assert USERS["admin"]["password_hash"] != "securepr-admin-password"


def test_stored_password_hashes_verify_with_expected_passwords():
    assert check_password_hash(USERS["demo"]["password_hash"], "securepr-demo-password")
    assert check_password_hash(USERS["admin"]["password_hash"], "securepr-admin-password")
