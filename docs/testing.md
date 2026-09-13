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

## 3. Required Demonstration Sequence

1. Establish a clean baseline that passes the required controls.
2. Create a pull request containing a controlled, intentionally vulnerable change.
3. Verify that the expected security control detects the issue.
4. Verify that the security gate produces `BLOCK`.
5. Capture evidence of the finding and gate decision without exposing sensitive data.
6. Correct the vulnerability.
7. Re-run the workflow on the corrected pull request.
8. Verify that the required controls pass and the gate produces `PASS`.
9. Capture evidence and update documentation with the actual results.

## 4. Safety Requirements

- Use fake secrets only.
- Never use real API keys, passwords, private keys, tokens, or cloud credentials in demonstrations.
- Keep vulnerable demonstrations limited to the sample application and repository.
- Do not scan or attack production systems.
- Avoid creating vulnerabilities that could affect unrelated users or infrastructure.

## 5. Evidence

Planned evidence includes:

- Successful baseline workflow
- Secret-detection failure
- SAST finding
- Dependency finding
- Security-test result
- `BLOCK` gate result
- Corrected `PASS` result
- Relevant GitHub Actions logs
- Screenshots or exported results needed for the final report/presentation

Evidence will only be collected after the corresponding control has actually been executed.

## 6. Completion Criteria

Phase 1 is complete when requirements, architecture, security coverage, threat model, and testing strategy are documented consistently with the planned MVP.

Implementation is not considered complete until the actual security checks and tests run successfully, the workflow behaves as intended, a vulnerable change is blocked, a corrected change passes, evidence is collected, and documentation reflects the verified implementation.
