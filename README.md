# SecurePR

**Secure Pull Request Security Gate**

**Course:** Secure Software Development  
**Project:** Final MVP / Proof of Concept

## Overview

SecurePR is a DevSecOps proof of concept that places automated security checks directly into a pull-request workflow.

The MVP will use a small sample application and demonstrate what happens when vulnerable code is submitted: security checks run, findings are reported, and the pull request is either blocked or allowed to continue.

The focus is on integrating security into the software development lifecycle rather than building another standalone vulnerability scanner.

## Project Goal

The main question SecurePR addresses is:

> **Can security checks become a repeatable development gate before vulnerable code is merged?**

The project will connect security requirements and threat modeling to practical automated checks and a clear merge decision.

## MVP Scope

- Use a small application as the codebase under review.
- Trigger security checks from a GitHub pull request.
- Run SAST against the source code.
- Detect committed secrets.
- Check dependencies for known vulnerabilities.
- Run selected security tests.
- Normalize or summarize important findings.
- Block a pull request when required security checks fail.
- Demonstrate the same workflow passing after the vulnerability is fixed.

### Example Workflow

```text
Code Change
    ↓
Pull Request
    ↓
Security Checks
    ├── SAST
    ├── Secret Detection
    ├── Dependency Check
    └── Security Tests
    ↓
Security Gate
   ↙     ↘
BLOCK    PASS
```

## SDLC Connection

SecurePR will document a small threat model and use it to define security requirements for the sample application. Those requirements will then inform the automated checks.

```text
Threat
  ↓
Security Requirement
  ↓
Security Control
  ↓
Automated Check
  ↓
Gate Decision
```

This connects the project's implementation to the secure-SDLC concepts covered in the course.

## Planned Architecture

```text
Developer
   ↓
GitHub Repository
   ↓
Pull Request
   ↓
GitHub Actions
   ├── SAST
   ├── Secret Detection
   ├── Dependency Analysis
   └── Security Tests
   ↓
SecurePR Gate
   ↓
Block / Pass
```

## Tech Stack

- **Primary Language:** Python
- **Sample Application:** Python
- **CI/CD:** GitHub Actions
- **SAST:** CodeQL and/or Semgrep
- **Secret Detection:** Gitleaks
- **Dependency Security:** pip-audit
- **Security Testing:** pytest
- **Containers:** Docker
- **Configuration:** YAML
- **Version Control:** Git / GitHub

The MVP will use a small number of well-understood tools instead of trying to integrate every available security scanner.

## Planned Repository Structure

```text
SecurePR/
├── app/
├── tests/
├── security/
│   ├── rules/
│   └── threat-model/
├── scripts/
├── .github/
│   └── workflows/
├── docker/
└── README.md
```

The structure will separate the sample application, security logic, tests, automation, and documentation.

## Course Alignment

SecurePR applies the course material on secure SDLC, security requirements, STRIDE/threat modeling, secure architecture, secure coding, SAST, secrets management, dependency security, security testing, CI/CD, DevSecOps, and shift-left security.

## Expected Demonstration

The final MVP should show an intentionally vulnerable pull request being detected and blocked, followed by a corrected pull request passing the same security checks.

The important result is the development workflow itself: **identify → report → remediate → verify**.

## Out of Scope

- Enterprise-scale security platforms
- Large numbers of scanner integrations
- Full vulnerability-management systems
- Support for every programming language
- Production SaaS deployment
- Advanced ML-based vulnerability detection
- Generic security scoring

## Status

This repository currently defines the project and MVP. Implementation will begin with the sample application, threat model, security requirements, and first automated gate.
