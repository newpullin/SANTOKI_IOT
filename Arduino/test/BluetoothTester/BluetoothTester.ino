#include <SoftwareSerial.h>

// TX, RX 0,1 에다가 꽂으면 안됨
#define TX_PIN 3
#define RX_PIN 4


SoftwareSerial BT( TX_PIN, RX_PIN);

void setup() {
   // put your setup code here, to run once:
   Serial.begin(9600);
   
   while(!Serial) {
    ;
   }

   BT.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    BT.write(Serial.read());
  }
  else if(BT.available()) {
    Serial.write(BT.read());
  }
}
