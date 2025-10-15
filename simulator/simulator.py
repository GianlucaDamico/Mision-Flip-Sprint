import os, json, time, random, argparse
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER_HOST", "localhost")
PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
USER = os.getenv("MQTT_USERNAME", "guest")
PWD  = os.getenv("MQTT_PASSWORD", "guest")
TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "telem")

def jitter(base, j=0.3):
    return base + random.uniform(-j, j)

def main(parcel_id, anomaly=False, seconds=60):
    client = mqtt.Client(client_id=f"sim-{parcel_id}", clean_session=False, protocol=mqtt.MQTTv311)
    client.username_pw_set(USER, PWD)
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    t0 = time.time()
    while time.time() - t0 < seconds:
        # Normal ranges: temp 3-6 C, g_force around 0-1
        temp = random.uniform(3, 6)
        g = random.uniform(0.2, 1.0)

        # Inject anomaly (sustained)
        if anomaly and (time.time() - t0) > seconds/3:
            temp = random.uniform(9.0, 12.5)  # above threshold
            g = random.uniform(2.6, 4.0) if random.random() < 0.3 else g

        payload = {
            "temp": round(temp, 2),
            "g_force": round(g, 2),
            "parcel_id": parcel_id,
            "ts": datetime.now(timezone.utc).isoformat()
        }
        topic = f"{TOPIC_PREFIX}/{parcel_id}/events"
        client.publish(topic, json.dumps(payload), qos=1)
        time.sleep(2.0)
    client.loop_stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcel", default="BX-001")
    parser.add_argument("--anomaly", action="store_true")
    parser.add_argument("--seconds", type=int, default=90)
    args = parser.parse_args()
    main(args.parcel, args.anomaly, args.seconds)
