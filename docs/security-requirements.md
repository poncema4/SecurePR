# SecurePR Security Requirements

## Overview

SecurePR evaluates pull-request changes using layered security controls. The gate is reusable across repositories you own or are authorized to assess.

These requirements define automated coverage; they do not claim automation can prove every security property.

## Core Requirements

SecurePR shall:

1. Detect selected security defects before merge.
2. Detect exposed secrets and credential-like material.
3. Analyze supported programming languages with applicable SAST tooling.
4. Audit supported dependency ecosystems when a relevant manifest exists.
5. Run applicable security and correctness tests.
6. Analyze security-relevant CI/CD configuration where practical.
7. Map implemented coverage to OWASP Top 10:2025 and secure-coding principles.
8. Detect high-confidence hard-coded credentials and privileged identity values.
9. Aggregate duplicate scanner findings without hiding distinct findings in detailed evidence.
10. Produce exactly one overall `PASS` or `BLOCK` decision.
11. Explain blocking results and remediation steps.
12. Always recommend human review.
13. Never automatically modify source code, rotate credentials, or merge a pull request.
14. Report unsupported or unavailable analysis coverage instead of silently treating it as secure.
15. Remain reusable without requiring GitHub Marketplace publication.
16. Measure gate behavior with TP, FP, TN, precision, recall, and F1 from labeled cases.
17. Report cumulative accuracy on every PR and, when a trusted expected-outcome label is present, report the current PR's expected-versus-actual classification immediately.

## OWASP Top 10:2025 Coverage Model

The coverage model includes A01 through A10:

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

Context-dependent areas must remain human-review boundaries rather than being presented as completely automated.

## Language and Repository Requirements

The gate detects applicable CodeQL-supported languages, including C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, and Swift.

PHP and Scala are not supported by CodeQL in this MVP. Their presence must produce an explicit coverage boundary rather than a false PASS for CodeQL coverage.

Common dependency manifests are detected and ecosystem-specific audits run only when applicable.

## Gate Requirements

`PASS` requires every configured blocking control to succeed and no blocking security finding to remain.

`BLOCK` occurs when a configured blocking control fails or a blocking security finding remains.

There is no third gate state.

Every PASS and BLOCK outcome shall state that human review is recommended.

## Human Review Boundary

Automated checks do not replace review of business logic, architecture, threat assumptions, authorization intent, deployment context, or other context-dependent security decisions. A PASS is not proof of zero vulnerabilities.

## Accuracy Requirement

A benchmark case requires a known expected result and an observed actual result.

A trusted reviewer may label a real PR with `securepr-expected-pass` or `securepr-expected-block`. SecurePR then reports the current PR's expected result, actual gate result, and classification in the Actions summary.

Normal PRs without an expected-outcome label are not counted as TP, FP, TN, or FN.

The permanent benchmark ledger is `docs/accuracy/benchmark-results.csv`. It is deliberately updated only after labeled cases are executed and verified; ordinary PRs must not silently mutate it.

Measurements describe the labeled corpus and configuration, not universal real-world detection accuracy.
