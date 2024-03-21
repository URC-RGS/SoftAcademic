// подключаем библиотеки 
#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <ServoSmooth.h>
#include <Config.h>
#include "MS5837.h"
#include <GyverFilters.h>
#include <Wire.h>

ServoSmooth servos[8];
AsyncStream<100> serialCom(&Serial1, '\n');
// TODO подобрать параметры измерения вольтажа
GKalman testFilter(10, 10, 0.1);
uint32_t turnTimer;
int ledState = LOW;
MS5837 sensor;


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  // подключение отладочного сериала 
  Serial.begin(BITRATE);
  // подключение сериала для общения с постом управления 
  Serial1.setRX(UART_RX);
  Serial1.setTX(UART_TX);
  pinMode(UART_COM, OUTPUT);
  digitalWrite(UART_COM, LOW);
  Serial1.begin(BITRATE);
  
  if (DEPTH) {
    Wire.setSDA(20);
    Wire.setSCL(21);
    Wire.begin();

    while (!sensor.init()) {
      Serial.println("Init failed!");
      Serial.println("Are SDA/SCL connected correctly?");ё
      Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
      Serial.println("\n\n\n");
      delay(5000);
    }
    sensor.setModel(MS5837::MS5837_30BA);
    sensor.setFluidDensity(997); // плотность воды 
  }

  // подключаем моторы 
  servos[0].attach(PIN_MOTOR_0, 1000, 2000);
  servos[0].setSpeed(SPEED_MOTORS);
  servos[0].setAccel(ACCEL_MOTORS);
  servos[0].setAutoDetach(false);
  // servos[0].setDirection(REVERSE_MOTOR_0);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000);
  servos[1].setSpeed(SPEED_MOTORS);
  servos[1].setAccel(ACCEL_MOTORS);
  servos[1].setAutoDetach(false);
  // servos[1].setDirection(REVERSE_MOTOR_1);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000);
  servos[2].setSpeed(SPEED_MOTORS);
  servos[2].setAccel(ACCEL_MOTORS);
  servos[2].setAutoDetach(false);
  // servos[2].setDirection(REVERSE_MOTOR_2);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000);
  servos[3].setSpeed(SPEED_MOTORS);
  servos[3].setAccel(ACCEL_MOTORS);
  servos[3].setAutoDetach(false);
  // servos[3].setDirection(REVERSE_MOTOR_3);

  servos[4].attach(PIN_MOTOR_4, 1000, 2000);
  servos[4].setSpeed(SPEED_MOTORS);
  servos[4].setAccel(ACCEL_MOTORS);
  servos[4].setAutoDetach(false);
  // servos[4].setDirection(REVERSE_MOTOR_4);

  servos[5].attach(PIN_MOTOR_5, 1000, 2000);
  servos[5].setSpeed(SPEED_MOTORS);
  servos[5].setAccel(ACCEL_MOTORS);
  servos[5].setAutoDetach(false);
  // servos[5].setDirection(REVERSE_MOTOR_5);

  servos[6].attach(PIN_SERVO_CAM, 1000, 2000);
  servos[6].setSpeed(SPEED_SERVO);
  servos[6].setAccel(ACCELERATE_SERVO);
  servos[6].writeMicroseconds(1500);
  servos[6].setAutoDetach(false);

  servos[7].attach(PIN_SERVO_ARM, 1000, 2000);
  servos[7].setSpeed(SPEED_SERVO);
  servos[7].setAccel(ACCELERATE_SERVO);
  servos[7].writeMicroseconds(1500);
  servos[7].setAutoDetach(false);

  servos[0].writeMicroseconds(2000);
  servos[1].writeMicroseconds(2000);
  servos[2].writeMicroseconds(2000);
  servos[3].writeMicroseconds(2000);
  servos[4].writeMicroseconds(2000);
  servos[5].writeMicroseconds(2000);
  delay(5000);
  // servos[0].writeMicroseconds(1000);
  // servos[1].writeMicroseconds(1000);
  // servos[2].writeMicroseconds(1000);
  // servos[3].writeMicroseconds(1000);
  // servos[4].writeMicroseconds(1000);
  // servos[5].writeMicroseconds(1000);
  // delay(5000);
  servos[0].writeMicroseconds(1500);
  servos[1].writeMicroseconds(1500);
  servos[2].writeMicroseconds(1500);
  servos[3].writeMicroseconds(1500);
  servos[4].writeMicroseconds(1500);
  servos[5].writeMicroseconds(1500);
  delay(5000);

  digitalWrite(LED_BUILTIN, LOW);

}

void loop(){
  
}


void loop1() {
  if (millis()- turnTimer >= 15){
    turnTimer = millis();
    servos[0].tick();
    servos[1].tick();
    servos[2].tick();
    servos[3].tick();
    servos[4].tick();
    servos[5].tick();
    servos[6].tick();
    servos[7].tick();

    // мигалка для индикации работы
    if (ledState == LOW) ledState = HIGH;
      else ledState = LOW;
    digitalWrite(LED_BUILTIN, ledState);
  }
    
  // если данные получены
  if (serialCom.available()) {

    // парсим данные по резделителю возвращает список интов 
    GParser data = GParser(serialCom.buf, ' ');

    if (DEBUG) Serial.println(serialCom.buf);

    if (data.amount() == 11){

      int data_input[data.amount()];
      int am = data.parseInts(data_input);

      // отправляем значения движители 
      servos[0].writeMicroseconds(data_input[0]);
      servos[1].writeMicroseconds(3000 - data_input[1]);
      servos[2].writeMicroseconds(data_input[2]);
      servos[3].writeMicroseconds(3000 - data_input[3]);
      servos[4].writeMicroseconds(3000 - data_input[4]);
      servos[5].writeMicroseconds(data_input[5]);

      // отправляем значения на сервопривод камеры и манипулятора 
      servos[6].writeMicroseconds(data_input[8]);
      servos[7].writeMicroseconds(data_input[9]);

      if (FEEDBEAK){
        // sensor.read();
        digitalWrite(UART_COM, HIGH);
        delay(5);

        // ответ на пост управления, в перспективе отправка данных с датчика оринтеции 
        Serial1.println(testFilter.filtered(analogRead(28) * 0.0359));
        // Serial1.print(' ');
        // Serial1.print(sensor.temperature());
        // Serial1.print(' ');
        // Serial1.println(sensor.depth()); 

        if (DEBUG) {
          Serial.println(testFilter.filtered(analogRead(28) * 0.0359));
          // Serial.print(' ');
          // Serial.print(sensor.temperature());
          // Serial.print(' ');
          // Serial.println(sensor.depth()); 
        }
        delay(5);
        digitalWrite(UART_COM, LOW);
      }
    }
  }  
}
