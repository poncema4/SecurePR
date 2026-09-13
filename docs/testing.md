# SecurePR Testing Strategy

## 1. Testing Goals

Testing must show that SecurePR can:

1. Detect defined security problems.
2. Block a pull request when a required blocking control fails.
3. Allow a corrected pull request to pass.
4. Operate against repositories other than its Flask sample.
5. Produce one clear overall PASS/BLOCK result without unnecessary duplicate findings.
6. Report coverage boundaries instead of silently treating unavailable analysis as secure.
7. Produce reproducible results from actual tool execution.

## 2. Development-Time Tests

During implementation, run targeted tests for changed scripts and configuration so broken code is not knowingly committed. These are development checks, not the final Phase 4 accuracy claim.

Current Phase 4 test areas include:

- repository/language detection
- unsupported-language detection
- SARIF parsing and normalized finding keys
- custom SecurePR Semgrep configuration
- accuracy-metric formula implementation
- existing Flask security tests
- workflow YAML/configuration consistency

## 3. Final Phase 4 Validation

The comprehensive validation occurs **at the end of Phase 4**, after implementation and documentation are stable.

The final sequence is:

1. Local verification of the complete repository.
2. Validate workflow configuration and reusable workflow integration.
3. Run the consolidated Phase 4 PR through the SecurePR gate.
4. Exercise the reusable workflow against SecurePR, CookieGuard, and NetDefender using their actual supported languages/artifacts.
5. Create controlled vulnerable cases for applicable security controls.
6. Verify those vulnerable cases are blocked.
7. Correct them and verify PASS.
8. Test safe edge cases to identify false positives.
9. Test known vulnerable cases that are difficult for the configured tools to detect to measure false negatives.
10. Record every benchmark case and expected classification.
11. Calculate TP, FP, TN, FN, precision, recall, and F1.
12. Record the tested categories, tool configuration, limitations, and coverage boundaries.
13. Audit all documentation against the final implementation and measurements.
14. Merge the one consolidated Phase 4 PR.
15. Verify the post-merge `main` workflow passes.

## 4. Accuracy Metrics

For the controlled benchmark:

- **TP:** vulnerable case correctly blocked.
- **FP:** safe case incorrectly blocked.
- **TN:** safe case correctly passed.
- **FN:** vulnerable case incorrectly passed.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

Do not claim 90% or 100% accuracy without measured results. If the benchmark produces lower or higher values, report the actual result and explain the corpus limitations.

## 5. PASS/BLOCK and Human Review

There are exactly two gate outcomes:

- `PASS` — configured blocking controls passed and no blocking normalized finding remains.
- `BLOCK` — at least one configured blocking control failed or a blocking normalized finding remains.

There is no separate `REVIEW` gate state. Human review is always recommended for both outcomes, especially for business logic, design, authorization intent, architecture, and findings that may be false positives.

## 6. PR Versus Main

A passing PR does not guarantee that the post-merge `main` workflow will pass. The PR run and push-to-main run are separate executions. Final validation therefore requires both.

## 7. Safety

- Use synthetic secrets only.
- Never use real API keys, passwords, tokens, private keys, or cloud credentials.
- Keep intentionally vulnerable examples isolated and controlled.
- Do not test production systems.
- Do not automatically exploit discovered vulnerabilities.

## 8. Completion Criteria

Phase 4 is complete only when implementation, local verification, reusable-repository demonstrations, final benchmark metrics, documentation audit, one consolidated PR, merge, and post-merge `main` verification all pass.
