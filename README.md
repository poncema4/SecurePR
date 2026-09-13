# SecurePR

## Secure Pull Request Security Gate

SecurePR is a DevSecOps proof of concept that places repeatable security checks into a pull-request workflow for a small Python application. The goal is to demonstrate how security requirements are translated into automated controls and a clear security-gate decision before code is merged.

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
   ├── Security Tests
   ├── Secret Detection (Gitleaks)
   ├── Semgrep SAST
   ├── Dependency Audit (pip-audit)
   └── CodeQL SAST
   ↓
Security Gate
   ↓
PASS / BLOCK
```

The sample application is intentionally small so the project can focus on demonstrating security controls rather than building a large product. The checks remain separated enough to be reused with another compatible repository later.

## Phase 2 Progress

### Completed baseline

The repository currently contains:

- A small Flask sample application
- Password-hash-based authentication logic using Werkzeug
- Login, user-profile, and input-validation endpoints
- Pytest security and behavior tests
- Cross-platform local setup and verification scripts
- GitHub Actions security workflow
- CodeQL SAST
- Semgrep SAST
- Gitleaks secret detection
- pip-audit dependency auditing
- Python compilation verification

The dependency baseline was also corrected after CI identified a known vulnerability in the earlier pytest 8.4.2 resolution. `requirements.txt` now requires `pytest>=9.0.3,<10`.

### Verified CI baseline

The latest baseline workflow run on `main` completed successfully. The five current jobs all passed:

- Security Tests — passed
- Secret Detection — passed
- Semgrep SAST — passed
- Dependency Audit — passed
- CodeQL — passed

This verifies the clean baseline. It does **not** yet prove that SecurePR can detect and block an intentionally vulnerable pull request; that is the next demonstration stage.

## Local Setup and Verification

### Linux or macOS (Bash)

```bash
chmod +x scripts/setup.sh scripts/verify.sh
./scripts/setup.sh
./scripts/verify.sh
```

The setup script creates `.venv` and installs the dependency ranges from `requirements.txt`. The verification script automatically uses that virtual environment when it exists.

### Windows (PowerShell)

If PowerShell's execution policy prevents local scripts from running, allow scripts for the current PowerShell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run:

```powershell
.\scripts\setup.ps1
.\scripts\verify.ps1
```

The PowerShell setup script creates `.venv` and installs the project dependencies. The verification script uses the local virtual environment automatically when it exists.

## What You Can Test Now

From a clean checkout of `main`, the first local test should establish the same clean baseline that CI uses.

### 1. Run the local application tests

Linux/macOS:

```bash
./scripts/verify.sh
```

Windows PowerShell:

```powershell
.\scripts\verify.ps1
```

You should see pytest complete successfully followed by Python compilation completing without errors. Do not treat an expected result as evidence until you have actually run it locally.

### 2. Inspect the GitHub Actions baseline

Open the Actions page for the repository and inspect the latest `SecurePR Security Gate` run. The current baseline should show all five jobs passing.

### 3. Do not modify `main` with a vulnerable example yet

The clean baseline is intentionally kept safe. The next stage will create a separate demonstration branch and pull request containing a controlled, synthetic vulnerability. That PR will be used to verify that the expected scanner actually detects the issue and that the security gate fails for the right reason.

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

| Area | Control | Current Phase 2 status |
|---|---|---|
| SAST | CodeQL | Baseline verified |
| Additional SAST | Semgrep | Baseline verified |
| Secrets | Gitleaks | Baseline verified |
| Python dependencies | pip-audit | Baseline verified |
| Dependency changes | GitHub Dependency Review where supported | Planned/conditional |
| Security behavior | pytest | Baseline verified |
| Workflow security | Workflow permissions and review | Baseline implemented; targeted validation next |
| CI orchestration | GitHub Actions | Baseline verified |
| Application | Python / Flask | Implemented |
| Optional container support | Docker | Conditional; not currently required |

## Expected Demonstration

The completed project will demonstrate:

1. A clean baseline that passes.
2. An intentionally vulnerable pull request containing a controlled, synthetic security issue.
3. The relevant security control detecting the issue.
4. A failed security gate / `BLOCK` result.
5. Evidence of the finding without exposing real credentials or sensitive information.
6. A corrected pull request.
7. A passing security gate / `PASS` result.

The demonstration is being built incrementally. Documentation will be updated with actual findings and results after each demonstration rather than describing unexecuted results as completed.

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
│   ├── setup.sh
│   ├── setup.ps1
│   ├── verify.sh
│   └── verify.ps1
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

**Phase 2 — clean baseline verified.** The sample application, baseline tests, cross-platform setup, and first automated security checks are implemented and the latest five-job GitHub Actions baseline passed. The next step is the controlled vulnerable-PR demonstration, followed by the corrected-PR demonstration and evidence collection.
