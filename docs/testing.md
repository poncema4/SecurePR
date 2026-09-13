# SecurePR Testing Strategy

## 1. Testing Goals

Testing must show that SecurePR can:

1. Detect defined security problems.
2. Block a pull request when a required blocking control fails.
3. Allow a corrected pull request to pass.
4. Produce reproducible results from actual tool execution rather than assumed results.
5. Produce one clear overall PR decision while preserving detailed tool logs for diagnosis.

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

Verify that GitHub Actions starts on the intended events, executes required controls, produces one overall PASS/BLOCK result, and preserves enough step-level detail to diagnose a failure.

## 3. Phase 3 Baseline Result

The earlier clean baseline was verified in GitHub Actions. The five required controls passed, and the explicit Security Gate passed on the Phase 3 implementation pull request.

| Control | Clean baseline / corrected result |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | PASS |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | PASS |

The local Windows PowerShell verification was also executed using `.venv` and produced `8 passed`.

After the Phase 3 refinement, the workflow is being re-verified with one consolidated job before Phase 3 is declared complete.

## 4. Phase 3 Vulnerable Demonstration

A separate pull request intentionally committed a synthetic AWS-style access key to `demo/intentional-secret.py`.

The actual earlier workflow result was:

| Control | Vulnerable demonstration |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | FAIL — synthetic secret detected |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | FAIL / BLOCK |

Gitleaks reported the finding under its `aws-access-token` rule. The value was fake and non-sensitive. The failed Secret Detection control caused the Security Gate to block as designed.

The vulnerable pull request was not merged.

## 5. Phase 3 Corrected Demonstration

A separate clean branch was created from `main` so the corrected demonstration did not retain the vulnerable secret in its commit history. The corrected example used an environment variable rather than committing a credential value.

The actual earlier workflow result was:

| Control | Corrected demonstration |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | PASS |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |
| Security Gate | PASS |

The corrected pull request was also not merged, preserving a clean `main` baseline.

## 6. Accuracy and False-Positive / False-Negative Testing

SecurePR does not claim perfect detection accuracy.

A false positive is a finding where a scanner reports a suspicious pattern that is actually safe. A false negative is a vulnerability that exists but is not detected by the configured controls. Both matter to a security gate.

Phase 3 handles this by:

- Layering Gitleaks, Semgrep, CodeQL, pip-audit, and pytest rather than relying on one tool.
- Using controlled vulnerable examples to verify that an expected finding is actually blocked.
- Using corrected examples to verify that a safe remediation passes.
- Keeping real secrets out of demonstrations.
- Treating a blocking scanner result as a review requirement, not as proof that the scanner is infallible.
- Requiring human review for business logic, design decisions, and findings that may be false positives.

A passing SecurePR result means the configured checks passed. It does not prove that the application has zero vulnerabilities.

## 7. Remediation and Merge Safety

SecurePR does not automatically edit the PR or merge it into `main`.

The intended remediation loop is:

```text
Finding
  ↓
SecurePR reports the failed control
  ↓
Developer/reviewer inspects the finding
  ↓
Fix is committed to the PR
  ↓
SecurePR runs again
  ↓
PASS → eligible for normal human merge review
BLOCK → investigate and fix
```

This avoids silently applying an incorrect fix to a false positive and avoids automatically merging code that has not received human review.

If an explicit remediation-assistance feature is added later, it must require a user action and the resulting change must pass SecurePR before it can be merged.

## 8. Safety Requirements

- Use fake secrets only.
- Never use real API keys, passwords, private keys, tokens, or cloud credentials in demonstrations.
- Keep vulnerable demonstrations limited to the sample application and repository.
- Do not scan or attack production systems.
- Avoid creating vulnerabilities that could affect unrelated users or infrastructure.
- When a secret is detected, do not attempt to reuse it or treat it as a credential.

## 9. Evidence

Verified Phase 3 evidence includes:

- Clean baseline workflow
- Local `.venv` verification result
- Gitleaks secret-detection failure
- Gitleaks finding details for the synthetic AWS-style credential
- `BLOCK` Security Gate result
- Corrected pull-request workflow
- `PASS` Security Gate result
- Relevant GitHub Actions job results and logs
- Post-refinement consolidated gate run

Screenshots can be collected from these completed runs for the final report and presentation.

## 10. Completion Criteria

Phase 1 is complete when requirements, architecture, security coverage, threat model, and testing strategy are documented consistently with the planned MVP.

Phase 2 is complete when the sample application, tests, local setup, and baseline security workflow are implemented and the required baseline controls pass.

Phase 3 is complete when:

- One consolidated Security Gate job runs the required controls.
- The pull request receives one clear PASS/BLOCK result.
- A failed control is still visible with enough step-level detail to diagnose it.
- An intentionally vulnerable pull request is actually detected and blocked.
- A corrected pull request actually passes.
- The workflow does not automatically modify or merge source code.
- False-positive and false-negative limitations are documented honestly.
- The clean `main` baseline remains intact.
- Temporary demonstration branches are removed after testing.
- The final post-refinement `main` workflow passes.

The first nine conditions have been addressed; the final post-refinement workflow run is the remaining verification step before Phase 3 is declared complete.
