#include <Arduino.h>
#include <AsyncStream.h>
#include <GParser.h>

// асинхронная читалка Serial
// а также любых из класса Stream
// указываем обработчик, терминатор (символ конца приёма) и таймаут в мс
// в <> указан размер буфера!

AsyncStream<100> serial1(&Serial1, '\n');


void setup() {
  Serial.begin(115200);

  Serial1.begin(115200);
  Serial1.setRX(17);
  Serial1.setTX(16);
}

void loop() {
  // если данные получены
  if (serial1.available()) {     
    Serial1.println(serial1.buf);
  }
}