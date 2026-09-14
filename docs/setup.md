# SecurePR Setup

SecurePR is a **security harness**, not a standalone vulnerability scanner. The harness coordinates existing security-analysis engines, project tests, repository profiling, result aggregation, policy, and reporting. CodeQL, Semgrep, Gitleaks, dependency auditors, and project tests provide the underlying evidence; SecurePR turns that evidence into one `PASS` or `BLOCK` gate.

The MVP is designed around the user's own repositories. It is not currently a hosted service for granting SecurePR access to arbitrary third-party repositories.

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

## Linux local setup

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

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the local verification directly:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

Local verification validates the Python-side SecurePR implementation. It does not replace the complete GitHub Actions gate, which also runs GitHub-specific CodeQL, Gitleaks, Semgrep, dependency, SARIF, and summary steps.

## Windows PowerShell setup

From the SecurePR repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
.\scripts\verify.ps1
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run local verification:

```powershell
python -m pytest -q
python -m compileall -q app security tests scripts
python .\scripts\accuracy_report.py
```

If `python` is not recognized, install Python 3.11+ and make sure Python is available on `PATH`.

## Add SecurePR to one of your repositories

SecurePR is reusable through `.github/workflows/reusable-security.yml`. The target repository does not copy the scanner implementation; it calls the SecurePR harness.

In the target repository, create:

```text
.github/workflows/securepr.yml
```

Use:

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

For reproducibility, pin the reusable workflow to a reviewed SecurePR commit SHA instead of `main`.

### What happens when the PR runs

```text
Target repository PR
        ↓
SecurePR reusable harness
        ↓
Repository profile
        ↓
Applicable project tests
        ↓
Gitleaks + Semgrep + CodeQL + dependency audit
        ↓
Security evidence / SARIF
        ↓
SecurePR policy + aggregation
        ↓
🟢 SecurePR: PASS
or
🔴 SecurePR: BLOCK
```

The harness determines which language and dependency controls are applicable. CodeQL is used for languages detected as CodeQL-supported; unsupported extensions are reported by repository profiling rather than silently treated as covered.

## Using the harness on additional owned repositories

For each repository you own:

1. Add the small caller workflow above.
2. Push it to a branch and open a PR.
3. Confirm `SecurePR Security Gate` runs.
4. Review the Check Results and native tool output.
5. Fix blocking findings on the same PR branch.
6. Push the fix and let the same gate rerun.
7. Merge only after the PR gate passes and human review is complete.
8. Confirm the independent push-to-`main` SecurePR run passes.

The target repository does not need to contain SecurePR's `scripts/`, `.semgrep_securepr.yml`, or reporting implementation. Those are supplied by the reusable SecurePR workflow.

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

The caller workflow includes the `labeled` pull-request event. Adding one of these labels therefore triggers a fresh SecurePR run against the current PR head.

The Actions summary then reports the current benchmark context:

- Expected result: `PASS` or `BLOCK`.
- Actual SecurePR result: `PASS` or `BLOCK`.
- Classification: correct or incorrect.
- Cumulative TP, FP, TN, precision, recall, and F1 from the benchmark CSV.

This is the realtime expected-versus-actual measurement for a labeled PR.

## Why the benchmark CSV is not automatically changed

`docs/accuracy/benchmark-results.csv` is a reviewed ground-truth ledger. SecurePR intentionally does **not** append every normal PR to it.

For example, if SecurePR returns `BLOCK`, that does not prove that `BLOCK` was the correct expected outcome. A human reviewer must establish the expected result independently.

After a labeled benchmark PR has been executed and verified, record that case in the CSV through a reviewed repository change. The row should contain the expected and actual results and enough notes to identify the evidence.

This prevents SecurePR from defining its own ground truth and then using that same result to claim accuracy.

## Understanding the accuracy report

The cumulative benchmark uses:

- **TP:** expected `BLOCK`, actual `BLOCK`.
- **FP:** expected `PASS`, actual `BLOCK`.
- **TN:** expected `PASS`, actual `PASS`.
- **FN:** expected `BLOCK`, actual `PASS`.

From those values:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 × Precision × Recall / (Precision + Recall)
```

A percentage is meaningful only for the labeled benchmark corpus. It is not a universal claim about SecurePR's real-world vulnerability-detection accuracy.

## Testing a BLOCK and PASS on one PR

Use a controlled synthetic case only.

1. Create a branch.
2. Introduce a known high-confidence security issue.
3. Open one PR.
4. Add `securepr-expected-block` after the ground truth is independently established.
5. Verify `🔴 SecurePR: BLOCK` and the expected-versus-actual accuracy result.
6. Fix the issue on the **same branch and same PR**.
7. Push the fix and let SecurePR rerun.
8. If the corrected state is independently expected to pass, use `securepr-expected-pass` for the current benchmark run.
9. Verify `🟢 SecurePR: PASS`.

Never use real passwords, API keys, tokens, private keys, or cloud credentials in a benchmark.

## PASS and BLOCK

The harness has only two gate outcomes:

- `🟢 SecurePR: PASS` — applicable blocking controls completed successfully and no blocking security finding remains.
- `🔴 SecurePR: BLOCK` — a blocking control failed or a blocking security finding remains.

Human review is always recommended for both outcomes. SecurePR never automatically remediates source code, rotates credentials, dismisses findings, or merges a pull request.

## Linux and Windows compatibility

The developer-side setup is supported on Linux and Windows through the Python helper scripts. The actual GitHub Actions security gate executes on Linux, so the target repository's developer workstation does not need to match the runner operating system.

Repository code itself still determines whether its own project tests, package managers, build tools, and dependency ecosystems are available to the gate.

## Current MVP limitation

The MVP is currently intended for the user's own repositories and authorized repository work. It does not provide a hosted account-management layer, automatic authorization into arbitrary organizations, or a service for scanning repositories to which the user has no access.

Expanding beyond this scope would require additional access, trust, configuration, and multi-repository management design.

## Recommended verification order

1. Run local setup and tests.
2. Add the caller workflow to an owned repository.
3. Open a normal PR and verify the gate.
4. Review the full Actions summary and evidence artifacts.
5. Test a controlled BLOCK case.
6. Fix it on the same PR and verify PASS.
7. Test one or more labeled real-PR benchmark cases.
8. Record verified benchmark cases in the CSV through reviewed changes.
9. Merge after the PR gate passes and human review is complete.
10. Verify the post-merge `main` run.
