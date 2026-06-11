"""
NetTension — Data Cleaner

Transforms raw CNMC and Eurostat data into analysis-ready format.

Key transformations:
  1. N/A → NaN (handled at load time via na_values)
  2. Convert numeric columns to float
  3. Trimestre → datetime (2005T1 → 2005-01-01)
  4. Filter relevant concepts (ingresos, trafico, lineas_o_accesos)
  5. Merge Mercados + Datos Generales
"""

import pandas as pd
import numpy as np
from pathlib import Path


PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"

NUMERIC_COLS_MERCADOS = [
    "ingresos", "ingresos_por_operador",
    "clientes", "clientes_por_operador",
    "lineas_o_accesos", "tasa_de_penetracion",
    "lineas_o_accesos_por_operador", "portabilidades",
    "trafico", "trafico_por_operador",
    "mensajes", "mensajes_por_operador_1",
    "trafico_de_datos", "circuitos",
    "publicidad", "contrataciones",
]

NUMERIC_COLS_GENERALES = [
    "ingresos", "ingresos_por_operador",
    "empleados_por_operador", "paquetes",
]


def to_float(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Safely convert string columns with dots-as-decimals to float."""
    available = [c for c in cols if c in df.columns]
    for col in available:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def parse_trimestre(series: pd.Series) -> pd.Series:
    """Convert CNMC trimestre format to datetime.

    2005T1 → 2005-01-01
    2025T4 → 2025-10-01
    """
    parts = series.str.extract(r"(\d{4})T(\d)")
    year = parts[0].astype(int)
    month = parts[1].astype(int).map({1: 1, 2: 4, 3: 7, 4: 10})
    return pd.to_datetime(year.astype(str) + "-" + month.astype(str) + "-01")


def clean_mercados(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline for CNMC Mercados."""
    df = df.copy()
    df = to_float(df, NUMERIC_COLS_MERCADOS)
    df["trimestre_dt"] = parse_trimestre(df["trimestre"])
    df["year"] = df["trimestre_dt"].dt.year
    df["quarter"] = df["trimestre_dt"].dt.quarter
    return df


def clean_datos_generales(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline for CNMC Datos Generales."""
    df = df.copy()
    df = to_float(df, NUMERIC_COLS_GENERALES)
    df["trimestre_dt"] = parse_trimestre(df["trimestre"])
    df["year"] = df["trimestre_dt"].dt.year
    df["quarter"] = df["trimestre_dt"].dt.quarter
    return df
