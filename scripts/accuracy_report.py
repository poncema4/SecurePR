from __future__ import annotations

import csv
import sys
from pathlib import Path

from scripts.accuracy_metrics import calculate


DEFAULT_RESULTS = Path("docs/accuracy/benchmark-results.csv")


def render(path: Path) -> str:
    if not path.exists():
        return (
            "**Accuracy status:** Benchmark pending — no accuracy percentage is claimed. "
            "Final Phase 4 validation will measure TP, FP, TN, FN, precision, recall, and F1."
        )

    with path.open(newline="", encoding="utf-8") as handle:
        metrics = calculate(list(csv.DictReader(handle)))

    return (
        "**Accuracy status:** Latest controlled benchmark results\n\n"
        f"- TP: {metrics.tp}\n"
        f"- FP: {metrics.fp}\n"
        f"- TN: {metrics.tn}\n"
        f"- FN: {metrics.fn}\n"
        f"- Precision: {metrics.precision:.4f}\n"
        f"- Recall: {metrics.recall:.4f}\n"
        f"- F1: {metrics.f1:.4f}\n\n"
        "These measurements describe the tested benchmark corpus and configuration; "
        "they are not a universal guarantee of vulnerability-detection accuracy."
    )


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_RESULTS
    print(render(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
