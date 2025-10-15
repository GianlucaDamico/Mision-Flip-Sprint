-- KPI 1: %% de envíos en SLA (sin alertas críticas) en la última hora
WITH shipments AS (
  SELECT DISTINCT parcel_id
  FROM telemetry_events
  WHERE ts_utc >= NOW() - INTERVAL '1 hour'
),
alerted AS (
  SELECT DISTINCT parcel_id
  FROM alerts
  WHERE alerted_at >= NOW() - INTERVAL '1 hour'
)
SELECT
  ROUND(100.0 * (SELECT COUNT(*) FROM shipments s WHERE NOT EXISTS (SELECT 1 FROM alerted a WHERE a.parcel_id = s.parcel_id)) / GREATEST(1, (SELECT COUNT(*) FROM shipments)), 2) AS pct_sla;
