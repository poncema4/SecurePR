from __future__ import annotations

from security.python_runtime import declared_version, is_supported_version, version_message


if __name__ == "__main__":
    version = declared_version()
    print(version_message(version))
    if not is_supported_version(version):
        raise SystemExit(1)
