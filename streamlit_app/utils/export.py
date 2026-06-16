import streamlit as st
import pandas as pd

def download_button(df: pd.DataFrame, filename: str, label: str = "📥 Descargar CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(label, csv, filename, "text/csv", width="stretch")
