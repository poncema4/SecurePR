# SecurePR Architecture

## 1. System Purpose

SecurePR is a reusable pull-request security gate. The application being changed is the target; SecurePR is the automation that evaluates the change. The Phase 2 Flask application is only the controlled demonstration target used to develop the gate.

## 2. High-Level Flow

```text
Developer
   ↓
Pull Request
   ↓
Repository profiling
   ├── languages
   ├── manifests
   └── applicable checks
   ↓
One SecurePR Security Gate Job
   ├── CodeQL semantic SAST
   ├── Semgrep SAST + SecurePR rules
   ├── Gitleaks
   ├── applicable dependency audit
   ├── project security/correctness tests
   └── normalized SARIF finding aggregation
   ↓
PASS / BLOCK
   ↓
Human review is always recommended
```

## 3. Harness Versus Analysis Engines

SecurePR is the **harness**: it orchestrates tools, determines applicability, enforces blocking policy, normalizes findings, and publishes the final result.

### CodeQL

CodeQL is a semantic static-analysis engine. It builds a representation of supported source code and runs security queries against that representation. It is responsible for deep source-code/data-flow analysis; SecurePR consumes its results rather than reimplementing CodeQL.

### Semgrep

Semgrep provides complementary rule-based SAST. SecurePR also maintains project-specific rules for high-confidence patterns such as hard-coded password/credential values and hard-coded privileged usernames.

### Gitleaks

Gitleaks scans repository history/changes for secret and credential material. SecurePR treats a detected secret as a blocking control and keeps real credentials out of demonstrations.

### Dependency analysis

Dependency tools identify known vulnerabilities in package ecosystems. The MVP applies an audit when a supported dependency manifest is present instead of pretending every repository has Python dependencies.

### Project tests

Project tests verify behavior that static analysis cannot reliably prove. A failing required test blocks the PR.

## 4. Repository Profiling

`scripts/repository_profile.py` detects CodeQL-supported languages and common package manifests while reporting known CodeQL coverage boundaries such as PHP and Scala.

The profile is used to avoid treating an unsupported language as successfully analyzed. Unsupported source extensions produce an explicit coverage warning.

## 5. Finding Aggregation

SARIF-producing SAST tools can report the same underlying issue. `scripts/summarize_sarif.py` normalizes results using tool, rule, file, line, and message so repeated identical reports can be presented as one meaningful finding. Native tool logs remain available for diagnosis.

The aggregator must not collapse distinct findings merely because they share a file.

## 6. Security Decision

Only two outcomes are allowed:

- **PASS:** all configured blocking controls pass and no blocking normalized finding remains.
- **BLOCK:** a configured blocking control fails or a blocking normalized finding remains.

There is no third `REVIEW` state. Both outcomes state that human review is always recommended.

## 7. Trust Boundaries

1. Developer-controlled pull-request changes enter the CI environment.
2. Pull-request source code interacts with GitHub Actions.
3. External dependency metadata and package installation influence analysis.
4. Third-party actions and security tools are part of the CI supply chain.
5. Tool output becomes input to SecurePR's final decision.
6. A reusable workflow must explicitly identify which repository is being analyzed.

## 8. PR and Main Verification

A passing PR is not a guarantee that the post-merge `main` execution will pass. The PR and push-to-main workflows are separate executions. Phase 4 completion therefore requires both a passing consolidated PR and a successful post-merge `main` run.

## 9. MVP Reuse Boundary

The Phase 4 MVP is reusable across the user's own repositories through the reusable workflow. It is intentionally not being packaged for GitHub Marketplace. The design may later support broader distribution without making that a Phase 4 requirement.
