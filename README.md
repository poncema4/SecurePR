# SecurePR

**Automated Secure Code Review & DevSecOps Security Gate**

**Course:** Secure Software Development  
**Project:** Final Course MVP / Proof of Concept  
**Status:** Planned

## 1. Project Overview

SecurePR is a proof-of-concept DevSecOps security gate that brings application-security checks into the normal pull-request workflow.

The project is built around a practical development question:

> **Should this code be allowed to move forward in the software development lifecycle?**

A developer will submit a change to a small sample application. SecurePR will run a defined set of security checks, collect the results, provide useful developer-facing feedback, and make a clear gate decision: **pass or block**.

The MVP is intentionally focused. It will demonstrate the security workflow end to end rather than attempt to reproduce every capability of a commercial application-security platform.

## 2. Course Alignment

SecurePR is designed for **Seton Hall University — Secure Software Development**.

The project directly connects to course topics including:

- Secure SDLC
- Security requirements engineering
- STRIDE and threat modeling
- Secure architecture
- Secure coding
- Injection and input-validation issues
- Authentication/authorization security considerations
- SAST
- Secrets management
- Dependency security
- Security testing
- DAST concepts
- DevSecOps and shift-left security
- Secure build/deployment practices
- Structured secure code review

## 3. Problem Statement

Security reviews performed only near the end of development can allow defects to travel through multiple stages of the SDLC before they are discovered. Manual review is also difficult to make consistent across every change.

SecurePR demonstrates a different approach: place repeatable security controls at the pull request, where developers are already reviewing and discussing changes.

The system should connect a security requirement to a concrete automated check and ultimately to a development decision:

```text
Threat / Security Requirement
            ↓
        Security Control
            ↓
       Automated Check
            ↓
          Finding
            ↓
       Security Gate
        ↙          ↘
     BLOCK          PASS
```

## 4. Project Objectives

The MVP will aim to:

1. Integrate security checks into a GitHub pull-request workflow.
2. Analyze a small sample application for selected security weaknesses.
3. Detect secrets or credential-like material.
4. Check dependencies for known security concerns.
5. Run security-focused automated tests.
6. Normalize important findings into a consistent format where useful.
7. Provide understandable remediation information to the developer.
8. Block a pull request when configured security requirements are not satisfied.
9. Demonstrate that a corrected change can pass the same security gate.

## 5. MVP Scope

### 5.1 Sample Application

A small intentionally testable application will provide the codebase on which SecurePR operates.

The sample application will contain both secure code and controlled vulnerable examples so the pipeline can demonstrate meaningful failures and subsequent remediation.

The sample application will remain deliberately small. It exists to demonstrate the security workflow, not to become a second large software project.

### 5.2 Pull Request Workflow

A GitHub pull request will act as the primary security decision point.

The workflow will:

1. Trigger when a relevant pull request is opened or updated.
2. Build or prepare the sample application.
3. Run configured security checks.
4. Collect the results.
5. Determine whether configured security requirements were violated.
6. Publish useful feedback.
7. Return a passing or failing gate status.

### 5.3 SAST

The MVP will use static analysis to identify selected security weaknesses in source code.

The initial implementation will focus on a small number of high-value patterns rather than attempting to detect every possible vulnerability.

### 5.4 Secret Detection

SecurePR will detect accidentally committed secrets or credential-like values, such as API keys, passwords, or access tokens.

A detected secret should be treated as a security-gate failure in the demonstration.

### 5.5 Dependency Security

The pipeline will inspect application dependencies for known security concerns using an appropriate package/dependency auditing mechanism.

This demonstrates that secure development includes the software supply chain, not only code written by the developer.

### 5.6 Security Tests

The project will include automated security-focused tests tied to selected security requirements.

These tests will demonstrate that security requirements can be verified continuously rather than checked only during a final review.

### 5.7 Gate Decision

The core feature is the decision produced by the checks.

Example:

```text
SECURITY GATE: BLOCKED

Findings
--------
HIGH    Hardcoded credential
HIGH    Injection-related issue
MEDIUM  Vulnerable dependency

Action
------
Fix the findings before merging.
```

After remediation:

```text
SECURITY GATE: PASSED

Checks
------
PASS    Static analysis
PASS    Secret detection
PASS    Dependency audit
PASS    Security tests

Action
------
Pull request may proceed.
```

The project will emphasize the gate decision and technical findings instead of reducing the entire process to a numerical security score.

## 6. Threat Modeling and Requirements

The project will begin with a small threat model for the sample application. STRIDE will be used where appropriate to identify threats and establish relevant security requirements.

The important relationship is:

```text
Threat
  ↓
Security Requirement
  ↓
Design / Coding Control
  ↓
Automated Verification
  ↓
Pull Request Decision
```

This keeps the automated checks connected to the secure SDLC instead of treating scanners as isolated tools.

## 7. Planned Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
Pull Request
    |
    v
GitHub Actions
    |
    +------------------+------------------+------------------+
    |                  |                  |                  |
    v                  v                  v                  v
  SAST          Secret Detection   Dependency Audit   Security Tests
    |                  |                  |                  |
    +------------------+------------------+------------------+
                           |
                           v
                    Finding Collection
                           |
                           v
                     Security Gate
                      /          \
                   BLOCK          PASS
```

The sample application, security checks, gate logic, and workflow configuration will remain separated so each part has a clear responsibility.

## 8. Tech Stack

| Area | Technology | Purpose |
|---|---|---|
| Primary Language | **Python** | Sample application and security-related logic where appropriate |
| Automation Language | **Python / YAML** | Check orchestration and GitHub Actions configuration |
| CI/CD | **GitHub Actions** | Pull-request security workflow |
| Static Analysis | **CodeQL / Semgrep** | Source-code security analysis |
| Secret Detection | **Gitleaks or equivalent** | Credential/secret detection |
| Dependency Analysis | **pip-audit** | Python dependency security checks |
| Security Testing | **pytest** | Automated application/security tests |
| Containerization | **Docker** | Reproducible application/test environment where useful |
| Version Control | **Git / GitHub** | Source control and pull-request workflow |
| Configuration | **YAML / TOML** | Tool and workflow configuration |

The exact tool combination will be kept small enough for the MVP to be reliable and understandable. CodeQL, Semgrep, or another equivalent tool may be selected during implementation based on which produces the clearest demonstration for the sample codebase.

## 9. Planned Repository Structure

The repository will separate the demonstration application from the security tooling and supporting documentation.

```text
SecurePR/
├── sample-app/
│   ├── src/
│   └── tests/
├── securepr/
│   ├── src/
│   └── tests/
├── security/
│   ├── policies/
│   ├── rules/
│   └── test-cases/
├── .github/
│   └── workflows/
├── docker/
├── docs/
└── README.md
```

The structure is intended to make the boundary between the application being analyzed, SecurePR's logic/configuration, security policies, CI workflow, and documentation obvious.

## 10. Findings and Developer Feedback

A finding should contain enough context for a developer to understand what failed.

Where available, findings will include:

- Severity
- Security category
- File and location
- Description
- Detection source
- Why the issue matters
- Remediation guidance
- Gate impact

Example:

```text
Severity: HIGH
Category: Injection
Location: sample-app/src/routes.py:42
Detected by: Static analysis

Issue:
Untrusted input reaches a database operation without
appropriate parameterization.

Recommendation:
Use parameterized database operations instead of
constructing queries from untrusted input.

Gate impact: BLOCK
```

## 11. Secure Development Lifecycle Demonstration

The MVP will demonstrate the following development cycle:

```text
Define Security Requirement
          ↓
Identify Threat
          ↓
Implement Control
          ↓
Developer Opens Pull Request
          ↓
Automated Security Checks
          ↓
Findings / Feedback
          ↓
BLOCK or PASS
          ↓
Remediation
          ↓
Checks Run Again
```

The implementation will focus on the automated portion while documenting how the threat model and security requirements informed the checks.

## 12. Expected Demonstration

The final MVP should support a short, repeatable demonstration:

1. Show the sample application's relevant security requirement.
2. Open a pull request containing an intentionally vulnerable change.
3. Allow GitHub Actions to run the SecurePR checks.
4. Show the resulting finding.
5. Show the security gate blocking the change.
6. Correct the vulnerability.
7. Update the pull request.
8. Run the checks again.
9. Show the passing gate.

This demonstrates the complete security feedback loop rather than only showing a scanner's output.

## 13. Security Principles

### Shift Left

Security checks occur during development, before code is treated as ready to merge.

### Defense in Depth

Multiple checks provide different forms of assurance rather than relying on a single scanner.

### Least Privilege

The workflow and sample application will use only the permissions required for their responsibilities.

### Fail Safely

Configured high-impact security failures should prevent the protected workflow from treating the change as ready to merge.

### Actionable Results

Security feedback should explain what was detected and what the developer should investigate or change.

## 14. Out of Scope for the MVP

The initial version will not attempt to become an enterprise application-security platform.

Out of scope:

- Dozens of scanner integrations
- Support for every programming language
- Enterprise vulnerability-management workflows
- Multi-tenant SaaS architecture
- Organization-wide policy management
- Advanced machine-learning vulnerability detection
- Large-scale distributed scanning
- Complete automated penetration testing
- Production deployment of the platform
- A generic security score

## 15. Future Enhancements

Possible future additions include:

- OWASP ZAP DAST integration
- Fuzzing stages
- Container image scanning
- SBOM generation
- Additional CodeQL/Semgrep rules
- Rich pull-request annotations
- Expanded security policies
- Historical security results
- Additional language support

These enhancements are secondary to completing a reliable end-to-end MVP.

## 16. Project Definition

SecurePR is a **secure-development workflow proof of concept**. Its purpose is to show how security requirements and automated verification can become part of the normal developer workflow, resulting in a concrete decision about whether a change should proceed.

The finished MVP should be small enough to understand completely, but substantial enough to demonstrate secure SDLC, secure coding, automated testing, and DevSecOps principles in one working flow.