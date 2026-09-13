# SecurePR Threat Model

## 1. Scope

The threat model covers the sample application, pull-request workflow, GitHub Actions automation, project dependencies, security tools, and the final security-gate decision.

No real credentials are required or intended to be project assets.

## 2. Assets

- Application source code
- Application security behavior
- Dependency definitions and lock information, where used
- GitHub Actions workflow configuration
- CI permissions and tokens
- Security-tool results
- Security-gate decision
- CI logs and evidence artifacts
- Synthetic demonstration data

## 3. Trust Boundaries

### TB-01 — Pull Request to CI

Developer-controlled changes enter an automated CI environment. Pull-request content must not automatically be treated as trusted workflow configuration or shell input.

### TB-02 — Workflow to External Tools

The workflow invokes scanners, dependency services, package managers, and third-party actions. These integrations introduce supply-chain and input-handling considerations.

### TB-03 — Tool Output to Gate

Security-tool results become inputs to the final PASS/BLOCK decision. Exit codes and step outcomes must be interpreted consistently.

### TB-04 — Workflow to GitHub Resources

Actions may have access to repository metadata, pull requests, code-scanning results, or tokens. Permissions should follow least privilege.

## 4. STRIDE Analysis

| STRIDE category | SecurePR example |
|---|---|
| Spoofing | Malicious or unauthorized workflow/action behavior presented as trusted automation |
| Tampering | Pull-request code or workflow changes altering security checks |
| Repudiation | Lack of reliable CI results or evidence for a gate decision |
| Information Disclosure | Secrets or sensitive values exposed in source, logs, artifacts, or scanner output |
| Denial of Service | Malicious changes causing resource-intensive scans or dependency operations |
| Elevation of Privilege | Excessive GitHub token permissions or unsafe workflow execution |

## 5. Threats and Treatments

| ID | Threat | Primary treatment |
|---|---|---|
| T-01 | Secret committed to the repository | Gitleaks and synthetic-secret tests |
| T-02 | Injection vulnerability introduced in source code | CodeQL / Semgrep and pytest |
| T-03 | Unsafe deserialization introduced | SAST and security tests |
| T-04 | Path traversal introduced | SAST and security tests |
| T-05 | Authentication or authorization failure | Security tests, SAST, and human review |
| T-06 | Weak or unsafe cryptographic use | SAST and review |
| T-07 | Vulnerable dependency introduced | pip-audit and dependency review |
| T-08 | GitHub Actions workflow abused | Least-privilege permissions, workflow review, and targeted checks |
| T-09 | Sensitive information exposed through logs or errors | SAST and security tests |
| T-10 | Supply-chain risk in automation or dependencies | Dependency controls, action review, and least privilege |

## 6. Phase 3 Assessment

The Phase 3 security-gate behavior was demonstrated with actual pull requests and then independently verified on the resulting `main` state.

### T-01 — Secret committed

A controlled synthetic AWS-style access key was introduced on a separate vulnerable demonstration branch. Gitleaks detected the value under `aws-access-token`, the Secret Detection step failed, and the overall SecurePR gate returned `BLOCK`. No real credential was used.

A separate corrected demonstration branch used an environment variable instead of committing a credential. The configured controls passed and the SecurePR gate returned `PASS`.

### Gate integrity

The final workflow uses one `SecurePR Security Gate` job. Its security controls are separate steps within that job, and the final result step evaluates their outcomes. A failure of any configured blocking step produces `BLOCK`; successful completion of all configured controls produces `PASS`.

CodeQL also uploads its analysis results to GitHub Code Scanning. This is an additional reporting surface, not a second SecurePR job or required SecurePR status check.

The remaining threats in this model have not all been individually demonstrated. Their controls remain subject to future targeted tests, scanner findings, threat-model review, or human review as appropriate.

## 7. Risk Treatment

SecurePR prioritizes threats that can be checked repeatedly in CI. Intentionally vulnerable demonstrations use synthetic data and controlled code changes only. The project does not target production systems or real credentials.

Context-dependent issues, especially business logic and some authorization/design decisions, remain subject to human review and threat modeling.
