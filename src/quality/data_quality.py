"""Data quality checks for processed NetTension datasets.

Runs against processed parquets in data/processed (or a provided DuckDB connection).
Produces a JSON report and a Markdown summary in reports/quality/.

Focus: high-signal checks (schema/coverage/ranges) to catch regressions without noise.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports" / "quality"

REQUIRED_TABLES = [
    "fact_observed_agg",
    "fact_eurostat_es",
    "kpi_hhi",
    "kpi_nsi",
    "kpi_elasticity",
    "dim_time",
    "dim_operator",
    "dim_service",
    "dim_geography",
    "cnmc_mercados_clean",
]


@dataclass
class CheckResult:
    name: str
    status: str  # pass|fail|warn|skip
    detail: str
    value: Any = None


def _has_cols(df: pd.DataFrame, cols: Iterable[str]) -> bool:
    return all(c in df.columns for c in cols)


def check_table_exists(path: Path, table: str) -> CheckResult:
    if path.exists():
        return CheckResult(f"exists:{table}", "pass", f"found {path.name}")
    return CheckResult(f"exists:{table}", "fail", f"missing {path}")


def check_non_empty(df: pd.DataFrame, table: str) -> CheckResult:
    n = len(df)
    if n > 0:
        return CheckResult(f"rows:{table}", "pass", f"{n} rows", n)
    return CheckResult(f"rows:{table}", "fail", "0 rows", n)


def check_no_nulls(df: pd.DataFrame, table: str, cols: list[str]) -> CheckResult:
    present = [c for c in cols if c in df.columns]
    if not present:
        return CheckResult(f"nulls:{table}", "skip", f"none of {cols} present")
    nulls = {c: int(df[c].isna().sum()) for c in present}
    bad = {c: n for c, n in nulls.items() if n > 0}
    if bad:
        return CheckResult(f"nulls:{table}", "fail", f"nulls in key cols: {bad}", bad)
    return CheckResult(f"nulls:{table}", "pass", f"no nulls in {present}")


def check_hhi_range(df: pd.DataFrame, table: str = "kpi_hhi") -> CheckResult:
    if "hhi" not in df.columns:
        return CheckResult("range:hhi", "skip", "column hhi not present")
    s = pd.to_numeric(df["hhi"], errors="coerce").dropna()
    if s.empty:
        return CheckResult("range:hhi", "fail", "no numeric hhi values")
    lo, hi = float(s.min()), float(s.max())
    ok = (lo >= 0) and (hi <= 10000)
    status = "pass" if ok else "fail"
    return CheckResult("range:hhi", status, f"min={lo:.2f}, max={hi:.2f} (expected 0..10000)", {"min": lo, "max": hi})


def check_positive(df: pd.DataFrame, table: str, cols: list[str]) -> CheckResult:
    present = [c for c in cols if c in df.columns]
    if not present:
        return CheckResult(f"positive:{table}", "skip", f"none of {cols} present")
    bad = {}
    for c in present:
        s = pd.to_numeric(df[c], errors="coerce")
        neg = int((s < 0).sum())
        if neg:
            bad[c] = neg
    if bad:
        return CheckResult(f"positive:{table}", "warn", f"negative values: {bad}", bad)
    return CheckResult(f"positive:{table}", "pass", f"non-negative in {present}")


def check_year_coverage(df: pd.DataFrame, table: str, col: str = "year") -> CheckResult:
    if col not in df.columns:
        # try to infer from trimestre like 2005T1
        if "trimestre" in df.columns:
            try:
                years = df["trimestre"].astype(str).str.extract(r"(\d{4})")[0].dropna().astype(int)
                if years.empty:
                    return CheckResult(f"coverage:{table}", "skip", "cannot infer years")
                lo, hi = int(years.min()), int(years.max())
                status = "pass" if (lo <= 2006 and hi >= 2024) else "warn"
                return CheckResult(f"coverage:{table}", status, f"years inferred {lo}-{hi}", {"min": lo, "max": hi})
            except Exception as e:
                return CheckResult(f"coverage:{table}", "skip", f"infer failed: {e}")
        return CheckResult(f"coverage:{table}", "skip", f"no {col}/trimestre column")
    years = pd.to_numeric(df[col], errors="coerce").dropna().astype(int)
    if years.empty:
        return CheckResult(f"coverage:{table}", "fail", "no valid years")
    lo, hi = int(years.min()), int(years.max())
    status = "pass" if (lo <= 2006 and hi >= 2024) else "warn"
    return CheckResult(f"coverage:{table}", status, f"years {lo}-{hi}", {"min": lo, "max": hi})


def run_quality_checks(proc_dir: Path = PROC) -> dict:
    results: list[CheckResult] = []
    tables: dict[str, pd.DataFrame] = {}

    for t in REQUIRED_TABLES:
        p = proc_dir / f"{t}.parquet"
        res = check_table_exists(p, t)
        results.append(res)
        if res.status == "pass":
            try:
                tables[t] = pd.read_parquet(p)
            except Exception as e:
                results.append(CheckResult(f"read:{t}", "fail", f"cannot read: {e}"))

    # per-table checks
    if "kpi_hhi" in tables:
        df = tables["kpi_hhi"]
        results.append(check_non_empty(df, "kpi_hhi"))
        results.append(check_no_nulls(df, "kpi_hhi", ["hhi"]))
        results.append(check_hhi_range(df))
        results.append(check_year_coverage(df, "kpi_hhi"))
    if "kpi_nsi" in tables:
        df = tables["kpi_nsi"]
        results.append(check_non_empty(df, "kpi_nsi"))
        results.append(check_positive(df, "kpi_nsi", ["network_stress_index", "nsi"]))
        results.append(check_year_coverage(df, "kpi_nsi"))
    if "kpi_elasticity" in tables:
        df = tables["kpi_elasticity"]
        results.append(check_non_empty(df, "kpi_elasticity"))
        results.append(check_positive(df, "kpi_elasticity", ["revenue_per_line", "traffic_per_line"]))
        results.append(check_year_coverage(df, "kpi_elasticity"))
    if "fact_observed_agg" in tables:
        df = tables["fact_observed_agg"]
        results.append(check_non_empty(df, "fact_observed_agg"))
        results.append(check_year_coverage(df, "fact_observed_agg"))
        results.append(check_positive(df, "fact_observed_agg", ["revenue", "ingresos", "trafico", "traffic", "lineas", "lines"]))
    if "fact_eurostat_es" in tables:
        df = tables["fact_eurostat_es"]
        results.append(check_non_empty(df, "fact_eurostat_es"))
        results.append(check_year_coverage(df, "fact_eurostat_es", col="year"))
    for dim in ["dim_time", "dim_operator", "dim_service", "dim_geography"]:
        if dim in tables:
            results.append(check_non_empty(tables[dim], dim))

    summary = {
        "pass": sum(1 for r in results if r.status == "pass"),
        "fail": sum(1 for r in results if r.status == "fail"),
        "warn": sum(1 for r in results if r.status == "warn"),
        "skip": sum(1 for r in results if r.status == "skip"),
    }
    ok = summary["fail"] == 0
    return {
        "ok": ok,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "proc_dir": str(proc_dir),
        "summary": summary,
        "checks": [asdict(r) for r in results],
    }


def write_reports(report: dict, out_dir: Path = REPORT_DIR) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "data_quality_report.json"
    md_path = out_dir / "data_quality_report.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Data Quality Report",
        "",
        f"- Generated (UTC): {report['generated_at']}",
        f"- Processed dir: `{report['proc_dir']}`",
        f"- Status: {'OK' if report['ok'] else 'FAIL'}",
        f"- Summary: {report['summary']}",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for c in report["checks"]:
        detail = str(c["detail"]).replace("\n", " ")[:120]
        lines.append(f"| {c['name']} | {c['status']} | {detail} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    report = run_quality_checks(PROC)
    jp, mp = write_reports(report, REPORT_DIR)
    print(f"Data quality: {'OK' if report['ok'] else 'FAIL'} - {report['summary']}")
    print(f"Reports: {jp} | {mp}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
