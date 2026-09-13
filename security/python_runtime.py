"""Python runtime policy checks used by SecurePR."""

from __future__ import annotations

import sys
from typing import Tuple

SUPPORTED_MINIMUM: Tuple[int, int] = (3, 11)


def is_supported_version(version: tuple[int, int]) -> bool:
    """Return True when the Python major/minor version meets policy."""
    return version >= SUPPORTED_MINIMUM


def current_version() -> tuple[int, int]:
    """Return the running interpreter's major/minor version."""
    return sys.version_info[:2]


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
