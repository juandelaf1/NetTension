# NetTension — Roadmap

> **Delivery:** Week of June 15, 2026
>
> **Legend:** ✅ Done · 🔷 In Progress · ◻️ Pending

---

## Sprint 1: Repo Setup & Professional Polish (Done)

| Task | Status |
|------|--------|
| Rewrite README in English (Problem → Hypotheses → Results → Conclusions) | ✅ |
| Create banner SVG in `assets/` | ✅ |
| Define file manifest & .gitignore | ✅ |
| Remove agent protocol docs from repo | ✅ |
| Initial commit with tag `v0.1.0` | 🔷 |

## Sprint 2: Power BI Dashboard (Days 1–2)

| Task | Status |
|------|--------|
| Import 14 .parquet files into Power BI | ◻️ |
| Create star schema relationships | ◻️ |
| Add DAX measures (CAGR, HHI, Scissors, NSI, Macro) | ◻️ |
| Build Page 1: Market Overview | ◻️ |
| Build Page 2: Network Stress & Infrastructure | ◻️ |
| Build Page 3: European Context & Regulatory | ◻️ |
| Build Page 4: Fair Share Simulator (What-If) | ◻️ |
| Build Page 5: Governance & Bias Audit | ◻️ |
| Deploy to Power BI Service (public URL) | ◻️ |

## Sprint 3: Docker & Supplementary (Days 3–4)

| Task | Status |
|------|--------|
| Create Dockerfile for ETL pipeline | ◻️ |
| Push to Docker Hub | ◻️ |
| Jupyter notebook with Plotly (EDA companion) | ◻️ |
| (Optional) Streamlit What-If simulator | ◻️ |

## Sprint 4: Validation & Presentation (Days 5–7)

| Task | Status |
|------|--------|
| Validate with non-technical user (capture screenshot) | ◻️ |
| Prepare 7-minute oral presentation script (ES/EN) | ◻️ |
| Final repo review and cleanup | ◻️ |
| Final commit with tag `v1.0.0` | ◻️ |
| Submission | ◻️ |

---

## Files Included in Repository

```
NetTension/
├── .github/workflows/ci.yml
├── .gitignore
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── assets/
│   └── banner.svg
├── data/
│   ├── processed/     (14 .parquet + extracted .txt)
│   └── SOURCES.yaml
├── docs/
│   └── DATA_MODEL.md
├── reports/
│   └── EDA_SUMMARY.md
└── src/
    ├── loader/
    ├── transform/
    └── pipeline/
```

**Excluded:** `data/raw/`, agent protocol docs (`docs/00_*`–`08_*`), `.pbix`, environment files.
