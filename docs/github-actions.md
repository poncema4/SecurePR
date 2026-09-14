# GitHub Actions and SecurePR Security Gate

## Purpose

SecurePR uses GitHub Actions as the execution layer for its reusable **security harness**. The harness coordinates multiple independent security engines and project checks, then applies one common policy to produce `PASS` or `BLOCK`.

The authoritative workflow is `.github/workflows/security.yml`. It defines the stable `SecurePR Security Gate` job and the final gate policy. `.github/workflows/reusable-security.yml` exposes the same implementation for authorized target repositories.

## One-job architecture

The gate exposes one job named `SecurePR Security Gate`. Tools run as steps inside that job so a repository can require one stable security check.

The job includes repository profiling, applicable project tests, Gitleaks, Semgrep, dependency auditing, CodeQL, SARIF finding evaluation, accuracy reporting, and final PASS/BLOCK reporting.

```text
SecurePR Security Gate
        │
        ├── Applicability / repository profile
        ├── Project tests
        ├── Gitleaks
        ├── Semgrep
        ├── Dependency audit
        └── CodeQL
                 ↓
        Evidence / SARIF
                 ↓
        SecurePR policy + aggregation
                 ↓
             PASS / BLOCK
```

## Rule Book

SecurePR does not use a single prompt to judge a PR. The executable policy is layered across:

- `.github/workflows/security.yml` — orchestration and final gate decision.
- `.semgrep_securepr.yml` — SecurePR-specific Semgrep rules.
- Semgrep `p/security-audit` — broad rule-based SAST.
- CodeQL `security-extended` — semantic/data-flow analysis.
- Gitleaks — secret detection.
- `pip-audit` / `npm audit` — supported dependency vulnerability auditing.
- Target repository tests — application-specific checks.
- `repository_profile.py` — applicability and language detection.
- `summarize_sarif.py` — security-evidence aggregation.

See `docs/security-checks.md` for the complete control reference.

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

The called workflow checks out the target repository, obtains the SecurePR tooling at the requested ref, profiles the target, runs applicable controls, and publishes the gate result.

## How the engines work together

The engines are complementary rather than interchangeable:

- **CodeQL** performs semantic security analysis and can reason about source structure and data flow.
- **Semgrep** performs rule-based SAST using both its broad security rules and SecurePR's custom rules.
- **Gitleaks** specializes in detecting secret and credential material.
- **Dependency auditors** identify known vulnerabilities in supported package ecosystems.
- **Project tests** validate application behavior and security properties that generic static analysis may not know.

SecurePR is responsible for deciding which controls apply, collecting their outcomes, aggregating scanner evidence, and turning the combined evidence into the single gate result.

## PASS/BLOCK

There are only two outcomes:

- **PASS:** configured blocking controls pass and no blocking security finding remains.
- **BLOCK:** a configured blocking control fails or a blocking security finding remains.

Human review is always recommended for both outcomes. SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges pull requests.

## OWASP Top 10:2025

OWASP Top 10:2025 is used as a coverage framework. SecurePR maps automated evidence from the engines and project checks to the categories; it does not implement ten separate scanners or claim complete automation.

A category PASS means the mapped automated controls passed. It does not prove the complete category is secure.

## Evidence

SARIF and diagnostic outputs are retained in the `securepr-evidence` Actions artifact. Native tool output remains available in the individual Actions steps.

## Accuracy status

Every PR receives an accuracy section in the Actions summary. An ordinary PR shows the cumulative labeled benchmark but is not counted as a TP, FP, TN, or FN because ground truth is unknown.

For a controlled benchmark PR, a trusted reviewer adds `securepr-expected-pass` or `securepr-expected-block`. The workflow reports the current PR's expected result, actual result, and classification correctness alongside cumulative TP, FP, TN, precision, recall, and F1.

The current reviewed benchmark contains 35 cases: 15 TP, 0 FP, 15 TN, and 5 FN. This is 85.71% conventional classification accuracy, 100% precision, 75.00% recall, and 85.71% F1 for the controlled corpus only.

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
5. Inspect the Actions summary and native engine evidence.
6. If benchmarking a real PR, add the trusted expected-outcome label and verify expected versus actual.
7. After merge, confirm the independent `main` run passes.
8. Add verified benchmark cases to the CSV through a reviewed change.
