# SecurePR Testing Strategy

## Overview
Testing must show that SecurePR can detect defined security problems, block unsafe pull requests, allow corrected changes to pass, operate against repositories other than the Flask demonstration target, and report its security coverage and accuracy limits honestly.

## Development-Time Tests

Run targeted tests for changed scripts and configuration so broken code is not knowingly committed.

Current test areas include:

- repository/language detection
- unsupported-language detection
- SARIF parsing and conservative finding aggregation
- custom SecurePR Semgrep configuration
- accuracy-metric formula implementation
- pending and measured accuracy reporting
- existing Flask security tests
- workflow YAML/configuration consistency

Finding-aggregation tests prove both that identical cross-tool findings can be grouped and that distinct findings at the same file/line are not incorrectly collapsed.

## Local Verification

From the repository root:

```bash
python -m pytest -q
python -m compileall -q app security tests scripts
```

These checks validate the SecurePR implementation itself. GitHub Actions remains the authoritative environment for the complete gate because the workflows invoke CodeQL, Semgrep, Gitleaks, dependency audits, and GitHub-specific security reporting.

## Testing PASS and BLOCK

Use controlled synthetic examples only. Never commit real credentials or attack production systems.

### BLOCK test
1. Create an isolated test change containing a known high-confidence security defect, such as a synthetic hard-coded credential that matches the SecurePR rule.
2. Open or update a PR against `main`.
3. Confirm the `SecurePR Security Gate` job reports `BLOCK`.
4. Inspect the Check Results table and native tool output.

### PASS test
1. Remove or remediate the synthetic defect on the **same branch and same PR**.
2. Push the correction.
3. Confirm the same gate reruns and reports `PASS` when all applicable controls pass.
4. Confirm human-review guidance remains present.

## Reusable-Repository Testing

The reusable workflow is intended for repositories you control. A target repository can call:

```yaml
jobs:
  securepr:
    uses: poncema4/SecurePR/.github/workflows/reusable-security.yml@main
```

For stronger reproducibility, pin the reusable workflow to a reviewed commit SHA.

Test portability using repositories with different stacks, such as:

- SecurePR — Python
- CookieGuard — JavaScript/TypeScript/Node/Next.js
- NetDefender — whatever supported source languages and dependency artifacts are actually present

Do not assume every target receives identical checks. Repository profiling determines which language, dependency, project-test, and CodeQL controls are applicable.

## Accuracy Benchmark

Accuracy must come from a controlled labeled benchmark, not from the fact that a normal PR passed.

For each case, record the expected and actual gate result in `docs/accuracy/benchmark-results.csv`.

- **TP:** vulnerable case correctly blocked.
- **FP:** safe case incorrectly blocked.
- **TN:** safe case correctly passed.
- **FN:** vulnerable case incorrectly passed.

`Precision = TP / (TP + FP)`

`Recall = TP / (TP + FN)`

`F1 = 2 × (Precision × Recall) / (Precision + Recall)`

An empty benchmark ledger intentionally produces `Benchmark pending — no accuracy percentage is claimed.` Once actual labeled cases are recorded, every PR reports the measured TP, FP, TN, precision, recall, and F1.

Do not claim 90% or 100% accuracy without measured results. The measurements describe the tested corpus and configuration only.

## PASS/BLOCK and Human Review

There are exactly two gate outcomes:

- `PASS` — configured blocking controls passed and no blocking security finding remains.
- `BLOCK` — at least one configured blocking control failed or a blocking security finding remains.

There is no separate `REVIEW` gate state. Human review is always recommended for both outcomes, especially for business logic, design, authorization intent, architecture, and findings that may be false positives.

## Pull Request Versus Main

A passing PR does not guarantee that the post-merge `main` workflow will pass. The PR run and push-to-main run are separate executions. Final verification requires both.

## Safety

- Use synthetic secrets only.
- Never use real API keys, passwords, tokens, private keys, or cloud credentials.
- Keep intentionally vulnerable examples isolated and controlled.
- Do not test production systems.
- Do not automatically exploit discovered vulnerabilities.

## Completion Criteria

The MVP is complete when implementation, local verification, reusable-repository demonstrations, documentation audit, consolidated PR validation, merge, and post-merge `main` verification pass. The benchmark is separately considered complete only after its labeled cases have actually been executed and recorded.
