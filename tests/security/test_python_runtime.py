from pathlib import Path

from security.python_runtime import (
    SUPPORTED_MINIMUM,
    declared_version,
    is_supported_version,
    parse_version,
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


def test_parse_version_accepts_python_prefix():
    assert parse_version("python3.12") == (3, 12)


def test_parse_version_rejects_invalid_value():
    try:
        parse_version("not-a-version")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid Python version declaration should fail")


def test_declared_version_reads_python_version_file(tmp_path: Path):
    (tmp_path / ".python-version").write_text("3.10\n", encoding="utf-8")
    assert declared_version(tmp_path) == (3, 10)


def test_declared_version_falls_back_to_running_interpreter(tmp_path: Path):
    from security.python_runtime import current_version

    assert declared_version(tmp_path) == current_version()
