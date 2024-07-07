#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>

const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

ESP8266WebServer server(80);
SoftwareSerial ArduinoSerial(D2, D3); // RX, TX

float heartRate = 0;
float temperature = 0;
float ecg = 0;
float spo2 = 0;

void setup() {
  Serial.begin(115200);
  ArduinoSerial.begin(9600);
  Serial.print("Hello");
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/data", HTTP_GET, handleGetData);
  server.begin();
}

void loop() {
  server.handleClient();
  
  if (ArduinoSerial.available()) {

    String payload = ArduinoSerial.readStringUntil('\n');
    payload.trim();
    
    sscanf(payload.c_str(), "%f,%f,%f,%f", &heartRate, &temperature, &ecg, &spo2);
  }
}

void handleGetData() {
  DynamicJsonDocument doc(1024);
  doc["heartRate"] = heartRate;
  doc["temperature"] = temperature;
  doc["ecg"] = ecg;
  doc["spo2"] = spo2;

  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}