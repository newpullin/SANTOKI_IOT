#include "DHT.h"
#include <SoftwareSerial.h>

#define TX_PIN 3
#define RX_PIN 4

#define DHT_PIN 2
#define DHTTYPE DHT11

#define GREEN_PIN 8
#define YELLOW_PIN 7

DHT dht(DHT_PIN, DHTTYPE);

int hum;
int temp;
String s_hum = ":h:";
String s_tem = ":t:";
String readString;

SoftwareSerial BT(TX_PIN, RX_PIN);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  BT.print(s_hum+String(hum)+s_tem+String(temp));
  while(BT.available()) {
    delay(3);
    char c = BT.read();
    readString += c;
  } vc  
  readString.trim();

  if(readString.length() > 0) {
    if(readString.startsWith("on")) {
      digitalWrite(GREEN_PIN, HIGH);
      digitalWrite(YELLOW_PIN, LOW);
    }
    if(readString.startsWith("of")) {
      digitalWrite(GREEN_PIN, LOW);
      digitalWrite(YELLOW_PIN, HIGH);
    }
  }
  Serial.println(readString);
  readString = "";
  delay(5000);
}
