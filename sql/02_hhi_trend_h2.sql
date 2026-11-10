-- Hypothesis: H2 Market Concentration
-- Purpose: Track average HHI and classification over key years.
-- Inputs: kpi_hhi(year, hhi, classification)
-- Output: avg HHI by year/classification snapshot
SELECT
  year,
  round(avg(hhi), 0)::INT AS avg_hhi,
  classification
FROM kpi_hhi
WHERE year IN (2005, 2010, 2015, 2020, 2025)
GROUP BY year, classification
ORDER BY year;
