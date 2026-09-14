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
    if not path.exists():
        return (
            "**Accuracy status:** Benchmark pending — no accuracy percentage is claimed.\n\n"
            "No labeled benchmark CSV is present yet. Final Phase 4 validation will measure "
            "TP, FP, TN, FN, precision, recall, and F1.\n\n"
            "**Formulas:** TP = expected BLOCK + actual BLOCK; FP = expected PASS + actual BLOCK; "
            "TN = expected PASS + actual PASS; FN = expected BLOCK + actual PASS. "
            "Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
            "F1 = 2 × Precision × Recall / (Precision + Recall)."
        )

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return (
            "**Accuracy status:** Benchmark pending — no labeled benchmark cases have been recorded yet.\n\n"
            "No accuracy percentage is claimed. Add controlled benchmark cases with an expected "
            "PASS/BLOCK label and the observed SecurePR result before reporting TP/FP/TN/FN.\n\n"
            "**Formulas:** TP = expected BLOCK + actual BLOCK; FP = expected PASS + actual BLOCK; "
            "TN = expected PASS + actual PASS; FN = expected BLOCK + actual PASS. "
            "Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
            "F1 = 2 × Precision × Recall / (Precision + Recall)."
        )

    incomplete = [row for row in rows if row.get("expected") not in {"PASS", "BLOCK"} or row.get("actual") not in {"PASS", "BLOCK"}]
    if incomplete:
        raise ValueError(f"Benchmark contains {len(incomplete)} unlabeled or invalid case(s).")

    metrics = calculate(rows)
    total = metrics.tp + metrics.fp + metrics.tn + metrics.fn

    return (
        "**Accuracy status:** Latest controlled benchmark results\n\n"
        f"- Labeled cases: {total}\n"
        f"- TP: {metrics.tp}\n"
        f"- FP: {metrics.fp}\n"
        f"- TN: {metrics.tn}\n"
        f"- FN: {metrics.fn}\n"
        f"- Precision: {metrics.precision:.4f}\n"
        f"- Recall: {metrics.recall:.4f}\n"
        f"- F1: {metrics.f1:.4f}\n\n"
        "**Formulas:** Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
        "F1 = 2 × Precision × Recall / (Precision + Recall).\n\n"
        "These measurements describe the labeled benchmark corpus and configuration; "
        "they are not a universal guarantee of vulnerability-detection accuracy."
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
