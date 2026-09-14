from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

try:
    from scripts.accuracy_metrics import calculate
    from scripts.owasp_report import render as render_owasp
except ModuleNotFoundError:
    from accuracy_metrics import calculate
    from owasp_report import render as render_owasp


DEFAULT_RESULTS = Path("docs/accuracy/benchmark-results.csv")
VALID_OUTCOMES = {"PASS", "BLOCK"}


def render(path: Path) -> str:
    formulas = (
        "**Formulas:** TP = expected BLOCK + actual BLOCK; FP = expected PASS + actual BLOCK; "
        "TN = expected PASS + actual PASS; FN = expected BLOCK + actual PASS. "
        "Precision = TP / (TP + FP). Recall = TP / (TP + FN). "
        "F1 = 2 × Precision × Recall / (Precision + Recall)."
    )

    if not path.exists():
        cumulative = (
            "Benchmark pending — no labeled benchmark cases are recorded yet. "
            "No accuracy percentage is claimed."
        )
    else:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        if not rows:
            cumulative = (
                "Benchmark pending — no labeled benchmark cases are recorded yet. "
                "No accuracy percentage is claimed."
            )
        else:
            incomplete = [
                row for row in rows
                if row.get("expected") not in VALID_OUTCOMES
                or row.get("actual") not in VALID_OUTCOMES
            ]
            if incomplete:
                raise ValueError(
                    f"Benchmark contains {len(incomplete)} unlabeled or invalid case(s)."
                )

            metrics = calculate(rows)
            total = metrics.tp + metrics.fp + metrics.tn + metrics.fn
            cumulative = (
                f"Labeled benchmark cases: {total}\n\n"
                f"- TP: {metrics.tp}\n"
                f"- FP: {metrics.fp}\n"
                f"- TN: {metrics.tn}\n"
                f"- FN: {metrics.fn}\n"
                f"- Precision: {metrics.precision:.4f}\n"
                f"- Recall: {metrics.recall:.4f}\n"
                f"- F1: {metrics.f1:.4f}"
            )

    expected = os.environ.get("SECUREPR_EXPECTED_OUTCOME", "").strip().upper()
    actual = os.environ.get("SECUREPR_ACTUAL_OUTCOME", "").strip().upper()

    if expected in VALID_OUTCOMES and actual in VALID_OUTCOMES:
        classification = "CORRECT" if expected == actual else "INCORRECT"
        current_case = (
            "\n\n### Current PR benchmark case\n\n"
            f"- Expected: `{expected}`\n"
            f"- Actual: `{actual}`\n"
            f"- Classification: `{classification}`\n\n"
            "This PR is treated as a benchmark case only because an expected outcome was explicitly supplied. "
            "The committed CSV is not modified automatically."
        )
    elif expected or actual:
        current_case = (
            "\n\nCurrent PR benchmark status could not be measured because both expected and actual "
            "outcomes must be `PASS` or `BLOCK`."
        )
    else:
        current_case = (
            "\n\nNo expected benchmark outcome was supplied for this PR. "
            "The cumulative benchmark is reported, but this ordinary PR is not counted as a TP, FP, TN, or FN."
        )

    owasp = render_owasp(Path("."))
    return cumulative + current_case + "\n\n" + formulas + "\n\n" + owasp


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
