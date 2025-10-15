-- GreenDelivery schema (UTC timestamps)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS telemetry_events (
  id BIGSERIAL PRIMARY KEY,
  parcel_id TEXT NOT NULL,
  temp_c NUMERIC NOT NULL,
  g_force NUMERIC NOT NULL,
  ts_utc TIMESTAMPTZ NOT NULL,
  received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  raw_json JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_parcel_ts ON telemetry_events (parcel_id, ts_utc);

-- Alerts table (when N consecutive violations are detected)
CREATE TABLE IF NOT EXISTS alerts (
  id BIGSERIAL PRIMARY KEY,
  parcel_id TEXT NOT NULL,
  first_violation_ts TIMESTAMPTZ NOT NULL,
  alerted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  temp_threshold NUMERIC NOT NULL,
  gforce_threshold NUMERIC NOT NULL,
  consecutive_required INT NOT NULL,
  consecutive_observed INT NOT NULL,
  reason TEXT NOT NULL   -- e.g., 'temp' or 'g_force'
);

-- Optional: ground-truth labels table for evaluation
CREATE TABLE IF NOT EXISTS labels (
  id BIGSERIAL PRIMARY KEY,
  parcel_id TEXT NOT NULL,
  ts_utc TIMESTAMPTZ NOT NULL,
  label TEXT NOT NULL CHECK (label IN ('NORMAL','ALERT'))
);

-- Minimal RBAC: read-only and writer roles
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_writer') THEN
    CREATE ROLE app_writer LOGIN PASSWORD 'change_me_writer';
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_reader') THEN
    CREATE ROLE app_reader LOGIN PASSWORD 'change_me_reader';
  END IF;
END$$;

GRANT INSERT, SELECT ON telemetry_events, alerts TO app_writer;
GRANT SELECT ON telemetry_events, alerts, labels TO app_reader;
