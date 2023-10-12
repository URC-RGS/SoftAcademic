// подключаем библиотеки 
#include <Arduino.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <Config.h>
#include <GyverFilters.h>
#include <LiquidCrystal_I2C.h>

AsyncStream<100> serial(&Serial, '\n');
AsyncStream<100> serial1(&Serial1, '\n');
AsyncStream<100> serial2(&Serial2, '\n');

uint32_t turnTimer;
int ledState = LOW;

void setup() {
  Serial.begin(BITRATE);

  // подключение сериала для общения с роботом 
  Serial1.setRX(UART_0_RX);
  Serial1.setTX(UART_0_TX);
  Serial1.begin(BITRATE);
  pinMode(UART_COM, OUTPUT);
  digitalWrite(UART_COM, HIGH);

  // подключение сериала для общения с постом управления 
  Serial2.setRX(UART_1_RX);
  Serial2.setTX(UART_1_TX);
  Serial2.begin(BITRATE);

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(19, OUTPUT);
}

void loop() {
  // если данные получены
  if (serial2.available()) {     

    // выводим их (как char*)
    Serial1.println(serial2.buf);  

    Serial.println(serial2.buf);   
  }

  // мигалка для индикации работы 
  if (millis()- turnTimer >= 200){
    turnTimer = millis();

    if (ledState == LOW) ledState = HIGH;
    else ledState = LOW;

    digitalWrite(LED_BUILTIN, ledState);
   }
}