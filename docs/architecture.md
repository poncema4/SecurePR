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
   ├── Source-code analysis
   ├── Secret detection
   ├── Dependency analysis
   ├── Security tests
   └── Workflow/configuration checks
   ↓
Security Gate
   ↓
PASS / BLOCK
```

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

A deliberately small Python application will provide realistic source code and security behavior for the checks. It will contain enough functionality to demonstrate selected injection, authentication/authorization, input-validation, error-handling, and dependency scenarios without becoming a large application.

### Security Test Suite

Pytest will exercise security properties that static analysis cannot reliably prove, including behavior and regression cases.

### Static Analysis

CodeQL and Semgrep will provide complementary source-code analysis. Rules will be selected for the actual Python application rather than enabling an unnecessarily broad collection of checks.

### Secret Detection

Gitleaks will scan the repository for credential-like material. Demonstration secrets will always be synthetic.

### Dependency Analysis

pip-audit will check Python dependencies against known vulnerability information. GitHub Dependency Review may be used for pull-request dependency changes where supported by the repository configuration.

### GitHub Actions

GitHub Actions will orchestrate the controls. Workflow permissions and handling of untrusted pull-request data are themselves treated as security concerns.

## 5. Gate Model

The final workflow will have an explicit gate stage. Required blocking controls must succeed for a `PASS`. A defined blocking finding or failed required security test results in `BLOCK`.

The precise implementation of the gate will be finalized after the first workflow is built so that it reflects actual tool exit codes and supported behavior.

## 6. Reusability

Security checks and gate logic should remain sufficiently separated from the sample application's business logic so the workflow can later be adapted to another compatible repository. Reusability is a design goal, not a reason to build a full commercial platform.

## 7. Trust Boundaries

1. Developer-controlled pull-request changes entering the CI environment.
2. Pull-request source code interacting with GitHub Actions.
3. External dependency metadata and package installation.
4. Third-party GitHub Actions used by the workflow.
5. Security-tool output becoming a gate decision.

The workflow must avoid treating untrusted pull-request content as trusted workflow configuration or shell input.
