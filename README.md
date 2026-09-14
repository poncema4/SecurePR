# SecurePR

Reusable pull-request security gate for Secure Software Development and DevSecOps.

## Overview

SecurePR is a GitHub Actions security gate that combines repository tests, secret detection, SAST, dependency auditing, and security-result evaluation into one `PASS` or `BLOCK` decision.

SecurePR is the orchestration and policy layer. CodeQL, Semgrep, Gitleaks, dependency auditors, and project tests provide the underlying security evidence.

## Table of Contents

- [Problem](#problem)
- [Objectives](#objectives)
- [MVP Scope](#mvp-scope)
- [Architecture](#architecture)
- [Features](#features)
- [Setup](#setup)
- [Use SecurePR](#use-securepr)
- [Continuous Integration](#continuous-integration)
- [OWASP Top 10:2025](#owasp-top-102025)
- [Accuracy](#accuracy)
- [Documentation](#documentation)
- [Limitations](#limitations)
- [Legal and Ethical Note](#legal-and-ethical-note)

## Problem

Pull requests can introduce vulnerabilities through source code, dependencies, credentials, configuration, authentication, authorization, and CI/CD changes. Individual scanners provide different evidence, so developers still need a consistent way to decide whether a change should proceed.

SecurePR provides one reusable security gate and one consistent reporting model.

## Objectives

1. Run repeatable security controls on every applicable pull request.
2. Reuse the same gate across repositories without copying the implementation.
3. Detect applicable languages, dependency manifests, and project tests.
4. Combine complementary security engines into one decision.
5. Report clear `PASS` or `BLOCK` results with remediation guidance.
6. Map automated evidence to OWASP Top 10:2025 without claiming complete category coverage.
7. Measure gate behavior with labeled benchmark cases and TP/FP/TN/FN metrics.
8. Keep remediation and merging under developer/reviewer control.

## MVP Scope

### Included

- One authoritative `SecurePR Security Gate` job.
- Reusable GitHub Actions workflow.
- Repository and language profiling.
- Python and JavaScript/TypeScript project-test support when applicable.
- CodeQL security-extended analysis for supported languages.
- Semgrep SAST and SecurePR-specific high-confidence rules.
- Gitleaks secret detection.
- Python and npm dependency auditing when applicable.
- SARIF finding evaluation and evidence artifacts.
- OWASP Top 10:2025 coverage mapping.
- PASS/BLOCK reporting and empirical accuracy reporting.

### Not included

- Automatic source-code remediation.
- Automatic credential rotation.
- Automatic pull-request merging.
- Proof that a PASS means vulnerability-free software.
- Complete automated verification of every OWASP category.

## Architecture

```text
Pull Request
     |
     v
Repository Profile
     |
     +--> Project Tests
     +--> Gitleaks
     +--> Semgrep
     +--> CodeQL
     +--> Dependency Audit
     |
     v
SARIF / CI Evidence
     |
     v
SecurePR Policy + Aggregation
     |
     v
PASS / BLOCK
     |
     v
Human Review
```

## Features

| Control | Purpose |
|---|---|
| Repository profiling | Detect applicable languages, manifests, and unsupported CodeQL extensions |
| CodeQL | Semantic security analysis for supported languages |
| Semgrep | Rule-based SAST and SecurePR-specific checks |
| Gitleaks | Secret and credential detection |
| Dependency audits | Known vulnerability checks for supported ecosystems |
| Project tests | Repository-specific correctness and security behavior |
| SARIF evaluation | Consolidated machine-readable security evidence |
| Accuracy reporting | Cumulative benchmark metrics plus current labeled-PR accuracy |

## Setup

Local setup works on Linux and Windows. The full gate runs in GitHub Actions on a Linux runner.

See [`docs/setup.md`](docs/setup.md) for setup commands, verification, reusable-workflow configuration, and benchmark instructions.

Quick local verification:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

## Use SecurePR

Add this workflow to a repository you own or are authorized to assess:

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

For stronger reproducibility, pin the reusable workflow to a reviewed SecurePR commit SHA.

The target repository remains the code being analyzed. SecurePR detects which controls apply and reports the resulting gate decision.

## Continuous Integration

The authoritative job is named `SecurePR Security Gate` and produces only:

- `PASS` — applicable blocking controls passed and no blocking security finding remains.
- `BLOCK` — a blocking control failed or a blocking security finding remains.

The Actions summary reports Check Results, OWASP Top 10:2025 coverage, fixes, remediation, accuracy, human-review guidance, and the full run link.

Fixes are pushed to the same PR branch and the same gate is rerun. SecurePR does not auto-remediate or merge.

## OWASP Top 10:2025

OWASP Top 10:2025 is a coverage framework, not ten separate scanners. A green row means the mapped automated controls passed; it does not prove the entire category is secure.

| Category | Main evidence |
|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, project tests |
| A02 Security Misconfiguration | CodeQL, Semgrep |
| A03 Software Supply Chain Failures | Dependency audits, CodeQL, Semgrep |
| A04 Cryptographic Failures | CodeQL, Semgrep |
| A05 Injection | CodeQL, Semgrep, project tests |
| A06 Insecure Design | Automated indicators, tests, human review |
| A07 Authentication Failures | CodeQL, Semgrep, project tests |
| A08 Software or Data Integrity Failures | CodeQL, Semgrep, dependency audits |
| A09 Security Logging & Alerting Failures | CodeQL, Semgrep, human review |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, project tests |

## Accuracy

SecurePR reports accuracy from labeled cases only.

Every PR shows the current cumulative benchmark. A normal PR is **not** automatically treated as a TP, FP, TN, or FN because its expected security outcome is unknown.

A real PR can be evaluated immediately as a benchmark case when a trusted reviewer adds exactly one label:

- `securepr-expected-pass`
- `securepr-expected-block`

The Actions summary then shows the current PR's expected result, actual result, and whether the classification was correct, alongside cumulative TP, FP, TN, precision, recall, and F1.

The committed CSV is a reviewed benchmark ledger. It is intentionally **not** modified by every ordinary PR. After a labeled benchmark case is verified, its expected and actual result can be added to `docs/accuracy/benchmark-results.csv` through a normal reviewed change.

This prevents SecurePR from inventing ground truth or silently changing its reported accuracy.

## Documentation

- [`docs/setup.md`](docs/setup.md) — Linux/Windows setup, reuse, and real-PR accuracy workflow
- [`docs/architecture.md`](docs/architecture.md) — architecture and component boundaries
- [`docs/security-requirements.md`](docs/security-requirements.md) — security requirements and gate policy
- [`docs/security-checks.md`](docs/security-checks.md) — security controls and OWASP mapping
- [`docs/threat-model.md`](docs/threat-model.md) — assets, trust boundaries, threats, and treatments
- [`docs/testing.md`](docs/testing.md) — local, CI, PASS/BLOCK, reuse, and benchmark testing
- [`docs/github-actions.md`](docs/github-actions.md) — GitHub Actions and reusable workflow behavior
- [`docs/accuracy/methodology.md`](docs/accuracy/methodology.md) — accuracy methodology
- [`docs/accuracy/benchmark-results.csv`](docs/accuracy/benchmark-results.csv) — labeled benchmark evidence

## Limitations

- Static analysis can miss vulnerabilities and produce false positives.
- CodeQL coverage is limited to supported languages.
- Dependency auditing depends on supported ecosystems and manifests.
- Tests cover only the behavior they exercise.
- A06 Insecure Design and other context-dependent risks require human review.
- Accuracy metrics describe the labeled benchmark corpus, not universal real-world detection accuracy.

Human security review is always recommended.

## Legal and Ethical Note

Use SecurePR only on repositories and systems you own or are authorized to assess. Use synthetic security fixtures; never commit real credentials for testing. Do not use SecurePR to bypass access controls or test production systems without authorization.
