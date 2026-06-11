"""
NetTension — Fix double-encoding in CNMC parquet files.

The CSV was read correctly with latin-1 encoding, but when
saved to parquet the Unicode strings got double-encoded.

Symptoms:
  'Tráfico' stored as bytes b'Tr\xc3\x83\xc2\xa1fico'
  instead of b'Tr\xc3\xa1fico'

Fix: encode each string as latin-1 (reversing the mistaken
UTF-8 → latin-1 reinterpretation), then decode as UTF-8.
"""
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"

TEXT_COLS_MERCADOS = [
    "trimestre", "pais", "tipo_de_mercado", "servicio", "concepto",
    "operador", "tipo_de_ingreso", "tipo_de_cliente", "segmento",
    "tipo_de_trafico", "tipo_de_contrato", "tipo_de_linea",
    "tipo_de_mensaje", "tipo_de_trafico_de_mensaje",
    "tecnologia_de_acceso", "velocidad_baf", "tipo_de_oferta",
    "tipo_de_tarifa", "tipo_de_ce_minorista", "tipo_de_circuito",
    "tipo_de_emision", "tipo_de_operador", "tipo_de_medio",
    "tipo_de_publicidad", "tipo_de_contratacion",
    "tipo_servicio_audiovisual_mayorista", "tipo_de_ba_may",
    "tipo_de_interconexion", "tipo_de_tarificacion_en_interconexion",
    "tipo_de_ambito", "tipo_de_acceso_de_infraestructuras",
    "unidades",
]

TEXT_COLS_GENERALES = [
    "trimestre", "pais", "tipo_de_mercado", "servicio", "concepto",
    "operador", "tipo_de_ingreso", "tipo_de_paquete", "unidades",
]


def fix_double_encoding(series):
    """Fix strings that were double-encoded via UTF-8 -> latin-1."""
    def _fix(val):
        if not isinstance(val, str):
            return val
        try:
            return val.encode("latin-1", errors="surrogateescape").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return val
    return series.apply(_fix)


def fix_file(filename, text_cols):
    path = PROCESSED_DIR / filename
    if not path.exists():
        print(f"[SKIP] {filename} not found")
        return
    df = pd.read_parquet(path)
    for col in text_cols:
        if col in df.columns:
            df[col] = fix_double_encoding(df[col])
    df.to_parquet(path, index=False)
    print(f"[FIX] {filename}: {len(df)} rows, {len(text_cols)} text columns fixed")

    # Verify
    test = df[text_cols].select_dtypes(include="object")
    for col in test.columns:
        for val in test[col].dropna().unique()[:5]:
            if any(ord(c) > 127 for c in str(val)):
                print(f"  Sample: {col} = {repr(val)}")
                break
    return df


if __name__ == "__main__":
    print("Fixing double-encoding in parquet files...")
    fix_file("cnmc_mercados_clean.parquet", TEXT_COLS_MERCADOS)
    fix_file("cnmc_datos_generales_clean.parquet", TEXT_COLS_GENERALES)
    print("Done.")
