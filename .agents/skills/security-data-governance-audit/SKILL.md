---
name: security-data-governance-audit
description: Audit secrets, privacy, public data safety, dependency risk, notebook outputs, and data governance for a public data science repository.
---

# Security And Data Governance Audit

Use this skill for security, privacy, secrets, data governance, dependency, or
public-release audits.

## Required Context

Read:

- `.agents/agents/security-data-governance-officer.md`
- `.agents/rules/data-and-privacy-rules.md`
- `.agents/rules/review-and-release-rules.md`

Inspect the relevant files and current diff.

## Audit Workflow

1. **Secrets scan**
   - Search for tokens, keys, passwords, connection strings, private URLs, and
     credentials.
   - Include notebooks and config files.

2. **Data exposure scan**
   - Check committed datasets.
   - Check notebook outputs.
   - Check generated reports.
   - Flag personal, private, or regulated data.

3. **Dependency and execution risk**
   - Inspect new dependencies.
   - Check network calls.
   - Check shell command execution.
   - Check unsafe deserialization or arbitrary file loading.

4. **Governance review**
   - Confirm data provenance.
   - Confirm license notes when known.
   - Confirm environment variable guidance for credentials.

## Suggested Search Patterns

```bash
rg -n "api[_-]?key|token|secret|password|passwd|bearer|authorization|client_secret|private_key|BEGIN [A-Z ]*PRIVATE KEY"
rg -n "read_csv|read_parquet|to_csv|to_parquet|requests\\.|httpx\\.|urllib"
```

## Output Format

```markdown
## Security Verdict
Pass / Partial / Fail

## Findings
1. [Severity] <Finding title>
   Evidence:
   Exposure scenario:
   Fix:
   Confidence:

## Governance Notes
- 

## Checks Run
- 

## Not Checked
- 
```

## Exit Criteria

The audit is complete only when secrets, data exposure, dependency risk, and
provenance are considered.
