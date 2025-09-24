#include <WiFi.h>
#include <PubSubClient.h>

// WiFi configuration
const  char* ssid = "NETGEAR60";
const char* password = "aquaticpotato892";

// konfiguracja MQTT
const char* mqtt_server = "192.168.0.50"; // Raspberry Pi IP

WiFiClient espClient;
PubSubClient client(espClient);

// noise sensor pin
#define SOUND_PIN 34


void setup_wifi()
{
  delay(10);
  Serial.println();
  Serial.print("Łączenie z ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi połączone!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect()
{
  while(!client.connected())
  {
    Serial.print("Łączenie z MQTT...");
    if(client.connect("ESP32Client"))
    {
      Serial.println("Połączono!");
    } else
    {
      Serial.print("błąd, rc=");
      Serial.print(client.state());
      Serial.println("Ponawianie za 3s");
      delay(3000);
    }
  }
}

void setup()
{
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);

}

void loop()
{
  if(!client.connected())
  {
    reconnect();
  }
  client.loop();
  // odczyt z czujnika hałasu
  int sound_value = analogRead(SOUND_PIN);
  Serial.print("Hałas: ");
  Serial.println(sound_value);

  // sending by MQTT
  char msg[10];
  sprintf(msg, "%d", sound_value); // funkcja sprintf zapisuje wynik do zmiennej msg, "%d" to format, zmienia na liczbę całkowitą
  client.publish("stacja", msg);
  delay(5000);
}

