# SecurePR Setup

SecurePR is a **security harness**, not a standalone vulnerability scanner. The harness coordinates existing security-analysis engines, project tests, repository profiling, evidence aggregation, policy, and reporting. CodeQL, Semgrep, Gitleaks, dependency auditors, and project tests provide the underlying evidence; SecurePR turns that evidence into one `PASS` or `BLOCK` gate.

## Requirements

For local development:

- Python 3.11 or newer
- Git
- A repository checkout

For the complete gate:

- GitHub repository
- GitHub Actions enabled
- Permission to add the workflow to the repository

The complete SecurePR gate runs on a GitHub-hosted Linux runner. The local helper scripts work on Linux and Windows.

## Local verification

From the SecurePR repository root:

```bash
chmod +x scripts/setup.sh scripts/verify.sh
./scripts/setup.sh
./scripts/verify.sh
```

Optional Python selection:

```bash
PYTHON_BIN=python3.12 ./scripts/setup.sh
```

Run local verification directly:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

Local verification validates the Python-side SecurePR implementation. It does not replace the complete GitHub Actions gate, which also runs GitHub-specific CodeQL, Gitleaks, Semgrep, dependency, SARIF, and summary steps.

## Add SecurePR to an authorized repository

SecurePR is reusable through `.github/workflows/reusable-security.yml`. The target repository does not copy the scanner implementations; it calls the SecurePR harness.

Create `.github/workflows/securepr.yml` in the target repository:

```yaml
name: SecurePR Security Gate

on:
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened, labeled]
  push:
    branches: [main]

jobs:
  securepr:
    uses: poncema4/SecurePR/.github/workflows/reusable-security.yml@main
```

For reproducibility and stronger supply-chain control, pin the reusable workflow to a reviewed SecurePR commit SHA instead of `main`.

## What happens when a PR runs

```text
Target repository PR
        ↓
SecurePR reusable harness
        ↓
Repository profile / applicability
        ↓
Project tests + dependency audit
        ↓
Gitleaks + Semgrep + CodeQL
        ↓
Security evidence / SARIF
        ↓
SecurePR policy + aggregation
        ↓
PASS or BLOCK
        ↓
Human review
```

The harness determines which language and dependency controls are applicable. CodeQL runs for languages detected as CodeQL-supported; unsupported extensions are reported by repository profiling rather than silently treated as covered.

## What each engine does

- **CodeQL:** semantic/data-flow source-code security analysis using the configured `security-extended` query suite.
- **Semgrep:** rule-based SAST using `p/security-audit` plus SecurePR's custom `.semgrep_securepr.yml` rules.
- **Gitleaks:** secret and credential detection.
- **Dependency auditors:** known vulnerability checks for supported Python/npm dependency manifests.
- **Project tests:** application-specific security/correctness evidence.

SecurePR is the layer that orchestrates these engines, evaluates applicability, aggregates their evidence, and publishes the final gate decision.

## Where the rule book lives

There is no single security prompt. The main policy sources are:

- `.github/workflows/security.yml` — authoritative workflow and final PASS/BLOCK policy.
- `.semgrep_securepr.yml` — SecurePR-specific Semgrep rules.
- `docs/security-checks.md` — human-readable control inventory and OWASP mapping.
- `scripts/repository_profile.py` — language/dependency applicability.
- `scripts/summarize_sarif.py` — SARIF finding aggregation.
- `scripts/accuracy_report.py` — controlled benchmark reporting.

## Using the harness on additional repositories

For each repository you own or are authorized to assess:

1. Add the caller workflow above.
2. Push it to a branch and open a PR.
3. Confirm `SecurePR Security Gate` runs.
4. Review the Check Results and native engine output.
5. Fix blocking findings on the same PR branch.
6. Push the fix and let the same gate rerun.
7. Merge only after the PR gate passes and human review is complete.
8. Confirm the independent push-to-`main` SecurePR run passes.

The target repository does not need to contain SecurePR's scanner or reporting implementation. Those are supplied by the reusable workflow.

## Real-PR accuracy testing

A normal PR has no independent ground-truth security outcome, so SecurePR must not automatically count every PR as a benchmark case.

For a deliberately selected real PR, a trusted reviewer can add exactly one expected-outcome label:

```text
securepr-expected-pass
```

or

```text
securepr-expected-block
```

The caller workflow includes the `labeled` pull-request event, so adding one of these labels triggers a fresh SecurePR run against the current PR head.

The Actions summary reports the expected result, actual SecurePR result, classification correctness, and cumulative TP, FP, TN, precision, recall, and F1.

## Benchmark and current MVP result

`docs/accuracy/benchmark-results.csv` is a reviewed ground-truth ledger and is not automatically changed by ordinary PR runs.

The current 37-case controlled benchmark contains 15 TP, 0 FP, 16 TN, and 6 FN:

- Conventional classification accuracy: **83.78%**
- Precision: **100%**
- Recall: **71.43%**
- F1: **83.33%**

PR #63 / Actions run #202 is the latest manual PASS case. PR #64 / Actions run #203 is the latest manual hardcoded-password BLOCK case, but SecurePR returned PASS; it is therefore a recorded false negative. The credential-detection fix in the follow-up validation PR adds a Python AST-based high-confidence assignment rule.

These metrics describe the labeled benchmark corpus and configuration only; they are not universal real-world accuracy claims.

## PASS and BLOCK

- `PASS` — applicable blocking controls completed successfully and no blocking security finding remains.
- `BLOCK` — a blocking control failed or a blocking security finding remains.

Human review is always recommended for both outcomes. SecurePR never automatically remediates source code, rotates credentials, dismisses findings, or merges a pull request.

## Recommended verification order

1. Run local setup and tests.
2. Add the caller workflow to an owned/authorized repository.
3. Open a normal PR and verify the gate.
4. Review the full Actions summary and evidence artifacts.
5. Test a controlled BLOCK case.
6. Fix it on the same PR and verify PASS.
7. Test labeled benchmark cases.
8. Record verified benchmark cases in the CSV through reviewed changes.
9. Merge after the PR gate passes and human review is complete.
10. Verify the post-merge `main` run.
