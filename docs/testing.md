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

## 3. Phase 2 Baseline Result

The clean baseline has now been executed in GitHub Actions on `main`.

The latest baseline run completed successfully with all five current jobs passing:

| Control | Result |
|---|---|
| Security Tests | PASS |
| Gitleaks Secret Detection | PASS |
| Semgrep SAST | PASS |
| pip-audit Dependency Audit | PASS |
| CodeQL | PASS |

This is a verified baseline result, not a predicted result. The local verification scripts are also part of the Phase 2 implementation so the application tests and Python compilation can be reproduced on Linux/macOS and Windows.

## 4. Required Demonstration Sequence

The security demonstrations will now proceed from the verified clean baseline:

1. Preserve the clean `main` baseline.
2. Create a separate demonstration branch.
3. Introduce one controlled, intentionally vulnerable change using synthetic/non-sensitive data.
4. Open a pull request against `main`.
5. Verify that the expected security control detects the issue.
6. Verify that the security gate produces `BLOCK` or an equivalent failed required check.
7. Capture evidence of the finding and gate decision without exposing sensitive data.
8. Correct the vulnerability on the demonstration branch.
9. Re-run the workflow on the corrected pull request.
10. Verify that the required controls pass and the gate produces `PASS` or an equivalent successful required check.
11. Capture evidence and update this document, the README, and the other project documentation with the actual results.

The vulnerable and corrected demonstrations will be kept separate from the clean baseline so `main` remains a known-good starting point.

## 5. Safety Requirements

- Use fake secrets only.
- Never use real API keys, passwords, private keys, tokens, or cloud credentials in demonstrations.
- Keep vulnerable demonstrations limited to the sample application and repository.
- Do not scan or attack production systems.
- Avoid creating vulnerabilities that could affect unrelated users or infrastructure.

## 6. Evidence

Planned evidence includes:

- Successful baseline workflow
- Local verification result
- Secret-detection failure
- SAST finding
- Dependency finding where safely reproducible
- Security-test result
- `BLOCK` gate result
- Corrected `PASS` result
- Relevant GitHub Actions logs
- Screenshots or exported results needed for the final report/presentation

Evidence will only be collected after the corresponding control has actually been executed.

## 7. Completion Criteria

Phase 1 is complete when requirements, architecture, security coverage, threat model, and testing strategy are documented consistently with the planned MVP.

Phase 2 baseline implementation is complete when the sample application, tests, local setup, and baseline security workflow are implemented and the required baseline controls pass. That baseline has now been verified.

The security-gate demonstration portion of Phase 2 is not considered complete until an intentionally vulnerable pull request is actually detected and blocked, a corrected version actually passes, evidence is collected, and the documentation reflects those real results.
