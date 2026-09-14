# SecurePR Testing Strategy

## Overview

Testing must show that SecurePR detects defined security problems, blocks unsafe pull requests, allows corrected changes to pass, works as a reusable workflow, and reports accuracy honestly.

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
4. Inspect the Check Results table and native tool output.

### PASS test

1. Fix the synthetic defect on the **same branch and same PR**.
2. Push the correction.
3. Confirm the same gate reruns and reports `PASS` when all applicable controls pass.
4. Confirm human-review guidance remains present.

Do not create a second PR just to test the remediation path.

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

The pull-request workflow listens for `labeled` as well as normal PR updates. Adding one of these labels triggers a fresh gate run, which reports the current PR's expected result, actual result, and whether the classification is correct. It also reports cumulative metrics from the committed benchmark CSV.

This provides real-time measurement without allowing an arbitrary PR to redefine the ground truth.

## Benchmark CSV

`docs/accuracy/benchmark-results.csv` is a reviewed labeled evidence ledger. It is **not** automatically appended on every PR.

After a benchmark PR is executed and verified, record its expected and actual result in the CSV through a normal reviewed change. Use a distinct case identifier for each deliberate case.

Current metrics are calculated from every completed labeled row:

- **TP:** expected BLOCK, actual BLOCK.
- **FP:** expected PASS, actual BLOCK.
- **TN:** expected PASS, actual PASS.
- **FN:** expected BLOCK, actual PASS.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × Precision × Recall / (Precision + Recall)`

The current benchmark describes its labeled corpus only; it is not a universal real-world accuracy claim.

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
