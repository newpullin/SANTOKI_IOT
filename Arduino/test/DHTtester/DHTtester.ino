#include "DHT.h"

#define DHT_PIN 2
#define DHTTYPE DHT11

int hum;
int temp;

DHT dht(DHT_PIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
}

void loop() {
  hum =  dht.readHumidity();
  temp = dht.readTemperature();

  Serial.print("Hum : ");
  Serial.print(hum);
  Serial.print(" Tem : ");
  Serial.print(temp);
  Serial.print("\n");
  delay(3000);
}


// https://it-g-house.tistory.com/9
