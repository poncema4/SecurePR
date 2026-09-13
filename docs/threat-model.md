# SecurePR Threat Model

## 1. Scope

The threat model covers the sample application, pull-request workflow, GitHub Actions automation, project dependencies, security tools, reusable workflow, repository profiling, finding aggregation, and final security-gate decision.

No real credentials are required or intended to be project assets.

## 2. Assets

- Application source code
- Application security behavior
- Dependency definitions and lock information
- GitHub Actions workflow configuration
- CI permissions and tokens
- Security-tool results
- Security-gate decision
- CI logs and evidence artifacts
- Synthetic demonstration data
- Repository/language applicability information

## 3. Trust Boundaries

### TB-01 — Pull Request to CI

Developer-controlled changes enter an automated CI environment. Pull-request content must not automatically be treated as trusted workflow configuration or shell input.

### TB-02 — Workflow to External Tools

The workflow invokes scanners, dependency services, package managers, and third-party actions. These integrations introduce supply-chain and input-handling considerations.

### TB-03 — Tool Output to Gate

Security-tool results become inputs to the final PASS/BLOCK decision. Exit codes and step outcomes must be interpreted consistently.

### TB-04 — Workflow to GitHub Resources

Actions may have access to repository metadata, pull requests, code-scanning results, or tokens. Permissions should follow least privilege.

### TB-05 — Reusable Workflow to Calling Repository

The reusable workflow executes against the caller repository while obtaining SecurePR tooling from the SecurePR repository. The workflow must clearly distinguish target-repository files from SecurePR tooling files.

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
| T-07 | Vulnerable dependency introduced | Applicable dependency audits |
| T-08 | GitHub Actions workflow abused | Least-privilege permissions, workflow review, and targeted checks |
| T-09 | Sensitive information exposed through logs or errors | SAST and security tests |
| T-10 | Supply-chain risk in automation or dependencies | Dependency controls, action review, and least privilege |
| T-11 | Unsupported language silently treated as secure | Repository profiler and explicit coverage boundary |
| T-12 | Duplicate scanner findings overwhelm the developer | Conservative SARIF normalization |
| T-13 | Reusable workflow analyzes the wrong repository | Explicit target checkout and tooling checkout separation |
| T-14 | Scanner false positive or false negative | Controlled final benchmark and human review |
| T-15 | PR passes but resulting main state differs | Independent post-merge main workflow |

## 6. Phase 3 Assessment

Phase 3 security-gate behavior was demonstrated with actual pull requests and then independently verified on the resulting `main` state. The controlled synthetic secret was detected and blocked, while the corrected demonstration passed.

## 7. Phase 4 Assessment Boundary

Phase 4 expands the model to repository portability and multi-language analysis. The project will not claim that unsupported languages, design-level issues, or business-logic weaknesses are automatically proven safe.

Final Phase 4 validation must measure false positives and false negatives using TP, FP, TN, FN, precision, recall, and F1 on a defined benchmark corpus.

## 8. Risk Treatment

SecurePR prioritizes threats that can be checked repeatedly in CI. Intentionally vulnerable demonstrations use synthetic data and controlled code changes only. The project does not target production systems or real credentials.

Context-dependent issues, especially business logic and some authorization/design decisions, remain subject to human review and threat modeling. Human review is always recommended even after a PASS.
