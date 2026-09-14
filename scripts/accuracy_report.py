from __future__ import annotations

import csv
import sys
from pathlib import Path

try:
    from scripts.accuracy_metrics import calculate
except ModuleNotFoundError:
    from accuracy_metrics import calculate


DEFAULT_RESULTS = Path("docs/accuracy/benchmark-results.csv")


def render(path: Path) -> str:
    formulas = (
        "**Formulas:** TP = expected BLOCK + actual BLOCK; FP = expected PASS + actual BLOCK; "
        "TN = expected PASS + actual PASS; FN = expected BLOCK + actual PASS. "
        "Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
        "F1 = 2 × Precision × Recall / (Precision + Recall)."
    )

    if not path.exists():
        return (
            "Benchmark pending — no labeled benchmark cases are recorded yet. No accuracy percentage is claimed.\n\n"
            + formulas
        )

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return (
            "Benchmark pending — no labeled benchmark cases are recorded yet. No accuracy percentage is claimed.\n\n"
            + formulas
        )

    incomplete = [
        row for row in rows
        if row.get("expected") not in {"PASS", "BLOCK"}
        or row.get("actual") not in {"PASS", "BLOCK"}
    ]
    if incomplete:
        raise ValueError(f"Benchmark contains {len(incomplete)} unlabeled or invalid case(s).")

    metrics = calculate(rows)
    total = metrics.tp + metrics.fp + metrics.tn + metrics.fn
    return (
        f"Labeled benchmark cases: {total}\n\n"
        f"- TP: {metrics.tp}\n"
        f"- FP: {metrics.fp}\n"
        f"- TN: {metrics.tn}\n"
        f"- FN: {metrics.fn}\n"
        f"- Precision: {metrics.precision:.4f}\n"
        f"- Recall: {metrics.recall:.4f}\n"
        f"- F1: {metrics.f1:.4f}\n\n"
        + formulas
    )


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_RESULTS
    try:
        print(render(path))
    except (OSError, ValueError) as exc:
        print(f"Accuracy report error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
