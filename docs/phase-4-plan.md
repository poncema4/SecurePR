# SecurePR Phase 4 — Reusable Security Gate Expansion

## Overview
Phase 4 turns the Phase 3 security gate into a reusable MVP that can be applied to the user's own repositories without being tied to the SecurePR Flask sample application.

## Objectives
- Profile repositories and determine applicable security controls.
- Support broad multi-language analysis through the analyzers available to SecurePR.
- Expand coverage around OWASP Top 10:2025 and related secure-coding principles.
- Detect high-confidence insecure or missing security controls where automation can support the conclusion.
- Normalize duplicate findings so developers receive one meaningful finding instead of repeated copies.
- Keep exactly two gate outcomes: `PASS` and `BLOCK`.
- Report measured accuracy honestly using TP, FP, TN, precision, recall, and F1.
- Reuse the gate across the user's own repositories without GitHub Marketplace packaging.

## Product Model
SecurePR is the **harness, orchestration, policy, aggregation, and reporting layer**. It does not replace specialist security engines.

- **CodeQL** performs semantic source-code analysis for supported languages.
- **Semgrep** provides complementary rule-based SAST and SecurePR-specific patterns.
- **Gitleaks** detects credential and secret material.
- **Dependency auditing** identifies known vulnerable dependencies where a supported package-manager audit is available.
- **Project security tests and correctness checks** verify behavior that static analysis cannot prove.
- **Repository profiling** identifies languages, manifests, and applicable CodeQL coverage.
- **SecurePR policy/reporting** aggregates these signals into one PASS/BLOCK decision and actionable remediation guidance.

A PASS never means that the repository is guaranteed vulnerability-free. Human review is always recommended.

## Phase 4 Scope

### 1. Broad multi-language support
SecurePR shall detect supported CodeQL languages and analyze applicable source code without assuming that the repository is Python-only. The MVP targets CodeQL-supported language families relevant to the project, including C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, and Swift.

PHP and Scala are not CodeQL-supported languages. If either is detected, SecurePR must report the coverage boundary rather than silently treating the repository as fully analyzed.

### 2. Repository-aware applicability
SecurePR shall inspect repository files and manifests to determine which checks are applicable and should avoid irrelevant dependency checks while making missing coverage visible.

Examples:
- `requirements.txt` → Python dependency audit
- `package-lock.json` → npm dependency audit
- Python source/tests → Python tests and CodeQL Python analysis
- JavaScript/TypeScript → Node project checks and CodeQL JavaScript/TypeScript analysis
- supported compiled languages → CodeQL analysis where configuration permits

### 3. Security-principle coverage
Phase 4 uses OWASP Top 10:2025 as one coverage framework and expands the existing matrix to include:

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

The controls should additionally account for common secure-coding concerns such as hard-coded usernames/passwords, secrets, unsafe deserialization, path traversal, SSRF, XSS, command injection, SQL injection, weak cryptography, disabled TLS verification, sensitive logging, error leakage, CI/CD risks, dependency risk, and unsafe workflow input where applicable.

OWASP Top 10:2025 is the current released OWASP Top 10 used by this project. The project must not claim that every category can be completely automated.

### 4. Missing security controls
SecurePR should identify high-confidence cases where a security control is clearly unsafe or absent from the changed implementation when automated evidence supports the conclusion.

Examples:
- hard-coded password or credential material → blocking finding
- hard-coded privileged username in security-sensitive source → blocking finding when matched by policy
- unsafe password handling → blocking SAST/test finding where detected
- security-sensitive authentication change without reliable automated proof → do not invent a vulnerability; automated checks still PASS/BLOCK based on actual evidence and human review remains recommended

The gate has only two outcomes: **PASS** or **BLOCK**. There is no third REVIEW state. Every PASS and BLOCK result states that human review is always recommended.

### 5. Finding aggregation
SecurePR should provide one meaningful finding per unique issue rather than bombarding developers with the same issue from multiple tools.

Identical SARIF findings are normalized using location, rule, and message. Tool names are preserved in the normalized summary so the developer can see which engines independently reported the same issue. Distinct findings at the same file and line remain distinct.

### 6. Reusable integration
SecurePR will be reusable across the user's own repositories through a reusable GitHub Actions workflow. The MVP does not require GitHub Marketplace publication.

Initial portability targets:
- SecurePR — Python
- CookieGuard — JavaScript/TypeScript/Node/Next.js
- NetDefender — the languages and security artifacts actually implemented there

The reusable workflow checks out the calling repository, profiles it, applies applicable controls, and publishes the same PASS/BLOCK gate.

## PASS/BLOCK Semantics

**PASS** means all configured blocking controls completed successfully and no blocking normalized finding remains.

**BLOCK** means at least one configured blocking control failed or a blocking normalized finding remains.

Both outcomes must state that human review is always recommended. SecurePR never automatically edits source code, rotates credentials, or merges a pull request.

## PR Versus Main Branch
A passing PR is strong evidence that the tested PR execution passed the configured gate, but it is not a guarantee that the post-merge `main` run will pass. The PR and post-merge workflows are separate executions. Phase 4 completion therefore requires a successful post-merge `main` run after the consolidated PR is merged.

## Accuracy and False-Positive / False-Negative Validation

Accuracy is a final Phase 4 validation activity, not something declared complete from individual development runs.

SecurePR shall use a controlled benchmark containing intentionally vulnerable and intentionally safe cases. Cases use synthetic credentials and isolated examples.

For each case, record the expected classification and SecurePR's actual classification.

### Confusion matrix
- **True Positive (TP):** vulnerable case correctly blocked.
- **False Positive (FP):** safe case incorrectly blocked.
- **True Negative (TN):** safe case correctly passed.
- **False Negative (FN):** vulnerable case incorrectly passed.

### Precision
`Precision = TP / (TP + FP)`

Precision answers: **When SecurePR blocks a tested case, how often is that block correct?**

### Recall
`Recall = TP / (TP + FN)`

Recall answers: **Of the known vulnerable cases in the benchmark, how many did SecurePR detect?**

### F1 score
`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

Every PR reports the current accuracy status. Until the final benchmark is executed, it reports that the benchmark is pending and does not claim an accuracy percentage. After results exist, every PR reports the latest measured TP, FP, TN, precision, recall, and F1 and identifies the benchmark scope.

The final report must present the measured results and their tested security categories. These measurements describe the tested corpus and configuration; they are not a universal guarantee of detection accuracy.

## Final Phase 4 Validation
Comprehensive validation occurs only after implementation and documentation are stable:

1. Local SecurePR verification passes.
2. Custom policy and repository-profile tests pass.
3. Reusable workflow syntax and configuration are validated.
4. The consolidated Phase 4 PR passes SecurePR.
5. The reusable workflow is exercised against SecurePR, CookieGuard, and NetDefender using their actual supported languages/artifacts.
6. Intentional synthetic vulnerabilities are blocked.
7. Corrected versions pass.
8. Safe edge cases are tested for false positives.
9. Known vulnerable cases are tested for false negatives.
10. The controlled benchmark is executed.
11. TP/FP/TN/FN, precision, recall, and F1 are calculated from actual results.
12. Documentation is audited against the implementation and measured results.
13. The one consolidated PR is merged.
14. The post-merge `main` workflow passes.
15. The Phase 4 branch is deleted after merge.

## Out of Scope for the MVP
- GitHub Marketplace publication
- Public SaaS service
- Automatic remediation
- Automatic merging
- Guaranteed detection of every vulnerability
- Full support for every programming language ever created
- Enterprise vulnerability-management features
- A generic security score that hides individual findings
