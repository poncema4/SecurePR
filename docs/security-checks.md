# SecurePR Security Checks

## Overview
This document is the **conceptual security coverage matrix** for SecurePR. The executable workflows determine what actually runs for a repository. SecurePR uses layered controls rather than treating one scanner as a complete security solution.

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
| Access control | CodeQL/Semgrep + security tests | Partial | Context-dependent authorization remains a human-review boundary |
| Authentication | CodeQL/Semgrep + tests | Partial | Password/credential handling and auth changes covered where detectable |
| Cryptography | CodeQL/Semgrep + tests | Partial | Weak algorithms, insecure randomness/material, disabled TLS where rules support it |
| Security misconfiguration | SAST + configuration/workflow checks | Partial | Repository-aware configuration coverage |
| Software supply chain | Dependency audits + workflow checks | Partial | Applicable ecosystem audits |
| Software/data integrity | SAST + dependency/CI checks | Partial | Build/dependency/workflow integrity |
| Logging/alerting | SAST + tests | Partial | Sensitive logging/error disclosure patterns |
| Exceptional conditions | SAST + tests | Partial | Error handling/fail-open patterns where detectable |
| CI/CD security | Workflow checks + review | Partial | Permissions, untrusted input, shell interpolation, action usage |
| Container security | Container scanner/config checks | Conditional | Only when repository uses containers and the corresponding scanner is added |
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

The workflow maps implemented controls and findings to these categories where a defensible mapping exists. OWASP Top 10:2025 is a coverage framework, not a claim that every category can be completely automated.

## Tool Responsibilities

### CodeQL
CodeQL performs semantic source-code analysis for supported languages and can identify security-relevant data-flow and coding patterns. CodeQL results are uploaded to GitHub Code Scanning. SecurePR treats CodeQL as a major analysis engine, not as the complete security decision.

### Semgrep
Semgrep provides complementary rule-based SAST. SecurePR adds local rules for high-confidence hard-coded password/credential values, hard-coded privileged usernames, unsafe dynamic evaluation, and explicitly disabled TLS verification. Semgrep results are emitted as SARIF so SecurePR can normalize them with other SARIF-producing controls.

### Gitleaks
Gitleaks detects credential and secret material. PR comments and duplicate summaries remain disabled so SecurePR can provide one overall gate result. Real credentials must never be used in demonstrations.

### Dependency audits
Python projects use pip-audit where applicable. JavaScript/TypeScript projects use npm audit when an npm lockfile is present. Additional ecosystems can be added when the audit is reliable and appropriately scoped.

### Project tests
Tests validate security behavior and correctness that static analysis cannot reliably prove. A required failing test blocks the gate.

## Finding Aggregation

`scripts/summarize_sarif.py` normalizes findings using artifact location, line, rule, and message. This prevents identical CodeQL/Semgrep reports from producing multiple copies of the same meaningful finding in the SecurePR summary. Tool names remain visible so the developer can see which engines reported the issue.

Aggregation is deliberately conservative: distinct findings are not merged merely because they share a file or line.

## Gate Design

The gate remains one GitHub Actions job named `SecurePR Security Gate`. Individual controls run as steps, and the final result produces exactly one `PASS` or `BLOCK` decision.

PASS and BLOCK remediation text always states that human review is recommended. SecurePR does not automatically remediate or merge.

## Accuracy and Coverage Status

Every PR reports the current benchmark status. Before the final benchmark is executed, the report states **Benchmark pending — no accuracy percentage is claimed**. After results exist, every PR reports TP, FP, TN, precision, recall, and F1 for the latest controlled benchmark.

For the final benchmark:

- **TP:** vulnerable case correctly blocked.
- **FP:** safe case incorrectly blocked.
- **TN:** safe case correctly passed.
- **FN:** vulnerable case incorrectly passed.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

The measurements describe the tested benchmark corpus and configuration. They do not prove universal detection accuracy.
