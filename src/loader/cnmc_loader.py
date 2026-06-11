"""
NetTension — CNMC Mercados Loader

Loads and unions the 5 CNMC Mercados CSV files
into a single pandas DataFrame (2005–2025).

Columns (48):
  _id, trimestre, pais, tipo_de_mercado, servicio, concepto,
  operador, tipo_de_ingreso, tipo_de_cliente, segmento,
  tipo_de_trafico, tipo_de_contrato, tipo_de_linea,
  tipo_de_mensaje, tipo_de_trafico_de_mensaje,
  tecnologia_de_acceso, velocidad_baf, tipo_de_oferta,
  tipo_de_tarifa, tipo_de_ce_minorista, tipo_de_circuito,
  tipo_de_emision, tipo_de_operador, tipo_de_medio,
  tipo_de_publicidad, tipo_de_contratacion,
  tipo_servicio_audiovisual_mayorista, tipo_de_ba_may,
  tipo_de_interconexion, tipo_de_tarificacion_en_interconexion,
  tipo_de_ambito, tipo_de_acceso_de_infraestructuras,
  unidades, ingresos, ingresos_por_operador, clientes,
  clientes_por_operador, lineas_o_accesos, tasa_de_penetracion,
  lineas_o_accesos_por_operador, portabilidades, trafico,
  trafico_por_operador, mensajes, mensajes_por_operador_1,
  trafico_de_datos, circuitos, publicidad, contrataciones

Licence: CC-BY-SA-4.0
Source: https://catalogodatos.cnmc.es/
"""

from pathlib import Path
import pandas as pd


RAW_DIR = Path(__file__).parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"


MERCADOS_FILES = [
    "cnmc_mercados_2005_2009.csv",
    "cnmc_mercados_2010_2014.csv",
    "cnmc_mercados_2015_2019.csv",
    "cnmc_mercados_2020_2024.csv",
    "cnmc_mercados_2025T1_2025T4.csv",
]

DTYPE_MAP = {col: "object" for col in range(48)}
DTYPE_MAP[0] = "int64"  # _id


def load_mercados(directory: Path = RAW_DIR) -> pd.DataFrame:
    """Load and union all 5 CNMC Mercados CSV files."""
    frames = []
    for fname in MERCADOS_FILES:
        path = directory / fname
        if not path.exists():
            print(f"[WARN] File not found: {path}")
            continue
        # Files use comma separator; trailing empty column exists (49 vs 48)
        # Files are UTF-8 encoded (confirmed by encoding test)
        df = pd.read_csv(
            path,
            sep=",",
            encoding="utf-8",
            low_memory=False,
            na_values=["N/A", ""],
        )
        # Drop any unnamed trailing column
        unnamed = [c for c in df.columns if "Unnamed" in c]
        if unnamed:
            df.drop(columns=unnamed, inplace=True)
            print(f"      Dropped trailing column: {unnamed[0]}")
        print(f"[LOAD] {fname}: {len(df)} rows × {len(df.columns)} cols")
        frames.append(df)

    if not frames:
        raise FileNotFoundError("No CNMC Mercados files found")

    union = pd.concat(frames, axis=0, ignore_index=True)
    print(f"[UNION] Mercados: {len(union)} total rows")
    return union


def save_processed(df: pd.DataFrame, name: str = "cnmc_mercados_union.parquet"):
    """Save processed DataFrame to parquet (compressed, fast)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / name
    df.to_parquet(path, index=False)
    print(f"[SAVE] {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    df = load_mercados()
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Period range: {df['trimestre'].min()} → {df['trimestre'].max()}")
    save_processed(df)
