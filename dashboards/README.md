# Metabase setup (quick guide)

1) Connect to Postgres using the same creds as in `.env`.
2) Create three Questions using the SQL in this folder:
   - KPI1: `kpi1_sla.sql`
   - KPI2: `kpi2_ttd.sql`
   - KPI3: `kpi3_fp.sql`
3) Add the Questions to a new Dashboard `GreenDelivery KPIs`.
4) Configure an Email or Slack alert on KPI2 or KPI1 and set a condition (e.g., average seconds to detect > 30). Enable 'Don't notify more than once per hour' to throttle.
