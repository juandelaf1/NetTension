-- Hypothesis: H1 Scissors Effect
-- Purpose: Compare traffic vs revenue index over key years to show divergence gap.
-- Inputs: fact_observed_agg(year, quarter, data_traffic_index, revenue_index)
-- Output: yearly/quarterly scissors gap snapshot
SELECT
  year,
  quarter,
  data_traffic_index,
  revenue_index,
  (data_traffic_index - revenue_index) AS scissors_gap
FROM fact_observed_agg
WHERE year IN (2005, 2010, 2015, 2020, 2025)
ORDER BY year, quarter;
