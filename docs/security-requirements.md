# SecurePR Security Requirements

## 1. Purpose

SecurePR evaluates pull-request changes using layered security controls. The gate is intended to be reusable across the user's own repositories and is not limited to the Phase 2 Python sample application.

These requirements define intended automated coverage. They are not a claim that automation can prove every security property.

## 2. Core Requirements

SecurePR shall:

1. Detect selected security defects before merge.
2. Detect exposed secrets and credential-like material.
3. Analyze supported programming languages with applicable SAST tooling.
4. Audit supported dependency ecosystems when a relevant manifest exists.
5. Run applicable security and correctness tests.
6. Analyze security-relevant CI/CD configuration where practical.
7. Map implemented coverage to OWASP Top 10:2025 and related secure-coding principles.
8. Detect high-confidence hard-coded credentials and privileged identity values.
9. Aggregate duplicate scanner findings into one meaningful result where the findings represent the same issue.
10. Produce exactly one overall `PASS` or `BLOCK` decision.
11. Explain blocking results and remediation steps.
12. Always recommend human review in PASS and BLOCK remediation guidance.
13. Never automatically modify source code, rotate credentials, or merge a pull request.
14. Report unsupported or unavailable analysis coverage rather than silently treating it as secure.
15. Remain reusable across the user's own repositories without requiring GitHub Marketplace publication.
16. Provide a controlled final accuracy benchmark using TP, FP, TN, FN, precision, recall, and F1.

## 3. OWASP Top 10:2025 Coverage Model

The Phase 4 coverage model includes:

- A01 Broken Access Control
- A02 Security Misconfiguration
- A03 Software Supply Chain Failures
- A04 Cryptographic Failures
- A05 Injection
- A06 Insecure Design
- A07 Authentication Failures
- A08 Software or Data Integrity Failures
- A09 Security Logging & Alerting Failures
- A10 Mishandling of Exceptional Conditions

Additional secure-coding concerns include secrets, SQL/command/template injection, XSS, SSRF, unsafe deserialization, path traversal, weak cryptography, disabled TLS verification, sensitive logging, error leakage, CI/CD permissions, unsafe workflow input, dependency vulnerabilities, and integrity-sensitive operations where applicable.

The project must identify context-dependent areas as human-review boundaries rather than claiming that they are completely automated.

## 4. Language and Repository Requirements

The gate shall detect applicable CodeQL-supported languages, including C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, and Swift.

PHP and Scala are not supported by CodeQL in this MVP. Their presence must produce an explicit coverage boundary rather than a false PASS for CodeQL coverage.

The gate shall detect common dependency manifests and only run ecosystem-specific audits when applicable.

## 5. Finding Requirements

A high-confidence hard-coded password, credential, or privileged username detected by SecurePR policy is a blocking finding.

Multiple tools may report the same underlying issue. SecurePR shall normalize identical SARIF findings so the developer sees one meaningful finding while detailed tool logs remain available.

## 6. Gate Requirements

`PASS` requires every configured blocking control to succeed and no blocking normalized finding to remain.

`BLOCK` occurs when a configured blocking control fails or a blocking normalized finding remains.

There is no third gate state.

Every PASS and BLOCK remediation section shall state that human review is always recommended.

## 7. Human Review Boundary

Automated checks do not replace review of business logic, architecture, threat assumptions, authorization intent, deployment context, or other context-dependent security decisions. A PASS is not proof of zero vulnerabilities.

## 8. Accuracy Requirement

At the end of Phase 4, SecurePR shall execute a controlled benchmark containing known vulnerable and known safe cases.

Record:

- TP — vulnerable and blocked
- FP — safe and blocked
- TN — safe and passed
- FN — vulnerable and passed

Calculate:

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

The final report must state the benchmark scope and must not present the measurements as universal accuracy.
