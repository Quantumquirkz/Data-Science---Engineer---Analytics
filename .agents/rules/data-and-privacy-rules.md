# Data And Privacy Rules

Data workflows must be reproducible, explainable, and safe for a public
portfolio repository.

## Data Provenance

- Document where data came from.
- Distinguish public data, synthetic data, benchmark data, and user-provided
  data.
- Include license or terms notes when known.
- If provenance is unclear, say so instead of inventing it.

## Sensitive Data

Do not commit:

- API keys or tokens.
- Raw personally identifiable information.
- Private credentials.
- Proprietary datasets.
- Notebook outputs that expose private rows.

## Data Quality

Check:

- Missingness.
- Duplicates.
- Units.
- Time zones.
- Outliers.
- Schema drift.
- Target leakage.
- Train/test contamination.

## Storage

- Keep large raw datasets out of Git unless explicitly justified.
- Prefer `data/README.md` plus download or simulation instructions.
- Keep generated outputs small, stable, and intentionally documented.
