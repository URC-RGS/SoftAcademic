#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <Config.h>


Servo servos[8];
AsyncStream<50> serial(&Serial, '\n');
uint32_t servoTimer;


void setup() {
  // подключение отладочного сериала 
  Serial.begin(9600);
  // подключение сериала для общения с постом управления 
  Serial1.begin(UART_SPEED);
  Serial1.setRX(UART_RX);
  Serial1.setTX(UART_TX);

  // подключаем моторы 
  servos[0].attach(PIN_MOTOR_0, 1000, 2000, 90);
  servos[1].attach(PIN_MOTOR_1, 1000, 2000, 90);
  servos[2].attach(PIN_MOTOR_2, 1000, 2000, 90);
  servos[3].attach(PIN_MOTOR_3, 1000, 2000, 90);
  servos[4].attach(PIN_MOTOR_4, 1000, 2000, 90);
  servos[5].attach(PIN_MOTOR_5, 1000, 2000, 90);
  // подключаем камеру и устанавливаем стартовое положение 
  servos[6].attach(PIN_SERVO_CAM);
  servos[6].write(90);
  // подключаем манипулятор и устанавливаем стартовое положение 
  servos[7].attach(PIN_SERVO_ARM);
  servos[6].write(90);
  delay(1000);
  Serial.println("Start ROV");

}

void loop() {
    if (serial.available()) {     // если данные получены
    GParser data = GParser(serial.buf, ' ');
    int am = data.split();
    if (am == 8) {
      int pin = data.getInt(0);
      int pwm_out = data.getInt(1);
      if (pin > -1 and pin < 8 and pwm_out > 999 and pwm_out < 2001){
        Serial.print("Output: ");
        Serial.print(pin);
        Serial.print(" PWM: ");
        Serial.println(pwm_out);
        // непосредственно подача шим на указанный пин
        servos[pin].writeMicroseconds(pwm_out);
        Serial.println("OK");} 
      
      else Serial.println("Error");
      }
    else Serial.println("Error"); 
  }
}
