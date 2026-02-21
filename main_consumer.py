#main_consumer.py
import json
import queue
import paho.mqtt.client as mqtt
import logging

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "factory/sensor/data"

logging.basicConfig(level=logging.INFO)

# This queue must be imported by the server
sensor_queue = queue.Queue(maxsize=1000)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT")
        client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        # FIX: Just put it in the queue. DO NOT .get() it here.
        sensor_queue.put(payload)
        logging.info(f"Queued data for Engine #{payload.get('unit_nr')}")
    except Exception as e:
        logging.error(f"Error: {e}")

def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="Industrial_Sensor_Consumer")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    # Use loop_start() so it runs in a background thread 
    # and doesn't block the rest of the script
    client.loop_start()
    return client