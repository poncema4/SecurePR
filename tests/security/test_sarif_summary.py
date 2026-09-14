import json
from pathlib import Path

from scripts.summarize_sarif import finding_key, iter_results


def test_sarif_results_are_read_and_keyed():
    results = Path(__file__).parent / "_temporary_test.sarif"
    try:
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
        items = list(iter_results(results.parent))
        matched = [item for item in items if item["result"].get("ruleId") == "py/test-rule"]
        assert matched
        assert finding_key(matched[0]) == ("app.py", 10, "py/test-rule", "Unsafe flow")
    finally:
        results.unlink(missing_ok=True)


def test_identical_cross_tool_finding_has_one_key():
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


def test_securepr_custom_security_rules_are_present():
    config = Path('.semgrep_securepr.yml').read_text(encoding='utf-8')
    for rule_id in (
        'securepr-hardcoded-password',
        'securepr-hardcoded-privileged-username',
        'securepr-unsafe-eval',
        'securepr-unverified-tls-python',
    ):
        assert rule_id in config
    assert 'tests/**' in config and 'docs/**' in config
