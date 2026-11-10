-- Purpose: Service distribution by category and market type (dimension summary).
-- Inputs: dim_service(category, market_type)
-- Output: service counts by category/market type
SELECT
  category,
  market_type,
  count(*) AS num_services
FROM dim_service
GROUP BY category, market_type
ORDER BY category, market_type;
