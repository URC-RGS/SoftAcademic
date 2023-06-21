#include <Arduino.h>
#include <AsyncStream.h>
#include <GParser.h>

// асинхронная читалка Serial
AsyncStream<100> serial(&Serial1, '\n');


void setup() {
  Serial.begin(115200);

  Serial1.setRX(17);
  Serial1.setTX(16);
  Serial1.begin(115200);

}

void loop() {
  // если данные получены
  if (serial.available()) {     
    Serial1.println(serial.buf);
  }
}