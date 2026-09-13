from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable


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


def finding_key(item: dict) -> tuple:
    result = item["result"]
    location = (result.get("locations") or [{}])[0]
    physical = location.get("physicalLocation") or {}
    region = physical.get("region") or {}
    return (
        item["tool"],
        result.get("ruleId", "unknown"),
        physical.get("artifactLocation", {}).get("uri", "unknown"),
        region.get("startLine", 0),
        result.get("message", {}).get("text", "").strip(),
    )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    findings = {}
    for item in iter_results(root):
        findings[finding_key(item)] = item

    summary = Path("securepr-findings.md")
    with summary.open("w", encoding="utf-8") as out:
        out.write("### SecurePR normalized findings\n\n")
        if not findings:
            out.write("No findings were reported by SARIF-producing checks.\n")
            print("No SARIF findings detected.")
            return 0
        out.write("| Tool | Rule | Location | Finding |\n|---|---|---|---|\n")
        for key, item in findings.items():
            _, rule, uri, line, message = key
            message = message.replace("|", "\\|")
            out.write(f"| {item['tool']} | `{rule}` | `{uri}:{line}` | {message} |\n")

    print(f"Detected {len(findings)} unique normalized security findings.")
    for key in list(findings)[:20]:
        tool, rule, uri, line, message = key
        print(f"::error title={tool}:{rule}::{uri}:{line} — {message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
