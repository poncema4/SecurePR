# SecurePR

Reusable Pull Request Security Gate for Secure Software Development and DevSecOps.

SecurePR is a GitHub Actions security gate for repositories you own or are authorized to assess. It coordinates repository tests, secret detection, static analysis, dependency auditing, and security-finding evaluation and produces one pull-request decision: `PASS` or `BLOCK`.

SecurePR is the harness, orchestration, policy, aggregation, and reporting layer. CodeQL, Semgrep, Gitleaks, dependency auditors, and project tests provide the underlying security evidence.

---

## Overview

SecurePR is designed to make security checks a consistent part of the pull-request workflow without requiring each repository to implement and maintain the same security pipeline independently.

The MVP is built around one GitHub Actions job named `SecurePR Security Gate`. The job detects which controls are applicable to the target repository, runs those controls, evaluates their results, and publishes a consolidated security summary.

The intended model is:

```text
Developer
   |
   v
Pull Request
   |
   v
SecurePR Security Gate
   |
   +-- Repository profile
   +-- Project tests / type checks
   +-- Gitleaks
   +-- Semgrep
   +-- CodeQL
   +-- Dependency audits
   +-- SARIF evaluation
   +-- OWASP Top 10:2025 mapping
   |
   v
PASS or BLOCK
   |
   v
Human security review
```

SecurePR does not claim that a passing repository is vulnerability-free. The gate reports whether the applicable automated controls passed.

---

## Table of Contents

- [Overview](#overview)
- [Problem](#problem)
- [Objectives](#objectives)
- [MVP Scope](#mvp-scope)
- [Architecture](#architecture)
- [Security Controls](#security-controls)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Setup and Installation](#setup-and-installation)
- [How to Use SecurePR](#how-to-use-securepr)
- [Continuous Integration](#continuous-integration)
- [OWASP Top 10:2025 Coverage](#owasp-top-102025-coverage)
- [Accuracy Benchmark](#accuracy-benchmark)
- [Documentation](#documentation)
- [Security Scope and Limitations](#security-scope-and-limitations)
- [Legal and Ethical Note](#legal-and-ethical-note)
- [Final MVP Status](#final-mvp-status)

---

## Problem

Pull requests can introduce security weaknesses through application code, dependencies, credentials, configuration, authentication and authorization logic, CI/CD changes, or error handling.

A single security tool cannot reliably cover every relevant risk. Different engines provide different types of evidence, while repository tests can identify application-specific behavior that general-purpose scanners cannot understand.

Without a common security gate, developers may have to interpret several independent checks and decide manually whether a pull request should proceed.

SecurePR addresses this problem by coordinating complementary security controls behind one reusable pull-request gate and one consistent decision model.

---

## Objectives

The SecurePR MVP has the following objectives:

1. Provide one repeatable security gate for pull requests.
2. Reuse the same security workflow across repositories owned or controlled by the developer.
3. Detect applicable languages, dependency manifests, and project tests before running repository-specific controls.
4. Combine multiple security-analysis engines without presenting their results as separate competing gates.
5. Produce a clear `PASS` or `BLOCK` decision.
6. Map applicable controls to OWASP Top 10:2025 categories without claiming complete automated coverage.
7. Preserve machine-readable security evidence through GitHub Actions artifacts.
8. Measure gate behavior empirically using labeled benchmark cases and TP/FP/TN/FN metrics.
9. Keep remediation under developer and reviewer control rather than automatically changing source code or merging pull requests.

---

## MVP Scope

### Included

- Reusable GitHub Actions workflow for other repositories.
- One authoritative `SecurePR Security Gate` job.
- Repository and language profiling.
- Python and JavaScript/TypeScript project-test support when applicable.
- CodeQL security-extended analysis for supported languages.
- Semgrep security analysis and SecurePR-specific rules.
- Gitleaks secret detection.
- Python and npm dependency auditing when supported manifests are present.
- SARIF-based security-finding evaluation.
- OWASP Top 10:2025 coverage mapping.
- Consolidated PASS/BLOCK reporting.
- Accuracy benchmark tooling and labeled benchmark ledger.
- GitHub Actions evidence artifacts.
- Human-review guidance and explicit security limitations.

### Not included

- Automatic source-code remediation.
- Automatic credential rotation.
- Automatic pull-request merging.
- Complete automated verification of every OWASP Top 10:2025 category.
- CodeQL analysis of languages that CodeQL does not support.
- A claim of universal vulnerability-detection accuracy.

---

## Architecture

SecurePR separates the gate from the security-analysis engines that provide evidence.

```text
Target Repository
       |
       v
Repository Profile
       |
       +------------------------------+
       |                              |
       v                              v
Project Validation              Security Analysis
       |                              |
       |                    +---------+---------+
       |                    |         |         |
       v                    v         v         v
 Python / Node           Gitleaks  Semgrep   CodeQL
       |                    |         |         |
       +--------------------+---------+---------+
                            |
                            v
                    Dependency Audits
                            |
                            v
                     SARIF Evaluation
                            |
                            v
                  OWASP Coverage Mapping
                            |
                            v
                      PASS / BLOCK
```

### Component responsibilities

| Component | Responsibility |
|---|---|
| SecurePR | Applicability, orchestration, policy, aggregation, reporting, and gate decision |
| Repository profiler | Detects applicable languages, manifests, and unsupported extensions |
| CodeQL | Semantic security analysis for supported languages |
| Semgrep | Rule-based source analysis and SecurePR-specific rules |
| Gitleaks | Secret and credential detection |
| `pip-audit` | Python dependency vulnerability auditing |
| `npm audit` | npm dependency vulnerability auditing when a lockfile is available |
| Project tests | Repository-specific correctness and security behavior |
| SARIF | Machine-readable security-result evidence |

---

## Security Controls

SecurePR currently combines the following controls:

1. **Repository profiling** — identifies applicable languages and dependency manifests and reports unsupported CodeQL extensions rather than silently treating them as analyzed.
2. **Project validation** — runs applicable Python tests, Python compilation, JavaScript/TypeScript tests, and type checks.
3. **Secret detection** — uses Gitleaks to identify credentials, tokens, passwords, and other secret material.
4. **Semgrep SAST** — runs security rules plus SecurePR-specific high-confidence checks for hardcoded credentials, privileged usernames, unsafe dynamic evaluation, and disabled Python TLS verification.
5. **CodeQL SAST** — runs security-extended queries for detected CodeQL-supported languages.
6. **Dependency auditing** — runs `pip-audit` for Python requirements and `npm audit` when an npm lockfile is available.
7. **SARIF evaluation** — consolidates machine-readable security findings for the final gate decision.
8. **Accuracy reporting** — calculates empirical TP, FP, TN, FN, precision, recall, and F1 from labeled benchmark cases.

SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges pull requests.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Workflow | GitHub Actions | Pull-request security gate and reusable workflow |
| Semantic SAST | CodeQL | Language-aware security analysis |
| Rule-based SAST | Semgrep | Pattern-based security analysis and custom rules |
| Secret scanning | Gitleaks | Credential and secret detection |
| Python dependency audit | `pip-audit` | Known vulnerability detection in Python dependencies |
| npm dependency audit | `npm audit` | Known vulnerability detection in npm dependencies |
| Evidence | SARIF | Standard machine-readable security findings |
| Tooling | Python | SecurePR support scripts and metric calculations |
| Testing | pytest and repository tests | Validation of SecurePR and target repositories |
| Version control | Git and GitHub | Source control, pull requests, and CI verification |

---

## Repository Structure

```text
SecurePR/
├── app/                         # Sample application used by project tests
├── security/                    # Security/runtime policy helpers
├── tests/                       # SecurePR and sample-application tests
├── scripts/                     # Reusable gate support scripts
│   ├── repository_profile.py
│   ├── summarize_sarif.py
│   ├── accuracy_metrics.py
│   ├── accuracy_report.py
│   ├── check_python_version.py
│   └── verification/support scripts
├── docs/
│   ├── architecture.md
│   ├── security-requirements.md
│   ├── security-checks.md
│   ├── threat-model.md
│   ├── testing.md
│   ├── github-actions.md
│   └── accuracy/
│       └── benchmark-results.csv
├── .github/workflows/
│   ├── security.yml             # SecurePR's own gate
│   └── reusable-security.yml    # Reusable gate for other repositories
├── .semgrep_securepr.yml        # SecurePR-specific Semgrep rules
├── .python-version              # Repository Python runtime declaration
├── requirements.txt
└── README.md
```

`.python-version` and `.semgrep_securepr.yml` intentionally remain at the repository root because they are repository-level configuration files.

---

## Setup and Installation

### Clone the repository

```bash
git clone https://github.com/poncema4/SecurePR.git
cd SecurePR
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the local tests

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
```

The GitHub Actions workflow is the authoritative verification of the exact revision used by the pull-request gate.

---

## How to Use SecurePR

### Test SecurePR itself

SecurePR's own workflow runs for pushes to `main` and pull requests targeting `main`.

For a controlled blocking-path test:

1. Create a test branch.
2. Add a synthetic security issue that is safe to use as a fixture.
3. Open one pull request to `main`.
4. Confirm `SecurePR Security Gate` reports `BLOCK`.
5. Fix the issue on the same branch.
6. Push the fix to the same pull request.
7. Confirm the gate reports `PASS`.

Do not use real credentials as test fixtures.

### Use SecurePR with another repository

SecurePR is designed to be reused without copying its implementation into every repository.

Create `.github/workflows/securepr.yml` in the target repository:

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

For stronger supply-chain control, replace `@main` with a reviewed SecurePR commit SHA.

The target repository remains the code being analyzed. SecurePR checks out the target repository, detects its applicable languages and manifests, and runs the relevant controls.

The intended reuse model is:

```text
CookieGuard  ----\
NetDefender  -----+----> SecurePR reusable workflow
Other repos  ----/
```

SecurePR should be added to a repository only after reviewing the controls that apply to that repository.

---

## Continuous Integration

The authoritative job is named:

```text
SecurePR Security Gate
```

It is intentionally one job with multiple steps so the repository can require one stable security check.

The pull-request summary follows this order:

1. `SecurePR: PASS` or `SecurePR: BLOCK`
2. Check Results
3. Result explanation
4. OWASP Top 10:2025 Coverage
5. Fixes to make this PASS
6. Remediation
7. Accuracy
8. Human review
9. Full Actions run link

A `PASS` means the applicable required controls completed without a blocking result. A `BLOCK` means one or more required controls failed or produced a blocking security finding.

Fixes are made on the same pull request branch and the gate is rerun. SecurePR does not automatically remediate or merge changes.

---

## OWASP Top 10:2025 Coverage

SecurePR uses OWASP Top 10:2025 as a coverage framework. It is not ten separate scanners, and a green category does not prove that the entire category is secure.

| OWASP category | Applicable controls |
|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, applicable project tests |
| A02 Security Misconfiguration | CodeQL, Semgrep, applicable project tests |
| A03 Software Supply Chain Failures | Dependency audits, CodeQL, Semgrep |
| A04 Cryptographic Failures | CodeQL, Semgrep, applicable project tests |
| A05 Injection | CodeQL, Semgrep, applicable project tests |
| A06 Insecure Design | Automated indicators, project tests, human architecture and threat-model review |
| A07 Authentication Failures | CodeQL, Semgrep, applicable project tests |
| A08 Software or Data Integrity Failures | CodeQL, Semgrep, dependency audits, applicable tests |
| A09 Security Logging & Alerting Failures | CodeQL, Semgrep, human operational review |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, applicable project tests |

CodeQL is applied only to supported languages. Unsupported extensions are reported rather than silently treated as covered.

---

## Accuracy Benchmark

SecurePR measures gate behavior with a labeled benchmark rather than claiming accuracy from ordinary pull requests.

The benchmark ledger is:

```text
docs/accuracy/benchmark-results.csv
```

The file records cases in this format:

```csv
case_id,category,description,expected,actual,notes
```

The metrics are:

```text
TP = expected BLOCK and actual BLOCK
FP = expected PASS and actual BLOCK
TN = expected PASS and actual PASS
FN = expected BLOCK and actual PASS

Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 × Precision × Recall / (Precision + Recall)
```

The current ledger contains four controlled cases: two expected BLOCK cases and two expected PASS cases. All four were classified correctly by the corresponding GitHub Actions runs.

The benchmark file is a labeled evidence ledger, not an automatically generated log. A normal pull request cannot safely append itself to this file because SecurePR does not know the expected ground-truth result for an arbitrary change. Benchmark cases are added only after a test case has a known expected outcome and the observed Actions result has been verified.

This means the CSV should not change on every ordinary pull request. It changes when a new labeled benchmark case is deliberately executed and recorded.

---

## Documentation

| File | Purpose |
|---|---|
| `README.md` | Project overview, objectives, MVP scope, architecture, setup, usage, and final status |
| `docs/architecture.md` | SecurePR architecture and component boundaries |
| `docs/security-requirements.md` | Security requirements and gate expectations |
| `docs/security-checks.md` | Security controls and OWASP coverage mapping |
| `docs/threat-model.md` | Threats and trust boundaries |
| `docs/testing.md` | Local, CI, blocking-path, and benchmark testing procedures |
| `docs/github-actions.md` | GitHub Actions and reusable workflow behavior |
| `docs/accuracy/benchmark-results.csv` | Labeled benchmark evidence |

Final documentation is organized by topic rather than by development phase. There is intentionally no `docs/phase-4-plan.md` in the final MVP.

---

## Security Scope and Limitations

SecurePR is an automated security gate, not proof that software is secure.

Important limitations include:

- Static-analysis tools can miss vulnerabilities and produce false positives.
- OWASP categories are broad and cannot all be comprehensively automated.
- A06 Insecure Design requires human architecture, threat-model, requirements, and business-logic review.
- CodeQL coverage is limited to supported languages.
- Dependency auditing applies only to supported ecosystems and manifests.
- Project tests establish only the behavior they exercise.
- A `PASS` means the mapped applicable controls passed; it does not mean every vulnerability has been eliminated.
- Accuracy metrics describe the labeled benchmark dataset and should not be presented as universal real-world detection accuracy.

Human security review is always recommended.

---

## Legal and Ethical Note

SecurePR is intended for repositories and systems you own or are authorized to assess.

Do not place real secrets or credentials into benchmark fixtures. Do not use SecurePR to bypass access controls or test systems without authorization.

Security findings should be interpreted within the application's architecture, threat model, deployment environment, and organizational security process.

---

## Final MVP Status

SecurePR's final MVP provides a reusable pull-request security gate with repository profiling, project validation, CodeQL, Semgrep, Gitleaks, dependency auditing, SARIF evidence, OWASP Top 10:2025 coverage mapping, and empirical benchmark reporting.

The current labeled benchmark contains four controlled cases with two expected BLOCK results and two expected PASS results. All four matched their expected outcomes.

The MVP is ready to be reused in other repositories through the reusable workflow. Future work can expand the benchmark dataset, add ecosystem-specific controls, and broaden language/framework coverage without changing the core PASS/BLOCK gate model.
