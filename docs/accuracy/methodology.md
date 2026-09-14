# SecurePR Accuracy Measurement

## Purpose

SecurePR does not claim a universal detection-accuracy percentage from a single successful or failed pull request. Detection quality is measured from controlled, labeled benchmark cases.

## Required benchmark fields

`docs/accuracy/benchmark-results.csv` records one case per row:

- `case_id`: stable identifier for the controlled case.
- `category`: security category or control being evaluated.
- `description`: short description of the case.
- `expected`: ground-truth gate result, `PASS` or `BLOCK`.
- `actual`: observed SecurePR gate result, `PASS` or `BLOCK`.
- `notes`: evidence, tool output, or explanation for the classification.

A row must have both `expected` and `actual` populated with valid `PASS`/`BLOCK` values before it contributes to the metrics.

## Confusion matrix

For each labeled case:

- **True Positive (TP):** expected `BLOCK`, actual `BLOCK`.
- **False Positive (FP):** expected `PASS`, actual `BLOCK`.
- **True Negative (TN):** expected `PASS`, actual `PASS`.
- **False Negative (FN):** expected `BLOCK`, actual `PASS`.

## Formulas

**Precision** measures how often a SecurePR BLOCK corresponds to a case that should actually be blocked:

`Precision = TP / (TP + FP)`

**Recall** measures how often SecurePR blocks cases that should actually be blocked:

`Recall = TP / (TP + FN)`

**F1** balances precision and recall:

`F1 = 2 × Precision × Recall / (Precision + Recall)`

The implementation returns `0` when a denominator is zero rather than inventing a percentage.

## Per-use interpretation

A normal pull request provides an observed gate result, but it does not automatically provide ground truth. Therefore a PR PASS/BLOCK result is not itself a TP, FP, TN, or FN.

When a controlled case has a known expected result, record the expected and observed outcomes in the benchmark CSV. Re-running the same controlled case after a fix creates new evidence; it should be recorded with a distinct case identifier or benchmark revision so the measurement history remains auditable.

This prevents SecurePR from calling an unknown result a false positive or false negative merely because a developer disagrees with a tool. False-positive and false-negative classifications require a ground-truth label supported by the controlled benchmark evidence.

## Final Phase 4 benchmark

The final Phase 4 validation should include both vulnerable/block cases and safe/pass cases across the supported security controls. The resulting CSV is the source data for TP, FP, TN, FN, precision, recall, and F1.

The benchmark should be executed only after the implementation and documentation stabilize, as defined by the Phase 4 plan. Until then, the Actions summary reports **Benchmark pending** rather than an unsupported accuracy percentage.
