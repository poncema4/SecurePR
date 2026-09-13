# SecurePR Architecture

## 1. System Purpose

SecurePR places security controls into the pull-request workflow for a small Python application. The architecture separates the application being evaluated from the automation that evaluates it.

## 2. High-Level Flow

```text
Developer
   ↓
Pull Request
   ↓
GitHub Actions
   ↓
One SecurePR Security Gate Job
   ├── Python runtime policy
   ├── Security tests
   ├── Secret Detection (Gitleaks)
   ├── Semgrep SAST
   ├── Dependency Audit (pip-audit)
   ├── CodeQL initialization
   └── CodeQL analysis
   ↓
PASS / BLOCK
   ↓
Human review before merge
```

Phase 3 uses one GitHub Actions job named `SecurePR Security Gate`. The individual controls run as separate steps inside that job. This gives the pull request one authoritative SecurePR status while preserving step-level logs for diagnosis. The final step evaluates the configured control outcomes and publishes the PASS/BLOCK summary.

## 3. Control Flow

```text
Threat
  ↓
Security Requirement
  ↓
Security Control
  ↓
Automated Check
  ↓
Finding / Test Result
  ↓
SecurePR Security Gate
  ↓
PASS / BLOCK
```

Each security concern is mapped to a requirement and one or more controls. The workflow preserves enough tool output to explain a failure without exposing the synthetic secret itself.

## 4. Main Components

### Sample Application

The Phase 2 application is a deliberately small Flask service. It provides authentication, user-profile, and input-validation behavior that can be exercised by tests and analyzed by security tooling.

### Security Test Suite

Pytest exercises application behavior and security properties that static analysis cannot reliably prove. The suite is run in GitHub Actions and can also be run locally through the platform-specific verification scripts.

### Static Analysis

CodeQL and Semgrep provide complementary source-code analysis. CodeQL performs semantic analysis and uploads its results to GitHub Code Scanning, while Semgrep provides focused rule-based analysis. A successful CodeQL analysis means the configured analysis completed; it is not a claim that no CodeQL finding exists.

### Secret Detection

Gitleaks scans repository changes for credential-like material. The Phase 3 demonstration verified this path with a synthetic AWS-style access key. Gitleaks identified the finding under `aws-access-token`, causing the Secret Detection step to fail and the overall gate to BLOCK.

### Dependency Analysis

pip-audit checks the Python dependency requirements against known vulnerability information. The dependency baseline was adjusted after CI identified a vulnerability in the earlier pytest 8.4.2 resolution; the current requirement is `pytest>=9.0.3,<10`. The Phase 3 secret demonstrations did not change dependencies, so pip-audit passed those runs.

### SecurePR Security Gate

The authoritative gate is the single `SecurePR Security Gate` job. Its configured blocking controls are the runtime policy, dependency installation, security tests, Gitleaks, Semgrep, pip-audit, and successful CodeQL initialization and analysis. If any configured control step does not succeed, the final step publishes `BLOCK` and exits unsuccessfully. If all configured controls succeed, it publishes `PASS`.

GitHub Code Scanning may display CodeQL results separately in the repository interface. That reporting surface is not a second SecurePR job or a second required SecurePR status check.

## 5. Phase 3 Demonstration Results

The intentional vulnerable demonstration used a separate pull request and a fake AWS-style credential. Gitleaks failed, while the other configured controls completed successfully. The overall SecurePR result was BLOCK because Secret Detection failed.

The corrected demonstration started from a clean `main` baseline and used an environment variable instead of a committed credential. The configured controls passed and the overall SecurePR result was PASS.

The demonstration pull requests were not merged, so the vulnerable or corrected example files did not alter `main`.

## 6. Reusability

Security checks and gate logic remain sufficiently separated from the sample application's business logic so the workflow can later be adapted to another compatible repository. Reusability is a design goal, not a reason to build a full commercial platform.

## 7. Trust Boundaries

1. Developer-controlled pull-request changes entering the CI environment.
2. Pull-request source code interacting with GitHub Actions.
3. External dependency metadata and package installation.
4. Third-party GitHub Actions and security tools used by the workflow.
5. Security-tool output becoming inputs to the final PASS/BLOCK result.
