from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable


OWASP_COVERAGE = [
    (
        "A01 Broken Access Control",
        ("access control", "authorization", "privilege", "idor", "insecure direct object", "path traversal"),
        "CodeQL / Semgrep / project tests",
        "Authorization, privilege, object-access, and traversal weaknesses",
    ),
    (
        "A02 Security Misconfiguration",
        ("misconfig", "insecure configuration", "debug", "tls", "verify=false", "security setting", "default credential"),
        "Semgrep / CodeQL / configuration checks",
        "Unsafe configuration and insecure defaults",
    ),
    (
        "A03 Software Supply Chain Failures",
        ("dependency", "supply chain", "package", "npm", "pip", "workflow", "github action"),
        "Dependency audit / GitHub Actions checks",
        "Known dependency risk and workflow/supply-chain trust boundaries",
    ),
    (
        "A04 Cryptographic Failures",
        ("crypt", "cipher", "hash", "password storage", "tls", "ssl", "certificate", "weak crypto"),
        "CodeQL / Semgrep / dependency audit",
        "Weak or unsafe cryptographic and transport-security practices",
    ),
    (
        "A05 Injection",
        ("injection", "sql", "command injection", "shell", "eval", "exec", "xss", "cross-site scripting", "ldap"),
        "CodeQL / Semgrep",
        "SQL, command, code, XSS, and related injection patterns",
    ),
    (
        "A06 Insecure Design",
        ("insecure design", "design flaw", "business logic", "workflow abuse", "missing authorization"),
        "Automated coverage + human review",
        "Design-level security weaknesses that cannot be fully established by static automation",
    ),
    (
        "A07 Authentication Failures",
        ("authentication", "authn", "login", "session", "credential", "password", "mfa", "multi-factor", "token"),
        "CodeQL / Semgrep / project tests",
        "Authentication, session, credential, and MFA-related weaknesses",
    ),
    (
        "A08 Software or Data Integrity Failures",
        ("integrity", "deserializ", "signature", "supply chain", "trusted source", "workflow", "artifact"),
        "CodeQL / dependency / workflow checks",
        "Integrity, unsafe deserialization, trusted-source, and artifact risks",
    ),
    (
        "A09 Security Logging & Alerting Failures",
        ("logging", "log", "audit trail", "alert", "monitoring", "security event"),
        "CodeQL / Semgrep + human review",
        "Unsafe or missing security logging and alerting patterns",
    ),
    (
        "A10 Mishandling of Exceptional Conditions",
        ("exception", "error handling", "error", "failure", "catch", "unchecked", "panic"),
        "CodeQL / Semgrep",
        "Unsafe exception, error, failure, and exceptional-condition handling",
    ),
]


def iter_results(root: Path) -> Iterable[dict]:
    for path in sorted(root.rglob("*.sarif")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for run in data.get("runs", []):
            tool = run.get("tool", {}).get("driver", {}).get("name", path.stem)
            for result in run.get("results", []):
                yield {"tool": tool, "result": result}


def finding_key(item: dict) -> tuple[str, int, str, str]:
    result = item["result"]
    location = (result.get("locations") or [{}])[0]
    physical = location.get("physicalLocation") or {}
    region = physical.get("region") or {}
    uri = physical.get("artifactLocation", {}).get("uri", "unknown")
    line = int(region.get("startLine", 0))
    rule = result.get("ruleId", "unknown")
    message = result.get("message", {}).get("text", "").strip()
    return uri, line, rule, message


def finding_text(item: dict) -> str:
    result = item["result"]
    message = result.get("message", {}).get("text", "")
    rule = result.get("ruleId", "")
    properties = result.get("properties") or {}
    tags = properties.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    return " ".join([str(rule), str(message), " ".join(map(str, tags))]).lower()


def owasp_categories(items: list[dict]) -> dict[str, list[dict]]:
    matches: dict[str, list[dict]] = {name: [] for name, *_ in OWASP_COVERAGE}
    for item in items:
        text = finding_text(item)
        for name, keywords, *_ in OWASP_COVERAGE:
            if any(keyword in text for keyword in keywords):
                matches[name].append(item)
    return matches


def write_owasp_table(out, items: list[dict]) -> None:
    matches = owasp_categories(items)
    out.write("### OWASP Top 10:2025 Coverage — Check Results\n\n")
    out.write(
        "Each category is a coverage mapping, not proof that the entire category is secure. "
        "**PASS** means no SARIF finding was mapped to that category in this run; **BLOCK** means "
        "at least one mapped finding was reported. A PASS never replaces human review.\n\n"
    )
    out.write("| OWASP Top 10:2025 category | Result | Automated coverage | What it checks |\n")
    out.write("|---|---|---|---|\n")
    for name, _keywords, controls, description in OWASP_COVERAGE:
        status = "🔴 BLOCK" if matches[name] else "🟢 PASS"
        out.write(f"| {name} | {status} | {controls} | {description} |\n")
    out.write("\n")
    out.write(
        "**Coverage limitation:** OWASP categories are broader than any individual automated rule set. "
        "A category can report PASS while still containing risks that require manual review, threat modeling, "
        "testing, architecture review, or controls not implemented by SecurePR.\n"
    )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    grouped: dict[tuple[str, int, str, str], list[dict]] = defaultdict(list)
    all_items: list[dict] = []
    for item in iter_results(root):
        all_items.append(item)
        grouped[finding_key(item)].append(item)

    summary = Path("securepr-findings.md")
    with summary.open("w", encoding="utf-8") as out:
        out.write("### SecurePR normalized findings\n\n")
        if not grouped:
            out.write("No findings were reported by SARIF-producing checks.\n\n")
            write_owasp_table(out, [])
            print("No SARIF findings detected.")
            return 0
        out.write("| Location | Tools | Rules | Findings |\n|---|---|---|---|\n")
        for (uri, line, rule, message), items in sorted(grouped.items()):
            tools = sorted({item["tool"] for item in items})
            safe_message = message.replace("|", "\\|")
            out.write(
                f"| `{uri}:{line}` | {', '.join(tools)} | `{rule}` | {safe_message} |\n"
            )
        out.write("\n")
        write_owasp_table(out, all_items)

    print(f"Detected {len(grouped)} unique normalized security findings across SARIF-producing checks.")
    for (uri, line, rule, message), _items in list(sorted(grouped.items()))[:20]:
        print(f"::error title=SecurePR finding::{uri}:{line} — {rule}: {message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
