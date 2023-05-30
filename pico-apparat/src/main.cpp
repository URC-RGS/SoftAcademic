// подключаем библиотеки 
#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <ServoSmooth.h>
#include <Config.h>
#include <GyverFilters.h>


ServoSmooth servos[6];
AsyncStream<100> serial(&Serial1, '\n');
// TODO подобрать параметры измерения вольтажа
GKalman testFilter(10, 10, 0.1);
uint32_t turnTimer;


void setup() {
  // подключение отладочного сериала 
  Serial.begin(115200);
  // подключение сериала для общения с постом управления 
  // !!! ВАЖНО !!!
  // на Serial сидит крыса и ей критично чтобы перед инициализацией были определены пины,
  // иначе она убивает ядро и пика начинает определяться как неопознанное устройство 
  Serial1.setRX(UART_RX);
  Serial1.setTX(UART_TX);
  Serial1.begin(115200);

  // подключаем моторы 
  servos[0].attach(PIN_MOTOR_0, 1000, 2000);
  servos[0].setSpeed(2000);
  servos[0].setAccel(0.95);
  servos[0].writeMicroseconds(1500);
  servos[0].setAutoDetach(false);

  servos[1].attach(PIN_MOTOR_1, 1000, 2000);
  servos[1].setSpeed(2000);
  servos[1].setAccel(0.95);
  servos[1].writeMicroseconds(1500);
  servos[1].setAutoDetach(false);

  servos[2].attach(PIN_MOTOR_2, 1000, 2000);
  servos[2].setSpeed(2000);
  servos[2].setAccel(0.95);
  servos[2].writeMicroseconds(1500);
  servos[2].setAutoDetach(false);

  servos[3].attach(PIN_MOTOR_3, 1000, 2000);
  servos[3].setSpeed(2000);
  servos[3].setAccel(0.95);
  servos[3].writeMicroseconds(1500);
  servos[3].setAutoDetach(false);

  delay(3000);

  // подключаем камеру и устанавливаем стартовое положение 
  servos[4].attach(PIN_SERVO_CAM, 600, 2400);
  servos[4].setSpeed(200);
  servos[4].setAccel(0.2);
  // плавно поворачиваем сервопривод камеры в вверхнее положение 
  for (int pos = 90; pos <= 180; pos += 1) { 
    servos[4].setTargetDeg(pos);              
    delay(20);}
  delay(500);
  // плавно поворачиваем сервопривод камеры в нижнее положение
  for (int pos = 180; pos >= 0; pos -= 1) { 
    servos[4].setTargetDeg(pos);              
    delay(20);}
  delay(500);
  // плавно поворачиваем сервопривод камеры в среднее положение
  for (int pos = 0; pos <= 90; pos += 1) { 
    servos[4].setTargetDeg(pos);             
    delay(20);}
  delay(500);

  // подключаем манипулятор
  servos[5].attach(PIN_SERVO_ARM, 600, 2400);
  servos[5].setSpeed(100);
  servos[5].setAccel(0.5);
}

void loop() {
  if (millis()- turnTimer >= 20){
    turnTimer = millis();
    servos[0].tick();
    servos[1].tick();
    servos[2].tick();
    servos[3].tick();
    servos[4].tick();
    servos[5].tick();
  }
    
  // если данные получены
  if (serial.available()) {
    // парсим данные по резделителю возвращает список интов 
    GParser data = GParser(serial.buf, ' ');
    if (DEBUG) Serial.println(serial.buf);
    int data_input[data.amount()];
    int am = data.parseInts(data_input);

    // отправляем значения на микроконтроллер 
    int motor_0_out = 1000 + (data_input[0] * 10);
    int motor_1_out = 1000 + (data_input[1] * 10);
    int motor_2_out = 1000 + (data_input[2] * 10);
    int motor_3_out = 1000 + (data_input[3] * 10);

    servos[0].setTarget(motor_0_out);
    servos[1].setTarget(motor_1_out);
    servos[2].setTarget(motor_2_out);
    servos[3].setTarget(motor_3_out);

    // отправляем значения на сервопривод камеры и манипулятора 
    servos[4].setTargetDeg(data_input[8]);
    servos[5].setTargetDeg(data_input[9]);

    // отправка вольтажа на пост управления 
    // Serial1.println(testFilter.filtered(analogRead(28)));
    Serial1.println(serial.buf);
    if (DEBUG) Serial.println(testFilter.filtered(analogRead(28)));
  }  
}
