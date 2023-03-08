#include "Arduino.h"

/*
  Данный код позволяет принять данные, идущие из порта, в строку (String) без "обрывов"
*/
String strData = "";
boolean recievedFlag;
void setup() {
  Serial1.begin(115200);
  delay(1000);
  Serial.println("start");
}
void loop() {
  while (Serial1.available() > 0) {         // ПОКА есть что то на вход    
    strData += (char)Serial1.read();        // забиваем строку принятыми данными
    recievedFlag = true;                   // поднять флаг что получили данные
    delay(10);                              // ЗАДЕРЖКА. Без неё работает некорректно!
  }
  if (recievedFlag) { 
    Serial.print("input ::: ");            // если данные получены
    Serial.println(strData);               // вывести
    strData = "";                          // очистить
    recievedFlag = false;                  // опустить флаг
  }
}