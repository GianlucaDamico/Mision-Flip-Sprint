-- KPI 3: %% de falsos positivos (alertas sin incidente real en ±120s)
-- Load ground-truth into 'labels' table beforehand.
WITH alerts_window AS (
  SELECT a.id, a.parcel_id, a.alerted_at
  FROM alerts a
  WHERE a.alerted_at >= NOW() - INTERVAL '1 day'
),
tp AS (
  SELECT aw.id
  FROM alerts_window aw
  WHERE EXISTS (
    SELECT 1 FROM labels l
    WHERE l.parcel_id = aw.parcel_id
      AND l.label = 'ALERT'
      AND l.ts_utc BETWEEN aw.alerted_at - INTERVAL '120 seconds' AND aw.alerted_at + INTERVAL '120 seconds'
  )
)
SELECT
  ROUND(100.0 * ( (SELECT COUNT(*) FROM alerts_window) - (SELECT COUNT(*) FROM tp) ) / GREATEST(1,(SELECT COUNT(*) FROM alerts_window) ), 2) AS pct_false_positives;
