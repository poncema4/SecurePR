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

The checks run as separate steps inside one job. This keeps the tools logically separated and visible in the Actions logs while giving the pull request one overall SecurePR status instead of five separate job-level results. A final step writes a short PASS/BLOCK summary with a table and a link to the full Actions run.

The sample application is intentionally small so the project can focus on demonstrating security controls rather than building a large product.

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
- A single SecurePR Security Gate job with an explicit PASS/BLOCK result

The dependency baseline was corrected after CI identified a known vulnerability in the earlier pytest 8.4.2 resolution. `requirements.txt` now requires `pytest>=9.0.3,<10`.

### Verified clean baseline

The earlier Phase 3 clean baseline passed all required controls:

- Security Tests — PASS
- Secret Detection — PASS
- Semgrep SAST — PASS
- Dependency Audit — PASS
- CodeQL — PASS
- Security Gate — PASS

The new single-job gate architecture is being verified again after the Phase 3 refinement before the phase is declared complete.

### Controlled vulnerable-PR demonstration

A separate Phase 3 demonstration pull request intentionally introduced a **synthetic AWS-style access key** into `demo/intentional-secret.py`. No real credential was used.

Gitleaks detected the value using its `aws-access-token` rule. The finding was reported against the demonstration file and the Secret Detection control failed. The Security Gate then failed because one of its required controls was unsuccessful.

The demonstrated result was therefore:

```text
Synthetic secret introduced
        ↓
Gitleaks → BLOCKING FINDING
        ↓
Secret Detection → FAIL
        ↓
SecurePR Security Gate → BLOCK
```

The vulnerable demonstration was kept off `main` and the demonstration PR was closed without merging it.

### Corrected-PR demonstration

A separate clean demonstration branch was created from `main`. Instead of committing a credential, the corrected example read the credential from the execution environment with `os.getenv()`.

The corrected pull request passed all five required controls and the Security Gate. It was also closed without merging, so `main` remained the clean project baseline.

### PASS/BLOCK reporting and remediation policy

SecurePR is intentionally concise at the top level:

- **🟢 PASS** — the required automated checks completed successfully and no blocking result was reported by SecurePR.
- **🔴 BLOCK** — at least one required control failed and the PR should be reviewed before merging.

The summary identifies each control, its result, what it checks, and a link to the full Actions run. The detailed tool output remains available in the individual workflow steps.

SecurePR does **not** automatically edit source code or merge a pull request. That is deliberate: an automated scanner can produce a false positive, and automatically changing or merging code could make the situation worse. The normal remediation loop is to review the finding, fix the PR, push the change, and let SecurePR run again.

A future opt-in remediation feature could propose or prepare changes, but it should require an explicit user action and remain separate from the blocking gate.

## Accuracy and False-Positive / False-Negative Handling

SecurePR does not claim perfect detection accuracy. Security scanners can produce false positives, while static analysis can miss vulnerabilities that depend on runtime behavior, business logic, configuration, or a code path outside the tool's coverage.

The Phase 3 design reduces these risks by layering controls rather than relying on one scanner:

- Gitleaks checks committed secret patterns and was validated with a controlled synthetic secret.
- Semgrep and CodeQL provide complementary static analysis.
- pip-audit checks known dependency vulnerabilities.
- Pytest verifies security behavior that static analysis cannot prove reliably.
- Threat modeling and human review cover design and business-logic issues that automation cannot reliably determine.
- Vulnerable and corrected demonstrations are used to verify that the gate actually blocks and passes the expected cases.

A blocking result means **review required**, not that the scanner is infallible. A passing result means the configured controls passed; it does not prove that the application contains no vulnerabilities.

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

The Phase 3 refinement is also verified through a new clean `main` workflow run before Phase 3 is considered complete.

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

The project only claims coverage that is demonstrated by the implemented controls and tests. The Phase 3 demonstrations specifically verify the secret-detection path and PASS/BLOCK gate behavior.

## Security Controls

| Area | Control | Phase 3 status |
|---|---|---|
| SAST | CodeQL | Baseline and corrected PR verified |
| Additional SAST | Semgrep | Baseline and corrected PR verified |
| Secrets | Gitleaks | Clean baseline passed; synthetic secret was detected and blocked |
| Python dependencies | pip-audit | Baseline and corrected PR verified |
| Dependency changes | GitHub Dependency Review where supported | Conditional / not yet demonstrated |
| Security behavior | pytest | Baseline and corrected PR verified |
| Security Gate | Single-job PASS/BLOCK result | Refinement implemented; final clean run pending |
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
- Automatic source-code modification or automatic pull-request merging

## Future Enhancements

- DAST with OWASP ZAP
- Fuzz testing
- Container image scanning
- SBOM generation and analysis
- More project-specific security rules
- Detailed pull-request security reporting
- Workflow-specific security linting
- Broader vulnerable-PR demonstrations for selected SAST findings
- Explicit, user-triggered remediation proposals that never merge automatically

## Status

**Phase 3 — security gate refinement in final verification.** The clean baseline, intentional synthetic-secret blocking demonstration, corrected passing demonstration, single-job gate design, concise PASS/BLOCK reporting, and no-auto-merge policy are implemented. The final post-refinement workflow run must pass before Phase 3 is declared complete.
# Manual Phase 3 PASS test
