# SecurePR Testing Strategy

## Overview
Testing must show that SecurePR can detect defined security problems, block unsafe pull requests, allow corrected changes to pass, operate against repositories other than the Flask sample, and report its security coverage and accuracy limits honestly.

## Development-Time Tests

During implementation, run targeted tests for changed scripts and configuration so broken code is not knowingly committed. These are development checks, not the final Phase 4 accuracy claim.

Current Phase 4 test areas include:

- repository/language detection
- unsupported-language detection
- SARIF parsing and conservative normalized finding keys
- custom SecurePR Semgrep configuration
- accuracy-metric formula implementation
- per-run accuracy status reporting
- existing Flask security tests
- workflow YAML/configuration consistency

A finding normalization test must prove both that identical cross-tool findings can be grouped and that distinct findings at the same file/line are not incorrectly collapsed.

## Final Phase 4 Validation

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
11. Calculate TP, FP, TN, precision, recall, and F1.
12. Record the tested categories, tool configuration, limitations, and coverage boundaries.
13. Audit all documentation against the final implementation and measurements.
14. Merge the one consolidated Phase 4 PR.
15. Verify the post-merge `main` workflow passes.

## Accuracy Metrics

For the controlled benchmark:

- **TP:** vulnerable case correctly blocked.
- **FP:** safe case incorrectly blocked.
- **TN:** safe case correctly passed.
- **FN:** vulnerable case incorrectly passed.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

Every PR reports the current benchmark status. Before the final benchmark exists, the status is explicitly **Benchmark pending — no accuracy percentage is claimed**. After benchmark results are committed, every PR reports the latest measured TP, FP, TN, precision, recall, and F1.

Do not claim 90% or 100% accuracy without measured results. If the benchmark produces lower or higher values, report the actual result and explain the corpus limitations.

## PASS/BLOCK and Human Review

There are exactly two gate outcomes:

- `PASS` — configured blocking controls passed and no blocking normalized finding remains.
- `BLOCK` — at least one configured blocking control failed or a blocking normalized finding remains.

There is no separate `REVIEW` gate state. Human review is always recommended for both outcomes, especially for business logic, design, authorization intent, architecture, and findings that may be false positives.

## PR Versus Main

A passing PR does not guarantee that the post-merge `main` workflow will pass. The PR run and push-to-main run are separate executions. Final validation therefore requires both.

## One-PR Phase Workflow

Phase 4 uses one feature branch and one consolidated PR. If a check fails, fix the same branch and same PR. Do not create another PR for the phase. Before merge, audit all relevant implementation and documentation again.

## Safety

- Use synthetic secrets only.
- Never use real API keys, passwords, tokens, private keys, or cloud credentials.
- Keep intentionally vulnerable examples isolated and controlled.
- Do not test production systems.
- Do not automatically exploit discovered vulnerabilities.

## Completion Criteria

Phase 4 is complete only when implementation, local verification, reusable-repository demonstrations, final benchmark metrics, documentation audit, one consolidated PR, merge, and post-merge `main` verification all pass.
