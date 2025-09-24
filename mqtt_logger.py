import sqlite3
import paho.mqtt.client as mqtt
import time
import sys
import os

BROKER = "localhost"           # lokalny broker - jeśli uruchamiasz na tym samym RPi
TOPIC = "stacja"
DB_FILE = "mqtt_data.db"

# --- baza ---
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS pomiary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    payload TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# --- callbacki ---
def on_connect(client, userdata, flags, rc):
    print(f"[on_connect] rc={rc}")
    if rc == 0:
        print("[on_connect] Połączono z brokerem, subskrybuję topic...")
        client.subscribe(TOPIC)
    else:
        print("[on_connect] Błąd połączenia, rc=", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[on_subscribe] subskrypcja potwierdzona, mid={mid}, qos={granted_qos}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
    except Exception as e:
        payload = str(msg.payload)
    print(f"[on_message] {msg.topic} -> {payload}")
    print(f"[on_message] baza: {os.path.abspath(DB_FILE)}")

    try:
        conn = sqlite3.connect(DB_FILE)  # otwieramy połączenie
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pomiary (topic, payload) VALUES (?, ?)", 
            (msg.topic, payload)
        )
        conn.commit()
        conn.close()  # zamykamy połączenie
    except Exception as e:
        print("[on_message] Błąd zapisu do DB:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

try:
    print("Łączenie z brokerem:", BROKER)
    client.connect(BROKER, 1883, 60)
except Exception as e:
    print("Błąd przy connect():", e)
    sys.exit(1)

print("Czekam na dane...")
client.loop_forever()

