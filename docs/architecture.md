# SecurePR Architecture

## Overview
SecurePR is a reusable pull-request **security harness**. The application being changed is the target; SecurePR is the automation that determines applicability, orchestrates multiple security engines, collects evidence, applies policy, aggregates results, and reports one gate decision.

SecurePR is not itself a replacement for CodeQL, Semgrep, Gitleaks, dependency auditors, or project tests. Those engines provide specialized security evidence under the SecurePR harness.

The Flask application in this repository is a controlled demonstration target used to validate the harness, not a requirement for using SecurePR.

## High-Level Flow
```text
Developer
   ↓
Pull Request
   ↓
SecurePR Harness
   ├── Repository / language profiling
   ├── Project tests
   ├── Gitleaks
   ├── Semgrep
   ├── Dependency audit
   └── CodeQL
            ↓
      Security Evidence / SARIF
            ↓
    SecurePR Aggregation + Policy
            ↓
       PASS / BLOCK
            ↓
       Human Review
```

## Harness Versus Analysis Engines

The separation of responsibilities is fundamental to the MVP:

| Layer | Responsibility |
|---|---|
| SecurePR harness | Workflow orchestration, applicability, policy, aggregation, reporting, and PASS/BLOCK decision |
| CodeQL | Semantic source-code and data-flow security analysis |
| Semgrep | Rule-based SAST, including SecurePR custom rules |
| Gitleaks | Secret and credential detection |
| Dependency auditors | Known vulnerability checks for supported package ecosystems |
| Project tests | Repository-specific behavior and security assertions |

SecurePR consumes these tools' evidence rather than attempting to reimplement their scanners.

## Rule Book / Policy Sources

There is no single LLM prompt that defines SecurePR security policy. The rule book is layered:

1. `.github/workflows/security.yml` is the authoritative orchestration and final gate policy.
2. `.semgrep_securepr.yml` contains SecurePR-specific Semgrep rules.
3. Semgrep `p/security-audit` supplies broader SAST coverage.
4. CodeQL `security-extended` supplies semantic security queries for detected supported languages.
5. Gitleaks supplies secret-detection evidence.
6. `pip-audit` and `npm audit` supply supported dependency vulnerability evidence.
7. Target-repository tests supply application-specific evidence.
8. `repository_profile.py` determines which language and dependency controls apply.
9. `summarize_sarif.py` aggregates SARIF findings for SecurePR reporting.

The detailed control inventory is maintained in `docs/security-checks.md`.

## CodeQL

The workflow initializes CodeQL only when `repository_profile.py` detects a supported CodeQL language. It requests the `security-extended` query suite. CodeQL builds an analysis representation of the supported source code and runs security queries; SecurePR then consumes the resulting evidence as one layer of the gate.

## Semgrep

Semgrep runs both its `p/security-audit` configuration and `.semgrep_securepr.yml`. The custom SecurePR rules provide high-confidence checks for selected credential, privileged-identity, dynamic-evaluation, and Python TLS patterns. The hard-coded credential policy uses a raw-text regex rule for non-Python files and a Python AST-based assignment rule for Python files, closing the validated gap exposed by PR #64.

## Gitleaks

Gitleaks is the dedicated secret-detection engine. SecurePR treats a failing Gitleaks control or detected secret as blocking evidence according to the workflow policy.

## Dependency Analysis

Dependency auditing is applicability-driven. `pip-audit` runs when `requirements.txt` is present, and `npm audit` runs when `package-lock.json` is present. SecurePR does not pretend that a dependency ecosystem exists when its manifest is absent.

## Repository Profiling

`scripts/repository_profile.py` detects CodeQL-supported languages and common package manifests while reporting known CodeQL coverage boundaries such as PHP and Scala.

The profile is used to avoid treating an unsupported language as successfully analyzed. Unsupported source extensions produce an explicit coverage boundary.

## Finding Aggregation

Semgrep and CodeQL produce SARIF evidence. `scripts/summarize_sarif.py` scans SARIF recursively and groups identical findings by artifact location, start line, rule ID, and message. Tool name is excluded from the identity key so duplicate reports can be consolidated while distinct findings remain visible.

Native tool logs remain available for diagnosis.

## OWASP Top 10:2025 Coverage

OWASP Top 10:2025 is used as a coverage framework. SecurePR maps the automated controls that actually run to applicable categories rather than implementing ten separate scanners.

A category PASS means the mapped automated controls passed; it does not prove the complete OWASP category is secure. Context-dependent risks, including insecure design, business logic, authorization intent, and architecture, retain a human-review boundary.

## Security Decision

Only two outcomes are allowed:

- **PASS:** all configured blocking controls pass and no blocking security finding remains.
- **BLOCK:** a configured blocking control fails or a blocking security finding remains.

There is no third `REVIEW` state. Both outcomes state that human review is recommended.

## Accuracy

The benchmark is a reviewed ground-truth corpus. The current 37-case corpus contains 15 TP, 0 FP, 16 TN, and 6 FN, producing 83.78% conventional classification accuracy, 100% precision, 71.43% recall, and 83.33% F1. These measurements describe the controlled corpus and configuration only.

## Trust Boundaries

1. Developer-controlled pull-request changes enter the CI environment.
2. Pull-request source code interacts with GitHub Actions.
3. External dependency metadata and package installation influence analysis.
4. Third-party actions and security tools are part of the CI supply chain.
5. Tool output becomes input to SecurePR's final decision.
6. A reusable workflow must explicitly identify which repository is being analyzed.
7. SecurePR tooling should be pinned to an intentional ref so a target repository does not silently analyze itself with unrelated tooling state.

## PR and Main Verification

A passing PR is not a guarantee that the post-merge `main` execution will pass. The PR and push-to-main workflows are separate executions. Final verification therefore requires both a passing PR and a successful post-merge `main` run.

## Reuse Boundary

SecurePR is reusable across repositories you control through `.github/workflows/reusable-security.yml`. The target repository supplies its own source code, manifests, and project tests; SecurePR supplies the security-gate harness and policy. The MVP is not packaged for GitHub Marketplace.
