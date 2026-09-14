from __future__ import annotations

from pathlib import Path

from scripts.accuracy_report import render


def test_accuracy_report_is_explicitly_pending_before_final_benchmark(tmp_path: Path) -> None:
    report = render(tmp_path / "missing-results.csv")

    assert "Benchmark pending" in report
    assert "No accuracy percentage is claimed" in report


def test_accuracy_report_renders_measured_metrics(tmp_path: Path) -> None:
    results = tmp_path / "results.csv"
    results.write_text(
        "case,expected,actual\n"
        "vulnerable-1,BLOCK,BLOCK\n"
        "safe-1,PASS,PASS\n"
        "safe-2,PASS,BLOCK\n"
        "vulnerable-2,BLOCK,PASS\n",
        encoding="utf-8",
    )

    report = render(results)

    assert "TP: 1" in report
    assert "FP: 1" in report
    assert "TN: 1" in report
    assert "FN: 1" in report
    assert "Precision: 0.5000" in report
    assert "Recall: 0.5000" in report
    assert "F1: 0.5000" in report


def test_accuracy_report_renders_current_labeled_pr(monkeypatch, tmp_path: Path) -> None:
    results = tmp_path / "results.csv"
    results.write_text(
        "case,expected,actual\n"
        "safe-1,PASS,PASS\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("SECUREPR_EXPECTED_OUTCOME", "BLOCK")
    monkeypatch.setenv("SECUREPR_ACTUAL_OUTCOME", "BLOCK")

    report = render(results)

    assert "Current PR benchmark case" in report
    assert "Expected: `BLOCK`" in report
    assert "Actual: `BLOCK`" in report
    assert "Classification: `CORRECT`" in report


def test_accuracy_report_does_not_count_unlabeled_pr(monkeypatch, tmp_path: Path) -> None:
    results = tmp_path / "results.csv"
    results.write_text(
        "case,expected,actual\n"
        "safe-1,PASS,PASS\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("SECUREPR_EXPECTED_OUTCOME", raising=False)
    monkeypatch.delenv("SECUREPR_ACTUAL_OUTCOME", raising=False)

    report = render(results)

    assert "No expected benchmark outcome was supplied" in report
