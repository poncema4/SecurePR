# SecurePR

## Secure Pull Request Security Gate

SecurePR is a reusable DevSecOps PR security gate. It orchestrates multiple security-analysis engines and project checks, aggregates their results, and produces one clear `PASS` or `BLOCK` decision before a pull request is merged.

The Phase 2 Flask application remains a controlled sample target. It is not the product boundary: Phase 4 makes the gate repository-aware and broadly multi-language for the user's own repositories.

SecurePR does not claim complete vulnerability detection. Different security concerns require different controls, and design/business-logic issues can still require human review.

## Architecture

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
   ├── Project security/correctness tests
   └── Normalized finding aggregation
   ↓
One PASS / BLOCK result
   ↓
Human review is always recommended
```

SecurePR is the **harness/orchestration and policy layer**. CodeQL, Semgrep, Gitleaks, dependency auditing, and project tests are the analysis engines and evidence sources.

## Phase Plan

### Phase 1 — Planning & Security Design — complete

Security requirements, architecture, threat model, security coverage matrix, testing strategy, and project documentation were established.

### Phase 2 — Application & Security-Test Foundation — complete

The controlled Flask application, organized pytest suite, local setup/verification scripts, Python runtime policy, and baseline security foundation were implemented.

### Phase 3 — Automated Security Gate / DevSecOps CI — complete

A single `SecurePR Security Gate` job was implemented with Python runtime policy, dependency installation, security tests, Gitleaks, Semgrep, pip-audit, CodeQL, PASS/BLOCK reporting, protected `main`, and controlled vulnerable/corrected demonstrations.

### Phase 4 — Reusable Multi-Language MVP — in progress

Phase 4 expands SecurePR from a working Python-focused gate into a reusable MVP for the user's own repositories. The phase includes repository/language profiling, broad CodeQL-supported language coverage, OWASP Top 10:2025 mapping, additional security policies, missing-control indicators, normalized findings, reusable workflow integration, portability testing, and final accuracy measurement.

The complete Phase 4 plan is in [`docs/phase-4-mvp.md`](docs/phase-4-mvp.md).

## Security Coverage

SecurePR uses OWASP Top 10:2025 as one coverage framework and also addresses common secure-coding and DevSecOps concerns such as secrets, injection, authentication, authorization, cryptography, dependency/supply-chain risk, configuration, CI/CD security, unsafe deserialization, path traversal, SSRF, XSS, sensitive logging, error leakage, and exceptional-condition handling where applicable.

The project does **not** claim that every OWASP category can be completely automated. SecurePR must report coverage boundaries instead of silently treating unsupported or context-dependent areas as secure.

## PASS/BLOCK reporting

The gate reports:

1. Overall SecurePR result
2. Check Results
3. **Fixes to make this PASS**
4. Remediation
5. Accuracy boundary
6. Full Actions run link

There are only two gate outcomes: `PASS` and `BLOCK`. Every outcome states that human review is always recommended.

A blocking result explains why the control failed, why it matters, what the developer should fix, and the expected result after remediation. SecurePR never automatically edits source code, rotates credentials, or merges a pull request.

## Accuracy

SecurePR does not claim 100% accuracy. Phase 4 includes a controlled benchmark of vulnerable and safe cases that will be executed at the **end of the phase**, after implementation and documentation stabilize.

The benchmark records:

- **TP:** vulnerable case correctly blocked
- **FP:** safe case incorrectly blocked
- **TN:** safe case correctly passed
- **FN:** vulnerable case incorrectly passed

Precision: `TP / (TP + FP)`

Recall: `TP / (TP + FN)`

F1: `2 × (Precision × Recall) / (Precision + Recall)`

The final report will present the measured results and their tested security categories. These measurements describe the benchmark corpus; they are not a universal guarantee of detection accuracy.

## Reuse for the MVP

SecurePR is intended to be reusable across the user's own repositories through a reusable GitHub Actions workflow. It is **not** being packaged for GitHub Marketplace during the MVP.

The intended portability targets are:

- SecurePR — Python
- CookieGuard — JavaScript/TypeScript/Node/Next.js
- NetDefender — the languages and security artifacts actually implemented there

The reusable workflow profiles the calling repository and applies the controls that are applicable to it.

## Local Setup and Verification

### Linux or macOS (Bash)

```bash
chmod +x scripts/setup.sh scripts/verify.sh
./scripts/setup.sh
./scripts/verify.sh
```

### Windows (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
.\scripts\verify.ps1
```

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
│   ├── check_python_version.py
│   └── setup/verification scripts
├── docs/
│   ├── architecture.md
│   ├── security-requirements.md
│   ├── security-checks.md
│   ├── threat-model.md
│   ├── testing.md
│   └── phase-4-mvp.md
├── .github/workflows/
│   ├── security.yml
│   └── reusable-security.yml
├── .semgrep_securepr.yml
├── .python-version
└── requirements.txt
```

## Out of Scope for the MVP

- GitHub Marketplace publication
- Public SaaS hosting
- Automatic remediation
- Automatic merging
- Enterprise vulnerability-management features
- Guaranteed detection of every vulnerability
- Support for every programming language ever created
- Generic security scoring that hides individual findings

## Status

**Phase 4 — in progress.** The implementation is being expanded into the reusable multi-language MVP. Final accuracy benchmarking, cross-repository demonstrations, consolidated PR validation, merge verification, and final documentation sign-off occur at the end of the phase.
