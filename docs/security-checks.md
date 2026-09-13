# SecurePR Security Checks

## Coverage Matrix

| Security concern | Primary control(s) | Automation boundary | Phase 4 direction |
|---|---|---|---|
| Secrets / API keys / passwords / private keys | Gitleaks + SecurePR Semgrep rules | Automated | Block high-confidence findings |
| Hard-coded privileged usernames | SecurePR Semgrep rule | Automated / contextual | Block matched high-confidence cases |
| SQL / command / template injection | CodeQL + Semgrep + tests | Automated / partial | Multi-language coverage where tools support it |
| XSS | CodeQL + Semgrep + tests | Automated / partial | Applicable framework/source analysis |
| Path traversal | CodeQL + Semgrep + tests | Automated / partial | Applicable file-access surfaces |
| Unsafe deserialization | CodeQL + Semgrep + tests | Automated / partial | Applicable languages/frameworks |
| SSRF | CodeQL/Semgrep + tests | Partial | Conditional on URL-fetch surface |
| Access control | CodeQL/Semgrep + security tests | Partial | Context-dependent authorization remains human-reviewed |
| Authentication | CodeQL/Semgrep + tests | Partial | Password/credential handling and auth changes covered where detectable |
| Cryptography | CodeQL/Semgrep + tests | Partial | Weak algorithms, insecure randomness/material, disabled TLS where rules support it |
| Security misconfiguration | SAST + configuration/workflow checks | Partial | Expand repository-aware configuration coverage |
| Software supply chain | Dependency audits + workflow checks | Partial | Applicable ecosystem audits |
| Software/data integrity | SAST + dependency/CI checks | Partial | Build/dependency/workflow integrity |
| Logging/alerting | SAST + tests | Partial | Sensitive logging/error disclosure patterns |
| Exceptional conditions | SAST + tests | Partial | Error handling/fail-open patterns where detectable |
| CI/CD security | Workflow checks + review | Partial | Permissions, untrusted input, shell interpolation, action usage |
| Container security | Container scanner/config checks | Conditional | Only when repository uses containers |
| Insecure design | Threat model + review + indicators | Manual / partial | Never silently treated as fully automated |
| Business logic | Tests + review | Manual / partial | Requirement-specific evidence required |

## OWASP Top 10:2025

SecurePR uses OWASP Top 10:2025 as a coverage framework rather than as a single scanner. The ten categories are:

1. Broken Access Control
2. Security Misconfiguration
3. Software Supply Chain Failures
4. Cryptographic Failures
5. Injection
6. Insecure Design
7. Authentication Failures
8. Software or Data Integrity Failures
9. Security Logging & Alerting Failures
10. Mishandling of Exceptional Conditions

The workflow should map implemented controls and findings to these categories where a defensible mapping exists.

## Tool Responsibilities

### CodeQL

CodeQL performs semantic source-code analysis for supported languages and can identify security-relevant data-flow and coding patterns. CodeQL results are uploaded to GitHub Code Scanning. SecurePR treats CodeQL as a major analysis engine, not as the complete security decision.

### Semgrep

Semgrep provides complementary rule-based SAST. SecurePR adds local rules for high-confidence hard-coded password/credential values and hard-coded privileged usernames. Semgrep results are emitted as SARIF so SecurePR can normalize them with other SARIF-producing controls.

### Gitleaks

Gitleaks detects credential and secret material. PR comments and duplicate summaries remain disabled so SecurePR can provide one overall gate result. Real credentials must never be used in demonstrations.

### Dependency audits

Python projects use pip-audit where applicable. Phase 4 adds repository-aware support for additional ecosystems where the audit can be run reliably, beginning with npm lockfiles for JavaScript/TypeScript repositories.

### Project tests

Tests validate security behavior and correctness that static analysis cannot reliably prove. A required failing test blocks the gate.

## Finding Aggregation

`scripts/summarize_sarif.py` normalizes SARIF findings by tool, rule, file, line, and message. This prevents identical CodeQL/Semgrep reports from producing multiple copies of the same meaningful finding in the SecurePR summary. Native logs remain available.

Aggregation is deliberately conservative: distinct findings are not merged merely because they share a file.

## Gate Design

The gate remains one GitHub Actions job named `SecurePR Security Gate`. Individual controls run as steps, and the final result produces exactly one `PASS` or `BLOCK` decision.

PASS and BLOCK remediation text always states that human review is recommended. SecurePR does not automatically remediate or merge.

## Accuracy Boundary

SecurePR does not claim perfect accuracy. False positives and false negatives are expected possibilities. Final Phase 4 validation will use a controlled corpus and calculate TP, FP, TN, FN, precision, recall, and F1.

The measured benchmark will be used to describe tested effectiveness, not to claim universal accuracy.
