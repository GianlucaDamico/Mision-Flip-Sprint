# Flip Sprint: GreenDelivery — End-to-End Prototype

## Cómo arrancar (paso a paso)
1) Copia `.env.example` a `.env` y ajusta valores.
2) `docker compose up -d` (lanza Mosquitto, Postgres, Node-RED, Metabase).
3) Abre Node-RED en http://localhost:1880 (el flow ya está montado desde `flows/flows.json`).
4) (Opcional) Verifica BD: `docker exec -it postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"`.
5) Simula telemetría:
   ```bash
   cd simulator && python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python simulator.py --parcel BX-001 --seconds 120 --anomaly
   python simulator.py --parcel BX-002 --seconds 120
   ```
6) Configura Metabase en http://localhost:3000 y crea los KPIs con los SQL de `dashboards/`.
7) Importa etiquetas: carga `analytics/labels.csv` en la tabla `labels` (puedes usar Metabase o `\copy`).
8) Prueba la alerta en Slack (pon tu `SLACK_WEBHOOK_URL` en `.env`).

## Boss-Fight
Ejecuta `./boss_fight.sh` para simular caída de la BD 60s. Verás cómo la cola de reintentos evita pérdida de datos.

## Evaluación del modelo
```
python analytics/evaluate_model.py
```

## Estructura
Consulte la pauta del enunciado; este repo ya incluye `diagrams/`, `flows/`, `db/ddl.sql`, `dashboards/`, `analytics/`, `security/`, `doc/`, `video/`.

mario lo hizo todo