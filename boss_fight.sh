#!/usr/bin/env bash
set -euo pipefail
echo "Simulating DB outage for 60s..."
docker compose stop -t 0 postgres
sleep 60
docker compose start postgres
echo "Postgres back online."
