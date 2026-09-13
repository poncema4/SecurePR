# SecurePR Phase 4 — Reusable Multi-Language MVP

## 1. Objective

Phase 4 turns the Phase 3 security gate into a reusable MVP that can be applied to Marco's own repositories without being tied to the SecurePR Flask sample application.

The MVP remains a GitHub Actions PR security gate rather than a public marketplace product. Public marketplace publication, external SaaS hosting, and enterprise-scale deployment are outside this phase and may be discussed as future work in the report and presentation.

## 2. Product Model

SecurePR is the **harness, orchestration, policy, aggregation, and reporting layer**. It does not replace specialist security engines.

- **CodeQL** performs semantic source-code analysis and data-flow-oriented security analysis for supported languages.
- **Semgrep** provides complementary rule-based SAST and SecurePR-specific patterns.
- **Gitleaks** detects credential and secret material.
- **Dependency auditing** identifies known vulnerable dependencies where a supported package-manager audit is available.
- **Project security tests and correctness checks** verify behavior that static analysis cannot prove.
- **Repository profiling** identifies languages, manifests, and applicable CodeQL coverage.
- **SecurePR policy/reporting** aggregates these signals into one PASS/BLOCK decision and actionable remediation guidance.

A PASS never means that the repository is guaranteed vulnerability-free. Human review is always recommended.

## 3. Phase 4 Scope

### 3.1 Broad multi-language support

SecurePR shall detect supported CodeQL languages and analyze applicable source code without assuming that the repository is Python-only. The Phase 4 MVP targets the CodeQL-supported language families relevant to the project, including C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, and Swift.

PHP and Scala are not treated as CodeQL-supported languages. If either is detected, SecurePR must report the coverage boundary rather than silently treating the repository as fully analyzed.

### 3.2 Repository-aware applicability

SecurePR shall inspect repository files and manifests to determine which checks are applicable. It should avoid running irrelevant dependency checks while still making missing coverage visible.

Examples:

- `requirements.txt` → Python dependency audit
- `package-lock.json` → npm dependency audit
- Python source/tests → Python tests and CodeQL Python analysis
- JavaScript/TypeScript → Node project checks and CodeQL JavaScript/TypeScript analysis
- supported compiled languages → CodeQL language analysis where configuration permits

### 3.3 Security-principle coverage

Phase 4 shall expand coverage around OWASP Top 10:2025 and related secure-software-development principles. The project must not claim that automated tooling can fully prove every category.

The coverage model includes:

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

### 3.4 Missing security controls

SecurePR should identify high-confidence cases where a security control is clearly unsafe or absent from the changed implementation when automated evidence supports the conclusion. It must distinguish these from context-dependent design questions.

Examples include:

- hard-coded password or credential material → blocking finding
- hard-coded privileged username in security-sensitive source → blocking finding when matched by the policy
- unsafe password handling → blocking SAST/test finding where detected
- security-sensitive authentication change with no reliable automated proof → remain within the human-review boundary rather than inventing a vulnerability

The final gate has only two outcomes: **PASS** or **BLOCK**. There is no third REVIEW state. PASS and BLOCK remediation text always states that human review is recommended.

### 3.5 Finding aggregation

SecurePR should provide one meaningful finding per unique issue rather than bombarding developers with the same issue from multiple tools.

Where multiple SARIF-producing tools identify the same location/rule/message, SecurePR normalizes the results so the summary can present one finding while preserving each tool's detailed output in its native log.

The aggregation layer must not hide distinct findings merely because they occur in the same file.

### 3.6 Reusable integration for the MVP

SecurePR will be reusable across the user's own repositories through a reusable GitHub Actions workflow. The MVP does not require GitHub Marketplace publication.

The reusable workflow runs against the calling repository, profiles that repository, invokes the applicable security controls, and produces the same single `SecurePR Security Gate` decision.

The initial portability demonstrations should target:

- SecurePR itself — Python
- CookieGuard — JavaScript/TypeScript/Node/Next.js
- NetDefender — the languages and security artifacts actually implemented in that repository

A small additional supported-language fixture may be used if needed to demonstrate multi-language behavior without changing the project scope.

## 4. PASS/BLOCK Semantics

**PASS** means all configured blocking controls completed successfully and no blocking normalized finding remains.

**BLOCK** means at least one configured blocking control failed or a blocking normalized finding remains.

Both outcomes must state that human review is always recommended. SecurePR never automatically edits source code, rotates credentials, or merges a pull request.

## 5. PR Versus Main Branch

A passing PR is strong evidence that the tested PR commit passed the configured gate, but it is not a guarantee that the post-merge `main` run will pass.

The PR and post-merge workflows are separate executions. A merge can change the commit context, dependency state, generated files, workflow behavior, or other conditions. Therefore, Phase 4 completion requires a successful post-merge `main` run after the consolidated Phase 4 PR is merged.

## 6. Accuracy and False-Positive / False-Negative Validation

Accuracy is a final Phase 4 validation activity, not something that will be declared complete from individual development runs.

SecurePR shall use a controlled security benchmark containing intentionally vulnerable and intentionally safe cases. Cases must use synthetic credentials and safe, isolated examples.

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

The final report shall present TP, FP, TN, FN, precision, recall, and F1 for the benchmark and identify the tested security categories. The project must not claim universal accuracy from this benchmark. The results describe the tested corpus and configuration.

## 7. Final Phase 4 Validation

Thorough end-of-phase validation shall occur only after implementation and documentation are stable.

The final validation checklist is:

1. Local SecurePR verification passes.
2. Custom policy and repository-profile tests pass.
3. Reusable workflow syntax and configuration are validated.
4. SecurePR PR gate passes on the consolidated Phase 4 PR.
5. The same reusable workflow is exercised against the intended supported repositories.
6. Intentional synthetic vulnerabilities are blocked.
7. Corrected versions pass.
8. Safe edge cases do not create unacceptable false positives.
9. The controlled benchmark is executed.
10. TP/FP/TN/FN, precision, recall, and F1 are calculated from actual results.
11. Documentation matches the implementation and measured results.
12. The Phase 4 PR is merged.
13. The post-merge `main` workflow passes.
14. The Phase 4 branch is deleted after merge.

## 8. Out of Scope for the MVP

- GitHub Marketplace publication
- Public SaaS service
- Automatic remediation
- Automatic merging
- Guaranteed detection of every vulnerability
- Full support for every programming language ever created
- Enterprise vulnerability-management features
- A generic security score that hides individual findings

These can be discussed as future work without expanding the MVP implementation.
