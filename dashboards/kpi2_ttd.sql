-- KPI 2: Tiempo medio hasta detección (segundos)
-- Requires alerts.first_violation_ts populated by Node-RED
SELECT
  COALESCE(AVG(EXTRACT(EPOCH FROM (alerted_at - first_violation_ts))), 0) AS avg_seconds_to_detect
FROM alerts
WHERE alerted_at >= NOW() - INTERVAL '1 day';
