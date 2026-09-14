# SecurePR Accuracy Measurement

## Purpose

SecurePR measures the behavior of the **security harness and its configured multi-engine gate** from labeled benchmark cases. A normal pull request does not automatically provide ground truth, so a PASS or BLOCK result by itself is not a TP, FP, TN, or FN.

The measurement evaluates the configured combination of repository profiling, project checks, security engines, SARIF evaluation, and final gate policy. It does not measure one scanner in isolation.

The OWASP Top 10:2025 coverage table is a separate reporting layer. It does not change the overall PASS/BLOCK outcome used by the accuracy benchmark.

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

The current reviewed corpus contains 37 labeled cases:

- TP: 15
- FP: 0
- TN: 16
- FN: 6

Therefore:

- Conventional classification accuracy: `(TP + TN) / total` = **83.78%**
- Precision: **100%**
- Recall: **71.43%**
- F1: **83.33%**

The six false negatives are part of the measured MVP behavior. They should be investigated as possible detection gaps or application-context limitations rather than hidden or reclassified solely to improve a metric. The newest false negative is PR #64 / Actions run #203, where a synthetic `password = "demo_password"` assignment was expected to BLOCK but the gate returned PASS.

The Python AST credential-detection fix was validated after that benchmark case and is now part of `main`. PR #67 was an unlabeled manual validation and is intentionally not added to the benchmark CSV.

## OWASP reporting semantics

The benchmark's overall `actual` result remains the authoritative SecurePR gate outcome. OWASP category results are not additional benchmark classifications.

The Actions summary reports each OWASP category independently from the SARIF findings that can be mapped to that category. A category is:

- `BLOCK` when at least one SARIF finding is mapped to it through an explicit OWASP tag, an OWASP-mapped CWE, or a SecurePR custom rule.
- `PASS` when no mapped automated finding is reported for that category in the run.

A Semgrep or CodeQL step failure therefore does **not** fan out into ten OWASP `BLOCK` rows. Unmapped findings can still make the overall SecurePR gate `BLOCK`, but they are not assigned to an OWASP category without sufficient evidence.

This reporting distinction does not imply complete OWASP coverage. A category `PASS` means no mapped automated finding was reported; it does not prove that the category is secure. Human review remains required.

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

The OWASP reporting correction does not change the 37 historical gate outcomes, so no CSV row is added or rewritten for this PR.

## Interpretation

Accuracy metrics describe the labeled benchmark corpus and its configuration. They are not a universal real-world vulnerability-detection accuracy percentage.

High precision is especially important for a merge gate because excessive false positives can block legitimate development. Recall is also important because missed defects are security gaps. The MVP therefore reports both rather than optimizing a single number.

Human security review remains necessary, especially for business logic, architecture, threat assumptions, authorization intent, and other context-dependent risks.
