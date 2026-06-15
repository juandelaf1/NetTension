"""
NetTension — Eurostat SDMX-TSV Loader

Parses Eurostat compact TSV format (dimensions as rows,
time periods as columns) into tidy (long) DataFrames.

Supports: demo_pjan (population), nama_10_gdp (GDP)

Source: https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing
Licence: CC-BY-4.0
"""

from pathlib import Path
import pandas as pd


RAW_DIR = Path(__file__).parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"


def load_tsv_gz(filepath: Path) -> pd.DataFrame:
    """Load SDMX-TSV .gz file, parse dimensions and pivot to long format."""
    print(f"[LOAD] Reading {filepath.name}")

    raw = pd.read_csv(
        filepath,
        sep="\t",
        compression="gzip",
        encoding="utf-8",
        low_memory=False,
    )

    # First column is the dimension key; remaining are time periods
    dim_col_name = raw.columns[0]
    time_col_names = list(raw.columns[1:])

    # Extract dimension names from first column header
    dim_col_raw = dim_col_name.replace("\\TIME_PERIOD", "")
    dim_names = [c.strip() for c in dim_col_raw.split(",")]

    # Melt time columns into long format (use raw column strings directly)
    long = pd.melt(
        raw,
        id_vars=[dim_col_name],
        value_vars=time_col_names,
        var_name="time_period",
        value_name="value",
    )

    # Merge dimensions back via key column (avoids index alignment bug)
    dims = raw.iloc[:, 0].str.split(",", expand=True)
    dims.columns = dim_names
    dims[dim_col_name] = raw.iloc[:, 0]
    long = long.merge(dims, on=dim_col_name, how="left")
    long.drop(columns=[dim_col_name], inplace=True)

    # Strip whitespace from time_period values
    long["time_period"] = long["time_period"].str.strip()

    # Split value and flag (Eurostat appends flags like 'p' for provisional)
    flag_map = long["value"].str.extract(r"([\d\.\-]+)\s*(.*)", expand=True)
    long["value_num"] = pd.to_numeric(flag_map[0], errors="coerce")
    long["flag"] = flag_map[1].fillna("")

    print(f"[LOAD] {filepath.name}: {len(long)} rows × {len(long.columns)} cols")
    return long


def load_demo_pjan(directory: Path = RAW_DIR) -> pd.DataFrame:
    """Load Eurostat population data (demo_pjan)."""
    path = directory / "eurostat_demo_pjan.tsv.gz"
    if not path.exists():
        raise FileNotFoundError(f"demo_pjan not found: {path}")
    return load_tsv_gz(path)


def load_nama_gdp(directory: Path = RAW_DIR) -> pd.DataFrame:
    """Load Eurostat GDP data (nama_10_gdp)."""
    path = directory / "eurostat_nama_10_gdp.tsv.gz"
    if not path.exists():
        raise FileNotFoundError(f"nama_10_gdp not found: {path}")
    return load_tsv_gz(path)


def save_processed(df: pd.DataFrame, name: str):
    """Save processed DataFrame to parquet."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / name
    df.to_parquet(path, index=False)
    print(f"[SAVE] {path}")


if __name__ == "__main__":
    pop = load_demo_pjan()
    gdp = load_nama_gdp()
    print(f"\nPopulation: {pop.shape}, columns: {list(pop.columns)}")
    print(f"GDP: {gdp.shape}, columns: {list(gdp.columns)}")
    save_processed(pop, "eurostat_demo_pjan_tidy.parquet")
    save_processed(gdp, "eurostat_nama_10_gdp_tidy.parquet")
