// подключаем библиотеки 
#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <ServoSmooth.h>
#include <Config.h>
#include <GyverFilters.h>


ServoSmooth servos[6];
AsyncStream<100> serialCom(&Serial1, '\n');
// TODO подобрать параметры измерения вольтажа
GKalman testFilter(10, 10, 0.1);
uint32_t turnTimer;
int ledState = LOW;


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

  // подключаем моторы 
  servos[0].attach(PIN_MOTOR_0, 1000, 2000);
  servos[0].setSpeed(SPEED_MOTORS);
  servos[0].setAccel(ACCEL_MOTORS);
  servos[0].writeMicroseconds(1500);
  servos[0].setAutoDetach(false);
  servos[0].setDirection(REVERSE_MOTOR_0);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000);
  servos[1].setSpeed(SPEED_MOTORS);
  servos[1].setAccel(ACCEL_MOTORS);
  servos[1].writeMicroseconds(1500);
  servos[1].setAutoDetach(false);
  servos[1].setDirection(REVERSE_MOTOR_1);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000);
  servos[2].setSpeed(SPEED_MOTORS);
  servos[2].setAccel(ACCEL_MOTORS);
  servos[2].writeMicroseconds(1500);
  servos[2].setAutoDetach(false);
  servos[2].setDirection(REVERSE_MOTOR_2);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000);
  servos[3].setSpeed(SPEED_MOTORS);
  servos[3].setAccel(ACCEL_MOTORS);
  servos[3].writeMicroseconds(1500);
  servos[3].setAutoDetach(false);
  servos[3].setDirection(REVERSE_MOTOR_3);

  // подключаем камеру 
  servos[4].attach(PIN_SERVO_CAM, 600, 2400);
  servos[4].setSpeed(100);
  servos[4].setAccel(0);

  // подключаем манипулятор
  servos[5].attach(PIN_SERVO_ARM, 600, 2400);
  servos[5].setSpeed(200);
  servos[5].setAccel(0.99);
  servos[5].writeMicroseconds(2000);
  digitalWrite(LED_BUILTIN, LOW);

  // инициализируем моторы 
  delay(2000);
}

void loop() {
  if (millis()- turnTimer >= 15){
    turnTimer = millis();
    servos[0].tick();
    servos[1].tick();
    servos[2].tick();
    servos[3].tick();
    servos[4].tick();
    servos[5].tick();

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
      servos[1].writeMicroseconds(data_input[1]);
      servos[2].writeMicroseconds(data_input[2]);
      servos[3].writeMicroseconds(data_input[3]);

      // отправляем значения на сервопривод камеры и манипулятора 
      servos[4].writeMicroseconds(data_input[8]);
      servos[5].writeMicroseconds(data_input[9]);

      if (FEEDBEAK){
        // ответ на пост управления, в перспективе отправка данных с датчика оринтеции 
        Serial1.println(testFilter.filtered(analogRead(28)));

        if (DEBUG) Serial.println(testFilter.filtered(analogRead(28)));

      }
    }
  }  
}
