# SecurePR Security Checks

## Coverage Matrix

| Security concern | Primary control | Automation | Planned demonstration |
|---|---|---|---|
| Public API keys, tokens, passwords, private keys | Gitleaks | Automated | Synthetic secret in a test PR |
| SQL injection | CodeQL / Semgrep + pytest where applicable | Automated | Vulnerable and corrected code |
| Command injection | CodeQL / Semgrep + pytest | Automated | Unsafe command construction |
| Path traversal | CodeQL / Semgrep + pytest | Automated | Unsafe file-path handling |
| Unsafe deserialization | CodeQL / Semgrep + pytest | Automated | Unsafe deserialization pattern |
| SSRF | SAST + pytest where a URL-fetch surface exists | Partial | Controlled server-side request case |
| XSS | SAST + pytest where an output surface exists | Partial | Controlled output-encoding case |
| Authentication / authorization | pytest + SAST | Partial | Security behavior and regression tests |
| Weak security-sensitive cryptography | SAST + review | Automated / review | Insecure crypto pattern |
| Disabled TLS verification | SAST + tests where applicable | Automated / partial | Insecure TLS configuration |
| Vulnerable Python dependencies | pip-audit | Automated | Vulnerable dependency case when safely reproducible |
| Dependency changes | GitHub Dependency Review where supported | Automated | Dependency-changing PR |
| CI token permissions | Workflow checks + review | Automated / review | Permission configuration check |
| Unsafe workflow shell/input handling | Workflow checks + review | Partial | Untrusted PR input case |
| Debug / insecure configuration | SAST + tests + review | Partial | Insecure configuration case |
| Sensitive logging | SAST + pytest | Partial | Sensitive value logging case |
| Error / stack-trace leakage | pytest + SAST | Partial | Error-response regression |
| Fail-open behavior | pytest | Automated | Security control failure case |
| Untrusted data / integrity issues | SAST + pytest | Partial | Unsafe data-flow case |
| Container misconfiguration | Docker checks if Docker is retained | Conditional | Unsafe container configuration |
| Security design weaknesses | Threat model + human review | Manual | Threat-model review |
| Business-logic flaws | Tests + human review | Manual / partial | Requirement-specific case |

## Tool Responsibilities

### CodeQL

Use CodeQL for semantic source-code analysis and data-flow-oriented findings that fit the Python application.

### Semgrep

Use Semgrep for focused, readable rules and project-specific patterns that complement CodeQL.

### Gitleaks

Use Gitleaks for repository secret detection. Only fake demonstration credentials may be committed for testing.

### pip-audit

Use pip-audit to identify known vulnerabilities in Python dependencies.

### GitHub Dependency Review

Use Dependency Review where repository support permits pull-request dependency-diff analysis.

### pytest

Use pytest to verify security behavior that static analysis cannot establish reliably, including authentication, authorization, input validation, error handling, and regression requirements.

### Workflow Security Checks

Review and, where practical, automate checks for least-privilege permissions, unsafe shell interpolation, untrusted pull-request input, secret exposure, workflow triggers, and third-party action usage.

## Coverage Boundary

No individual scanner provides complete vulnerability coverage. SecurePR therefore combines static analysis, secret detection, dependency analysis, security tests, workflow checks, threat modeling, and human review. The project will only claim coverage that is demonstrated by the implemented controls and tests.
