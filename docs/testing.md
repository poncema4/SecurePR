# SecurePR Testing Strategy

## Overview

Testing must show that the SecurePR **harness** orchestrates its underlying engines correctly, detects defined security problems, blocks unsafe pull requests, allows corrected changes to pass, works as a reusable workflow, and reports benchmark behavior honestly.

SecurePR is not tested as if it were one scanner. The test strategy validates the interaction of repository profiling, project tests, Gitleaks, Semgrep, dependency audits, CodeQL, SARIF aggregation, and final PASS/BLOCK policy.

## Local Verification

From the repository root:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

On Windows PowerShell, use:

```powershell
python -m pytest -q
python -m compileall -q app security tests scripts
python .\scripts\accuracy_report.py
```

GitHub Actions is authoritative for the complete gate because it runs CodeQL, Semgrep, Gitleaks, dependency audits, and GitHub-specific reporting.

## PASS and BLOCK testing

Use controlled synthetic examples only. Never commit real credentials.

### BLOCK test

1. Create a safe synthetic change containing a known high-confidence security defect, such as a credential-like literal that matches a SecurePR rule.
2. Open one PR against `main`.
3. Confirm `SecurePR Security Gate` reports `BLOCK`.
4. Inspect the Check Results table and native engine output.

### PASS test

1. Fix the synthetic defect on the **same branch and same PR**.
2. Push the correction.
3. Confirm the same gate reruns and reports `PASS` when all applicable controls pass.
4. Confirm human-review guidance remains present.

Do not create a second PR just to test the remediation path.

## Engine-specific validation

Controlled cases should exercise the different evidence sources independently where practical:

- **Semgrep:** custom SecurePR rules and broader `p/security-audit` rules.
- **CodeQL:** supported-language semantic/data-flow security queries.
- **Gitleaks:** synthetic secret and credential cases.
- **Dependency audits:** intentionally selected vulnerable dependency fixtures where safe and reproducible.
- **Project tests:** application-specific security and correctness properties.
- **SARIF aggregation:** multiple scanner reports and duplicate/different finding behavior.

The purpose is to verify that SecurePR remains the harness and that each engine contributes its own evidence rather than being treated as interchangeable.

## Reusable workflow testing

Add the reusable workflow to a repository you own or are authorized to assess:

```yaml
jobs:
  securepr:
    uses: poncema4/SecurePR/.github/workflows/reusable-security.yml@main
```

For stronger reproducibility, pin the workflow to a reviewed SecurePR commit SHA.

The target repository determines which language, dependency, project-test, and CodeQL controls are applicable.

## Real-PR accuracy testing

A normal PR is not automatically a benchmark case because its expected security outcome is unknown.

For a controlled real-PR benchmark, a trusted reviewer adds exactly one expected-outcome label:

- `securepr-expected-pass`
- `securepr-expected-block`

The Actions summary reports the current PR's expected result, actual result, and whether the classification is correct. It also reports cumulative metrics from the committed benchmark CSV.

This provides real-time measurement without allowing an arbitrary PR to redefine the ground truth.

## Benchmark CSV

`docs/accuracy/benchmark-results.csv` is a reviewed labeled evidence ledger. It is **not** automatically appended on every PR.

The current benchmark contains 37 labeled cases:

- TP: 15
- FP: 0
- TN: 16
- FN: 6
- Conventional classification accuracy: 83.78%
- Precision: 100%
- Recall: 71.43%
- F1: 83.33%

PR #63 / Actions run #202 is a labeled PASS case. PR #64 / Actions run #203 is a labeled BLOCK case that returned PASS, so it is a measured false negative and is retained as evidence rather than being hidden. The follow-up credential-detection fix is validated independently.

The false negatives are part of the measured MVP evidence. They should be investigated for genuine detection gaps, but benchmark optimization must not weaken precision or create unsupported universal claims.

## Pull Request versus main

A passing PR does not guarantee that the post-merge `main` workflow will pass. Final verification requires both the PR run and the independent `main` run.

## Safety

- Use synthetic secrets only.
- Never use real API keys, passwords, tokens, private keys, or cloud credentials.
- Keep intentionally vulnerable examples isolated and controlled.
- Do not test production systems.
- Do not automatically exploit discovered vulnerabilities.

## Completion Criteria

The MVP is complete when implementation, local verification, reusable-workflow validation, documentation review, consolidated PR validation, merge, and post-merge `main` verification pass. Accuracy is continuously measurable for labeled benchmark cases and grows as verified cases are deliberately added to the benchmark ledger.
