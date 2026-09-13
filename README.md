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
One GitHub Actions Security Gate Job
   ├── Python Runtime Policy
   ├── Security Tests
   ├── Secret Detection (Gitleaks)
   ├── Semgrep SAST
   ├── Dependency Audit (pip-audit)
   └── CodeQL SAST
   ↓
One PASS / BLOCK result
   ↓
Human review before merge
```

The checks run as separate steps inside one job. This keeps the tools logically separated and visible in the Actions logs while giving the pull request one overall SecurePR status instead of a separate job for every tool. A final step writes a PASS/BLOCK summary with check results, remediation guidance, an accuracy boundary, and a link to the full Actions run.

## Phase 3 — Security Gate

The sample application is intentionally small so the project can focus on demonstrating security controls rather than building a large product.

The repository contains:

- A small Flask sample application
- Password-hash-based authentication using Werkzeug
- Login, user-profile, and input-validation endpoints
- Organized pytest unit and security tests
- Cross-platform local setup and verification scripts
- A Python runtime policy with upgrade guidance
- GitHub Actions security workflow
- CodeQL SAST
- Semgrep SAST
- Gitleaks secret detection
- pip-audit dependency auditing
- Python compilation verification
- A single SecurePR Security Gate job with an explicit PASS/BLOCK result

The dependency baseline uses `pytest>=9.0.3,<10` after CI identified a vulnerability in the earlier pytest 8.4.2 resolution.

### PASS/BLOCK reporting

The final workflow reports the same structure for both outcomes:

1. Overall SecurePR result
2. Check Results table
3. **Fixes to make this PASS**
4. Remediation
5. Accuracy boundary
6. Full Actions run link

For a BLOCK, the fixes section explains why each failed control matters, what the developer should change, and the expected result after remediation. For a PASS, it states that there are no blocking fixes and that human review remains required.

SecurePR does not automatically edit source code, rotate credentials, or merge a pull request. The developer reviews the finding, applies the fix, pushes the change, and lets the gate run again.

### Runtime policy

`.python-version` declares Python 3.12 for the project. SecurePR requires Python 3.11 or newer. The runtime policy is intentionally separate from `pip-audit`: the runtime control checks the Python interpreter policy, while pip-audit checks known vulnerabilities in Python packages.

### Accuracy and false-positive / false-negative handling

SecurePR does not claim perfect detection accuracy. Security scanners can produce false positives, while static analysis can miss vulnerabilities that depend on runtime behavior, business logic, configuration, or code paths outside a tool's coverage.

The design uses layered controls rather than relying on one scanner:

- Gitleaks checks committed secret patterns.
- Semgrep and CodeQL provide complementary static analysis.
- pip-audit checks known dependency vulnerabilities.
- Pytest verifies security behavior that static analysis cannot prove reliably.
- The Python runtime policy rejects unsupported runtimes and provides upgrade guidance.
- Threat modeling and human review cover design and business-logic issues that automation cannot reliably determine.
- Controlled vulnerable and corrected demonstrations verify that the gate can block and pass the expected cases.

A PASS means the configured controls passed; it does not prove that the application is vulnerability-free. A BLOCK means review is required; it does not by itself prove that a scanner finding is exploitable.

## Local Setup and Verification

Both platform-specific setup scripts create and use `.venv` for project dependencies.

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

## Test Organization

```text
tests/
├── __init__.py
├── unit/
│   └── test_app_endpoints.py
└── security/
    ├── test_authentication.py
    ├── test_input_validation.py
    └── test_python_runtime.py
```

The suite covers endpoint behavior, authentication success/failure, password hashing, invalid input, input-size boundaries, and the Python runtime policy.

## Security Controls

| Area | Control | Status |
|---|---|---|
| Runtime | Python runtime policy | Implemented and tested |
| SAST | CodeQL | Implemented and tested in CI |
| Additional SAST | Semgrep | Implemented and tested in CI |
| Secrets | Gitleaks | Synthetic-secret BLOCK demonstrated |
| Python dependencies | pip-audit | Implemented and tested in CI; baseline vulnerability remediation completed |
| Security behavior | pytest | Organized unit/security suite implemented |
| Security Gate | Single-job PASS/BLOCK result | Implemented with detailed remediation guidance |
| Workflow security | Workflow permissions and review | Implemented |
| CI orchestration | GitHub Actions | Implemented |
| Application | Python / Flask | Implemented |

## Project Structure

```text
SecurePR/
├── app/
│   ├── __init__.py
│   └── app.py
├── security/
│   ├── __init__.py
│   └── python_runtime.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── test_app_endpoints.py
│   └── security/
│       ├── test_authentication.py
│       ├── test_input_validation.py
│       └── test_python_runtime.py
├── scripts/
│   ├── __init__.py
│   ├── setup.sh
│   ├── setup.ps1
│   ├── verify.sh
│   ├── verify.ps1
│   └── check_python_version.py
├── docs/
│   ├── architecture.md
│   ├── security-requirements.md
│   ├── threat-model.md
│   ├── security-checks.md
│   └── testing.md
├── .github/
│   └── workflows/
│       └── security.yml
├── .python-version
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
- Automatic source-code modification or automatic pull-request merging

## Future Enhancements

- DAST with OWASP ZAP
- Fuzz testing
- Container image scanning
- SBOM generation and analysis
- More project-specific security rules
- Detailed pull-request security reporting
- Explicit, user-triggered remediation proposals that never merge automatically

## Status

**Phase 3 — complete.** The single-job security gate, layered security controls, organized security tests, Python runtime policy, detailed PASS/BLOCK reporting, no-auto-remediation policy, and protected `main` ruleset are implemented and validated. The controlled vulnerable and corrected demonstrations passed their intended BLOCK/PASS outcomes, and the post-merge `main` workflow was verified successfully.
