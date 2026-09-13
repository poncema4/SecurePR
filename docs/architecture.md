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
Required Checks
   ↓
PASS / BLOCK
```

The clean Phase 2 baseline currently executes five required security jobs. A failed required job causes the workflow/check suite to fail; the next demonstration stage will validate this behavior with an intentionally vulnerable pull request.

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
Gate Decision
```

Each security concern is mapped to a requirement and one or more controls. The workflow should preserve enough tool output to explain a failure without exposing secrets.

## 4. Main Components

### Sample Application

The Phase 2 application is a deliberately small Flask service. It provides authentication, user-profile lookup, and input-validation behavior that can be exercised by tests and analyzed by security tooling.

### Security Test Suite

Pytest exercises application behavior and security properties that static analysis cannot reliably prove. The suite is run in GitHub Actions and can also be run locally through the platform-specific verification scripts.

### Static Analysis

CodeQL and Semgrep provide complementary source-code analysis. CodeQL performs semantic analysis, while Semgrep provides focused rule-based analysis.

### Secret Detection

Gitleaks scans repository history for credential-like material. Demonstration secrets will always be synthetic.

### Dependency Analysis

pip-audit checks the Python dependency requirements against known vulnerability information. The Phase 2 baseline dependency requirement was adjusted after CI identified a vulnerability in the earlier pytest 8.4.2 resolution; the current requirement is `pytest>=9.0.3,<10`.

### GitHub Actions

GitHub Actions orchestrates the controls. The workflow uses repository-read permissions plus the permissions required by CodeQL to publish security-analysis results. Workflow permissions and handling of untrusted pull-request data are themselves treated as security concerns.

## 5. Current Phase 2 Gate Behavior

The current baseline consists of five required workflow jobs:

1. Security Tests
2. Secret Detection
3. Semgrep SAST
4. Dependency Audit
5. CodeQL

For the clean baseline, all five jobs completed successfully. The next implementation step is to exercise failure behavior with controlled vulnerable pull requests and document exactly which required check detects each vulnerability.

The project will not claim a specific scanner-to-gate behavior until it has been demonstrated with an actual pull request.

## 6. Reusability

Security checks and gate logic should remain sufficiently separated from the sample application's business logic so the workflow can later be adapted to another compatible repository. Reusability is a design goal, not a reason to build a full commercial platform.

## 7. Trust Boundaries

1. Developer-controlled pull-request changes entering the CI environment.
2. Pull-request source code interacting with GitHub Actions.
3. External dependency metadata and package installation.
4. Third-party GitHub Actions and security tools used by the workflow.
5. Security-tool output becoming a required-check result.

The workflow must avoid treating untrusted pull-request content as trusted workflow configuration or shell input.
