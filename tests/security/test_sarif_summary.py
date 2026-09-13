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
    assert finding_key(items[0]) == ("app.py", 10)


def test_same_location_from_multiple_tools_has_one_normalized_key():
    codeql = {
        "tool": "CodeQL",
        "result": {
            "ruleId": "py/test-rule",
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
            "ruleId": "custom/test-rule",
            "message": {"text": "Equivalent unsafe flow"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 10},
            }}],
        },
    }
    assert finding_key(codeql) == finding_key(semgrep)


def test_securepr_custom_credential_rules_match_high_confidence_cases():
    import re
    import yaml

    rules = yaml.safe_load(Path('.semgrep_securepr.yml').read_text(encoding='utf-8'))['rules']
    password_pattern = rules[0]['patterns'][0]['pattern-regex'].strip()
    username_pattern = rules[1]['patterns'][0]['pattern-regex'].strip()
    assert re.search(password_pattern, 'PASSWORD = "SuperSecret123!"')
    assert re.search(username_pattern, 'username = "admin"')
    assert not re.search(password_pattern, 'password = get_password_from_secret_manager()')
    assert not re.search(username_pattern, 'username = current_user.name')
