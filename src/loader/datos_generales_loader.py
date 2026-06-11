"""
NetTension — CNMC Datos Generales Loader

Loads the CNMC Datos Generales CSV file
(2005T1–2025T4, 14 columns).

Source: https://catalogodatos.cnmc.es/dataset/datos-generales
Licence: CC-BY-SA-4.0
"""

from pathlib import Path
import pandas as pd


RAW_DIR = Path(__file__).parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"

DATOS_GENERALES_FILE = "cnmc_datos_generales_2005T1_2025T4.csv"


def load_datos_generales(directory: Path = RAW_DIR) -> pd.DataFrame:
    """Load CNMC Datos Generales CSV."""
    path = directory / DATOS_GENERALES_FILE
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(
        path,
        sep=",",
        encoding="utf-8",
        low_memory=False,
        na_values=["N/A", ""],
    )
    print(f"[LOAD] {DATOS_GENERALES_FILE}: {len(df)} rows x {len(df.columns)} cols")
    print(f"[LOAD] Columns: {list(df.columns)}")
    return df


def save_processed(df: pd.DataFrame, name: str = "cnmc_datos_generales_clean.parquet"):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / name
    df.to_parquet(path, index=False)
    print(f"[SAVE] {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    df = load_datos_generales()
    print(f"Shape: {df.shape}")
    print(f"Period: {df['trimestre'].min()} -> {df['trimestre'].max()}")
    print(f"Operators: {sorted(df['operador'].dropna().unique())}")
    print(f"Concepts: {sorted(df['concepto'].dropna().unique())}")
    save_processed(df)
