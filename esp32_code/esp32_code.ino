#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// WiFi configuration
const char* ssid = "NETGEAR60";
const char* password = "aquaticpotato892";

// konfiguracja MQTT
const char* mqtt_server = "192.168.0.50"; // Raspberry Pi IP

WiFiClient espClient;
PubSubClient client(espClient);

// DHT configuration
#define DHTPIN 13        // pin, do którego podłączony jest DATA z DHT22
#define DHTTYPE DHT22   // typ czujnika
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Łączenie z ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi połączone!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Łączenie z MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Połączono!");
    } else {
      Serial.print("błąd, rc=");
      Serial.print(client.state());
      Serial.println("Ponawianie za 3s");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  dht.begin();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // odczyt temperatury i wilgotności
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Błąd odczytu z DHT22!");
    return;
  }

  Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.print("°C  Wilgotność: ");
  Serial.print(h);
  Serial.println("%");

  // wysyłanie temperatury
  char tempMsg[10];
  dtostrf(t, 6, 2, tempMsg);  // (wartość, szerokość, miejsca po przecinku, bufor)
  client.publish("stacja/temperatura", tempMsg);

  // wysyłanie wilgotności
  char humMsg[10];
  dtostrf(h, 6, 2, humMsg);
  client.publish("stacja/wilgotnosc", humMsg);

  delay(5000); // co 5 sekund
}
