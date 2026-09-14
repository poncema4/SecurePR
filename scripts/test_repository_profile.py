from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.repository_profile import profile


def test_detects_multiple_supported_languages_and_manifests():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "app.py").write_text("print('x')")
        (root / "app.ts").write_text("export const x = 1")
        (root / "go.mod").write_text("module example")
        result = profile(root)
        assert result["codeql_languages"] == ["go", "javascript-typescript", "python"]
        assert "Go modules" in result["manifests"]


def test_detects_unsupported_codeql_extensions():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "legacy.php").write_text("<?php echo 'x';")
        (root / "service.scala").write_text("object Service")
        result = profile(root)
        assert result["unsupported_extensions"] == [".php", ".scala"]


def test_ignores_generated_and_dependency_directories():
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "node_modules").mkdir()
        (root / "node_modules" / "bad.js").write_text("eval('x')")
        (root / "app.py").write_text("print('x')")
        result = profile(root)
        assert result["codeql_languages"] == ["python"]
