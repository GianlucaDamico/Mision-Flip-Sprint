import os
import json
import time
import random
import argparse
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# --- Configuración del broker MQTT desde variables de entorno ---
BROKER = os.getenv("MQTT_BROKER_HOST", "localhost")
PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
USER = os.getenv("MQTT_USERNAME", "guest")
PWD  = os.getenv("MQTT_PASSWORD", "guest")
TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "vacunas")

# --- Configuración de simulación ---
SIM_INTERVAL = int(os.getenv("SIM_INTERVAL", 5))  # segundos entre datos
TEMP_RANGE = (2.0, 8.0)       # °C
HUMIDITY_RANGE = (30.0, 60.0) # %
GFORCE_RANGE = (0.0, 2.0)     # G
GPS_PATH = [                   # ejemplo de ruta (lat, lon)
    (-34.608, -58.445),
    (-34.607, -58.444),
    (-34.606, -58.443),
    (-34.605, -58.442)
]

# --- Funciones para simular sensores ---
def generar_temperatura(anomaly=False):
    if anomaly:
        return round(random.uniform(9.0, 12.0), 2)
    return round(random.uniform(*TEMP_RANGE), 2)

def generar_humedad(anomaly=False):
    if anomaly:
        return round(random.uniform(70.0, 90.0), 1)
    return round(random.uniform(*HUMIDITY_RANGE), 1)

def generar_vibracion(anomaly=False):
    if anomaly:
        return round(random.uniform(3.0, 5.0), 2)
    return round(random.uniform(*GFORCE_RANGE), 2)

def generar_gps(index, anomaly=False):
    lat, lon = GPS_PATH[index % len(GPS_PATH)]
    if anomaly and random.random() < 0.3:
        # desviación aleatoria
        lat += random.uniform(0.01, 0.03)
        lon += random.uniform(0.01, 0.03)
    return {"lat": round(lat, 6), "lon": round(lon, 6)}

def generar_apertura(anomaly=False):
    if anomaly and random.random() < 0.3:
        return True
    return random.choice([True, False])

# --- Función principal ---
def main(parcel_id, anomaly=False, seconds=60):
    client = mqtt.Client(client_id=f"sim-{parcel_id}", clean_session=False, protocol=mqtt.MQTTv311)
    client.username_pw_set(USER, PWD)
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    start_time = time.time()
    gps_index = 0

    print(f"Simulación iniciada para {parcel_id}. Enviando datos cada {SIM_INTERVAL}s...")
    try:
        while time.time() - start_time < seconds:
            timestamp = datetime.now(timezone.utc).isoformat()

            temp = generar_temperatura(anomaly)
            hum = generar_humedad(anomaly)
            gforce = generar_vibracion(anomaly)
            gps = generar_gps(gps_index, anomaly)
            door = generar_apertura(anomaly)

            # Publica cada sensor en su topic
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/Temperatura", json.dumps({"ts": timestamp, "value": temp}), qos=1)
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/Humedad", json.dumps({"ts": timestamp, "value": hum}), qos=1)
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/gforce", json.dumps({"ts": timestamp, "value": gforce}), qos=1)
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/Coordenadas", json.dumps({"ts": timestamp, "value": gps}), qos=1)
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/PuertaAbierta", json.dumps({"ts": timestamp, "opened": door}), qos=1)

            # También enviamos un resumen general
            payload = {
                "tS": timestamp,
                "temp": temp,
                "humedad": hum,
                "gforce": gforce,
                "gps": gps,
                "puertaAbierta": door
            }
            client.publish(f"{TOPIC_PREFIX}/{parcel_id}/events", json.dumps(payload), qos=1)

            print("Datos enviados:", payload)
            gps_index += 1
            time.sleep(SIM_INTERVAL)

    except KeyboardInterrupt:
        print("Simulación detenida por usuario.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Cliente MQTT desconectado.")

# --- Ejecutable desde línea de comandos ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcel", default="BX-001", help="ID del paquete")
    parser.add_argument("--anomaly", action="store_true", help="Generar anomalías")
    parser.add_argument("--seconds", type=int, default=60, help="Duración de la simulación en segundos")
    args = parser.parse_args()

    main(args.parcel, args.anomaly, args.seconds)
