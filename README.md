# 🛡️ SecurePR — Reusable Pull Request Security Gate

SecurePR is a reusable DevSecOps security gate for repositories you control. It runs applicable project tests, secret detection, static analysis, dependency audits, and security-finding evaluation in one GitHub Actions job and produces one decision: `PASS` or `BLOCK`.

SecurePR is the **harness, orchestration, policy, aggregation, and reporting layer**. CodeQL, Semgrep, Gitleaks, dependency auditors, and repository tests provide the underlying security evidence.

---

## 📖 Table of Contents

- The Problem
- What SecurePR Does
- Features
- Architecture
- Tech Stack & Why
- Folder Structure
- Setup & Installation
- How to Run
- Continuous Integration
- OWASP Top 10:2025 Coverage
- Accuracy Benchmark
- Documentation Files
- Security Scope & Limitations
- Legal & Ethical Note
- Final MVP Status

---

## 🔍 The Problem

Pull requests can introduce security weaknesses through source code, dependencies, secrets, configuration, CI/CD changes, authentication and authorization logic, or unsafe error handling.

The problem is that no single security engine can reliably detect every class of vulnerability. A repository may pass one scanner while another scanner or the project's own tests identify a different risk.

SecurePR addresses this by putting complementary security controls behind one reusable pull-request gate:

```text
Pull Request
     │
     ▼
┌─────────────────────────────────────────┐
│          SecurePR Security Gate         │
│                                         │
│  Repository profile                     │
│  Project tests / type checks            │
│  Gitleaks secret detection              │
│  Semgrep rule-based SAST                │
│  CodeQL semantic SAST                   │
│  Dependency audits                      │
│  SARIF security-finding evaluation      │
└───────────────────┬─────────────────────┘
                    │
                    ▼
             PASS or BLOCK
                    │
                    ▼
          Human review recommended
```

SecurePR is therefore a **security gate**, not a claim that passing software is completely secure.

---

## 🛡️ What SecurePR Does

SecurePR profiles the target repository first so that checks can be applied according to the repository's actual languages, manifests, and available tests.

The workflow then runs applicable controls:

1. **Repository profiling** — detects CodeQL-supported languages, common dependency manifests, and unsupported CodeQL extensions that need to remain visible.
2. **Project tests** — runs applicable Python and JavaScript/TypeScript tests and type checks.
3. **Secret detection** — Gitleaks scans repository content for credentials and secret material.
4. **Rule-based SAST** — Semgrep runs security rules plus SecurePR-specific high-confidence rules.
5. **Semantic SAST** — CodeQL analyzes detected CodeQL-supported languages with security-extended queries.
6. **Dependency auditing** — `pip-audit` and `npm audit` run when their supported manifests are present.
7. **SARIF evaluation** — machine-readable findings from applicable security engines are evaluated for blocking findings.
8. **OWASP mapping** — the actual controls are mapped to OWASP Top 10:2025 categories for coverage reporting.
9. **Gate decision** — all required applicable controls are consolidated into one `PASS` or `BLOCK` result.

SecurePR does not automatically modify source code, rotate credentials, dismiss findings, or merge pull requests.

---

## ✨ Features

### MVP

1. **Reusable GitHub Actions workflow** — use SecurePR from other repositories you control without copying the security logic into every repository.
2. **Multi-language profiling** — dynamically identifies CodeQL-supported languages and common dependency manifests.
3. **Semantic SAST** — CodeQL security-extended analysis for supported languages.
4. **Rule-based SAST** — Semgrep security rules plus SecurePR-specific high-confidence rules for credentials, privileged usernames, unsafe dynamic evaluation, and disabled Python TLS verification.
5. **Secret detection** — Gitleaks-based credential and secret scanning.
6. **Dependency auditing** — applicable Python and npm dependency audits.
7. **Project validation** — applicable repository tests and type checks.
8. **SARIF evidence** — machine-readable security findings are retained in GitHub Actions evidence artifacts.
9. **PASS/BLOCK reporting** — one authoritative `SecurePR Security Gate` job and exactly two gate outcomes.
10. **OWASP Top 10:2025 coverage** — the ten categories are used as a coverage framework mapped to the controls that actually run.
11. **Accuracy benchmark** — controlled TP/FP/TN/FN measurement without inventing an accuracy percentage before labeled benchmark data exists.
12. **Human-review guidance** — every result states that human security review is recommended.

### Planned (post-MVP)

- Additional ecosystem-specific dependency auditors.
- More language and framework-specific SecurePR rules.
- Broader CI/CD and infrastructure-as-code security checks.
- Larger controlled benchmark datasets.
- Additional reusable-workflow demonstrations across CookieGuard and NetDefender.

---

## 🏗️ Architecture

```text
Developer
   │
   ▼
Pull Request
   │
   ▼
SecurePR Security Gate
   │
   ├── Repository / language profile
   ├── Project tests / type checks
   ├── Gitleaks
   ├── Semgrep
   ├── CodeQL
   ├── Dependency audits
   ├── SARIF finding evaluation
   └── OWASP Top 10:2025 mapping
   │
   ▼
SecurePR: PASS / BLOCK
   │
   ▼
Human security review recommended
```

### Security engine responsibilities

| Component | Responsibility |
|---|---|
| SecurePR | Orchestration, applicability, policy, aggregation, reporting, and gate decision |
| CodeQL | Semantic source-code security analysis for supported languages |
| Semgrep | Rule-based source-code analysis and SecurePR custom rules |
| Gitleaks | Secret and credential detection |
| `pip-audit` | Python dependency vulnerability auditing |
| `npm audit` | npm dependency vulnerability auditing when a lockfile is present |
| Project tests | Application-specific correctness and security behavior |
| SARIF | Standard machine-readable security-result evidence |

SecurePR does **not** replace these engines. It coordinates them and turns their applicable results into one consistent pull-request security decision.

---

## 🛠️ Tech Stack & Why

| Layer | Choice | Why |
|---|---|---|
| Harness | Python | Simple cross-repository tooling and testable security-policy logic |
| Semantic SAST | CodeQL | Language-aware data-flow and security analysis |
| Rule-based SAST | Semgrep | Fast pattern/rule analysis and custom repository security rules |
| Secret detection | Gitleaks | Dedicated secret-scanning engine |
| Python dependency audit | `pip-audit` | Audits Python packages against known vulnerability data |
| npm dependency audit | `npm audit` | Native npm dependency vulnerability auditing |
| CI/CD | GitHub Actions | Native pull-request checks, summaries, artifacts, and reusable workflows |
| Security evidence | SARIF | Standard format for machine-readable security findings |
| Testing | pytest + repository-specific checks | Verifies SecurePR behavior and target-repository behavior |
| Version control | Git / GitHub | Branch, PR, ruleset, and verification workflow |

SecurePR deliberately uses multiple specialized engines rather than attempting to implement a complete static-analysis or secret-scanning engine itself.

---

## 📁 Folder Structure

```text
SecurePR/
├── app/                         # Sample application used by the project tests
├── security/                    # Security/runtime policy helpers
├── tests/                       # SecurePR and sample-application tests
├── scripts/                     # Reusable gate support scripts
│   ├── repository_profile.py
│   ├── summarize_sarif.py
│   ├── accuracy_metrics.py
│   ├── accuracy_report.py
│   ├── check_python_version.py
│   └── setup/verification scripts
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
│   ├── security.yml             # SecurePR's own security gate
│   └── reusable-security.yml    # Reusable workflow for other repositories
├── .semgrep_securepr.yml        # SecurePR-specific Semgrep rules
├── .python-version              # Repository Python runtime declaration
├── requirements.txt
└── README.md
```

`.python-version` belongs at the repository root because it is a standard Python runtime-version declaration. `.semgrep_securepr.yml` belongs at the repository root because it is the repository-level Semgrep configuration consumed by the workflows. Neither file should be moved into `scripts/` or `docs/`.

---

## ▶️ Setup & Installation

### Clone the repository

```bash
git clone https://github.com/poncema4/SecurePR.git
cd SecurePR
```

### Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### Verify the local test suite

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
```

The GitHub Actions workflow remains the authoritative test of the exact repository revision used by the security gate.

---

## ▶️ How to Run

### Test SecurePR itself

SecurePR's own `.github/workflows/security.yml` runs when changes are pushed to `main` or submitted through a pull request targeting `main`.

For a controlled blocking-path demonstration:

1. Create a branch.
2. Add a synthetic security fixture that is safe to use for testing.
3. Open a pull request into `main`.
4. Confirm `SecurePR Security Gate` reports `BLOCK`.
5. Fix the same branch.
6. Push the fix to the same pull request.
7. Confirm the same gate changes to `PASS`.

Do not use real credentials as test fixtures.

### Reuse SecurePR in another repository

A repository you control can call the reusable workflow without copying the SecurePR implementation.

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

For stronger supply-chain control, a target repository can pin the reusable workflow to a reviewed SecurePR commit SHA instead of `main`.

The target repository remains the code being analyzed. SecurePR checks out that repository, detects its applicable languages/manifests, and runs the relevant security controls.

### Example reuse targets

The intended model is:

```text
CookieGuard ───────┐
NetDefender ───────┼──► SecurePR reusable workflow
Other repo ────────┘
```

Each repository receives checks appropriate to its own codebase. A repository is not treated as secure merely because a particular engine is not applicable to it.

---

## 🔄 Continuous Integration

SecurePR's authoritative GitHub Actions job is named:

```text
SecurePR Security Gate
```

The workflow is intentionally one job with multiple steps so repository branch protection can require one stable security check.

The summary is organized consistently for both outcomes:

1. `SecurePR: PASS` or `SecurePR: BLOCK`
2. **Check Results**
3. Result explanation
4. **OWASP Top 10:2025 Coverage**
5. **Fixes to make this PASS**
6. **Remediation**
7. **Accuracy**
8. **Human review**
9. Full Actions run link

### PASS

All required applicable controls completed successfully and no applicable security-finding evaluation produced a blocking result.

Human security review is still recommended before merge.

### BLOCK

One or more required applicable controls did not pass. The developer fixes the blocking result on the same PR/branch and reruns the gate.

Human security review is always recommended.

SecurePR never automatically modifies source code, rotates credentials, dismisses findings, or merges a pull request.

---

## 🔐 OWASP Top 10:2025 Coverage

SecurePR uses OWASP Top 10:2025 as a **coverage framework**, not as ten separate scanners and not as proof that every category is completely automated.

The OWASP category is evaluated through the actual controls that provide relevant evidence:

| OWASP 2025 category | Controls used by SecurePR |
|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, applicable project tests |
| A02 Security Misconfiguration | CodeQL, Semgrep, applicable project tests |
| A03 Software Supply Chain Failures | Dependency audits, CodeQL, Semgrep |
| A04 Cryptographic Failures | CodeQL, Semgrep, applicable project tests |
| A05 Injection | CodeQL, Semgrep, applicable project tests |
| A06 Insecure Design | Automated indicators, project tests, human architecture/threat-model review |
| A07 Authentication Failures | CodeQL, Semgrep, applicable project tests |
| A08 Software or Data Integrity Failures | CodeQL, Semgrep, dependency auditing, applicable tests |
| A09 Security Logging & Alerting Failures | CodeQL, Semgrep, operational/human review |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, applicable project tests |

A green OWASP row means the mapped applicable controls completed without a blocking result. It does **not** prove that the entire OWASP category is secure.

CodeQL is only considered applicable for languages it supports. Unsupported languages remain visible rather than being silently treated as analyzed.

---

## 📊 Accuracy Benchmark

Accuracy is measured using a controlled labeled benchmark, not inferred from an ordinary pull request.

The benchmark ledger is:

```text
docs/accuracy/benchmark-results.csv
```

Each case contains an expected gate result and the actual SecurePR result:

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

Until labeled benchmark cases have actually been executed and recorded, SecurePR reports:

```text
Benchmark pending — no accuracy percentage is claimed.
```

Once the benchmark is populated, the Actions summary and accuracy evidence report TP, FP, TN, FN, precision, recall, and F1.

---

## 📚 Documentation Files

| File | Read it when |
|---|---|
| `README.md` | You want the project overview, setup, architecture, usage, and final MVP behavior |
| `docs/architecture.md` | You want the internal SecurePR architecture and component boundaries |
| `docs/security-requirements.md` | You want the security requirements and gate expectations |
| `docs/security-checks.md` | You want the exact security controls and OWASP coverage mapping |
| `docs/threat-model.md` | You want the threats and trust boundaries considered by SecurePR |
| `docs/testing.md` | You want local, CI, blocking-path, and benchmark testing procedures |
| `docs/github-actions.md` | You want the GitHub Actions workflow, reusable workflow, and reporting behavior |
| `docs/accuracy/benchmark-results.csv` | You want the labeled accuracy benchmark cases |

There is intentionally no phase-based `docs/phase-4-plan.md` in the final MVP documentation. Final behavior is documented in the appropriate topic-specific files instead of a development-phase plan.

---

## ⚠️ Security Scope & Limitations

SecurePR is an automated security gate, not proof that software is secure.

Important boundaries include:

- Static-analysis tools can miss vulnerabilities and can produce false positives.
- OWASP categories are broad and cannot all be comprehensively automated.
- A06 Insecure Design requires meaningful human architecture, threat-model, requirements, and business-logic review.
- CodeQL coverage is limited to CodeQL-supported languages.
- Dependency auditing only applies where a supported dependency ecosystem and manifest are present.
- Project tests only establish what those tests actually exercise.
- A PASS means the mapped applicable controls passed; it does not mean every vulnerability has been eliminated.
- Accuracy percentages are not reported until labeled benchmark data exists.

Human security review is always recommended.

---

## ⚖️ Legal & Ethical Note

SecurePR is intended for repositories and systems you own or are authorized to assess.

Use security scanners, test fixtures, and dependency-analysis tooling responsibly. Do not place real secrets or credentials into benchmark fixtures. Do not use SecurePR to bypass access controls or test repositories without authorization.

Security results are technical evidence and should be interpreted within the application's architecture, threat model, deployment environment, and organizational security process.

---

## 🏁 Final MVP Status

**Final MVP implementation verified.**

SecurePR provides a reusable pull-request security gate with repository profiling, CodeQL, Semgrep, Gitleaks, dependency auditing, project tests, SARIF security-finding evaluation, OWASP Top 10:2025 coverage mapping, PASS/BLOCK reporting, reusable GitHub Actions support, and controlled accuracy measurement.

The final MVP is designed to be reused across repositories you control, including SecurePR itself and future integrations with CookieGuard and NetDefender. The benchmark remains pending until labeled benchmark executions are actually recorded.
