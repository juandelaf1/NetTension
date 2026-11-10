-- Hypothesis: H4 Network Stress
-- Purpose: Compare network stress index (traffic pressure proxy) vs revenue per line.
-- Inputs: fact_observed_agg(year, quarter, nsi, revenue_per_line)
-- Output: NSI and revenue per line snapshot
SELECT
  year,
  quarter,
  round(nsi, 0)::INT AS nsi,
  round(revenue_per_line, 2) AS revenue_per_line
FROM fact_observed_agg
WHERE year IN (2005, 2010, 2015, 2020, 2025)
ORDER BY year, quarter;
