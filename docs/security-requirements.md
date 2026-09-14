# SecurePR Security Requirements

## Overview

SecurePR is a reusable pull-request **security harness**. It evaluates pull-request changes through layered controls supplied by multiple security engines and the target repository, then applies a common policy to produce one `PASS` or `BLOCK` result.

These requirements define the automated coverage and gate behavior. They do not claim that automation can prove every security property.

## Core Requirements

SecurePR shall:

1. Orchestrate repeatable pull-request security checks before merge.
2. Use multiple complementary security engines rather than relying on one scanner.
3. Detect exposed secrets and credential-like material through dedicated secret detection and applicable SAST controls.
4. Analyze supported programming languages with applicable SAST tooling, including CodeQL and Semgrep.
5. Audit supported dependency ecosystems when a relevant manifest exists.
6. Run applicable project security and correctness tests.
7. Analyze security-relevant CI/CD configuration where practical.
8. Map implemented automated coverage to OWASP Top 10:2025 as a coverage framework.
9. Enforce SecurePR-specific high-confidence Semgrep rules for selected credential, privileged-identity, dynamic-evaluation, and TLS patterns.
10. Aggregate duplicate scanner findings without hiding distinct findings in detailed evidence.
11. Produce exactly one overall `PASS` or `BLOCK` decision.
12. Explain blocking results and remediation steps.
13. Always recommend human review.
14. Never automatically modify source code, rotate credentials, dismiss findings, or merge a pull request.
15. Report unsupported or unavailable analysis coverage instead of silently treating it as secure.
16. Remain reusable without requiring GitHub Marketplace publication.
17. Measure gate behavior with TP, FP, TN, precision, recall, and F1 from labeled cases.
18. Report cumulative benchmark status on every PR and, when a trusted expected-outcome label is present, report the current PR's expected-versus-actual classification immediately.

## Rule Book / Policy Sources

The SecurePR policy is layered rather than represented by one prompt:

- `.github/workflows/security.yml` — authoritative orchestration and final PASS/BLOCK policy.
- `.semgrep_securepr.yml` — SecurePR-specific Semgrep rules.
- Semgrep `p/security-audit` — broader SAST rules.
- CodeQL `security-extended` — semantic/data-flow security queries.
- Gitleaks — secret-detection evidence.
- `pip-audit` / `npm audit` — dependency vulnerability evidence when applicable.
- Target repository tests — application-specific security/correctness evidence.
- `repository_profile.py` — applicability and language/dependency detection.
- `summarize_sarif.py` — scanner-evidence aggregation.

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

SecurePR maps the automated controls that actually run to these categories. OWASP is not a separate scanner, and a mapped PASS does not prove the complete category is secure.

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

The current reviewed benchmark contains 37 cases: 15 TP, 0 FP, 16 TN, and 6 FN. This produces 83.78% conventional classification accuracy, 100% precision, 71.43% recall, and 83.33% F1 for the controlled corpus.

PR #63 / Actions run #202 is the latest labeled PASS case. PR #64 / Actions run #203 is the latest labeled BLOCK case but returned PASS, so it is recorded as a false negative. The follow-up fix adds a Python AST-based credential assignment rule and is validated independently before merge.

Normal PRs without an expected-outcome label are not counted as TP, FP, TN, or FN. Measurements describe the labeled corpus and configuration, not universal real-world detection accuracy.
