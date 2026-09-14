# SecurePR
**Reusable Pull Request Security Gate**

## Overview
SecurePR is a reusable DevSecOps PR security gate for the user's own repositories. It orchestrates security-analysis engines and project checks, aggregates their evidence, and produces one clear `PASS` or `BLOCK` decision before a pull request is merged.

## Problem
A pull request can introduce security weaknesses through source code, dependencies, secrets, configuration, CI/CD changes, or missing security controls. No single scanner can reliably cover all of those areas. SecurePR combines complementary controls and makes their coverage and limitations visible.

## Objectives
- Analyze supported programming languages with language-aware security tooling.
- Detect secrets, insecure coding patterns, vulnerable dependencies, and security-test failures.
- Check applicable OWASP Top 10:2025 and broader secure-coding principles.
- Identify high-confidence missing or unsafe security controls where automation can support the conclusion.
- Aggregate duplicate scanner findings into one meaningful result.
- Produce only `PASS` or `BLOCK` as the gate decision.
- Always recommend human security review.
- Measure false positives and false negatives with a controlled final benchmark.
- Reuse the same gate across the user's own repositories without GitHub Marketplace packaging.

## MVP Scope
- Repository and language profiling.
- CodeQL semantic SAST for supported languages.
- Semgrep SAST and SecurePR-specific security rules.
- Gitleaks secret detection.
- Applicable dependency audits.
- Applicable project security/correctness tests.
- CI/CD and workflow security analysis where practical.
- OWASP Top 10:2025 coverage mapping.
- Normalized findings and concise remediation guidance.
- PASS/BLOCK reporting with human-review guidance.
- Controlled TP/FP/TN/FN accuracy measurement at the end of Phase 4.
- Reusable GitHub Actions workflow for the user's own repositories.

## Architecture / Workflow
```text
Developer
  ↓
Pull Request
  ↓
SecurePR Security Gate
  ├── Repository / language profiling
  ├── CodeQL semantic SAST
  ├── Semgrep SAST + SecurePR rules
  ├── Gitleaks secret detection
  ├── Applicable dependency audits
  ├── Project security / correctness tests
  ├── CI/CD and configuration checks
  └── Finding normalization / policy
  ↓
One PASS / BLOCK result
  ↓
Human review is always recommended
```

SecurePR is the **harness, orchestration, policy, aggregation, and reporting layer**. CodeQL, Semgrep, Gitleaks, dependency auditing, and project tests are analysis engines or evidence sources. CodeQL performs semantic code analysis for supported languages; SecurePR does not reimplement CodeQL.

## Phase Plan

### Phase 1 — Planning & Security Design — complete
Security requirements, architecture, threat model, security coverage matrix, testing strategy, and project documentation were established.

### Phase 2 — Application & Security-Test Foundation — complete
The controlled Flask application, organized pytest suite, local setup/verification scripts, Python runtime policy, and baseline security foundation were implemented.

### Phase 3 — Automated Security Gate / DevSecOps CI — complete
A single `SecurePR Security Gate` job was implemented with runtime policy, dependency installation, security tests, Gitleaks, Semgrep, pip-audit, CodeQL, PASS/BLOCK reporting, protected `main`, and controlled vulnerable/corrected demonstrations.

### Phase 4 — Reusable Security Gate Expansion — in progress
Phase 4 turns the working gate into a reusable MVP for the user's own repositories. It includes repository/language profiling, applicable multi-language CodeQL analysis, OWASP Top 10:2025 mapping, broader security policies, missing-control indicators, normalized findings, reusable workflow integration, portability testing, and final accuracy measurement.

The detailed Phase 4 plan is in [`docs/phase-4-plan.md`](docs/phase-4-plan.md).

## Security Concepts
- Secure SDLC and shift-left security
- OWASP Top 10:2025
- SAST and semantic data-flow analysis
- Secrets and credential protection
- Authentication and authorization
- Injection, XSS, SSRF, path traversal, and unsafe deserialization
- Cryptography and TLS configuration
- Dependency and software supply-chain security
- Software/data integrity
- Security logging and error handling
- CI/CD and workflow security
- Security testing and correctness
- False-positive / false-negative measurement

## Expected Demonstration
Create a controlled vulnerable PR and a corrected PR, observe SecurePR block and pass the changes, inspect the single normalized finding summary, and then run the same reusable gate against the user's other repositories to demonstrate portability.

For the final Phase 4 benchmark, run controlled vulnerable and safe cases, record expected and actual PASS/BLOCK results, and calculate TP, FP, TN, FN, precision, recall, and F1.

## PASS/BLOCK Reporting
The gate reports:

1. Overall SecurePR result
2. Check Results
3. **Fixes to make this PASS**
4. Remediation
5. Accuracy status and boundary
6. Full Actions run link

There are exactly two gate outcomes: `PASS` and `BLOCK`. Every outcome states that human review is always recommended. A blocking result explains why the control failed, why it matters, what to fix, and the expected result after remediation.

## Accuracy
SecurePR does not claim 100% accuracy or a target percentage without measurement. Every PR run reports the status of the controlled benchmark:

- Before the final benchmark exists: **Benchmark pending — no accuracy percentage is claimed.**
- After final benchmark results are recorded: the run reports the latest measured TP, FP, TN, FN, precision, recall, and F1 and identifies the benchmark scope.

Definitions:

- **TP:** vulnerable case correctly blocked.
- **FP:** safe case incorrectly blocked.
- **TN:** safe case correctly passed.
- **FN:** vulnerable case incorrectly passed.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

These measurements describe the tested benchmark corpus and configuration. They are not a universal guarantee of vulnerability-detection accuracy.

## Reuse for the MVP
SecurePR is intended to be reused across the user's own repositories through a reusable GitHub Actions workflow. It is **not** being packaged for GitHub Marketplace during the MVP.

Initial portability targets:

- SecurePR — Python
- CookieGuard — JavaScript/TypeScript/Node/Next.js
- NetDefender — the languages and security artifacts actually implemented there

If a repository contains a language unsupported by CodeQL, SecurePR must report the coverage boundary instead of silently treating that language as analyzed.

## Security Scope and Limitations
SecurePR is an automated security gate, not a proof that software is secure. Context-dependent properties such as business logic, architecture, threat assumptions, authorization intent, and some insecure-design decisions can require human review. Human review is always recommended after a PASS or BLOCK result.

Unsupported or unavailable analysis must be visible in the gate output. SecurePR must never turn missing analysis into a silent security PASS.

## Tech Stack
| Area | Technology |
|---|---|
| Language | Python |
| Security analysis | CodeQL, Semgrep, Gitleaks |
| Dependency auditing | pip-audit, npm audit where applicable |
| CI/CD | GitHub Actions |
| Testing | pytest + repository-specific checks |
| Version Control | Git / GitHub |

## Project Structure
```text
SecurePR/
├── app/
├── security/
├── tests/
├── scripts/
│   ├── repository_profile.py
│   ├── summarize_sarif.py
│   ├── accuracy_metrics.py
│   ├── accuracy_report.py
│   ├── check_python_version.py
│   └── setup/verification scripts
├── docs/
│   ├── architecture.md
│   ├── security-requirements.md
│   ├── security-checks.md
│   ├── threat-model.md
│   ├── testing.md
│   ├── github-actions.md
│   └── phase-4-plan.md
├── .github/workflows/
│   ├── security.yml
│   └── reusable-security.yml
├── .semgrep_securepr.yml
├── .python-version
└── requirements.txt
```

## Out of Scope
- GitHub Marketplace publication
- Public SaaS hosting
- Automatic remediation
- Automatic merging
- Enterprise vulnerability management
- Guaranteed detection of every vulnerability
- Support for every programming language ever created
- Generic security scoring that hides individual findings

## Verification
Run automated verification from the repository root:

```text
python -m pytest -q
python -m compileall -q app security tests scripts
```

The final Phase 4 completion criteria also require reusable-workflow demonstrations, controlled vulnerable/safe cases, the accuracy benchmark, documentation audit, one consolidated PR, merge, and successful post-merge `main` verification.

## Documentation
- [Architecture](docs/architecture.md)
- [Security Requirements](docs/security-requirements.md)
- [Security Checks](docs/security-checks.md)
- [Threat Model](docs/threat-model.md)
- [Testing](docs/testing.md)
- [GitHub Actions](docs/github-actions.md)
- [Phase 4 Plan](docs/phase-4-plan.md)

## Status
**Phase 4 — in progress.** Implementation and documentation are being stabilized on the single consolidated Phase 4 PR. Final benchmark accuracy, cross-repository demonstrations, merge validation, and post-merge verification occur at the end of the phase.