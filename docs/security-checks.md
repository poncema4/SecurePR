# SecurePR Security Checks

## Overview

This document is the executable security-coverage and policy reference for the SecurePR MVP.

**SecurePR is the security harness. It is not a standalone scanner and it is not an LLM prompt.** SecurePR orchestrates multiple specialist security engines and project checks, collects their evidence, applies the gate policy, aggregates results, and publishes one `PASS` or `BLOCK` decision.

The primary policy implementation is `.github/workflows/security.yml`. The custom SecurePR Semgrep rules are in `.semgrep_securepr.yml`. The underlying engines provide the security evidence; SecurePR does not reimplement those engines.

## Security Decision Rule Book

```text
Pull Request
    ↓
Repository Profile / Applicability
    ↓
Project Tests + Dependency Audits
    ↓
Gitleaks + Semgrep + CodeQL
    ↓
SARIF / Tool Results
    ↓
SecurePR Aggregation + Policy
    ↓
PASS or BLOCK
```

A configured blocking control failure or a blocking security finding produces `BLOCK`. If all applicable blocking controls succeed and no blocking finding remains, the result is `PASS`.

There is no third `REVIEW` gate state. Human review is recommended for both outcomes.

## Core Gate Controls

| Control | Underlying engine / implementation | How SecurePR uses it | Gate behavior |
|---|---|---|---|
| Python runtime policy | SecurePR Python policy script | Checks the declared Python runtime against the supported minimum | BLOCK on unsupported declared runtime |
| Repository profile | SecurePR `repository_profile.py` | Detects applicable languages and dependency manifests | BLOCK if profiling fails; unsupported language boundaries are reported |
| Project tests | Target repository test suite | Exercises behavior that static analysis cannot fully prove | BLOCK on failure |
| Gitleaks | Gitleaks | Detects secrets, credentials, tokens, and other secret material | BLOCK on failure/finding |
| Semgrep | Semgrep `p/security-audit` + SecurePR custom rules | Performs rule-based SAST and high-confidence SecurePR-specific checks | BLOCK on failure/finding |
| Dependency audit | `pip-audit`, `npm audit` | Checks supported dependency ecosystems when their manifests are present | BLOCK on audit failure |
| CodeQL | GitHub CodeQL `security-extended` | Performs semantic/data-flow security analysis for detected CodeQL-supported languages | BLOCK on initialization/analysis failure |
| SARIF evaluation | SecurePR `summarize_sarif.py` | Aggregates SARIF security findings from scanner output | BLOCK when findings are reported |
| OWASP category mapping | SecurePR `owasp_report.py` | Assigns individual SARIF findings to only the OWASP categories supported by their rule/CWE evidence | Category BLOCK only when a mapped finding exists |

## SecurePR Custom Rules

`.semgrep_securepr.yml` is the main source of SecurePR-specific Semgrep policy. The current MVP includes high-confidence rules for:

- hard-coded password/credential-like literal values
- hard-coded privileged usernames such as `admin`, `root`, and `administrator`
- unsafe dynamic `eval` / `exec` use
- explicitly disabled Python TLS certificate verification such as `verify = False`

The hard-coded credential policy uses Semgrep's raw `regex` language for non-Python source files and a Python AST-based assignment rule for Python files. The Python rule is constrained to credential-like variable names and string literals of at least eight characters. This two-path design closes the validated manual false negative from PR #64 while preserving the raw-text coverage for non-Python files.

The PR #64 regression was a synthetic `password = "demo_password"` assignment that returned PASS even though the expected outcome was BLOCK. It is retained in the benchmark as an FN. PR #65 added the Python AST rule and validated the regression before merge; PR #67 then demonstrated the corrected BLOCK behavior and the subsequent PASS after the hardcoded password was removed.

Tests, documentation, and SecurePR tooling are excluded from these application-source rules where configured by the workflow.

These custom rules supplement, rather than replace, Semgrep's broader `p/security-audit` rules.

## CodeQL

CodeQL is an underlying semantic security-analysis engine. SecurePR does not define all CodeQL queries itself. The workflow initializes CodeQL for languages detected by `repository_profile.py` and requests the `security-extended` query suite.

CodeQL analyzes supported source code and can identify security properties involving program structure and data flow. Its findings become part of SecurePR's evidence and gate evaluation while native CodeQL evidence remains available for diagnosis.

## Semgrep

Semgrep is a complementary rule-based SAST engine. SecurePR runs both:

1. Semgrep's `p/security-audit` rules.
2. SecurePR's `.semgrep_securepr.yml` custom rules.

A Semgrep failure or reported security finding contributes to the final `BLOCK` decision. A Semgrep result does **not** by itself block all OWASP categories; the OWASP table uses finding-level category mapping.

## Gitleaks

Gitleaks is the dedicated secret-detection engine. It provides detection for credential and secret patterns that are different from general source-code SAST. SecurePR consumes the tool's result; it does not attempt to replace Gitleaks with a generic regular expression.

## Dependency Analysis

Dependency auditing is ecosystem-specific. The MVP runs `pip-audit` when `requirements.txt` is present and `npm audit` when `package-lock.json` is present. A repository without a currently supported dependency manifest does not fail merely because no dependency ecosystem applies.

## Repository Profiling and Language Applicability

`scripts/repository_profile.py` determines which CodeQL-supported languages and dependency manifests apply to the target repository. Supported CodeQL language families include C/C++, C#, Go, Java/Kotlin, JavaScript/TypeScript, Python, Ruby, Rust, and Swift.

PHP and Scala are explicit CodeQL coverage boundaries in this MVP. Unsupported source extensions are reported rather than silently treated as successfully analyzed.

## SARIF Evidence and Aggregation

Semgrep and CodeQL produce machine-readable SARIF evidence. `scripts/summarize_sarif.py` scans SARIF recursively and groups identical findings using artifact location, start line, rule ID, and message. Tool name is not used as the identity key, so duplicate reports from different engines can be consolidated while distinct findings at the same location remain separate.

Native tool output remains available for diagnosis.

## OWASP Top 10:2025 Coverage

OWASP Top 10:2025 is a **coverage framework**, not a separate SecurePR scanner. SecurePR now separates the **overall gate decision** from the **category result table**.

The overall gate remains unchanged:

- `BLOCK` when any required blocking control fails or a blocking security finding remains.
- `PASS` when all required blocking controls pass and no blocking security finding remains.

The OWASP table is finding-driven:

1. Each SARIF finding is inspected for an explicit OWASP tag, an OWASP-mapped CWE, or a SecurePR custom rule with a documented category mapping.
2. SecurePR custom rule IDs are normalized to their final rule component so SARIF IDs such as `securepr-tooling.securepr-python-hardcoded-credential` still match the documented SecurePR rule mapping.
3. A category is `BLOCK` only if one or more findings map to that category.
4. A category is `PASS` when no mapped finding exists for that category in the run.
5. An unmapped finding still affects the overall SecurePR gate but is not assigned to an OWASP category without sufficient evidence.

This prevents the previous behavior where a single failed Semgrep control caused all ten rows to show `BLOCK`. For example, a hardcoded credential maps to A04/A07, while an unsafe `eval` finding maps to A05; neither should make unrelated categories red merely because Semgrep failed.

| Category | Automated evidence mapping | Boundary |
|---|---|---|
| A01 Broken Access Control | OWASP/CWE mapping plus access-control-related SecurePR rules | Authorization intent and business logic require review |
| A02 Security Misconfiguration | OWASP/CWE mapping plus configuration/TLS SecurePR rules | Deployment/environment configuration may require review |
| A03 Software Supply Chain Failures | OWASP/CWE mapping for dependency/supply-chain findings | Dependency audit results remain part of the overall gate; full build/distribution trust cannot be proven by these checks |
| A04 Cryptographic Failures | OWASP/CWE mapping plus credential/TLS SecurePR rules | Cryptographic design and context may require review |
| A05 Injection | OWASP/CWE mapping plus unsafe-evaluation SecurePR rule | Runtime/framework behavior can exceed static coverage |
| A06 Insecure Design | Explicitly mapped findings only; absence of a finding is not proof of secure design | Architecture, requirements, threat assumptions, and business logic require review |
| A07 Authentication Failures | OWASP/CWE mapping plus credential/privileged-identity SecurePR rules | Correct authentication intent and operational controls require review |
| A08 Software or Data Integrity Failures | OWASP/CWE mapping for integrity/deserialization/trusted-source findings | End-to-end artifact and data trust may require review |
| A09 Security Logging & Alerting Failures | OWASP/CWE mapping for logging/alerting findings | Operational monitoring effectiveness requires review |
| A10 Mishandling of Exceptional Conditions | OWASP/CWE mapping for error handling/failing-open findings | Complete runtime failure behavior cannot be established statically |

A mapped category `PASS` means **no mapped automated finding was reported in that run**. It does not prove the entire OWASP category is secure. Human review remains required.

## Accuracy

The controlled benchmark is a reviewed ground-truth corpus in `docs/accuracy/benchmark-results.csv`. It currently contains 37 labeled cases: 15 TP, 0 FP, 16 TN, and 6 FN. That corresponds to 83.78% conventional classification accuracy, 100% precision, 71.43% recall, and 83.33% F1 for this controlled corpus.

PR #63 / Actions run #202 is the latest PASS benchmark case in the committed CSV. PR #64 / Actions run #203 is recorded as an FN because the observed gate result was PASS. PR #65 added the Python credential-detection fix, and PR #67 subsequently validated the corrected hardcoded-password behavior. The OWASP reporting change does not alter the 37-case CSV because it changes category presentation, not the observed overall gate outcomes.

These measurements describe the benchmark and its configuration only. They are not universal real-world accuracy claims. The six false negatives should be treated as evidence of the current benchmark's detection boundaries, not as permission to weaken precision merely to improve a metric.

## Gate Design

The authoritative workflow has one job named `SecurePR Security Gate` and exactly two gate outcomes: `PASS` and `BLOCK`.

SecurePR never automatically modifies source code, rotates credentials, dismisses findings, or merges pull requests. Human review is always recommended.
