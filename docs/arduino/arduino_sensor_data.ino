#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <SoftwareSerial.h>

MAX30105 particleSensor;
SoftwareSerial ESPSerial(3, 2); // RX, TX

const byte RATE_SIZE = 4; 
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0; 
float beatsPerMinute;
int beatAvg;

void setup() {
  Serial.begin(115200);  // For debugging
  ESPSerial.begin(9600); // For communication with ESP8266

  Serial.println("Initializing...");


  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 was not found. Please check wiring/power.");
    while (1);
  }
  
  particleSensor.setup(); 
  particleSensor.setPulseAmplitudeRed(0x0A); 
  particleSensor.setPulseAmplitudeGreen(0); 
  Serial.println("Place your index finger on the sensor with steady pressure.");
}

void loop() {
  long irValue = particleSensor.getIR();
  
  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;
      beatAvg = 0;
      for (byte x = 0 ; x < RATE_SIZE ; x++)
        beatAvg += rates[x];
      beatAvg /= RATE_SIZE;
    }
  }


  String dataString = String(beatAvg) + "," +
                      String(random(98, 100)) + "," +
                      String(random(0, 800)) + "," + 
                      String(random(95, 100)); 


  ESPSerial.println(dataString);


  Serial.print("IR=");
  Serial.print(irValue);
  Serial.print(", Avg BPM=");
  Serial.print(beatAvg);
  Serial.print(", Temp=");
  Serial.println(" C");
  Serial.println("Sent: " + dataString);

  if (irValue < 50000)
    Serial.println(" No finger?");

  delay(10); 
}