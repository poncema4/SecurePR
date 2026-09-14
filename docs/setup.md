# SecurePR Setup

SecurePR has two parts:

- **Local tooling:** optional Python setup for running tests and checking the reporting scripts.
- **GitHub Actions:** the actual security gate, which runs CodeQL, Semgrep, Gitleaks, dependency audits, and repository tests on a Linux runner.

The local setup works on Linux and Windows. The reusable GitHub Actions gate does not require SecurePR to be installed on the target machine.

## Requirements

- Python 3.11 or newer
- Git
- A GitHub repository you own or are authorized to assess

For the full security gate, the target repository must use GitHub Actions.

## Linux

From the SecurePR repository root:

```bash
chmod +x scripts/setup.sh scripts/verify.sh
./scripts/setup.sh
./scripts/verify.sh
```

Or set a specific Python executable:

```bash
PYTHON_BIN=python3.12 ./scripts/setup.sh
```

Activate the environment when working interactively:

```bash
source .venv/bin/activate
```

Run the local checks directly:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

## Windows PowerShell

From the SecurePR repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
.\scripts\verify.ps1
```

Activate the environment when working interactively:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the local checks directly:

```powershell
python -m pytest -q
python -m compileall -q app security tests scripts
python .\scripts\accuracy_report.py
```

If `python` is not available, install Python 3.11+ and make sure it is on `PATH`.

## Use SecurePR in another repository

Add a workflow such as `.github/workflows/securepr.yml` to the target repository:

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

For reproducibility, replace `@main` with a reviewed SecurePR commit SHA.

The called workflow checks out the target repository, detects its applicable languages and manifests, and runs the controls that apply to that repository.

## Real-PR accuracy measurement

A normal PR does not have known ground truth, so it is not automatically counted as TP, FP, TN, or FN.

To use a real PR as a labeled benchmark case, a trusted reviewer can add exactly one of these labels:

- `securepr-expected-pass`
- `securepr-expected-block`

The Actions summary then reports:

- expected result for the current PR
- actual SecurePR result for the current PR
- whether that case was classified correctly
- cumulative TP, FP, TN, precision, recall, and F1 from the committed benchmark CSV

The workflow does **not** automatically edit `docs/accuracy/benchmark-results.csv`. The expected result is ground truth and must be deliberately reviewed before a case becomes part of the permanent benchmark history.

After a benchmark PR is verified, record its expected and actual result in the CSV in a normal reviewed change. This keeps the ledger auditable and prevents an arbitrary PR from silently changing the project's reported accuracy.

## What "realtime accuracy" means

Every PR gets a current accuracy status in the Actions summary. A labeled benchmark PR gets an immediate expected-versus-actual classification for that run; an unlabeled PR shows the cumulative benchmark without pretending that the PR itself is a labeled case.

This is more accurate than assigning an arbitrary expected result to every PR. Accuracy percentages describe only the labeled benchmark corpus, not all repository changes.

## Recommended verification order

1. Run the local setup and tests.
2. Add the reusable workflow to the target repository.
3. Open a normal PR and verify `SecurePR Security Gate` runs.
4. For a controlled benchmark, have a trusted reviewer add the expected-outcome label.
5. Inspect the PR Actions summary for expected vs. actual and cumulative accuracy.
6. If the gate blocks, fix the same PR branch and rerun it.
7. After merge, verify the push-to-main run independently.
