#include <Arduino.h>
#include <AsyncStream.h>
#include <GParser.h>

// асинхронная читалка Serial
// а также любых из класса Stream
// указываем обработчик, терминатор (символ конца приёма) и таймаут в мс
// в <> указан размер буфера!

AsyncStream<100> serial(&Serial, '\n');


void setup() {
  Serial.begin(57600);
}

void loop() {
  // если данные получены
  if (serial.available()) {     
    GParser data(serial.buf, ',');
    int ints[data.amount()];
    // раскидает в указанный массив и вернёт количество
    int am2 = data.parseInts(ints);  
    // выводим
    Serial.println("");
    for (byte i = 0; i < am2; i++) Serial.println(ints[i]);
  }
}