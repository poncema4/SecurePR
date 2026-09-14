from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

CATEGORIES = {
    "A01": "Broken Access Control",
    "A02": "Security Misconfiguration",
    "A03": "Software Supply Chain Failures",
    "A04": "Cryptographic Failures",
    "A05": "Injection",
    "A06": "Insecure Design",
    "A07": "Authentication Failures",
    "A08": "Software or Data Integrity Failures",
    "A09": "Security Logging & Alerting Failures",
    "A10": "Mishandling of Exceptional Conditions",
}

CUSTOM_RULES = {
    "securepr-hardcoded-password": {"A04", "A07"},
    "securepr-python-hardcoded-credential": {"A04", "A07"},
    "securepr-hardcoded-privileged-username": {"A01", "A07"},
    "securepr-unsafe-eval": {"A05"},
    "securepr-unverified-tls-python": {"A02", "A04"},
}

CWE_MAP = {
    "200": {"A01"}, "201": {"A01"}, "284": {"A01"}, "285": {"A01"},
    "352": {"A01"}, "359": {"A01"}, "425": {"A01"}, "566": {"A01"},
    "639": {"A01"}, "668": {"A01"}, "862": {"A01"}, "863": {"A01"},
    "918": {"A01"},
    "5": {"A02"}, "11": {"A02"}, "13": {"A02"}, "15": {"A02"},
    "16": {"A02"}, "260": {"A02"}, "489": {"A02"}, "526": {"A02"},
    "547": {"A02"}, "611": {"A02"}, "614": {"A02"}, "776": {"A02"},
    "942": {"A02"}, "1004": {"A02"},
    "447": {"A03"}, "1035": {"A03"}, "1104": {"A03"}, "1329": {"A03"},
    "1357": {"A03"}, "1395": {"A03"},
    "261": {"A04"}, "296": {"A04"}, "319": {"A04"}, "320": {"A04"},
    "321": {"A04"}, "322": {"A04"}, "323": {"A04"}, "324": {"A04"},
    "325": {"A04"}, "326": {"A04"}, "327": {"A04"}, "328": {"A04"},
    "329": {"A04"}, "330": {"A04"}, "331": {"A04"}, "332": {"A04"},
    "334": {"A04"}, "335": {"A04"}, "336": {"A04"}, "337": {"A04"},
    "338": {"A04"}, "340": {"A04"}, "342": {"A04"}, "347": {"A04"},
    "523": {"A04"}, "757": {"A04"}, "759": {"A04"}, "760": {"A04"},
    "780": {"A04"}, "916": {"A04"}, "1240": {"A04"}, "1241": {"A04"},
    "20": {"A05"}, "74": {"A05"}, "76": {"A05"}, "77": {"A05"},
    "78": {"A05"}, "79": {"A05"}, "80": {"A05"}, "83": {"A05"},
    "89": {"A05"},
    "287": {"A07"}, "288": {"A07"}, "294": {"A07"}, "306": {"A07"},
    "307": {"A07"}, "384": {"A07"}, "521": {"A07"}, "522": {"A07"},
    "613": {"A07"}, "620": {"A07"}, "640": {"A07"}, "798": {"A07"},
    "345": {"A08"}, "494": {"A08"}, "502": {"A08"}, "565": {"A08"},
    "829": {"A08"}, "915": {"A08"},
    "117": {"A09"}, "223": {"A09"}, "532": {"A09"}, "778": {"A09"},
    "209": {"A10"}, "215": {"A10"}, "234": {"A10"}, "235": {"A10"},
    "248": {"A10"}, "252": {"A10"}, "274": {"A10"}, "280": {"A10"},
    "369": {"A10"}, "390": {"A10"}, "391": {"A10"}, "394": {"A10"},
    "396": {"A10"}, "397": {"A10"}, "460": {"A10"}, "476": {"A10"},
    "478": {"A10"}, "484": {"A10"}, "550": {"A10"}, "636": {"A10"},
    "703": {"A10"}, "754": {"A10"}, "755": {"A10"}, "756": {"A10"},
}


def _strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)


def _cwes(values: Iterable[str]) -> set[str]:
    found: set[str] = set()
    for value in values:
        for match in re.finditer(r"(?:CWE[-_:/ ]?)(\d{1,5})", value, re.IGNORECASE):
            found.add(match.group(1))
    return found


def _mapped_categories(result: dict, rule: dict) -> set[str]:
    rule_id = str(result.get("ruleId", ""))
    normalized_rule_id = rule_id.rsplit(".", 1)[-1]
    if normalized_rule_id in CUSTOM_RULES:
        return set(CUSTOM_RULES[normalized_rule_id])

    values = list(_strings(result.get("properties", {})))
    values += list(_strings(rule.get("properties", {})))
    values += list(_strings(rule.get("tags", [])))
    values += [str(result.get("message", {}).get("text", "")), rule_id]

    mapped: set[str] = set()
    for value in values:
        lower = value.lower()
        for code in CATEGORIES:
            if re.search(rf"\b(?:owasp[-_: ]?){code.lower()}\b", lower):
                mapped.add(code)
    for cwe in _cwes(values):
        mapped.update(CWE_MAP.get(cwe, set()))
    return mapped


def iter_findings(root: Path) -> Iterable[tuple[dict, dict]]:
    for path in sorted(root.rglob("*.sarif")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for run in data.get("runs", []):
            driver = run.get("tool", {}).get("driver", {})
            rules = driver.get("rules", []) or []
            rule_by_id = {str(rule.get("id")): rule for rule in rules}
            for result in run.get("results", []):
                yield result, rule_by_id.get(str(result.get("ruleId", "")), {})


def render(root: Path = Path(".")) -> str:
    blocked: dict[str, int] = {code: 0 for code in CATEGORIES}
    unmapped = 0
    for result, rule in iter_findings(root):
        categories = _mapped_categories(result, rule)
        if not categories:
            unmapped += 1
        for code in categories:
            blocked[code] += 1

    lines = [
        "### OWASP Top 10:2025 Coverage",
        "",
        "Each row is derived from findings that can be mapped to that OWASP category. "
        "A category is `BLOCK` only when at least one mapped security finding exists; otherwise it is `PASS`. "
        "This prevents one Semgrep/CodeQL finding from turning every category red. The overall SecurePR gate "
        "remains independent and can still be `BLOCK` because any required check failed.",
        "",
        "| OWASP category | Result | Mapped findings | Evidence basis |",
        "|---|---|---:|---|",
    ]
    for code, name in CATEGORIES.items():
        count = blocked[code]
        result = "🔴 BLOCK" if count else "🟢 PASS"
        lines.append(
            f"| {code}:2025 {name} | {result} | {count} | SARIF findings explicitly mapped by OWASP tag, CWE, or SecurePR custom rule |"
        )
    lines += [
        "",
        f"Unmapped SARIF findings: {unmapped}. Unmapped findings still affect the overall SecurePR gate, but are not assigned to an OWASP category without sufficient evidence.",
        "",
        "A category `PASS` is not a claim that the entire OWASP risk is secure; it means no mapped automated finding was reported for this run. Human review remains required.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(render(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")))
