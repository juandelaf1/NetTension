import streamlit as st
import pandas as pd
from io import BytesIO

def download_button(df: pd.DataFrame, filename: str, label: str = "📥 Download CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label, csv, filename, "text/csv", use_container_width=True)

def download_excel(dfs: dict, filename: str, label: str = "📥 Download Excel"):
    """Download multiple DataFrames as Excel with multiple sheets."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    st.download_button(label, output.getvalue(), filename, 
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)

def generate_report_pdf(filters: dict, kpis: dict) -> bytes:
    """Placeholder for PDF report generation (requires fpdf2 or reportlab)."""
    return b"PDF generation not implemented"