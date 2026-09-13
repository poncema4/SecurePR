"""Python runtime policy checks used by SecurePR."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Tuple

SUPPORTED_MINIMUM: Tuple[int, int] = (3, 11)
_VERSION_PATTERN = re.compile(r"^(?:python[- ]?)?(\d+)\.(\d+)(?:\.\d+)?$")


def is_supported_version(version: tuple[int, int]) -> bool:
    """Return True when the Python major/minor version meets policy."""
    return version >= SUPPORTED_MINIMUM


def current_version() -> tuple[int, int]:
    """Return the running interpreter's major/minor version."""
    return sys.version_info[:2]


def parse_version(value: str) -> tuple[int, int]:
    """Parse a Python major/minor version from a simple version declaration."""
    match = _VERSION_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Unsupported Python version declaration: {value!r}")
    return int(match.group(1)), int(match.group(2))


def declared_version(root: Path | None = None) -> tuple[int, int]:
    """Return the repository-declared Python version, or the running version.

    SecurePR uses .python-version as the explicit project runtime declaration.
    If it is absent, the actual CI/local interpreter is checked instead.
    """
    root = root or Path.cwd()
    version_file = root / ".python-version"
    if version_file.exists():
        return parse_version(version_file.read_text(encoding="utf-8").splitlines()[0])
    return current_version()


def version_message(version: tuple[int, int]) -> str:
    """Return a concise remediation message for the runtime policy."""
    major, minor = version
    if is_supported_version(version):
        return f"Python {major}.{minor} is within the supported runtime policy."

    required_major, required_minor = SUPPORTED_MINIMUM
    return (
        f"Python {major}.{minor} is outside the supported runtime policy. "
        f"Upgrade to Python {required_major}.{required_minor} or newer."
    )
