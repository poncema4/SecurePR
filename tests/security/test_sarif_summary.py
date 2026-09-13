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
    assert finding_key(items[0])[1:] == ("py/test-rule", "app.py", 10, "Unsafe flow")


def test_sarif_duplicate_results_share_one_key():
    item = {
        "tool": "CodeQL",
        "result": {
            "ruleId": "x",
            "message": {"text": "same"},
            "locations": [{"physicalLocation": {
                "artifactLocation": {"uri": "app.py"},
                "region": {"startLine": 1},
            }}],
        },
    }
    assert finding_key(item) == finding_key(item)


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
