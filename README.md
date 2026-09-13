# SecurePR

## Secure Pull Request Security Gate

SecurePR is a DevSecOps proof of concept that places repeatable security checks into a pull-request workflow for a small Python application. The project demonstrates how security requirements are translated into automated controls and a clear security-gate decision before code is merged.

SecurePR is not intended to claim complete vulnerability detection. Different security concerns require different controls, and some issues still require tests, threat modeling, or human review.

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

## Phase 3 — Security Gate Demonstrated

### Clean baseline

The repository contains:

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
- An explicit Security Gate that evaluates the five required checks

The dependency baseline was corrected after CI identified a known vulnerability in the earlier pytest 8.4.2 resolution. `requirements.txt` now requires `pytest>=9.0.3,<10`.

### Verified clean baseline

The clean `main` baseline has passed all five required security jobs:

- Security Tests — PASS
- Secret Detection — PASS
- Semgrep SAST — PASS
- Dependency Audit — PASS
- CodeQL — PASS

The explicit Security Gate also passed on the Phase 3 implementation pull request.

### Controlled vulnerable-PR demonstration

A separate Phase 3 demonstration pull request intentionally introduced a **synthetic AWS-style access key** into `demo/intentional-secret.py`. No real credential was used.

Gitleaks detected the value using its `aws-access-token` rule. The finding was reported against the demonstration file and the Secret Detection job failed. The Security Gate then failed because one of its required checks was unsuccessful.

The demonstrated result was therefore:

```text
Synthetic secret introduced
        ↓
Gitleaks → BLOCKING FINDING
        ↓
Secret Detection → FAIL
        ↓
Security Gate → BLOCK
```

The vulnerable demonstration was kept off `main` and the demonstration PR was closed without merging it.

### Corrected-PR demonstration

A separate clean demonstration branch was created from `main`. Instead of committing a credential, the corrected example read the credential from the execution environment with `os.getenv()`.

The corrected pull request passed:

- Security Tests — PASS
- Secret Detection — PASS
- Semgrep SAST — PASS
- Dependency Audit — PASS
- CodeQL — PASS
- Security Gate — PASS

The corrected PR was also closed without merging, so `main` remains the clean project baseline.

## Local Setup and Verification

Both platform-specific setup scripts create and use `.venv` for project dependencies.

### Linux or macOS (Bash)

```bash
chmod +x scripts/setup.sh scripts/verify.sh
./scripts/setup.sh
./scripts/verify.sh
```

The setup script creates `.venv` and installs the dependency ranges from `requirements.txt`. The verification script automatically uses the local virtual environment when it exists.

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

## What Has Been Tested

### Local baseline

The Windows PowerShell setup and verification were executed successfully using `.venv`:

```text
8 passed in 0.47s
SecurePR verification passed.
```

### GitHub Actions

The workflow has been tested on both clean and intentionally vulnerable pull-request states. The vulnerable demonstration produced a real Gitleaks finding and a failed Security Gate. The corrected demonstration produced successful results for all five required controls and a successful Security Gate.

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
- Container configuration issues if Docker becomes part of the implementation
- Security-design and business-logic issues through threat modeling and human review

The project only claims coverage that is demonstrated by the implemented controls and tests. The Phase 3 demonstration specifically verifies the secret-detection path and PASS/BLOCK gate behavior.

## Security Controls

| Area | Control | Phase 3 status |
|---|---|---|
| SAST | CodeQL | Baseline and corrected PR verified |
| Additional SAST | Semgrep | Baseline and corrected PR verified |
| Secrets | Gitleaks | Clean baseline passed; synthetic secret was detected and blocked |
| Python dependencies | pip-audit | Baseline and corrected PR verified |
| Dependency changes | GitHub Dependency Review where supported | Conditional / not yet demonstrated |
| Security behavior | pytest | Baseline and corrected PR verified |
| Security Gate | Explicit PASS/BLOCK job | Vulnerable PR blocked; corrected PR passed |
| Workflow security | Workflow permissions and review | Implemented and reviewed |
| CI orchestration | GitHub Actions | Verified |
| Application | Python / Flask | Implemented |
| Optional container support | Docker | Conditional; not currently required |

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
- Workflow-specific security linting
- Broader vulnerable-PR demonstrations for selected SAST findings

## Status

**Phase 3 — security gate and controlled secret-detection demonstration verified.** The clean baseline, explicit PASS/BLOCK gate, intentional synthetic-secret blocking demonstration, and corrected passing demonstration have all been executed. The demonstration pull requests remain unmerged so `main` stays clean.
