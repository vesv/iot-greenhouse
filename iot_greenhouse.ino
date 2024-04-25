#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int soilMoisturePin = A0; // Analog input pin for the soil moisture sensor
const int pumpPin = 7; // Digital output pin for the pump

void setup() {
    Serial.begin(9600);
    dht.begin();
    pinMode(pumpPin, OUTPUT); // Set the pump pin as an output

}

void loop() {
    delay(2000); // Wait a bit before taking the next reading
    
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    int soilMoistureRaw = analogRead(soilMoisturePin);
    
    if (soilMoisture < 410) { // 40% of 1023 is about 410
        digitalWrite(pumpPin, HIGH);
    } else if (soilMoisture > 614) { // 60% of 1023 is about 614
        digitalWrite(pumpPin, LOW);       
    //float soilMoisturePercent = (soilMoistureRaw / 1023.0) * 100;  // Convert to percentage
    //Serial.print('\n');
    //Serial.print("Current humidity = ");
    //Serial.print(h);
    //Serial.print("%  ");
    //Serial.print("temperature = ");
    //Serial.print(t);
    //Serial.print(" Soil Moisture = ") ;
    //Serial.print(soilMoisturePercent);

    Serial.print(h);
    Serial.print(",");
    Serial.print(t);
    Serial.print(",");
    Serial.println(soilMoisturePercent);

    }
