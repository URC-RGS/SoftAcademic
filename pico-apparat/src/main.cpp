#include <Arduino.h>
#include <Servo.h>
#include <GParser.h>
#include <AsyncStream.h>
#include <Config.h>
#include <GyverFilters.h>


Servo servos[6];
AsyncStream<100> serial(&Serial, '\n');
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

  Serial1.println("Start rov");

  // подключаем моторы 
  servos[0].attach(PIN_MOTOR_0, 1000, 2000, 90);
  servos[1].attach(PIN_MOTOR_1, 1000, 2000, 90);
  servos[2].attach(PIN_MOTOR_2, 1000, 2000, 90);
  servos[3].attach(PIN_MOTOR_3, 1000, 2000, 90);
  // подключаем камеру и устанавливаем стартовое положение 
  servos[4].attach(PIN_SERVO_CAM);
  // плавно поворачиваем сервопривод в вверхнее положение 
  for (int pos = 90; pos <= 180; pos += 1) { 
    servos[4].write(pos);              
    delay(20);}
  // плавно поворачиваем сервопривод в нижнее положение
  for (int pos = 180; pos >= 0; pos -= 1) { 
    servos[4].write(pos);              
    delay(20);}
  // плавно поворачиваем сервопривод в среднее положение
  for (int pos = 0; pos <= 90; pos += 1) { 
    servos[4].write(pos);             
    delay(20);}

  // подключаем манипулятор
  servos[5].attach(PIN_SERVO_ARM);
}

void loop() {
  // если данные получены
  if (serial.available()) {
    // парсим данные по резделителю возвращает список интов 
    GParser data = GParser(serial.buf, ' ');
    int data_input[data.amount()];
    int am = data.parseInts(data_input);

    // отправляем значения на микроконтроллер 
    servos[0].writeMicroseconds(1000 + (data_input[0] * 10));
    servos[1].writeMicroseconds(1000 + (data_input[1] * 10));
    servos[2].writeMicroseconds(1000 + (data_input[2] * 10));
    servos[3].writeMicroseconds(1000 + (data_input[3] * 10));

    // отправляем значения на сервопривод камеры и манипулятора 
    servos[4].write(data_input[8]);
    servos[5].write(data_input[9]);

    // отправка вольтажа на пост управления 
    Serial.println(testFilter.filtered(analogRead(28)));

  }  
}
