-- Purpose: Operator distribution by group (dimension summary).
-- Inputs: dim_operator(operator_group)
-- Output: operator counts by group
SELECT
  operator_group,
  count(*) AS num_operators
FROM dim_operator
GROUP BY operator_group
ORDER BY num_operators DESC;
