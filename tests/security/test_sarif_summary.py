import json
from pathlib import Path

from scripts.summarize_sarif import finding_key, iter_results


def test_sarif_results_are_read_and_normalized(tmp_path: Path):
    results = tmp_path / "codeql.sarif"
    results.write_text(json.dumps({
        "runs": [{
            "tool": {"driver": {"name": "CodeQL"}},
            "results": [{
                "ruleId": "py/test-rule",
                "message": {"text": "Unsafe flow"},
                "locations": [{"physicalLocation": {
                    "artifactLocation": {"uri": "app.py"},
                    "region": {"startLine": 10},
                }}],
            }],
        }]
    }), encoding="utf-8")
    items = list(iter_results(tmp_path))
    assert len(items) == 1
    assert finding_key(items[0]) == ("app.py", 10, "py/test-rule", "Unsafe flow")


def test_identical_cross_tool_finding_has_one_normalized_key():
    codeql = {
        "tool": "CodeQL",
        "result": {
            "ruleId": "test-rule",
            "message": {"text": "Unsafe flow"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 10},
            }}],
        },
    }
    semgrep = {
        "tool": "Semgrep",
        "result": {
            "ruleId": "test-rule",
            "message": {"text": "Unsafe flow"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 10},
            }}],
        },
    }
    assert finding_key(codeql) == finding_key(semgrep)


def test_distinct_findings_at_same_location_remain_distinct():
    first = {
        "tool": "CodeQL",
        "result": {
            "ruleId": "sql-injection",
            "message": {"text": "Unsafe query"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 10},
            }}],
        },
    }
    second = {
        "tool": "Semgrep",
        "result": {
            "ruleId": "command-injection",
            "message": {"text": "Unsafe command"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 10},
            }}],
        },
    }
    assert finding_key(first) != finding_key(second)


def test_securepr_custom_security_rules_match_high_confidence_cases():
    config = Path('.semgrep_securepr.yml').read_text(encoding='utf-8')
    assert 'password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token' in config
    assert '(admin|administrator|root|superuser)' in config
    assert '\\b(eval|exec)\\s*\\(' in config
    assert '\\bverify\\s*=\\s*False\\b' in config
    assert 'paths:' in config and 'tests/**' in config and 'docs/**' in config
