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
| CI token permissions | Workflow checks + review | Automated / review | Least-privilege workflow permissions implemented and reviewed |
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

Use CodeQL for semantic source-code analysis and data-flow-oriented findings that fit the Python application. CodeQL results are uploaded to GitHub Code Scanning. A successful analysis step means the analysis completed successfully; it is not, by itself, proof that no CodeQL finding exists. Phase 3 uses CodeQL as a complementary control rather than claiming complete vulnerability coverage.

### Semgrep

Use Semgrep for focused, readable rules and project-specific patterns that complement CodeQL. A blocking Semgrep result fails the SecurePR gate. Phase 3 verified successful runs for the clean and corrected demonstrations.

### Gitleaks

Use Gitleaks for repository secret detection. The Phase 3 vulnerable demonstration used a synthetic AWS-style access key that Gitleaks detected with its `aws-access-token` rule. The Secret Detection control failed as intended, and the SecurePR gate blocked the demonstration.

PR comments from the Gitleaks action are disabled in the consolidated workflow so SecurePR can present one concise overall result instead of producing an additional notification for the same finding. The detailed Gitleaks output remains in the Actions step logs.

### pip-audit

Use pip-audit to identify known vulnerabilities in Python dependencies. A failed audit blocks the SecurePR gate.

### GitHub Dependency Review

Use Dependency Review where repository support permits pull-request dependency-diff analysis. This remains conditional until it is configured and demonstrated.

### pytest

Use pytest to verify security behavior that static analysis cannot establish reliably, including authentication, authorization, input validation, error handling, and regression requirements. A failed test blocks the SecurePR gate.

### Workflow Security Checks

Review and, where practical, automate checks for least-privilege permissions, unsafe shell interpolation, untrusted pull-request input, secret exposure, workflow triggers, and third-party action usage. Phase 3 verifies the workflow permissions and keeps the gate workflow read-oriented except for CodeQL result upload requirements.

## Gate Design

The Phase 3 refinement uses **one GitHub Actions job** containing separate security-check steps rather than five independent jobs.

This is intentional:

- The checks remain logically separated and easy to inspect in the Actions log.
- The tools can still execute independently within the job.
- The pull request receives one overall SecurePR check instead of several job-level pass/fail checks.
- A final result step evaluates the required controls and writes one short PASS/BLOCK summary.
- The summary includes a table showing each control, its result, what it checks, and a link to the full Actions run.
- Failed controls remain visible in their individual step logs for diagnosis.
- Workflow concurrency cancels an obsolete run when a newer commit is pushed to the same PR, reducing redundant CI work.

The gate is conservative: a required control failure results in BLOCK. That reduces the chance that an obvious vulnerability passes silently, but it can increase false positives. A blocking result therefore means **review required**, not **scanner proved malicious code**.

## Accuracy Boundary

SecurePR does not claim perfect accuracy. False positives can occur when a tool matches a safe pattern, and false negatives can occur when a vulnerability is outside a tool's rules, requires runtime behavior, depends on business logic, or is otherwise difficult to observe statically.

Accuracy is addressed through layered controls and controlled validation rather than a single scanner score:

1. Use multiple complementary tools rather than one detector.
2. Use pytest for security behavior that static analysis cannot prove.
3. Validate the gate with known vulnerable and corrected examples.
4. Keep real credentials out of test cases.
5. Require human review for findings and design-level security decisions.
6. Avoid automatically dismissing findings merely because another scanner passes.

A future phase can add more targeted vulnerable/corrected demonstrations for selected SAST findings and dependency cases. Those demonstrations should be real, reproducible tests rather than claims of theoretical coverage.

## Remediation Policy

SecurePR reports the failed control and leaves the source-code change to the pull-request author or reviewer. It does not automatically edit files or merge a PR.

This is a security boundary, not a missing feature: automated remediation can introduce a new defect, choose the wrong fix for a false positive, or make a security decision without human review. If remediation assistance is added later, it should be explicit and user-triggered, and the resulting changes should return through the same SecurePR gate before merge.

## Phase 3 Demonstration

The secret-detection demonstration was performed on a separate branch so the clean `main` baseline remained intact.

### Vulnerable demonstration

A synthetic AWS-style access key was committed to `demo/intentional-secret.py`. Gitleaks detected it under `aws-access-token`, the Secret Detection control failed, and the SecurePR gate failed.

### Corrected demonstration

A separate clean branch from `main` used an environment variable instead of a committed credential. Secret Detection, Security Tests, Semgrep, pip-audit, CodeQL, and the gate all passed.

The vulnerable and corrected pull requests were both left unmerged and their temporary branches were cleaned up. Only `main` is intended to remain after Phase 3 testing.

## Coverage Boundary

No individual scanner provides complete vulnerability coverage. SecurePR therefore combines static analysis, secret detection, dependency analysis, security tests, workflow checks, threat modeling, and human review. The project only claims coverage that is demonstrated by the implemented controls and tests.
