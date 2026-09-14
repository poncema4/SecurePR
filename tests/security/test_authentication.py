from werkzeug.security import check_password_hash

from app.app import ADMIN_PASSWORD, DEMO_PASSWORD, USERS, authenticate


def test_demo_password_authenticates():
    assert authenticate("demo", DEMO_PASSWORD) is True


def test_admin_password_authenticates():
    assert authenticate("admin", ADMIN_PASSWORD) is True


def test_wrong_password_does_not_authenticate():
    assert authenticate("demo", "wrong-password") is False


def test_unknown_user_does_not_authenticate():
    assert authenticate("does-not-exist", DEMO_PASSWORD) is False


def test_passwords_are_stored_as_hashes_not_plaintext():
    assert USERS["demo"]["password_hash"] != DEMO_PASSWORD
    assert USERS["admin"]["password_hash"] != ADMIN_PASSWORD


def test_stored_password_hashes_verify_with_expected_passwords():
    assert check_password_hash(USERS["demo"]["password_hash"], DEMO_PASSWORD)
    assert check_password_hash(USERS["admin"]["password_hash"], ADMIN_PASSWORD)
