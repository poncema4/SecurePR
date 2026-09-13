# SecurePR Security Checks

## Coverage Matrix

| Security concern | Primary control | Automation | Phase 2 status |
|---|---|---|---|
| Public API keys, tokens, passwords, private keys | Gitleaks | Automated | Baseline scanner verified; vulnerable-PR demonstration next |
| SQL injection | CodeQL / Semgrep + pytest where applicable | Automated / partial | Tooling enabled; demonstration next where application surface supports it |
| Command injection | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; demonstration next |
| Path traversal | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; demonstration next |
| Unsafe deserialization | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; demonstration next |
| SSRF | SAST + pytest where a URL-fetch surface exists | Partial | Conditional on application surface |
| XSS | SAST + pytest where an output surface exists | Partial | Conditional on application surface |
| Authentication / authorization | pytest + SAST | Partial | Baseline application/tests implemented |
| Weak security-sensitive cryptography | SAST + review | Automated / review | Planned demonstration |
| Disabled TLS verification | SAST + tests where applicable | Automated / partial | Planned demonstration where meaningful |
| Vulnerable Python dependencies | pip-audit | Automated | Baseline audit verified |
| Dependency changes | GitHub Dependency Review where supported | Automated | Conditional / planned |
| CI token permissions | Workflow checks + review | Automated / review | Workflow permissions implemented; targeted validation next |
| Unsafe workflow shell/input handling | Workflow checks + review | Partial | Targeted validation next |
| Debug / insecure configuration | SAST + tests + review | Partial | Baseline configuration is implemented; targeted cases next |
| Sensitive logging | SAST + pytest | Partial | Planned demonstration |
| Error / stack-trace leakage | pytest + SAST | Partial | Baseline error handling is tested; targeted case next |
| Fail-open behavior | pytest | Automated | Planned demonstration |
| Untrusted data / integrity issues | SAST + pytest | Partial | Tooling/tests provide the foundation; targeted case next |
| Container misconfiguration | Docker checks if Docker is retained | Conditional | Docker is not currently required |
| Security design weaknesses | Threat model + human review | Manual | Threat model documented |
| Business-logic flaws | Tests + human review | Manual / partial | Requires requirement-specific tests/review |

## Tool Responsibilities

### CodeQL

Use CodeQL for semantic source-code analysis and data-flow-oriented findings that fit the Python application. The Phase 2 baseline CodeQL job has completed successfully.

### Semgrep

Use Semgrep for focused, readable rules and project-specific patterns that complement CodeQL. The Phase 2 baseline Semgrep job has completed successfully.

### Gitleaks

Use Gitleaks for repository secret detection. Only fake demonstration credentials may be committed for testing. The Phase 2 baseline secret scan has completed successfully.

### pip-audit

Use pip-audit to identify known vulnerabilities in Python dependencies. The Phase 2 baseline audit now passes with the current dependency requirements.

### GitHub Dependency Review

Use Dependency Review where repository support permits pull-request dependency-diff analysis. This remains conditional until it is configured and demonstrated.

### pytest

Use pytest to verify security behavior that static analysis cannot establish reliably, including authentication, authorization, input validation, error handling, and regression requirements. The baseline tests pass in CI.

### Workflow Security Checks

Review and, where practical, automate checks for least-privilege permissions, unsafe shell interpolation, untrusted pull-request input, secret exposure, workflow triggers, and third-party action usage. The baseline workflow uses restricted repository permissions and will be tested further with pull-request demonstrations.

## Phase 2 Demonstration Plan

The next stage will use separate pull-request branches to introduce controlled vulnerabilities one at a time. The purpose is to verify that the expected control actually detects the issue rather than assuming that a scanner will catch it.

Planned demonstrations include a synthetic secret exposure and selected source-code vulnerabilities that have a meaningful surface in the sample application. Each demonstration will record the actual finding, failing check, and remediation.

## Coverage Boundary

No individual scanner provides complete vulnerability coverage. SecurePR therefore combines static analysis, secret detection, dependency analysis, security tests, workflow checks, threat modeling, and human review. The project will only claim coverage that is demonstrated by the implemented controls and tests.
