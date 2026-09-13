from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Metrics:
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def precision(self) -> float:
        denominator = self.tp + self.fp
        return self.tp / denominator if denominator else 0.0

    @property
    def recall(self) -> float:
        denominator = self.tp + self.fn
        return self.tp / denominator if denominator else 0.0

    @property
    def f1(self) -> float:
        denominator = self.precision + self.recall
        return 2 * self.precision * self.recall / denominator if denominator else 0.0


def calculate(rows: list[dict[str, str]]) -> Metrics:
    counts = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    for row in rows:
        expected = row["expected"].strip().upper()
        actual = row["actual"].strip().upper()
        if expected not in {"PASS", "BLOCK"} or actual not in {"PASS", "BLOCK"}:
            raise ValueError(f"Expected PASS/BLOCK classifications, got {expected!r}/{actual!r}")
        if expected == "BLOCK" and actual == "BLOCK":
            counts["TP"] += 1
        elif expected == "PASS" and actual == "BLOCK":
            counts["FP"] += 1
        elif expected == "PASS" and actual == "PASS":
            counts["TN"] += 1
        else:
            counts["FN"] += 1
    return Metrics(**{key.lower(): value for key, value in counts.items()})


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/accuracy_metrics.py <benchmark.csv>")
        return 2
    with Path(sys.argv[1]).open(newline="", encoding="utf-8") as handle:
        metrics = calculate(list(csv.DictReader(handle)))
    print(f"TP={metrics.tp} FP={metrics.fp} TN={metrics.tn} FN={metrics.fn}")
    print(f"Precision={metrics.precision:.4f}")
    print(f"Recall={metrics.recall:.4f}")
    print(f"F1={metrics.f1:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
