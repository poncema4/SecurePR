from pathlib import Path

from scripts.owasp_report import render


def write_sarif(root: Path, rule_id: str, message: str, properties: dict | None = None) -> None:
    sarif = {
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "test", "rules": [{"id": rule_id}]}},
            "results": [{
                "ruleId": rule_id,
                "message": {"text": message},
                "properties": properties or {},
            }],
        }],
    }
    (root / "test.sarif").write_text(__import__("json").dumps(sarif), encoding="utf-8")


def test_hardcoded_password_blocks_only_credential_categories(tmp_path: Path) -> None:
    write_sarif(
        tmp_path,
        "securepr-tooling.securepr-python-hardcoded-credential",
        "Hard-coded password detected",
    )
    output = render(tmp_path)
    assert "A04:2025 Cryptographic Failures | 🔴 BLOCK | 1" in output
    assert "A07:2025 Authentication Failures | 🔴 BLOCK | 1" in output
    assert "A05:2025 Injection | 🟢 PASS | 0" in output
    assert "A10:2025 Mishandling of Exceptional Conditions | 🟢 PASS | 0" in output


def test_cwe_mapping_blocks_relevant_category_only(tmp_path: Path) -> None:
    write_sarif(
        tmp_path,
        "generic-sqli",
        "CWE-89 SQL injection",
    )
    output = render(tmp_path)
    assert "A05:2025 Injection | 🔴 BLOCK | 1" in output
    assert "A04:2025 Cryptographic Failures | 🟢 PASS | 0" in output
    assert "A01:2025 Broken Access Control | 🟢 PASS | 0" in output


def test_unmapped_finding_does_not_turn_every_category_red(tmp_path: Path) -> None:
    write_sarif(tmp_path, "generic-rule", "A finding without an OWASP/CWE mapping")
    output = render(tmp_path)
    assert "Unmapped SARIF findings: 1" in output
    assert output.count("🔴 BLOCK") == 0
    assert output.count("🟢 PASS") == 10
