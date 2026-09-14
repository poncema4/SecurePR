from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Iterable

CATEGORIES = (
    ("A01", "Broken Access Control"),
    ("A02", "Security Misconfiguration"),
    ("A03", "Software Supply Chain Failures"),
    ("A04", "Cryptographic Failures"),
    ("A05", "Injection"),
    ("A06", "Insecure Design"),
    ("A07", "Authentication Failures"),
    ("A08", "Software or Data Integrity Failures"),
    ("A09", "Security Logging & Alerting Failures"),
    ("A10", "Mishandling of Exceptional Conditions"),
)

CONTROL_MAP = {
    "A01": "CodeQL, Semgrep, project tests",
    "A02": "CodeQL, Semgrep",
    "A03": "Dependency audit, CodeQL, Semgrep",
    "A04": "CodeQL, Semgrep",
    "A05": "CodeQL, Semgrep, project tests",
    "A06": "CodeQL, Semgrep, project tests + human review",
    "A07": "CodeQL, Semgrep, project tests",
    "A08": "CodeQL, dependency audit, Semgrep",
    "A09": "CodeQL, Semgrep + human review",
    "A10": "CodeQL, Semgrep, project tests",
}

CWE_MAP = {
    "cwe-022": {"A01"},
    "cwe-074": {"A05"},
    "cwe-078": {"A05"},
    "cwe-079": {"A05"},
    "cwe-089": {"A05"},
    "cwe-090": {"A05"},
    "cwe-094": {"A05"},
    "cwe-113": {"A05"},
    "cwe-116": {"A05"},
    "cwe-117": {"A09"},
    "cwe-1275": {"A02", "A07"},
    "cwe-209": {"A10", "A09"},
    "cwe-215": {"A02"},
    "cwe-285": {"A01", "A07"},
    "cwe-295": {"A02", "A08"},
    "cwe-312": {"A04", "A09"},
    "cwe-326": {"A04"},
    "cwe-327": {"A02", "A04"},
    "cwe-352": {"A01", "A07"},
    "cwe-377": {"A08"},
    "cwe-502": {"A08"},
    "cwe-601": {"A01"},
    "cwe-611": {"A08"},
    "cwe-614": {"A02", "A07"},
    "cwe-643": {"A05"},
    "cwe-730": {"A05"},
    "cwe-732": {"A02", "A01"},
    "cwe-776": {"A08"},
    "cwe-918": {"A01"},
    "cwe-943": {"A05"},
}

# Keep keyword matching conservative. Scanner remediation text can contain
# broad words such as "secret-management" that should not create a second
# OWASP category for an otherwise credential-specific finding.
KEYWORD_MAP = {
    "hardcoded-credential": {"A04", "A07"},
    "hardcoded-password": {"A04", "A07"},
    "privileged-username": {"A01", "A07"},
    "unsafe-eval": {"A05"},
    "unverified-tls": {"A02", "A04"},
    "credential": {"A04", "A07"},
    "password": {"A04", "A07"},
    "authentication": {"A07"},
    "authorization": {"A01"},
    "access-control": {"A01"},
    "injection": {"A05"},
    "logging": {"A09"},
    "alert": {"A09"},
    "exception": {"A10"},
    "error-handling": {"A10"},
    "failing-open": {"A10"},
    "supply-chain": {"A03"},
    "dependency": {"A03", "A08"},
    "integrity": {"A08"},
    "deserialization": {"A08"},
    "cryptograph": {"A04"},
    "tls": {"A02", "A04"},
    "certificate": {"A02", "A04"},
    "misconfiguration": {"A02"},
    "debug": {"A02"},
}


def iter_sarif_results(root: Path) -> Iterable[tuple[str, dict]]:
    for path in sorted(root.rglob("*.sarif")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for run in data.get("runs", []):
            tool = run.get("tool", {}).get("driver", {}).get("name", path.stem)
            for result in run.get("results", []):
                yield tool, result


def categories_for_finding(tool: str, result: dict) -> set[str]:
    rule = str(result.get("ruleId", "")).lower()
    message = str((result.get("message") or {}).get("text", "")).lower()
    haystack = f"{rule} {message} {tool.lower()}"
    categories: set[str] = set()

    for cwe, mapped in CWE_MAP.items():
        if cwe in haystack:
            categories.update(mapped)
    for keyword, mapped in KEYWORD_MAP.items():
        if keyword in haystack:
            categories.update(mapped)

    return categories


def failed(value: str | None) -> bool:
    return value == "failure"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    blocked_by_finding = {code: [] for code, _ in CATEGORIES}
    finding_count = 0

    for tool, result in iter_sarif_results(root):
        categories = categories_for_finding(tool, result)
        if not categories:
            continue
        finding_count += 1
        rule = str(result.get("ruleId", "unknown"))
        message = str((result.get("message") or {}).get("text", "")).strip()
        location = (result.get("locations") or [{}])[0]
        physical = location.get("physicalLocation") or {}
        uri = (physical.get("artifactLocation") or {}).get("uri", "unknown")
        line = ((physical.get("region") or {}).get("startLine", 0))
        evidence = f"{tool}: {rule} at {uri}:{line}"
        if message:
            evidence += f" — {message}"
        for code in categories:
            blocked_by_finding[code].append(evidence)

    failure_categories: dict[str, set[str]] = {code: set() for code, _ in CATEGORIES}
    if failed(os.getenv("DEPENDENCY_RESULT")):
        for code in ("A03", "A08"):
            failure_categories[code].add("Dependency audit failed")
    if failed(os.getenv("TEST_RESULT")):
        for code in ("A01", "A05", "A06", "A07", "A10"):
            failure_categories[code].add("Project tests failed")
    if failed(os.getenv("NODE_TEST_RESULT")):
        for code in ("A01", "A05", "A06", "A07", "A10"):
            failure_categories[code].add("JavaScript/TypeScript tests failed")
    if failed(os.getenv("CODEQL_INIT_RESULT")) or failed(os.getenv("CODEQL_ANALYZE_RESULT")):
        for code, _ in CATEGORIES:
            failure_categories[code].add("CodeQL control failed")
    if failed(os.getenv("SEMGREP_RESULT")) and finding_count == 0:
        for code, _ in CATEGORIES:
            failure_categories[code].add("Semgrep control failed without classified SARIF evidence")
    if failed(os.getenv("GITLEAKS_RESULT")):
        for code in ("A04", "A07", "A08"):
            failure_categories[code].add("Gitleaks control failed")

    output = Path("securepr-owasp.md")
    with output.open("w", encoding="utf-8") as out:
        out.write("### OWASP Top 10:2025 Coverage\n\n")
        out.write(
            "These rows are **finding-specific coverage mappings**. A category is BLOCK only when a classified security finding maps to that category or an explicitly mapped control for that category failed. A PASS means no mapped blocking evidence was observed in this run; it does not prove the entire OWASP category is secure.\n\n"
        )
        out.write("| OWASP category | Result | Automated controls | Evidence |\n|---|---|---|---|\n")
        for code, name in CATEGORIES:
            evidence = blocked_by_finding[code] + sorted(failure_categories[code])
            result = "🔴 BLOCK" if evidence else "🟢 PASS"
            if evidence:
                detail = "<br>".join(evidence[:4])
                if len(evidence) > 4:
                    detail += f"<br>…and {len(evidence) - 4} more"
            else:
                detail = "No mapped blocking evidence"
            out.write(f"| {code}:2025 {name} | {result} | {CONTROL_MAP[code]} | {detail} |\n")
        out.write("\nHuman review is always recommended. OWASP coverage is a mapping of SecurePR's automated evidence, not a complete OWASP assessment.\n")

    print(f"Generated finding-specific OWASP coverage for {finding_count} classified SARIF findings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
