# SecurePR
**Reusable Pull Request Security Harness and Security Gate**

## Overview
SecurePR is a reusable **security harness** for GitHub pull requests. It is the orchestration, applicability, policy, aggregation, and reporting layer that coordinates multiple security engines and project checks into one consistent `PASS` or `BLOCK` result.

SecurePR is **not a standalone vulnerability scanner and does not rely on one security engine or one LLM prompt**. The underlying engines provide specialized evidence; SecurePR runs the applicable engines, evaluates their results, and presents the developer with one actionable gate.

The primary policy and orchestration implementation is `.github/workflows/security.yml`. The SecurePR-specific Semgrep rule set is `.semgrep_securepr.yml`.

## Problem
Pull requests can introduce security issues through source code, dependencies, credentials, configuration, authentication, authorization, and CI/CD changes. Running individual tools does not by itself provide one consistent decision, applicability model, or reporting format.

SecurePR provides the reusable harness around those tools so repositories can use a common security-gate workflow without copying the scanner implementations into each project.

## Objectives
- Run repeatable security checks on pull requests.
- Orchestrate complementary security engines under one gate.
- Detect applicable repository languages and dependency manifests.
- Produce clear `PASS` or `BLOCK` results with actionable remediation guidance.
- Map automated evidence to OWASP Top 10:2025 as a coverage framework.
- Measure gate behavior with labeled benchmark cases using TP, FP, TN, precision, recall, and F1.
- Keep remediation, approval, and merging under human control.

## MVP Scope
- Reusable GitHub Actions security harness.
- One authoritative `SecurePR Security Gate` job.
- Repository and language profiling.
- Project security/correctness tests when applicable.
- CodeQL `security-extended` analysis for detected supported languages.
- Semgrep `p/security-audit` plus SecurePR-specific rules.
- Gitleaks secret detection.
- Supported dependency auditing with `pip-audit` and `npm audit`.
- SARIF finding aggregation and evidence artifacts.
- OWASP Top 10:2025 coverage mapping.
- `PASS` / `BLOCK` reporting.
- Labeled expected-versus-actual accuracy measurement.
- Cumulative benchmark metrics from `docs/accuracy/benchmark-results.csv`.

## Architecture / Workflow
```text
Developer opens or updates Pull Request
                    ↓
             SecurePR Harness
                    ↓
        Repository / Applicability Profile
                    ↓
       ┌────────────┼──────────────┐
       ↓            ↓              ↓
 Project Tests   Security Engines  Dependency Audits
                    │
          ┌─────────┼─────────┐
          ↓         ↓         ↓
      Gitleaks   Semgrep    CodeQL
          │         │         │
          └─────────┼─────────┘
                    ↓
          Security Evidence / SARIF
                    ↓
        SecurePR Policy + Aggregation
                    ↓
              PASS or BLOCK
                    ↓
             Human Review
```

**SecurePR is the harness around the engines.** Gitleaks, Semgrep, CodeQL, dependency auditors, and project tests are the underlying evidence sources; SecurePR provides the common workflow, policy, aggregation, decision, and reporting layer.

## Rule Book / Policy Sources
SecurePR does not use a single prompt as its security rule book. The policy is implemented across the following layers:

| Source | Role |
|---|---|
| `.github/workflows/security.yml` | Authoritative orchestration and final PASS/BLOCK gate policy |
| `.semgrep_securepr.yml` | SecurePR-specific high-confidence Semgrep rules |
| Semgrep `p/security-audit` | Broad rule-based SAST coverage |
| CodeQL `security-extended` | Semantic and data-flow security analysis |
| Gitleaks | Secret and credential detection |
| `pip-audit` / `npm audit` | Known dependency vulnerability auditing |
| Target repository tests | Application-specific behavior/security checks |
| `scripts/repository_profile.py` | Determines applicable languages and dependency ecosystems |
| `scripts/summarize_sarif.py` | Aggregates SARIF security evidence |
| `scripts/accuracy_report.py` | Reports controlled benchmark behavior |

The detailed control mapping is documented in `docs/security-checks.md`.

## Tech Stack
| Area | Technology |
|---|---|
| Harness / Workflow | GitHub Actions |
| SAST Engines | CodeQL, Semgrep |
| Secret Detection | Gitleaks |
| Dependency Auditing | pip-audit, npm audit |
| Policy / Aggregation / Reporting | Python |
| Result Format | SARIF / GitHub Actions Summary |
| Testing | pytest, project tests, compilation checks |
| Version Control | Git / GitHub |

## Project Structure
```text
SecurePR/
├── .github/
│   └── workflows/
│       ├── security.yml
│       └── reusable-security.yml
├── app/
├── scripts/
│   ├── accuracy_metrics.py
│   ├── accuracy_report.py
│   ├── check_python_version.py
│   ├── repository_profile.py
│   └── summarize_sarif.py
├── security/
├── tests/
│   └── security/
├── docs/
│   ├── accuracy/
│   │   ├── benchmark-results.csv
│   │   └── methodology.md
│   ├── architecture.md
│   ├── github-actions.md
│   ├── security-checks.md
│   ├── security-requirements.md
│   ├── setup.md
│   ├── testing.md
│   └── threat-model.md
├── .semgrep_securepr.yml
├── .python-version
├── README.md
└── requirements.txt
```

## Security Controls
SecurePR's MVP combines:

- repository profiling and applicability detection
- project security and correctness tests
- CodeQL semantic security analysis
- Semgrep rule-based SAST and SecurePR-specific high-confidence rules
- Gitleaks secret detection
- dependency vulnerability auditing
- SARIF-based security finding evaluation
- OWASP Top 10:2025 coverage mapping
- consolidated `PASS` / `BLOCK` policy

## Expected Demonstration
Add the SecurePR reusable workflow to a repository, open a pull request, and inspect the `SecurePR Security Gate` result.

For a controlled benchmark, a trusted reviewer adds `securepr-expected-pass` or `securepr-expected-block`. SecurePR reruns the current PR and reports its expected result, actual result, classification correctness, and cumulative benchmark metrics in the Actions summary.

A normal PR is not automatically counted as a TP, FP, TN, or FN because its expected security outcome is unknown. The benchmark CSV is a reviewed evidence ledger and is not silently changed by every PR.

## Security Scope and Limitations
SecurePR is a reusable DevSecOps security harness, not a guarantee that a repository is vulnerability-free. Static analysis can miss issues and produce false positives; tests cover only the behavior they exercise; dependency checks depend on supported ecosystems; and CodeQL analysis depends on supported languages.

OWASP Top 10:2025 is used as a coverage framework. SecurePR maps applicable automated controls to the categories; it does not claim a separate complete OWASP scanner. A passing mapped control does not prove the entire category is secure, and context-dependent risks such as insecure design and business logic require human review.

The current MVP is intended for repositories that the user owns or is authorized to assess. It is not currently designed to provide a hosted multi-user service or automatically manage access to arbitrary third-party repositories.

SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges pull requests.

## Final MVP Status
The SecurePR MVP is **functionally complete as a reusable pull-request security harness**. The final MVP includes the authoritative security gate, reusable workflow, repository/language profiling, multiple underlying security engines, dependency auditing, project tests, SARIF evidence aggregation, OWASP coverage mapping, actionable reporting, and empirical benchmark measurement.

Final validation is based on controlled pull-request executions, the reviewed 26-case benchmark corpus, and successful post-merge `main` verification. The benchmark currently reports 10 TP, 0 FP, 11 TN, and 5 FN: 80.77% conventional classification accuracy, 100% precision, 66.67% recall, and 80.00% F1. These are controlled-corpus measurements, not universal real-world accuracy claims.

## Out of Scope
- Automatic vulnerability remediation.
- Automatic credential rotation.
- Automatic pull-request merging.
- Universal real-world accuracy claims.
- Complete automated coverage of every OWASP Top 10:2025 risk.
- Hosted security scanning for arbitrary third-party repositories.
- Enterprise vulnerability management or centralized security administration.

## Future Enhancements
- Broader ecosystem-specific dependency auditing.
- Additional repository-specific security rules.
- Expanded labeled benchmark corpus.
- Additional policy controls and reporting integrations.
- Broader access and multi-repository management beyond the current owner-authorized MVP scope.

## Verification
Run the local verification from the repository root:

```text
python -m pytest -q
python -m compileall -q app security tests scripts
python scripts/accuracy_report.py
```

The complete security gate runs through GitHub Actions. For setup, reusable-workflow configuration, benchmark labeling, and Linux/Windows instructions, see `docs/setup.md`.

## Documentation
- [Architecture](docs/architecture.md)
- [Setup](docs/setup.md)
- [Testing & Evidence](docs/testing.md)
- [GitHub Actions](docs/github-actions.md)
- [Security Checks / Rule Book](docs/security-checks.md)
- [Security Requirements](docs/security-requirements.md)
- [Threat Model](docs/threat-model.md)
- [Accuracy Methodology](docs/accuracy/methodology.md)
