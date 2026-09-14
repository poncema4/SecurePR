from __future__ import annotations

import json

from scripts.owasp_report import categories_for_finding


def test_hardcoded_credential_maps_only_to_relevant_categories() -> None:
    result = {"ruleId": "securepr-python-hardcoded-credential", "message": {"text": "Hardcoded credential"}}
    assert categories_for_finding("Semgrep", result) == {"A04", "A07"}


def test_command_injection_maps_to_injection() -> None:
    result = {"ruleId": "py/command-line-injection", "message": {"text": "Uncontrolled command line"}}
    assert categories_for_finding("CodeQL", result) == {"A05"}


def test_logging_finding_maps_to_injection_and_logging() -> None:
    result = {"ruleId": "py/log-injection", "message": {"text": "Log Injection"}}
    assert categories_for_finding("CodeQL", result) == {"A05"}


def test_sarif_fixture_shape_is_accepted(tmp_path) -> None:
    sarif = {
        "runs": [
            {
                "tool": {"driver": {"name": "Semgrep"}},
                "results": [
                    {
                        "ruleId": "securepr-unsafe-eval",
                        "message": {"text": "Unsafe eval"},
                        "locations": [{"physicalLocation": {"artifactLocation": {"uri": "app.py"}, "region": {"startLine": 3}}}],
                    }
                ],
            }
        ]
    }
    path = tmp_path / "semgrep-results.sarif"
    path.write_text(json.dumps(sarif), encoding="utf-8")
    assert path.exists()
