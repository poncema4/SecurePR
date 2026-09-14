# GitHub Actions and SecurePR Security Gate

## Purpose

SecurePR uses GitHub Actions for pull-request security checks and independent post-merge `main` verification.

The authoritative workflow is `.github/workflows/security.yml`. It calls `.github/workflows/reusable-security.yml`, which contains the actual gate implementation.

## One-job architecture

The gate exposes one job named `SecurePR Security Gate`. Tools run as steps inside that job so a repository can require one stable security check.

The gate includes repository profiling, applicable project tests, Gitleaks, Semgrep, dependency auditing, CodeQL, SARIF finding evaluation, accuracy reporting, and final PASS/BLOCK reporting.

## Reusable workflow

A repository you own or are authorized to assess can call:

```yaml
name: SecurePR Security Gate

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  securepr:
    uses: poncema4/SecurePR/.github/workflows/reusable-security.yml@main
```

For stronger reproducibility, pin the workflow to a reviewed SecurePR commit SHA.

The called workflow checks out the target repository, checks out the requested SecurePR tooling ref, profiles the target, runs applicable controls, and publishes the gate result.

## Real-time accuracy status

Every PR receives an accuracy section in the Actions summary.

An ordinary PR shows the cumulative labeled benchmark but is not counted as a TP, FP, TN, or FN because ground truth is unknown.

For a controlled real-PR benchmark, a trusted reviewer adds one of:

- `securepr-expected-pass`
- `securepr-expected-block`

The workflow then reports the current PR's expected result, actual SecurePR result, and whether the classification is correct, alongside cumulative TP, FP, TN, precision, recall, and F1.

The benchmark CSV is not automatically changed by the PR run. Permanent benchmark history is updated deliberately after the case has been reviewed and verified.

## PASS/BLOCK

There are only two outcomes:

- **PASS:** configured blocking controls pass and no blocking security finding remains.
- **BLOCK:** a configured blocking control fails or a blocking security finding remains.

Human review is always recommended for both outcomes. SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges pull requests.

## OWASP Top 10:2025

OWASP Top 10:2025 is used as a coverage framework. SecurePR maps automated evidence to the categories; it does not implement ten separate scanners or claim complete automation.

A category PASS means the mapped automated controls passed. It does not prove the complete category is secure.

## Evidence

SARIF and diagnostic outputs are retained in the `securepr-evidence` Actions artifact. Native tool output remains available in the individual Actions steps.

## Pull request versus main

A successful PR run does not guarantee that the post-merge `main` run will pass. Final verification requires both.

```text
PR → SecurePR PASS → human review → merge
                                      ↓
                              push to main
                                      ↓
                              SecurePR reruns
                                      ↓
                              main independently verified
```

## Development workflow

1. Run local tests and verification.
2. Open one consolidated PR for the change.
3. Fix any blocking result on the same PR branch.
4. Confirm `SecurePR Security Gate` passes.
5. Inspect the Actions summary and evidence artifacts.
6. If benchmarking a real PR, add the trusted expected-outcome label and verify expected versus actual.
7. After merge, confirm the independent `main` run passes.
8. Add verified benchmark cases to the CSV through a reviewed change.
