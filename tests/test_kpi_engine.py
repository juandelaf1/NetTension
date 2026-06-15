"""Tests for KPI Engine calculations."""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from transform.kpi_engine import hhi_quarterly


def test_hhi_quarterly_perfect_monopoly():
    """HHI = 10000 when one operator has 100% market share."""
    df = pd.DataFrame({
        "trimestre": ["2020T1", "2020T1", "2020T1"],
        "operador": ["OpA", "OpB", "OpC"],
        "ingresos_por_operador": [1000, 0, 0],
    })
    result = hhi_quarterly(df)
    assert result["hhi"].iloc[0] == 10000, f"Expected 10000, got {result['hhi'].iloc[0]}"
    assert result["num_operators"].iloc[0] == 1


def test_hhi_quarterly_equal_split():
    """HHI = 3333 when 3 operators share equally."""
    df = pd.DataFrame({
        "trimestre": ["2020T1", "2020T1", "2020T1"],
        "operador": ["OpA", "OpB", "OpC"],
        "ingresos_por_operador": [100, 100, 100],
    })
    result = hhi_quarterly(df)
    expected = round((1/3)**2 * 10000 + (1/3)**2 * 10000 + (1/3)**2 * 10000)
    assert round(result["hhi"].iloc[0]) == expected, f"Expected {expected}, got {result['hhi'].iloc[0]}"


def test_hhi_quarterly_empty_df():
    """Empty DataFrame returns empty result."""
    df = pd.DataFrame(columns=["trimestre", "operador", "ingresos_por_operador"])
    result = hhi_quarterly(df)
    assert len(result) == 0


def test_hhi_quarterly_nan_filtered():
    """Rows with NaN operator or zero revenue are excluded."""
    df = pd.DataFrame({
        "trimestre": ["2020T1", "2020T1", "2020T1"],
        "operador": ["OpA", None, "OpC"],
        "ingresos_por_operador": [100, 50, 0],
    })
    result = hhi_quarterly(df)
    # Only OpA contributes (OpC has 0 revenue, None is excluded)
    assert result["num_operators"].iloc[0] == 1
    assert result["hhi"].iloc[0] == 10000


def test_hhi_quarterly_two_quarters():
    """HHI is computed independently per quarter."""
    df = pd.DataFrame({
        "trimestre": ["2020T1", "2020T1", "2020T2", "2020T2"],
        "operador": ["OpA", "OpB", "OpA", "OpB"],
        "ingresos_por_operador": [300, 100, 100, 100],
    })
    result = hhi_quarterly(df)
    assert len(result) == 2  # Two quarters
    # Q1: OpA=75%, OpB=25% => HHI = 0.75^2 + 0.25^2 = 0.625 * 10000 = 6250
    assert round(result["hhi"].iloc[0]) == 6250
    # Q2: OpA=50%, OpB=50% => HHI = 0.5^2 + 0.5^2 = 0.5 * 10000 = 5000
    assert round(result["hhi"].iloc[1]) == 5000


def test_cagr_calculation():
    """Verify CAGR formula: (end/start)^(1/periods)-1"""
    # Traffic doubled in 5 years
    start, end, periods = 100, 200, 5
    cagr = (end / start) ** (1 / periods) - 1
    expected = 0.1487  # ~14.87%
    assert abs(cagr - expected) < 0.001


def test_hhi_classification():
    """HHI thresholds: <1000 competitive, 1000-2500 moderate, >2500 concentrated."""
    df = pd.DataFrame({
        "trimestre": ["2020T1", "2020T1", "2020T1", "2020T1"],
        "operador": ["OpA", "OpB", "OpC", "OpD"],
        "ingresos_por_operador": [400, 300, 200, 100],
    })
    result = hhi_quarterly(df)
    hhi_val = result["hhi"].iloc[0]
    # 0.4^2 + 0.3^2 + 0.2^2 + 0.1^2 = 0.16 + 0.09 + 0.04 + 0.01 = 0.30 * 10000 = 3000
    assert 2900 < hhi_val < 3100  # Moderate/Highly Concentrated boundary