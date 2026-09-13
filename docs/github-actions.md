# GitHub Actions and SecurePR Security Gate

## Purpose

SecurePR uses GitHub Actions to run the project's automated security controls whenever a pull request targets `main` and whenever a new commit is pushed to `main`. The workflow is designed to provide one authoritative PR gate while keeping the individual security tools visible in the Actions log.

The workflow is defined in `.github/workflows/security.yml`.

## Workflow architecture

Phase 3 uses **one GitHub Actions job** named `SecurePR Security Gate`. The security tools are separate steps inside that job rather than separate jobs.

The current sequence is:

1. **Checkout repository** — retrieves the repository, including history needed by security tooling.
2. **Set up Python** — uses Python 3.12 for the CI environment.
3. **Python runtime policy** — verifies that the repository's declared/resolved runtime is within SecurePR's supported Python policy.
4. **Install project dependencies** — installs the dependencies declared in `requirements.txt`.
5. **Security tests** — runs the pytest security test suite and Python compilation checks.
6. **Secret detection** — runs Gitleaks to look for committed credentials and other secret material.
7. **Semgrep SAST** — runs Semgrep Python/security rules to identify source-code security patterns.
8. **Dependency audit** — runs `pip-audit` against the declared Python dependencies.
9. **CodeQL analysis** — initializes CodeQL with the Python language and the `security-extended` query set.
10. **Perform CodeQL analysis** — completes the CodeQL analysis and uploads the results to GitHub's code-scanning system.
11. **Publish SecurePR result** — evaluates the configured control outcomes and publishes the final PASS/BLOCK summary.

The gate is conservative: a failure of a required control results in `BLOCK`. SecurePR does not automatically modify source code, rotate credentials, dismiss findings, or merge a pull request.

## SecurePR Security Gate vs. CodeQL Code Scanning

These are related, but they are **not two SecurePR jobs**.

### SecurePR Security Gate

`SecurePR Security Gate` is the project's authoritative required status check for protected `main`. It evaluates the outcomes of the configured controls and produces the final overall PASS or BLOCK result.

The required branch rule is tied to this one job. The goal is to give a pull request one clear merge-gating result instead of requiring every security tool to appear as an independent required check.

### CodeQL

CodeQL is one of the security-analysis controls executed inside the SecurePR job. It performs semantic source-code analysis for the Python application and uploads its analysis results to **GitHub Code Scanning**.

GitHub Code Scanning is therefore an additional reporting and analysis surface for CodeQL results. Seeing a CodeQL or Code Scanning result in the GitHub interface does **not** mean that SecurePR created a second job.

A successful CodeQL analysis step means the configured analysis completed successfully. It is not proof that the application contains no vulnerabilities. CodeQL findings still require review and remediation when applicable.

## Why GitHub displays `SecurePR Security Gate / SecurePR Security Gate`

GitHub displays workflow and job names together in some pull-request status views. The first name identifies the workflow, while the second identifies the job inside that workflow.

SecurePR intentionally uses the same name for both:

```text
Workflow: SecurePR Security Gate
Job:      SecurePR Security Gate
```

This can appear as:

```text
SecurePR Security Gate / SecurePR Security Gate (pull_request)
```

This does **not** represent two security-gate jobs. The workflow contains one job, and all of the individual security controls run as steps within that job.

## Pull-request checks and post-merge checks

The workflow has two triggers:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

The `pull_request` trigger validates a proposed change before it is merged into `main`. This is the run that satisfies the required `SecurePR Security Gate` branch rule.

The `push` trigger runs again when a commit reaches `main`. This second run is intentional. It verifies the actual resulting `main` branch state after the merge rather than relying only on the earlier PR revision.

Therefore, a normal successful merge can produce two relevant workflow runs:

```text
Pull request
    ↓
SecurePR Security Gate
    ↓
PASS
    ↓
PR may be merged
    ↓
commit reaches main
    ↓
SecurePR Security Gate runs again
    ↓
main is independently verified
```

The workflow also uses concurrency cancellation so obsolete runs for the same PR/ref can be cancelled when a newer change supersedes them.

## PASS and BLOCK behavior

### PASS

A PASS means all configured required controls completed successfully for that run. The final summary reports the check results and states that no blocking fixes are required. Human review is still required before merge.

### BLOCK

A BLOCK means at least one configured required control did not pass. The final summary identifies the failed control and provides:

- why the control failed;
- why the result matters;
- what the developer should fix;
- the expected result after the fix; and
- the remediation policy and accuracy boundary.

The developer then fixes the pull request and pushes the change. SecurePR runs again against the updated revision.

## Typical development workflow

SecurePR does not require a separate pull request for every commit. For normal Phase 4 and later development, work should be completed and tested on a feature branch first. Multiple related commits can be made on that branch, followed by one consolidated pull request into `main`.

Recommended workflow:

```text
feature branch
    ↓
implement related changes
    ↓
run local tests and security checks
    ↓
open one consolidated PR
    ↓
SecurePR Security Gate
    ↓
PASS → review and merge
BLOCK → fix and rerun
```

This keeps the pull-request history focused while still using SecurePR as the final automated security gate before merge.

## Phase 3 validation

Phase 3 was validated with both a known-bad synthetic example and a clean example.

- A vulnerable PR containing a synthetic AWS-style credential pattern was detected by Gitleaks and produced a final SecurePR BLOCK. An attempted merge was rejected because the required `SecurePR Security Gate` check was failing.
- A clean PR from the final protected `main` baseline passed the configured controls and was recognized by GitHub as mergeable.

These tests demonstrate both the intended PASS/BLOCK behavior and actual protected-branch enforcement. The synthetic secret was not a real credential and was not merged into `main`.

## Accuracy and security boundary

SecurePR is a layered security gate, not a proof that a repository is vulnerability-free. Static analysis and secret detection can produce false positives and can miss vulnerabilities involving runtime behavior, business logic, configuration, unavailable code paths, or patterns outside a tool's coverage.

A PASS means the configured automated controls passed for that revision. It does not eliminate the need for human review, secure design review, dependency judgment, or application-specific testing.

SecurePR deliberately does not perform automatic remediation or automatic merging. Security findings and code changes remain subject to developer and reviewer judgment.
