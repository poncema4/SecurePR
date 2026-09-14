# SecurePR Security Checks

## Overview
This document is the executable security-coverage reference for SecurePR. The workflow determines which controls actually run for a repository. SecurePR combines complementary automated controls instead of treating one scanner as proof that software is secure.

## Core Gate Controls

| Control | How SecurePR runs it | Gate behavior |
|---|---|---|
| Python runtime policy | Reads the repository runtime declaration and enforces the supported minimum | BLOCK on unsupported declared runtime |
| Repository profile | Detects applicable CodeQL languages and dependency manifests | BLOCK if profiling fails |
| Project tests | Runs applicable Python tests/compilation and JS/TS tests/type checks | BLOCK on failure |
| Gitleaks | Scans repository content/history for secrets and credential material | BLOCK on Gitleaks failure/finding |
| Semgrep | Runs security rules plus SecurePR-specific high-confidence rules and emits SARIF | BLOCK on failure/finding |
| Dependency audit | Runs pip-audit for Python and npm audit for npm lockfiles | BLOCK on audit failure |
| CodeQL | Initializes/analyzes detected CodeQL-supported languages with security-extended queries | BLOCK on initialization/analysis failure |
| SARIF security findings | Evaluates SARIF-producing security results | BLOCK when findings are reported |

## OWASP Top 10:2025 Coverage

OWASP Top 10:2025 is used as a **coverage framework**. It is not a claim that SecurePR can completely automate every category. The official OWASP project explicitly describes the Top 10 as an awareness document and states that tools cannot comprehensively detect or protect against all Top 10 risks, particularly insecure design.

| Category | Automated controls used by SecurePR | What the controls can check | Boundary |
|---|---|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, project tests | Authorization, privilege, object-access, SSRF/access-boundary and traversal patterns where supported | Intended authorization policy and business logic still need review |
| A02 Security Misconfiguration | CodeQL, Semgrep | Unsafe configuration, insecure defaults, debug/TLS/security-setting patterns where supported | Deployment/environment configuration may require review |
| A03 Software Supply Chain Failures | Dependency audit, CodeQL, Semgrep | Known dependency vulnerabilities plus source/workflow trust-boundary patterns where supported | Full build/distribution ecosystem trust cannot be proven by these checks |
| A04 Cryptographic Failures | CodeQL, Semgrep | Weak crypto, unsafe password/secret handling, TLS/certificate and randomness patterns where supported | Cryptographic design and context may require review |
| A05 Injection | CodeQL, Semgrep, project tests | SQL, command, code, XSS, template and related injection flows where supported | Runtime/framework behavior can exceed static coverage |
| A06 Insecure Design | CodeQL, Semgrep, project tests | Detectable insecure-design indicators and security-test failures | Architecture, threat model, requirements and business logic require human review |
| A07 Authentication Failures | CodeQL, Semgrep, project tests | Authentication, credential, session and related patterns where supported | Correct authentication intent and operational controls require review |
| A08 Software or Data Integrity Failures | CodeQL, dependency audit, Semgrep | Integrity boundaries, unsafe deserialization, artifact/trusted-source and dependency risks where supported | End-to-end artifact and data trust may require review |
| A09 Security Logging & Alerting Failures | CodeQL, Semgrep | Detectable unsafe/missing logging and alerting patterns | Operational monitoring and alerting effectiveness require review |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, project tests | Error/exception handling, failing-open and abnormal-condition patterns where supported | Complete runtime failure behavior cannot be established statically |

### Meaning of PASS and BLOCK in the OWASP table

- **PASS:** every automated control mapped to that category completed without a blocking result for the current run.
- **BLOCK:** at least one automated control mapped to that category failed or blocked.
- **Important:** PASS means the mapped automation passed. It does **not** mean the OWASP category is completely secure.

## SecurePR-Specific Semgrep Rules

SecurePR currently includes high-confidence rules for:

- Hard-coded password/credential-like values.
- Hard-coded privileged usernames such as `admin`, `administrator`, `root`, or `superuser`.
- Unsafe `eval`/`exec` use.
- Explicitly disabled Python TLS certificate verification such as `verify=False`.

Tests and documentation are excluded from these application-source rules so controlled examples do not create ordinary application findings.

## Gitleaks

Gitleaks is the dedicated secret-detection control. SecurePR does not replace Gitleaks with a simple regex. A real credential must never be committed to demonstrate a finding. Demonstrations should use controlled synthetic values or temporary fixtures.

## SARIF Evidence

Semgrep and CodeQL produce machine-readable security evidence. `scripts/summarize_sarif.py` reads SARIF files, preserves distinct findings, and writes a detailed `securepr-findings.md` artifact. The user-facing Actions summary does not expose a separate "normalized findings" section; the gate remains focused on the required PASS/BLOCK structure.

## Accuracy

Accuracy is documented and measured from labeled benchmark cases, not inferred from an ordinary PR passing.

- **TP:** expected BLOCK, actual BLOCK.
- **FP:** expected PASS, actual BLOCK.
- **TN:** expected PASS, actual PASS.
- **FN:** expected BLOCK, actual PASS.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × Precision × Recall / (Precision + Recall)`

The benchmark ledger is stored in `docs/accuracy/benchmark-results.csv`. No accuracy percentage is claimed until labeled benchmark results exist.

## Gate Design

The authoritative SecurePR workflow has one GitHub Actions job named `SecurePR Security Gate`. It produces exactly two outcomes: `PASS` or `BLOCK`.

The user-facing summary is ordered as:

1. `SecurePR: PASS` or `SecurePR: BLOCK`
2. Check Results
3. OWASP Top 10:2025 Coverage
4. Fixes to make this PASS
5. Remediation
6. Accuracy
7. Human review
8. Full Actions run link

SecurePR does not automatically modify source code, rotate credentials, or merge pull requests.
