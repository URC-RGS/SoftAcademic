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
  servos[0].attach(PIN_MOTOR_0, 1000, 2000, 90);
  servos[0].setSpeed(ACCELERATE_MOTOR);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000, 90);
  servos[1].setSpeed(ACCELERATE_MOTOR);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000, 90);
  servos[2].setSpeed(ACCELERATE_MOTOR);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000, 90);
  servos[3].setSpeed(ACCELERATE_MOTOR);

  servos[4].attach(PIN_MOTOR_4, 1000, 2000, 90);
  servos[4].setSpeed(ACCELERATE_MOTOR);

  servos[5].attach(PIN_MOTOR_5, 1000, 2000, 90);
  servos[5].setSpeed(ACCELERATE_MOTOR);

  servos[6].attach(PIN_SERVO_CAM, 1000, 2000, 90);
  servos[6].setSpeed(SPEED_SERVO);
  servos[6].setAccel(ACCELERATE_SERVO);

  servos[7].attach(PIN_SERVO_ARM, 1000, 2000, 90);
  servos[7].setSpeed(SPEED_SERVO);
  servos[7].setAccel(ACCELERATE_SERVO);

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
        servos[pin].setTarget(pwm_out);} 
      
      else Serial.println("Error");
      }
    else Serial.println("Error"); 
  }
}


