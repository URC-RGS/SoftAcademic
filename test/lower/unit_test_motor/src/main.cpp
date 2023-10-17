#include <Arduino.h>
#include <GParser.h>
#include <ServoSmooth.h>
#include <AsyncStream.h>
#include <Config.h>


ServoSmooth servos[8];
AsyncStream<50> serial(&Serial, '\n');
uint32_t servoTimer;

void setup() {
  Serial.begin(57600);
  
  // подключаем
  servos[0].attach(PIN_MOTOR_0, 1000, 2000);
  servos[0].setSpeed(SPEED_MOTOR);
  servos[0].setAccel(ACCELERATE_MOTOR);
  servos[0].writeMicroseconds(1500);
  servos[0].setAutoDetach(false);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000);
  servos[1].setSpeed(SPEED_MOTOR);
  servos[1].setAccel(ACCELERATE_MOTOR);
  servos[1].writeMicroseconds(1500);
  servos[1].setAutoDetach(false);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000);
  servos[2].setSpeed(SPEED_MOTOR);
  servos[2].setAccel(ACCELERATE_MOTOR);
  servos[2].writeMicroseconds(1500);
  servos[2].setAutoDetach(false);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000);
  servos[3].setSpeed(SPEED_MOTOR);
  servos[3].setAccel(ACCELERATE_MOTOR);
  servos[3].writeMicroseconds(1500);
  servos[3].setAutoDetach(false);

  servos[4].attach(PIN_MOTOR_4, 1000, 2000);
  servos[4].setSpeed(SPEED_MOTOR);
  servos[4].setAccel(ACCELERATE_MOTOR);
  servos[4].writeMicroseconds(1500);
  servos[4].setAutoDetach(false);

  servos[5].attach(PIN_MOTOR_5, 1000, 2000);
  servos[5].setSpeed(SPEED_MOTOR);
  servos[5].setAccel(ACCELERATE_MOTOR);
  servos[5].writeMicroseconds(1500);
  servos[5].setAutoDetach(false);

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
}


void loop() {
  // каждые 20 мс
  if (millis() - servoTimer >= 20) {  // взводим таймер на 20 мс (как в библиотеке)
    servoTimer += 20;
    for (byte i = 0; i < 8; i++) {
      servos[i].tickManual();   // двигаем все сервы. Такой вариант эффективнее отдельных тиков
    }
  } 

  if (serial.available()) {     // если данные получены
    GParser data = GParser(serial.buf, ' ');
    int am = data.split();
    if (am == 2) {
      int pin = data.getInt(0);
      int pwm_out = data.getInt(1);
      if (pin > -1 and pin < 8 and pwm_out > 999 and pwm_out < 2001){
        Serial.print("Output: ");
        Serial.print(data.getInt(0));
        Serial.print(" PWM: ");
        Serial.println(data.getInt(1));
        // непосредственно подача шим на указанный пин
        servos[pin].writeMicroseconds(pwm_out);} 

      else Serial.println("Error");
      }
    else Serial.println("Error"); 
  }
}


/*
   Данный код плавно двигает туда-сюда одной сервой (на пине 5)
   Наблюдаем за графиком угла в плоттере (Инструменты/Плоттер по последовательному соединения)
   Документация: https://alexgyver.ru/servosmooth/
*/

// #include <ServoSmooth.h>
// ServoSmooth servo;

// uint32_t tmr;
// boolean flag;

// void setup() {
//   Serial.begin(9600);
//   servo.attach(6, 500, 2400);      // подключить
//   servo.setSpeed(100);  // ограничить скорость
//   servo.setAccel(0.7);    // установить ускорение (разгон и торможение)
//   servo.setAutoDetach(false);
//   servo.setMaxAngle(180);
//   //servo.setDirection(REVERSE);
// }

// void loop() {
//   Serial.print(servo.getCurrentDeg());
//   Serial.print(' ');
//   Serial.print(servo.getTargetDeg());
//   Serial.print(' ');
//   Serial.println(servo.tick() * 10);	// состояние серво третьим графиком
//   delay(10);


//   static uint32_t timer;
//   if (millis() - timer > 3000) {
//     static bool kek = false;
//     kek = !kek;
//     timer = millis();
//     servo.setTargetDeg(kek ? 0 : 180);
//   }
// }