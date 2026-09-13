from __future__ import annotations

import json
import sys
from collections import defaultdict
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


def finding_key(item: dict) -> tuple[str, int]:
    result = item["result"]
    location = (result.get("locations") or [{}])[0]
    physical = location.get("physicalLocation") or {}
    region = physical.get("region") or {}
    return (
        physical.get("artifactLocation", {}).get("uri", "unknown"),
        int(region.get("startLine", 0)),
    )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    grouped: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for item in iter_results(root):
        grouped[finding_key(item)].append(item)

    summary = Path("securepr-findings.md")
    with summary.open("w", encoding="utf-8") as out:
        out.write("### SecurePR normalized findings\n\n")
        if not grouped:
            out.write("No findings were reported by SARIF-producing checks.\n")
            print("No SARIF findings detected.")
            return 0
        out.write("| Location | Tools | Rules | Findings |\n|---|---|---|---|\n")
        for (uri, line), items in sorted(grouped.items()):
            tools = sorted({item["tool"] for item in items})
            rules = sorted({item["result"].get("ruleId", "unknown") for item in items})
            messages = sorted({item["result"].get("message", {}).get("text", "").strip() for item in items})
            safe_messages = "<br>".join(message.replace("|", "\\|") for message in messages)
            out.write(
                f"| `{uri}:{line}` | {', '.join(tools)} | {', '.join(f'`{rule}`' for rule in rules)} | {safe_messages} |\n"
            )

    print(f"Detected {len(grouped)} unique security finding locations across SARIF-producing checks.")
    for (uri, line), items in list(sorted(grouped.items()))[:20]:
        messages = sorted({item["result"].get("message", {}).get("text", "").strip() for item in items})
        print(f"::error title=SecurePR finding::{uri}:{line} — {' / '.join(messages)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
