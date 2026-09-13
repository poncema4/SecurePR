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

Phase 3 adds an explicit Security Gate job. The gate runs after the five required security jobs and evaluates their GitHub Actions results. It uses an `always()` condition so a failed upstream security job still produces a visible gate decision.

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
Security Gate
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

CodeQL and Semgrep provide complementary source-code analysis. CodeQL performs semantic analysis, while Semgrep provides focused rule-based analysis.

### Secret Detection

Gitleaks scans repository changes for credential-like material. The Phase 3 demonstration verified this path with a synthetic AWS-style access key. Gitleaks identified the finding under `aws-access-token`, causing its job to fail.

### Dependency Analysis

pip-audit checks the Python dependency requirements against known vulnerability information. The Phase 2 baseline dependency requirement was adjusted after CI identified a vulnerability in the earlier pytest 8.4.2 resolution; the current requirement is `pytest>=9.0.3,<10`.

### Security Gate

The Security Gate depends on the five required jobs:

1. Security Tests
2. Secret Detection
3. Semgrep SAST
4. Dependency Audit
5. CodeQL

If all five jobs succeed, the gate prints a `PASS` decision. If any required job is not successful, the gate prints a `BLOCK` decision and fails the gate job.

## 5. Phase 3 Demonstration Results

The intentional vulnerable demonstration used a separate pull request and a fake AWS-style credential. Gitleaks failed, while the other required controls completed successfully. The Security Gate then failed because Secret Detection was unsuccessful.

The corrected demonstration started from clean `main` and used an environment variable instead of a committed credential. All five required jobs passed, and the Security Gate passed.

The demonstration pull requests were not merged, so the clean `main` branch remained unchanged by the vulnerable or corrected example files.

## 6. Reusability

Security checks and gate logic remain sufficiently separated from the sample application's business logic so the workflow can later be adapted to another compatible repository. Reusability is a design goal, not a reason to build a full commercial platform.

## 7. Trust Boundaries

1. Developer-controlled pull-request changes entering the CI environment.
2. Pull-request source code interacting with GitHub Actions.
3. External dependency metadata and package installation.
4. Third-party GitHub Actions and security tools used by the workflow.
5. Security-tool output becoming a required-check result.

The workflow must avoid treating untrusted pull-request content as trusted workflow configuration or shell input.
