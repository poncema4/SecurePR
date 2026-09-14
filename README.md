# SecurePR
**Reusable Pull Request Security Gate**

## Overview
SecurePR is a reusable DevSecOps pull-request security gate for repositories you control. It combines project tests, secret detection, SAST, dependency auditing, repository profiling, and OWASP Top 10:2025 coverage mappings into one GitHub Actions security decision: `PASS` or `BLOCK`.

SecurePR is the **harness, orchestration, policy, aggregation, and reporting layer**. CodeQL, Semgrep, Gitleaks, dependency audits, and project tests provide the underlying security evidence.

## Problem
Pull requests can introduce security weaknesses through source code, dependencies, secrets, configuration, CI/CD changes, authentication and authorization logic, or unsafe error handling. No single scanner can prove that a repository is secure, so SecurePR combines complementary controls and makes their boundaries visible.

## Objectives
- Analyze applicable programming languages with language-aware security tooling.
- Detect secrets, insecure coding patterns, dependency vulnerabilities, and failing security/correctness tests.
- Map automated controls to all ten OWASP Top 10:2025 categories without claiming that every category is fully automatable.
- Produce exactly one gate decision: `PASS` or `BLOCK`.
- Give developers actionable remediation guidance when a control blocks.
- Keep human security review as a recommendation after every result.
- Support reuse across repositories you control without GitHub Marketplace packaging.
- Measure false positives and false negatives with a controlled benchmark rather than inventing an accuracy percentage.

## MVP Scope
- Repository and language profiling.
- Multi-language CodeQL analysis for CodeQL-supported languages detected in the repository.
- Semgrep security analysis plus SecurePR-specific high-confidence rules.
- Gitleaks secret detection.
- Applicable Python and npm dependency audits.
- Applicable project tests and type checks.
- SARIF-based security finding detection and aggregation for machine-readable evidence.
- OWASP Top 10:2025 coverage mappings with PASS/BLOCK results.
- Reusable GitHub Actions workflow for repositories you control.
- Controlled TP/FP/TN/FN accuracy measurement documented separately from the normal gate decision.

## Architecture
```text
Developer
   ↓
Pull Request
   ↓
SecurePR Security Gate
   ├── Repository / language profile
   ├── Project tests
   ├── Secret detection (Gitleaks)
   ├── Rule-based SAST (Semgrep)
   ├── Semantic SAST (CodeQL)
   ├── Dependency audits
   ├── SARIF security-finding evaluation
   └── OWASP Top 10:2025 coverage mapping
   ↓
SecurePR: PASS / BLOCK
   ↓
Human security review is always recommended
```

## How Security Checks Work

### Gitleaks
Gitleaks scans repository content and history for credential and secret patterns such as API keys, tokens, passwords, and private-key material. A blocking Gitleaks result causes SecurePR to report `BLOCK`.

### Semgrep
Semgrep performs rule-based static analysis. SecurePR combines Semgrep's security rules with local high-confidence rules for hard-coded credentials, privileged usernames, unsafe dynamic evaluation, and explicitly disabled TLS verification. Findings are emitted as SARIF.

### CodeQL
SecurePR profiles the repository first, then passes the detected CodeQL-supported languages to CodeQL's semantic analysis. CodeQL analyzes supported source languages using security-extended queries. If a repository contains a language that CodeQL does not support, SecurePR must not silently treat that language as analyzed.

### Dependency audits
Python repositories use `pip-audit` when a supported Python dependency manifest is present. npm repositories use `npm audit` when `package-lock.json` is present. A dependency audit failure blocks the gate.

### Project tests
Repository tests and type checks validate behavior that static analysis cannot reliably establish. Applicable failing tests block the gate.

### Security findings
SARIF-producing security checks are evaluated for findings. SecurePR keeps detailed machine-readable evidence in the Actions artifact while the user-facing summary stays focused on the PASS/BLOCK decision, check results, OWASP coverage, remediation, accuracy, and human review.

## OWASP Top 10:2025 Coverage
SecurePR uses the official OWASP Top 10:2025 categories as a **coverage framework**, not as ten claims of complete automated detection. OWASP's guidance recognizes that automated tools cannot comprehensively detect or protect against every Top 10 risk, especially insecure design.

SecurePR does not implement a separate OWASP scanner. Instead, the OWASP categories are mapped to the security engines and project controls that actually run. The workflow records the result of those mapped controls for each category.

| Category | SecurePR automated coverage |
|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, project tests; authorization and access-boundary patterns where detectable |
| A02 Security Misconfiguration | CodeQL and Semgrep; insecure configuration/security-setting patterns where detectable |
| A03 Software Supply Chain Failures | Dependency audits plus CodeQL/Semgrep source and workflow-related analysis where supported |
| A04 Cryptographic Failures | CodeQL/Semgrep checks for weak or unsafe cryptographic, credential, and TLS practices where detectable |
| A05 Injection | CodeQL, Semgrep, and project tests for SQL, command, code, XSS, template, and related injection patterns where supported |
| A06 Insecure Design | Automated indicators plus project tests; architecture, threat-model, requirements, and business-logic review remain human responsibilities |
| A07 Authentication Failures | CodeQL, Semgrep, and project tests for authentication, credential, session, and related patterns where detectable |
| A08 Software or Data Integrity Failures | CodeQL, dependency auditing, and Semgrep for integrity boundaries, deserialization, artifact, and trusted-source risks where supported |
| A09 Security Logging & Alerting Failures | CodeQL/Semgrep for detectable logging and alerting patterns plus human review of operational coverage |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, and project tests for detectable error, exception, and fail-open patterns |

A green row means the mapped automated controls completed without a blocking result. It does **not** mean the entire OWASP category is proven secure.

## PASS/BLOCK Reporting
The GitHub Actions job is named **`SecurePR Security Gate`** and produces exactly two gate outcomes.

The Actions summary is intentionally organized as:

1. `SecurePR: PASS` or `SecurePR: BLOCK`
2. Check Results
3. The result explanation for the current gate
4. OWASP Top 10:2025 Coverage
5. Fixes to make this PASS
6. Remediation
7. Accuracy
8. Human review
9. Full Actions run link

### PASS
All required applicable controls completed successfully and no SARIF-producing security check reported a blocking finding. Human review is still recommended.

### BLOCK
One or more required SecurePR controls did not pass. The summary identifies the failed control and directs the developer to fix it on the same PR/branch before rerunning the gate. Human review is always recommended.

Remediation is performed by the developer; SecurePR never changes source code, rotates credentials, dismisses findings, or merges automatically.

## Reusing SecurePR in Other Repositories
The reusable workflow is designed for repositories you control. It is not a GitHub Marketplace action and does not require copying the security logic into every repository.

A target repository adds a small caller workflow such as:

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

The reusable workflow checks out the calling repository, detects applicable languages/manifests, runs applicable tests and audits, runs Gitleaks, Semgrep, and CodeQL where supported, evaluates security findings, and publishes the same PASS/BLOCK result.

For a repository that needs a pinned SecurePR revision, use a commit SHA or another reviewed ref instead of `main`. The SecurePR repository itself tests the reusable tooling from the PR under review so changes to the gate are exercised before merge.

Examples of intended targets include SecurePR itself, CookieGuard, and NetDefender. The actual checks depend on each target repository's languages, manifests, tests, and available security evidence.

## Accuracy
Accuracy is a benchmark property, not a normal PR confidence score. SecurePR records labeled benchmark cases with expected and actual `PASS`/`BLOCK` results and calculates:

- **TP:** expected `BLOCK`, actual `BLOCK`
- **FP:** expected `PASS`, actual `BLOCK`
- **TN:** expected `PASS`, actual `PASS`
- **FN:** expected `BLOCK`, actual `PASS`

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × Precision × Recall / (Precision + Recall)`

The benchmark ledger is `docs/accuracy/benchmark-results.csv`. Until labeled benchmark cases exist, the workflow reports that the benchmark is pending and does not claim an accuracy percentage. Once labeled results are recorded, the Actions summary reports TP, FP, TN, FN, precision, recall, and F1.

## Security Scope and Limitations
SecurePR is an automated security gate, not proof that software is secure. OWASP categories are broad, and many risks depend on application context, architecture, business logic, runtime behavior, configuration, deployment, and threat assumptions. Human review is always recommended.

CodeQL coverage is limited to languages supported by CodeQL. Other languages can still receive Semgrep, dependency, project-test, or other applicable checks, but SecurePR must not represent unsupported CodeQL analysis as completed.

## Tech Stack
| Area | Technology |
|---|---|
| Language | Python |
| SAST | CodeQL, Semgrep |
| Secret detection | Gitleaks |
| Dependency auditing | pip-audit, npm audit where applicable |
| CI/CD | GitHub Actions |
| Testing | pytest + repository-specific checks |
| Output | GitHub Actions job summary + SARIF/evidence artifacts |
| Version control | Git / GitHub |

## Project Structure
```text
SecurePR/
├── app/
├── security/
├── tests/
├── scripts/
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
│   ├── security.yml
│   └── reusable-security.yml
├── .semgrep_securepr.yml
├── .python-version
└── requirements.txt
```

`.python-version` belongs at the repository root because it is a standard Python runtime-version declaration. `.semgrep_securepr.yml` also belongs at the repository root because it is the SecurePR-specific Semgrep configuration consumed by the workflows. Neither file needs to be moved into `scripts/` or `docs/`.

## Out of Scope
- GitHub Marketplace publication
- Public SaaS hosting
- Automatic source remediation
- Automatic credential rotation
- Automatic merging
- Guaranteed detection of every vulnerability
- Complete automated proof of every OWASP Top 10:2025 category
- Generic security scores that hide individual findings

## Future Enhancements
- Additional ecosystem-specific dependency auditors.
- More language/framework-specific SecurePR rules.
- Broader CI/CD and infrastructure-as-code security checks.
- Expanded controlled benchmark cases.
- Additional reusable-workflow demonstrations across CookieGuard and NetDefender.

## Verification
From the repository root:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
```

For a normal SecurePR use, open a PR and inspect the `SecurePR Security Gate` job summary. To test a blocking path safely, use a controlled synthetic vulnerable fixture rather than a real credential. Fix the fixture on the same branch and push again to verify that the same PR changes from `BLOCK` to `PASS`.

For accuracy, inspect `docs/accuracy/benchmark-results.csv`. An empty ledger intentionally produces `Benchmark pending — no accuracy percentage is claimed.` The ledger should only contain labeled cases after the controlled benchmark has actually been executed; do not fill in `actual` values by assumption.

The GitHub Actions verification should also confirm the single `SecurePR Security Gate` job, all applicable security controls, the OWASP coverage table, the final PASS/BLOCK result, the accuracy section, the evidence artifact, and post-merge `main` verification.

## Documentation
- [Architecture](docs/architecture.md)
- [Security Requirements](docs/security-requirements.md)
- [Security Checks](docs/security-checks.md)
- [Threat Model](docs/threat-model.md)
- [Testing](docs/testing.md)
- [GitHub Actions](docs/github-actions.md)
- [Accuracy benchmark ledger](docs/accuracy/benchmark-results.csv)

## Final MVP Status
**Final MVP implementation — final verification in progress.** SecurePR provides a reusable pull-request security gate with multi-language CodeQL profiling, Semgrep, Gitleaks, dependency auditing, project tests, SARIF finding detection, OWASP Top 10:2025 coverage mappings, PASS/BLOCK reporting, human-review guidance, and controlled accuracy measurement. The implementation is designed for reuse across repositories you control and is not packaged for GitHub Marketplace. The benchmark remains pending until labeled benchmark executions are actually recorded.
