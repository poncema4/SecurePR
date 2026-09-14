# SecurePR
**Reusable Pull Request Security Gate**

## Overview
SecurePR is a security **harness** for GitHub pull requests. It orchestrates repository tests, secret detection, SAST, dependency auditing, CodeQL, Semgrep, Gitleaks, SARIF evaluation, and policy checks into one consistent `PASS` or `BLOCK` result.

SecurePR is the harness, orchestration, policy, aggregation, and reporting layer. The underlying tools provide the security evidence.

## Problem
Pull requests can introduce security issues through source code, dependencies, credentials, configuration, authentication, authorization, and CI/CD changes. Running individual tools does not by itself provide one consistent decision or reporting format.

SecurePR provides a reusable security gate that can be added to repositories without copying the security implementation into each project.

## Objectives
- Run repeatable security checks on pull requests.
- Combine complementary security tools into one gate.
- Detect applicable repository languages and dependency manifests.
- Produce clear `PASS` or `BLOCK` results with actionable remediation guidance.
- Map automated evidence to OWASP Top 10:2025.
- Measure gate behavior with labeled benchmark cases using TP, FP, TN, precision, recall, and F1.
- Keep remediation, approval, and merging under human control.

## MVP Scope
- Reusable GitHub Actions security harness.
- One authoritative `SecurePR Security Gate` job.
- Repository and language profiling.
- Project tests when applicable.
- CodeQL security-extended analysis for supported languages.
- Semgrep SAST and SecurePR security rules.
- Gitleaks secret detection.
- Supported dependency auditing.
- SARIF finding aggregation and evidence artifacts.
- OWASP Top 10:2025 coverage mapping.
- `PASS` / `BLOCK` reporting.
- Labeled real-PR expected-versus-actual accuracy measurement.
- Cumulative benchmark metrics from `docs/accuracy/benchmark-results.csv`.

## Architecture / Workflow
```text
Pull Request
     ↓
SecurePR Harness
     ├── Repository Profile
     ├── Project Tests
     ├── Gitleaks
     ├── Semgrep
     ├── CodeQL
     └── Dependency Audit
             ↓
       Security Evidence
             ↓
    Policy / Aggregation
             ↓
       PASS or BLOCK
             ↓
        Human Review
```

```text
Real Pull Request
       ↓
Trusted Expected-Outcome Label
       ↓
SecurePR Reruns
       ↓
Expected vs. Actual
       ↓
Correct / Incorrect
       ↓
Cumulative TP / FP / TN
Precision / Recall / F1
```

## Tech Stack
| Area | Technology |
|---|---|
| Workflow | GitHub Actions |
| Security Analysis | CodeQL, Semgrep |
| Secret Detection | Gitleaks |
| Dependency Auditing | pip-audit, npm audit |
| Policy / Reporting | Python |
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
- Repository profiling and applicability detection.
- Project security and correctness tests.
- CodeQL semantic security analysis.
- Semgrep static analysis and high-confidence SecurePR rules.
- Gitleaks secret detection.
- Dependency vulnerability auditing.
- SARIF-based security finding evaluation.
- OWASP Top 10:2025 coverage mapping.
- Consolidated `PASS` / `BLOCK` policy.

## Expected Demonstration
Add the SecurePR reusable workflow to a repository, open a pull request, and inspect the `SecurePR Security Gate` result.

For a controlled benchmark, a trusted reviewer adds `securepr-expected-pass` or `securepr-expected-block`. SecurePR reruns the current PR and reports its expected result, actual result, classification correctness, and cumulative benchmark metrics in the Actions summary.

A normal PR is not automatically counted as a TP, FP, TN, or FN because its expected security outcome is unknown. The benchmark CSV is therefore a reviewed evidence ledger and is not silently changed by every PR.

## Security Scope and Limitations
SecurePR is a reusable DevSecOps security harness, not a guarantee that a repository is vulnerability-free. Static analysis can miss issues and produce false positives; tests cover only the behavior they exercise; dependency checks depend on supported ecosystems; and CodeQL analysis depends on supported languages.

OWASP Top 10:2025 is used as a coverage framework. A passing mapped control does not prove the entire OWASP category is secure, and context-dependent risks such as insecure design require human review.

The current MVP is intended for repositories that the user owns or is authorized to assess. It is not currently designed to provide a hosted multi-user service or automatically manage access to arbitrary third-party repositories.

SecurePR never automatically edits source code, rotates credentials, dismisses findings, or merges pull requests.

## Final MVP Status
The SecurePR MVP is functionally complete as a reusable pull-request security harness. The implementation includes the security gate, reusable workflow, multi-language profiling, security tooling, evidence reporting, OWASP mapping, and empirical accuracy measurement for labeled benchmark cases.

Final validation consists of running the gate on controlled pull requests, expanding the labeled benchmark with independently reviewed cases, and confirming the post-merge `main` workflow.

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
- Expanded labeled real-PR benchmark corpus.
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
- [Security Checks](docs/security-checks.md)
- [Security Requirements](docs/security-requirements.md)
- [Threat Model](docs/threat-model.md)
- [Accuracy Methodology](docs/accuracy/methodology.md)
