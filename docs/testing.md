# SecurePR Testing Strategy

## 1. Testing Goals

Testing must show that SecurePR can:

1. Detect defined security problems.
2. Block a pull request when a required blocking control fails.
3. Allow a corrected pull request to pass.
4. Produce reproducible results from actual tool execution rather than assumed results.

## 2. Test Levels

### Unit Tests

Test application and security-related functions independently.

### Security Tests

Exercise authentication, authorization, input validation, error handling, and other security properties that scanners cannot reliably prove.

### Integration Tests

Verify interactions between the application, security checks, and gate logic where required.

### Tool Verification

Run CodeQL, Semgrep, Gitleaks, pip-audit, and applicable workflow checks against the actual repository and record their real results.

### Workflow Tests

Verify that GitHub Actions starts on the intended events, executes required controls, and produces the correct PASS/BLOCK behavior.

## 3. Phase 3 Baseline Result

The clean baseline has been verified in GitHub Actions. The five required controls passed, and the explicit Security Gate passed on the Phase 3 implementation pull request.

| Control | Clean baseline / corrected result |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | PASS |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | PASS |

The local Windows PowerShell verification was also executed using `.venv` and produced `8 passed`.

## 4. Phase 3 Vulnerable Demonstration

A separate pull request intentionally committed a synthetic AWS-style access key to `demo/intentional-secret.py`.

The actual workflow result was:

| Control | Vulnerable demonstration |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | FAIL — synthetic secret detected |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | FAIL / BLOCK |

Gitleaks reported the finding under its `aws-access-token` rule. The value was fake and non-sensitive. The failed Secret Detection job caused the Security Gate to fail as designed.

The vulnerable pull request was not merged.

## 5. Phase 3 Corrected Demonstration

A separate clean branch was created from `main` so the corrected demonstration did not retain the vulnerable secret in its commit history. The corrected example used an environment variable rather than committing a credential value.

The actual workflow result was:

| Control | Corrected demonstration |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | PASS |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | PASS |

The corrected pull request was also not merged, preserving a clean `main` baseline.

## 6. Safety Requirements

- Use fake secrets only.
- Never use real API keys, passwords, private keys, tokens, or cloud credentials in demonstrations.
- Keep vulnerable demonstrations limited to the sample application and repository.
- Do not scan or attack production systems.
- Avoid creating vulnerabilities that could affect unrelated users or infrastructure.
- When a secret is detected, do not attempt to reuse it or treat it as a credential.

## 7. Evidence

Verified Phase 3 evidence includes:

- Clean baseline workflow
- Local `.venv` verification result
- Gitleaks secret-detection failure
- Gitleaks finding details for the synthetic AWS-style credential
- `BLOCK` Security Gate result
- Corrected pull-request workflow
- `PASS` Security Gate result
- Relevant GitHub Actions job results and logs

Screenshots can be collected from these completed runs for the final report and presentation.

## 8. Completion Criteria

Phase 1 is complete when requirements, architecture, security coverage, threat model, and testing strategy are documented consistently with the planned MVP.

Phase 2 is complete when the sample application, tests, local setup, and baseline security workflow are implemented and the required baseline controls pass.

Phase 3 is complete when an explicit Security Gate is implemented, an intentionally vulnerable pull request is actually detected and blocked, a corrected pull request actually passes, the clean `main` baseline remains intact, and the documentation reflects the real results. These conditions have now been verified.
