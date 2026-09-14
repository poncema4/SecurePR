# GitHub Actions and SecurePR Security Gate

## Purpose
SecurePR uses GitHub Actions to run automated security controls for pull requests targeting `main` and for post-merge `main` verification.

The authoritative entry workflow is `.github/workflows/security.yml`. It calls `.github/workflows/reusable-security.yml`, which contains the reusable security-gate implementation.

## One-job architecture

The SecurePR repository keeps one job named `SecurePR Security Gate`. Individual tools run as steps inside that job so the PR has one authoritative required gate rather than many required tool checks.

The reusable implementation includes repository profiling, applicable project checks, Gitleaks, Semgrep, dependency auditing, CodeQL, normalized SARIF finding aggregation, per-run accuracy status, and final PASS/BLOCK reporting.

## SecurePR versus CodeQL

`SecurePR Security Gate` is the project's harness and policy layer. CodeQL is one analysis engine inside it.

CodeQL performs semantic source-code security analysis for supported languages and uploads results to GitHub Code Scanning. Code Scanning is an additional reporting surface, not a second SecurePR job.

SecurePR combines CodeQL with Semgrep, Gitleaks, dependency audits, project tests, repository profiling, and its own policy rules.

## Reusable workflow

Other repositories can call the reusable workflow from this repository without installing a GitHub Marketplace product. The called workflow checks out the target repository, checks out the SecurePR tooling at the requested ref, profiles the target repository, runs applicable controls, reports the current accuracy-benchmark status, and publishes the same PASS/BLOCK gate.

The SecurePR repository itself calls the same reusable workflow using the Phase 4 PR commit for its tooling, so the PR tests the implementation under review rather than an older `main` copy.

The MVP is intentionally limited to the user's own repositories. Public Marketplace packaging is outside Phase 4.

## Accuracy status on every PR

Every PR includes an accuracy section in the Actions summary.

- Before the final benchmark is executed: `Benchmark pending — no accuracy percentage is claimed.`
- After the benchmark results are recorded: the latest TP, FP, TN, precision, recall, and F1 are reported.

This status is informational and does not substitute for the final controlled benchmark. It prevents SecurePR from inventing an accuracy percentage while still making the current measurement state visible on every PR.

## PASS/BLOCK

There are only two gate outcomes:

- **PASS:** all configured blocking controls pass and no blocking normalized finding remains.
- **BLOCK:** at least one configured blocking control fails or a blocking normalized finding remains.

Every outcome states that human review is always recommended. SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges a PR.

## Finding aggregation

Semgrep and CodeQL produce SARIF results. SecurePR normalizes identical findings using location, rule, and message so the summary can present one meaningful issue rather than multiple copies. Tool names remain visible in the normalized summary. Distinct findings at the same file and line are not collapsed merely because they share a location.

## Pull request versus main

A successful PR run is not a guarantee that the post-merge `main` run will pass. The two executions can differ in commit context and repository state.

The required workflow therefore runs on both:

```text
PR → SecurePR PASS → human review → merge
                                      ↓
                              push to main
                                      ↓
                              SecurePR reruns
                                      ↓
                              main independently verified
```

Final Phase 4 completion requires the post-merge `main` run to pass.

## Development workflow

For Phase 4 and later, use one feature branch for the entire phase and one consolidated PR into `main`.

```text
feature branch
    ↓
implement entire phase
    ↓
local validation
    ↓
documentation audit
    ↓
one consolidated PR
    ↓
SecurePR PASS/BLOCK
    ↓
PASS → human review → merge
BLOCK → fix same branch/PR → rerun
    ↓
post-merge main verification
```

Do not create multiple PRs for one phase.
