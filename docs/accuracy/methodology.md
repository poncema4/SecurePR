# SecurePR Accuracy Measurement

## Purpose

SecurePR measures the behavior of the **security harness and its configured multi-engine gate** from labeled benchmark cases. A normal pull request does not automatically provide ground truth, so a PASS or BLOCK result by itself is not a TP, FP, TN, or FN.

The measurement evaluates the configured combination of repository profiling, project checks, security engines, SARIF evaluation, and final gate policy. It does not measure one scanner in isolation.

## Labeled benchmark cases

`docs/accuracy/benchmark-results.csv` is the reviewed benchmark ledger. Each completed row contains:

- `case_id` — stable case identifier.
- `category` — security category or control.
- `description` — short case description.
- `expected` — ground-truth `PASS` or `BLOCK`.
- `actual` — observed SecurePR `PASS` or `BLOCK`.
- `notes` — evidence and classification context.

Both expected and actual values must be known before a row contributes to the metrics.

## Current MVP benchmark

The current reviewed corpus contains 26 labeled cases:

- TP: 10
- FP: 0
- TN: 11
- FN: 5

Therefore:

- Conventional classification accuracy: `(TP + TN) / total` = **80.77%**
- Precision: **100%**
- Recall: **66.67%**
- F1: **80.00%**

The five false negatives are part of the measured MVP behavior. They should be investigated as possible detection gaps or application-context limitations rather than hidden or reclassified solely to improve a metric.

## Real pull-request benchmark mode

A real PR can be evaluated as a benchmark case during its Actions run when a trusted reviewer adds exactly one expected-outcome label:

- `securepr-expected-pass`
- `securepr-expected-block`

SecurePR immediately reports the current PR's expected result, actual gate result, and whether the classification is correct. It also reports cumulative metrics from the committed CSV.

This current-PR measurement does not automatically modify the CSV. The expected result is ground truth and must be deliberately reviewed before becoming permanent benchmark evidence.

## Metrics

- **TP:** expected `BLOCK`, actual `BLOCK`.
- **FP:** expected `PASS`, actual `BLOCK`.
- **TN:** expected `PASS`, actual `PASS`.
- **FN:** expected `BLOCK`, actual `PASS`.

`Accuracy = (TP + TN) / (TP + FP + TN + FN)`

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × Precision × Recall / (Precision + Recall)`

The implementation returns `0` when a denominator is zero rather than inventing a percentage.

## CSV update policy

The CSV is intentionally not appended on every ordinary PR. SecurePR cannot safely infer the expected outcome of arbitrary developer changes, and allowing arbitrary PRs to mutate the accuracy ledger would make the measurement easy to manipulate.

After a labeled benchmark PR has been executed and verified, record the case in the CSV through a normal reviewed change. Use a distinct case identifier for each deliberate benchmark case so the measurement history remains auditable.

## Interpretation

Accuracy metrics describe the labeled benchmark corpus and its configuration. They are not a universal real-world vulnerability-detection accuracy percentage.

High precision is especially important for a merge gate because excessive false positives can block legitimate development. Recall is also important because missed defects are security gaps. The MVP therefore reports both rather than optimizing a single number.

Human security review remains necessary, especially for business logic, architecture, threat assumptions, authorization intent, and other context-dependent risks.
