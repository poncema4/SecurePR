# GitHub Actions and SecurePR Security Gate

## Purpose
SecurePR uses GitHub Actions to run automated security controls for pull requests targeting `main` and for post-merge `main` verification.

The authoritative workflow in SecurePR is `.github/workflows/security.yml`. The reusable implementation is `.github/workflows/reusable-security.yml` and can be called by other repositories you control.

## One-job architecture

The SecurePR repository keeps one job named `SecurePR Security Gate`. Individual tools run as steps inside that job so the PR has one authoritative required gate rather than many required tool checks.

The gate includes repository profiling, applicable project checks, Gitleaks, Semgrep, dependency auditing, CodeQL, SARIF security-finding evaluation, accuracy reporting, and final PASS/BLOCK reporting.

## SecurePR versus security engines

`SecurePR Security Gate` is the **harness, orchestration, policy, aggregation, and reporting layer**. It does not replace specialist security engines.

- **CodeQL** performs semantic source-code analysis for supported languages.
- **Semgrep** performs complementary rule-based SAST and runs SecurePR-specific high-confidence rules.
- **Gitleaks** performs secret and credential detection.
- **Dependency auditors** check supported dependency manifests for known vulnerabilities.
- **Project tests** validate application behavior and security properties that static analysis cannot prove.
- **SecurePR** combines those signals, applies the gate policy, maps them to the OWASP Top 10:2025 coverage framework, and publishes one PASS/BLOCK result.

## OWASP Top 10:2025

SecurePR does not contain a separate scanner for each OWASP category. OWASP Top 10:2025 is a coverage framework used to organize the evidence produced by the underlying engines and project controls.

For example, injection-related coverage comes primarily from CodeQL, Semgrep, and project tests; cryptographic-failure coverage comes from CodeQL and Semgrep; supply-chain coverage includes dependency auditing; and insecure-design coverage necessarily includes human architecture and business-logic review.

A category row is `PASS` when its mapped automated controls pass and `BLOCK` when one of those mapped controls blocks. A category `PASS` is not proof that the entire category is secure.

## Reusable workflow

Other repositories can call the reusable workflow from this repository without installing a GitHub Marketplace product. The called workflow checks out the target repository, checks out the SecurePR tooling at the requested ref, profiles the target repository, runs applicable controls, reports the current accuracy-benchmark status, and publishes the same PASS/BLOCK gate.

A target repository can add:

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

For stronger reproducibility, pin the reusable workflow to a reviewed SecurePR commit SHA instead of tracking `main`.

The SecurePR repository itself checks out the PR head SHA for its tooling so changes to the gate are tested before they are merged. Other repositories normally use `main` or a pinned reviewed ref.

The intended initial targets are SecurePR, CookieGuard, and NetDefender. Applicability is repository-specific: languages, dependency manifests, tests, and available security evidence determine which controls actually run.

## Accuracy status on every PR

Every PR includes an accuracy section in the Actions summary.

- Before the final benchmark is executed: `Benchmark pending — no accuracy percentage is claimed.`
- After labeled benchmark results are recorded: the latest TP, FP, TN, precision, recall, and F1 are reported.

This status is informational and does not substitute for the controlled benchmark. It prevents SecurePR from inventing an accuracy percentage while making the current measurement state visible.

The source ledger is `docs/accuracy/benchmark-results.csv`.

## PASS/BLOCK

There are only two gate outcomes:

- **PASS:** all configured blocking controls pass and no blocking security finding remains.
- **BLOCK:** at least one configured blocking control fails or a blocking security finding remains.

The user-facing Actions summary is ordered as:

1. `SecurePR: PASS` or `SecurePR: BLOCK`
2. Check Results
3. Current gate result explanation
4. OWASP Top 10:2025 Coverage
5. Fixes to make this PASS
6. Remediation
7. Accuracy
8. Human review
9. Full Actions run link

Every outcome states that human review is always recommended. SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges a PR.

## Evidence

Detailed SARIF and diagnostic outputs are retained as an Actions artifact named `securepr-evidence`. The artifact is evidence, not a separate gate. Gitleaks also produces its own `gitleaks-results.sarif` artifact through the Gitleaks action.

The user-facing summary intentionally stays concise; detailed tool output remains available from the individual Actions steps and evidence artifacts.

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

## Development and testing workflow

Use one branch and one consolidated PR for a related implementation change. If the gate blocks, fix the issue on the same branch and rerun the same PR.

For final verification:

1. Run the local Python tests and compilation checks.
2. Open/update the consolidated PR.
3. Confirm `SecurePR Security Gate` passes.
4. Inspect the Actions summary, including Check Results and the OWASP coverage table.
5. Inspect `securepr-evidence` when detailed SARIF or diagnostics are needed.
6. After merge, confirm the independent `main` workflow passes.
7. Run the controlled accuracy benchmark separately and record actual expected/actual classifications in `docs/accuracy/benchmark-results.csv`.

Do not claim benchmark accuracy from a normal passing PR. Do not populate benchmark `actual` values unless the corresponding case was actually executed through the gate.
