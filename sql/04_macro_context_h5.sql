-- Hypothesis: H5 Macro Decline
-- Purpose: Telecom sector weight in economy (telecom revenue share of GDP).
-- Inputs: fact_eurostat_es(year, population, gdp_meur, gdp_per_capita), fact_observed_agg(year, revenue)
-- Output: macro context and telecom GDP share snapshot
SELECT
  f.year,
  f.population,
  f.gdp_meur,
  round(f.gdp_per_capita, 0)::INT AS gdp_per_capita,
  round(o.revenue / (f.gdp_meur * 1e6) * 100, 2) AS telecom_gdp_share
FROM fact_eurostat_es f
JOIN (
  SELECT year, avg(revenue) AS revenue
  FROM fact_observed_agg
  GROUP BY year
) o ON f.year = o.year
WHERE f.year IN (2005, 2010, 2015, 2020, 2025)
ORDER BY f.year;
