from security.python_runtime import (
    SUPPORTED_MINIMUM,
    is_supported_version,
    version_message,
)


def test_supported_minimum_is_python_3_11():
    assert SUPPORTED_MINIMUM == (3, 11)


def test_python_3_9_is_not_supported():
    assert is_supported_version((3, 9)) is False


def test_python_3_10_is_not_supported():
    assert is_supported_version((3, 10)) is False


def test_python_3_11_is_supported():
    assert is_supported_version((3, 11)) is True


def test_python_3_14_is_supported():
    assert is_supported_version((3, 14)) is True


def test_unsupported_version_has_upgrade_guidance():
    message = version_message((3, 9))
    assert "Upgrade to Python 3.11 or newer" in message


def test_supported_version_has_pass_message():
    message = version_message((3, 12))
    assert "within the supported runtime policy" in message
