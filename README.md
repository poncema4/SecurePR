# SecurePR

## Secure Pull Request Security Gate

SecurePR is a DevSecOps proof of concept that places repeatable security checks into a pull-request workflow for a small Python application. The goal is to demonstrate how security requirements can be translated into automated controls and a clear `PASS` or `BLOCK` decision before code is merged.

SecurePR is not intended to claim complete vulnerability detection. Different security concerns require different controls, and some issues still require tests, threat modeling, or human review.

## Problem

Security issues can enter software through source-code changes, exposed credentials, vulnerable dependencies, insecure configuration, weak cryptography, unsafe CI/CD workflows, and application behavior that static analysis cannot fully understand. SecurePR focuses on detecting a practical set of these issues early in the pull-request process.

## Architecture

```text
Developer
   ↓
Pull Request
   ↓
GitHub Actions
   ├── SAST
   ├── Secret Detection
   ├── Dependency Checks
   ├── Security Tests
   └── Workflow / Configuration Checks
   ↓
Security Gate
   ↓
PASS / BLOCK
```

The sample application is intentionally small so the project can focus on demonstrating security controls rather than building a large product. The checks remain separated enough to be reused with another compatible repository later.

## Phase 2 Baseline

The initial implementation now contains:

- A small Flask sample application
- Password-hash-based authentication logic
- Login, user-profile, and input-validation endpoints
- Pytest security and behavior tests
- A local verification script
- GitHub Actions orchestration for the baseline security gate
- CodeQL SAST
- Semgrep SAST
- Gitleaks secret detection
- pip-audit dependency auditing

This baseline is intentionally clean. Vulnerable changes will be introduced later through test pull requests so the gate can be evaluated without permanently placing intentionally vulnerable code on `main`.

## Security Coverage

The planned coverage includes:

- Exposed API keys, tokens, passwords, private keys, and other secrets
- SQL injection and other applicable injection flaws
- Unsafe command execution
- Path traversal
- Unsafe deserialization
- SSRF and XSS where the sample application provides a meaningful test surface
- Authentication and authorization weaknesses through tests and applicable static analysis
- Weak or unsafe cryptographic practices
- Disabled TLS verification and related insecure configurations
- Known vulnerable dependencies and dependency changes
- GitHub Actions permissions and unsafe workflow input handling
- Debug and insecure configuration
- Sensitive logging and error-information disclosure
- Fail-open and data-integrity issues
- Container configuration issues if Docker remains part of the implementation
- Security-design and business-logic issues through threat modeling and human review

The project will only claim coverage that is demonstrated by the implemented controls and tests.

## Security Controls

| Area | Control |
|---|---|
| SAST | CodeQL |
| Additional SAST | Semgrep |
| Secrets | Gitleaks |
| Python dependencies | pip-audit |
| Dependency changes | GitHub Dependency Review where supported |
| Security behavior | pytest |
| Workflow security | Dedicated workflow checks and review |
| CI orchestration | GitHub Actions |
| Application | Python / Flask |
| Optional container support | Docker |

## Expected Demonstration

The completed project will demonstrate a clean baseline, an intentionally vulnerable pull request that is detected and blocked, and a corrected pull request that passes the required security controls.

Demonstration credentials and secrets will be synthetic and non-sensitive.

## Project Structure

```text
SecurePR/
├── app/
│   ├── __init__.py
│   └── app.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── scripts/
│   └── verify.sh
├── docs/
│   ├── architecture.md
│   ├── security-requirements.md
│   ├── threat-model.md
│   ├── security-checks.md
│   └── testing.md
├── evidence/
│   └── verified results
├── .github/
│   └── workflows/
│       └── security.yml
├── requirements.txt
├── README.md
└── .gitignore
```

## Security Concepts

- Secure SDLC
- Security requirements
- STRIDE threat modeling
- Secure coding
- Static Application Security Testing (SAST)
- Secret management
- Dependency and software-supply-chain security
- Security testing
- CI/CD security
- DevSecOps and shift-left security

## Out of Scope

- Enterprise-scale security platforms
- Large numbers of scanner integrations
- Full vulnerability-management systems
- Support for every programming language
- Production deployment
- Advanced ML-based vulnerability detection
- Generic security scoring

## Future Enhancements

- DAST with OWASP ZAP
- Fuzz testing
- Container image scanning
- SBOM generation and analysis
- More project-specific security rules
- Detailed pull-request security reporting

## Status

**Phase 2 — baseline implementation.** The sample application, baseline tests, and first automated security checks are now in the repository. The next work is to execute and validate the baseline, fix any real failures, and then build the vulnerable-PR/BLOCK and corrected-PR/PASS demonstrations.
