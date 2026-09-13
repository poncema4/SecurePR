# SecurePR Security Checks

## Coverage Matrix

| Security concern | Primary control | Automation | Phase 3 status |
|---|---|---|---|
| Public API keys, tokens, passwords, private keys | Gitleaks | Automated | Synthetic AWS-style secret detected and blocked |
| SQL injection | CodeQL / Semgrep + pytest where applicable | Automated / partial | Tooling enabled; not specifically demonstrated in Phase 3 |
| Command injection | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; not specifically demonstrated in Phase 3 |
| Path traversal | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; not specifically demonstrated in Phase 3 |
| Unsafe deserialization | CodeQL / Semgrep + pytest | Automated / partial | Tooling enabled; not specifically demonstrated in Phase 3 |
| SSRF | SAST + pytest where a URL-fetch surface exists | Partial | Conditional on application surface |
| XSS | SAST + pytest where an output surface exists | Partial | Conditional on application surface |
| Authentication / authorization | pytest + SAST | Partial | Baseline application/tests implemented and passing |
| Weak security-sensitive cryptography | SAST + review | Automated / review | Not specifically demonstrated in Phase 3 |
| Disabled TLS verification | SAST + tests where applicable | Automated / partial | Not specifically demonstrated in Phase 3 |
| Vulnerable Python dependencies | pip-audit | Automated | Baseline and corrected demonstration verified |
| Dependency changes | GitHub Dependency Review where supported | Automated | Conditional / not yet demonstrated |
| CI token permissions | Workflow checks + review | Automated / review | Workflow permissions implemented and reviewed |
| Unsafe workflow shell/input handling | Workflow checks + review | Partial | Not specifically demonstrated in Phase 3 |
| Debug / insecure configuration | SAST + tests + review | Partial | Baseline configuration verified; broader cases remain |
| Sensitive logging | SAST + pytest | Partial | Not specifically demonstrated in Phase 3 |
| Error / stack-trace leakage | pytest + SAST | Partial | Baseline error handling tested |
| Fail-open behavior | pytest | Automated | Not specifically demonstrated in Phase 3 |
| Untrusted data / integrity issues | SAST + pytest | Partial | Tooling/tests provide the foundation |
| Container misconfiguration | Docker checks if Docker is retained | Conditional | Docker is not currently required |
| Security design weaknesses | Threat model + human review | Manual | Threat model documented |
| Business-logic flaws | Tests + human review | Manual / partial | Requires requirement-specific tests/review |

## Tool Responsibilities

### CodeQL

Use CodeQL for semantic source-code analysis and data-flow-oriented findings that fit the Python application. Phase 3 verified a successful clean run in both the vulnerable-secret and corrected demonstrations.

### Semgrep

Use Semgrep for focused, readable rules and project-specific patterns that complement CodeQL. Phase 3 verified successful runs for both demonstrations.

### Gitleaks

Use Gitleaks for repository secret detection. The Phase 3 vulnerable demonstration used a synthetic AWS-style access key that Gitleaks detected with its `aws-access-token` rule. The Secret Detection job failed as intended, and the Security Gate subsequently blocked the pull request.

### pip-audit

Use pip-audit to identify known vulnerabilities in Python dependencies. The baseline and corrected demonstration runs passed with the current dependency requirements.

### GitHub Dependency Review

Use Dependency Review where repository support permits pull-request dependency-diff analysis. This remains conditional until it is configured and demonstrated.

### pytest

Use pytest to verify security behavior that static analysis cannot establish reliably, including authentication, authorization, input validation, error handling, and regression requirements. The baseline and demonstration runs passed.

### Workflow Security Checks

Review and, where practical, automate checks for least-privilege permissions, unsafe shell interpolation, untrusted pull-request input, secret exposure, workflow triggers, and third-party action usage. Phase 3 verified the gate behavior and reviewed workflow permissions; broader workflow-security demonstrations remain future work.

## Phase 3 Demonstration

The secret-detection demonstration was performed on a separate branch so the clean `main` baseline remained intact.

### Vulnerable demonstration

A synthetic AWS-style access key was committed to `demo/intentional-secret.py`. Gitleaks detected it under `aws-access-token`, the Secret Detection job failed, and the Security Gate failed.

### Corrected demonstration

A separate clean branch from `main` used an environment variable instead of a committed credential. Secret Detection, Security Tests, Semgrep, pip-audit, CodeQL, and the Security Gate all passed.

The vulnerable and corrected pull requests were both left unmerged.

## Coverage Boundary

No individual scanner provides complete vulnerability coverage. SecurePR therefore combines static analysis, secret detection, dependency analysis, security tests, workflow checks, threat modeling, and human review. The project only claims coverage that is demonstrated by the implemented controls and tests.
