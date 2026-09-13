# GitHub Actions and SecurePR Security Gate

## Purpose

SecurePR uses GitHub Actions to run automated security controls for pull requests targeting `main` and for post-merge `main` verification.

The authoritative workflow is `.github/workflows/security.yml`. Phase 4 also adds `.github/workflows/reusable-security.yml` for reuse across the user's own repositories.

## One-job architecture

The SecurePR repository keeps one job named `SecurePR Security Gate`. Individual tools run as steps inside that job so the PR has one authoritative required gate rather than many required tool checks.

Phase 4 steps include repository profiling, Python/runtime and project checks where applicable, Gitleaks, Semgrep, dependency auditing, CodeQL, normalized SARIF finding aggregation, and final PASS/BLOCK reporting.

## SecurePR versus CodeQL

`SecurePR Security Gate` is the project's harness and policy layer. CodeQL is one analysis engine inside it.

CodeQL performs semantic source-code security analysis for supported languages and uploads results to GitHub Code Scanning. Code Scanning is an additional reporting surface, not a second SecurePR job.

SecurePR consumes CodeQL completion/results together with Semgrep, Gitleaks, dependency audits, tests, repository profiling, and its own policy rules.

## Reusable workflow

Other repositories can call the reusable workflow from this repository without installing a GitHub Marketplace product. The called workflow checks out the target repository, checks out the SecurePR tooling files, profiles the target repository, runs applicable controls, and publishes the same PASS/BLOCK gate.

The MVP is intentionally limited to the user's own repositories. Public Marketplace packaging is outside Phase 4.

## PASS/BLOCK

There are only two gate outcomes:

- **PASS:** all configured blocking controls pass and no blocking normalized finding remains.
- **BLOCK:** at least one configured blocking control fails or a blocking normalized finding remains.

Every outcome states that human review is always recommended. SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges a PR.

## Finding aggregation

Semgrep and CodeQL produce SARIF results. SecurePR normalizes identical findings by tool, rule, file, line, and message so the summary can present one meaningful issue rather than multiple copies. Native Actions logs remain available for investigation.

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
