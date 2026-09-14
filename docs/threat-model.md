# SecurePR Threat Model

## Scope
The threat model covers the sample application, pull-request workflow, GitHub Actions automation, project dependencies, multiple security engines, reusable workflow, repository profiling, finding aggregation, accuracy reporting, and final security-gate decision.

SecurePR itself is the **harness and policy layer**. CodeQL, Semgrep, Gitleaks, dependency auditors, and project tests are separate evidence-producing components under that harness.

No real credentials are required or intended to be project assets.

## Assets

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
- Controlled accuracy benchmark results

## Trust Boundaries

### TB-01 — Pull Request to CI
Developer-controlled changes enter an automated CI environment. Pull-request content must not automatically be treated as trusted workflow configuration or shell input.

### TB-02 — Workflow to Security Engines
The harness invokes scanners, dependency services, package managers, and third-party actions. These integrations introduce supply-chain and input-handling considerations.

### TB-03 — Tool Output to Gate
Security-tool results become inputs to the final PASS/BLOCK decision. Exit codes, findings, and step outcomes must be interpreted consistently.

### TB-04 — Workflow to GitHub Resources
Actions may have access to repository metadata, pull requests, code-scanning results, or tokens. Permissions should follow least privilege.

### TB-05 — Reusable Workflow to Calling Repository
The reusable workflow executes against the caller repository while obtaining SecurePR tooling from an intentional SecurePR ref. The workflow must clearly distinguish target-repository files from SecurePR tooling files.

### TB-06 — Benchmark Results to Accuracy Claims
Benchmark data influences reported precision, recall, F1, and classification accuracy. The benchmark must contain independently labeled cases and must not be presented as universal detection accuracy.

## STRIDE Analysis

| STRIDE category | SecurePR example |
|---|---|
| Spoofing | Malicious or unauthorized workflow/action behavior presented as trusted automation |
| Tampering | Pull-request code or workflow changes altering security checks |
| Repudiation | Lack of reliable CI results or evidence for a gate decision |
| Information Disclosure | Secrets or sensitive values exposed in source, logs, artifacts, or scanner output |
| Denial of Service | Malicious changes causing resource-intensive scans or dependency operations |
| Elevation of Privilege | Excessive GitHub token permissions or unsafe workflow execution |

## Threats and Treatments

| ID | Threat | Primary treatment |
|---|---|---|
| T-01 | Secret committed to the repository | Gitleaks and synthetic-secret tests |
| T-02 | Injection vulnerability introduced in source code | CodeQL / Semgrep and security tests |
| T-03 | Unsafe deserialization introduced | SAST and security tests |
| T-04 | Path traversal introduced | SAST and security tests |
| T-05 | Authentication or authorization failure | Security tests, SAST, and human review |
| T-06 | Weak or unsafe cryptographic use | SAST and review |
| T-07 | Vulnerable dependency introduced | Applicable dependency audits |
| T-08 | GitHub Actions workflow abused | Least-privilege permissions, workflow review, and targeted checks |
| T-09 | Sensitive information exposed through logs or errors | SAST and security tests |
| T-10 | Supply-chain risk in automation or dependencies | Dependency controls, action review, and least privilege |
| T-11 | Unsupported language silently treated as secure | Repository profiler and explicit coverage boundary |
| T-12 | Duplicate scanner findings overwhelm the developer | Conservative SARIF aggregation in detailed evidence |
| T-13 | Reusable workflow analyzes the wrong repository | Explicit target checkout and tooling checkout separation |
| T-14 | Scanner false positive or false negative | Controlled benchmark and human review |
| T-15 | PR passes but resulting main state differs | Independent post-merge main workflow |
| T-16 | Accuracy claim is made before measurement | Per-PR benchmark status and controlled benchmark |

## Security-Gate Assessment

The gate has been validated through pull-request executions and independent post-merge verification. Controlled synthetic demonstrations are used for blocking and passing behavior; real credentials are never required.

The MVP expands this model to repository portability, multi-language analysis, multiple underlying security engines, finding aggregation, and empirical accuracy measurement. It does not claim that unsupported languages, design-level issues, or business-logic weaknesses are automatically proven safe.

The current controlled benchmark contains 26 labeled cases: 10 TP, 0 FP, 11 TN, and 5 FN. This produces 80.77% conventional classification accuracy, 100% precision, 66.67% recall, and 80.00% F1 for the controlled corpus only.

## Risk Treatment

SecurePR prioritizes threats that can be checked repeatedly in CI. Intentionally vulnerable demonstrations use synthetic data and controlled code changes only. The project does not target production systems or real credentials.

Context-dependent issues, especially business logic and some authorization/design decisions, remain subject to human review and threat modeling. Human review is always recommended even after a PASS.
