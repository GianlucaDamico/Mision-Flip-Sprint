# CIA Mini-Threats & Mitigations (Security by Design)

**Confidentiality**
- Secrets in `.env`, never in repo or flows. Use Docker secrets in production.
- Principle of least privilege: DB roles `app_writer` (write), `app_reader` (read-only).
- MQTT auth (username/password). Prefer TLS in production (port 8883). Topics scoped by prefix per customer.

**Integrity**
- Node-RED validates schema/types and sensor ranges before writing.
- All events stored with raw JSON for auditing; compute checks (e.g., hashes) if needed.
- Labels loaded via controlled script; restrict `INSERT` to trusted pipelines.

**Availability**
- Retry queue persisted via `contextStorage: localfilesystem`.
- MQTT QoS=1 and persistent sessions to avoid loss.
- Stateless containers + volumes; can scale readers horizontally.

**Boss Fight Runbook (DB down 60s)**
1. Stop Postgres for 60s: `./boss_fight.sh`.
2. Observe Node-RED `retryQ` growth; no data lost due to queue + MQTT QoS.
3. When DB returns, queue drains and events persist in order.
4. Capture logs and include screenshot in the report.

**Zero-Trust & IAM**
- Network-level segmentation: broker, app, DB in a private network.
- Require MFA for Metabase admin. Restrict anonymous dashboards.
- Audit logs for DB connections and Node-RED admin access.
