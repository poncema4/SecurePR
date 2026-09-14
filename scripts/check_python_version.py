from __future__ import annotations

import re
import sys
from pathlib import Path

SUPPORTED_MINIMUM = (3, 11)
_VERSION_PATTERN = re.compile(r"^(?:python[- ]?)?(\d+)\.(\d+)(?:\.\d+)?$")


def parse_version(value: str) -> tuple[int, int]:
    match = _VERSION_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Unsupported Python version declaration: {value!r}")
    return int(match.group(1)), int(match.group(2))


def declared_version(root: Path | None = None) -> tuple[int, int]:
    root = root or Path.cwd()
    version_file = root / ".python-version"
    if version_file.exists():
        return parse_version(version_file.read_text(encoding="utf-8").splitlines()[0])
    return sys.version_info[:2]


def is_supported_version(version: tuple[int, int]) -> bool:
    return version >= SUPPORTED_MINIMUM


def version_message(version: tuple[int, int]) -> str:
    major, minor = version
    if is_supported_version(version):
        return f"Python {major}.{minor} is within the supported runtime policy."
    return f"Python {major}.{minor} is outside the supported runtime policy. Upgrade to Python 3.11 or newer."


if __name__ == "__main__":
    version = declared_version()
    print(version_message(version))
    if not is_supported_version(version):
        raise SystemExit(1)
