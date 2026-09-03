# SecurePR

**Secure Pull Request Security Gate**

**Course:** Secure Software Development  
**Project:** Final MVP / Proof of Concept

## Overview

SecurePR is a DevSecOps proof of concept that places automated security checks into a pull-request workflow. The goal is to detect selected security issues before vulnerable code is merged and give the developer a clear pass or block decision.

## Problem

Security issues can be found late in development when remediation is more expensive and disruptive. SecurePR tests how repeatable security checks can be placed directly into the development workflow.

## Objectives

- Run security checks automatically when a pull request is opened or updated.
- Detect selected source-code security issues.
- Detect committed secrets.
- Check dependencies for known vulnerabilities.
- Run selected security tests.
- Report useful findings and remediation guidance.
- Block or pass the pull request based on defined security requirements.

## MVP Scope

The MVP will include:

- A small sample application.
- GitHub pull-request automation.
- SAST using CodeQL and/or Semgrep.
- Secret detection using Gitleaks.
- Dependency checks using pip-audit.
- Security tests using pytest.
- A simple security gate with `BLOCK` and `PASS` outcomes.
- A demonstration of a vulnerable change being blocked and a corrected change passing.

## Architecture / Workflow

```text
Developer
  ↓
Pull Request
  ↓
GitHub Actions
  ├── SAST
  ├── Secret Detection
  ├── Dependency Check
  └── Security Tests
  ↓
Security Gate
  ↓
BLOCK / PASS
```

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

## Tech Stack

- **Language:** Python
- **Sample Application:** Python
- **CI/CD:** GitHub Actions
- **SAST:** CodeQL and/or Semgrep
- **Secret Detection:** Gitleaks
- **Dependency Security:** pip-audit
- **Security Testing:** pytest
- **Containers:** Docker
- **Configuration:** YAML
- **Version Control:** Git / GitHub

## Project Structure

```text
SecurePR/
├── app/
├── security/
├── tests/
├── scripts/
├── .github/
│   └── workflows/
├── docker/
├── docs/
└── README.md
```

## Security Concepts

- Secure SDLC
- Security requirements
- STRIDE and threat modeling
- Secure coding
- SAST
- Secret management
- Dependency/supply-chain security
- Security testing
- CI/CD
- DevSecOps
- Shift-left security

## Expected Demonstration

A pull request containing an intentionally vulnerable change will trigger the security checks and be blocked. After the issue is fixed, the checks will run again and the pull request will pass.

## Out of Scope

- Enterprise-scale security platforms
- Large numbers of scanner integrations
- Full vulnerability-management systems
- Support for every programming language
- Production SaaS deployment
- Advanced ML-based vulnerability detection
- Generic security scoring

## Future Enhancements

- DAST with OWASP ZAP
- Fuzzing
- Container-image scanning
- SBOM generation
- Additional security checks
- More detailed pull-request reporting

## Status

Planned MVP. Implementation will begin with the sample application, threat model, and first automated security gate.