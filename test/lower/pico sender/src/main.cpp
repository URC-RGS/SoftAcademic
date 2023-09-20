#include <Arduino.h>
#include <Config.h>

uint16_t count = 0;

void setup() {
  // инициализация отладочного сериала 
  Serial.begin(57600);
  
  // инициализация сериала для отправки на основной пульт 
  Serial1.setRX(UART_RX);
  Serial1.setTX(UART_TX);

  pinMode(UART_COM, OUTPUT);
  digitalWrite(UART_COM, HIGH);

  Serial1.begin(9600);
}

void loop() {
  // отправка строки 
  Serial1.println(count);
  Serial.print('send ');
  Serial.println(count);
  count  = count + 1;
  delay(TIMEOUT);                
}