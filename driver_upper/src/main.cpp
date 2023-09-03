// подключаем библиотеки 
#include <Arduino.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <Config.h>
#include <GyverFilters.h>

AsyncStream<100> serial(&Serial, '\n');
AsyncStream<100> serial1(&Serial1, '\n');
AsyncStream<100> serial2(&Serial2, '\n');

uint32_t turnTimer;
int ledState = LOW;

void setup() {
  Serial.begin(BITRATE);

  Serial1.setRX(UART_0_RX);
  Serial1.setTX(UART_0_TX);
  Serial1.begin(BITRATE);
  // подключение сериала для общения с постом управления 
  Serial2.setRX(UART_1_RX);
  Serial2.setTX(UART_1_TX);
  Serial2.begin(BITRATE);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (serial2.available()) {     // если данные получены
    Serial1.println(serial2.buf); // выводим их (как char*)   
    Serial.println(serial2.buf);   
  }

  if (millis()- turnTimer >= 200){
    turnTimer = millis();

    if (ledState == LOW) ledState = HIGH;
    else ledState = LOW;

    digitalWrite(LED_BUILTIN, ledState);
   }
}