# SecurePR Security Checks

## Overview

This document is the executable security-coverage reference for SecurePR. The workflow determines which controls apply to the target repository and combines their evidence into one gate.

## Core Gate Controls

| Control | How SecurePR runs it | Gate behavior |
|---|---|---|
| Python runtime policy | Reads the repository runtime declaration and enforces the supported minimum | BLOCK on unsupported declared runtime |
| Repository profile | Detects applicable CodeQL languages and dependency manifests | BLOCK if profiling fails |
| Project tests | Runs applicable Python and JS/TS tests/type checks | BLOCK on failure |
| Gitleaks | Scans repository content/history for secrets and credential material | BLOCK on failure/finding |
| Semgrep | Runs security rules plus SecurePR-specific high-confidence rules and emits SARIF | BLOCK on failure/finding |
| Dependency audit | Runs pip-audit for Python and npm audit for npm lockfiles | BLOCK on audit failure |
| CodeQL | Analyzes detected CodeQL-supported languages with security-extended queries | BLOCK on initialization/analysis failure |
| SARIF security findings | Evaluates SARIF-producing security results | BLOCK when findings are reported |

## OWASP Top 10:2025 Coverage

OWASP Top 10:2025 is a **coverage framework**. It is not a claim that SecurePR can completely automate every category.

| Category | Automated controls | Boundary |
|---|---|---|
| A01 Broken Access Control | CodeQL, Semgrep, project tests | Authorization intent and business logic require review |
| A02 Security Misconfiguration | CodeQL, Semgrep | Deployment/environment configuration may require review |
| A03 Software Supply Chain Failures | Dependency audit, CodeQL, Semgrep | Full build/distribution trust cannot be proven by these checks |
| A04 Cryptographic Failures | CodeQL, Semgrep | Cryptographic design and context may require review |
| A05 Injection | CodeQL, Semgrep, project tests | Runtime/framework behavior can exceed static coverage |
| A06 Insecure Design | CodeQL, Semgrep, project tests | Architecture, threat model, requirements, and business logic require human review |
| A07 Authentication Failures | CodeQL, Semgrep, project tests | Correct authentication intent and operational controls require review |
| A08 Software or Data Integrity Failures | CodeQL, dependency audit, Semgrep | End-to-end artifact and data trust may require review |
| A09 Security Logging & Alerting Failures | CodeQL, Semgrep | Operational monitoring effectiveness requires review |
| A10 Mishandling of Exceptional Conditions | CodeQL, Semgrep, project tests | Complete runtime failure behavior cannot be established statically |

A category PASS means its mapped automated controls passed. It does not prove that the complete OWASP category is secure.

## SecurePR-Specific Semgrep Rules

SecurePR includes high-confidence rules for:

- hard-coded password/credential-like values
- hard-coded privileged usernames
- unsafe `eval`/`exec` use
- explicitly disabled Python TLS certificate verification

Tests and documentation are excluded from these application-source rules.

## SARIF Evidence

Semgrep and CodeQL produce machine-readable security evidence. `scripts/summarize_sarif.py` groups identical findings for detailed evidence while preserving distinct findings. Native tool output remains available for diagnosis.

## Accuracy

Every PR reports cumulative labeled benchmark metrics. A normal PR is not counted as a TP, FP, TN, or FN without ground truth.

A trusted reviewer can add `securepr-expected-pass` or `securepr-expected-block` to a real PR. The current Actions run then reports expected result, actual result, and classification correctness immediately.

The benchmark ledger is `docs/accuracy/benchmark-results.csv`. It is intentionally not modified automatically by ordinary PR runs.

## Gate Design

The authoritative workflow has one job named `SecurePR Security Gate` and exactly two outcomes: `PASS` and `BLOCK`.

SecurePR does not automatically modify source code, rotate credentials, or merge pull requests. Human review is always recommended.
