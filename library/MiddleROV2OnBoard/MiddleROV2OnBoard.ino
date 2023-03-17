/*
 Name:		MiddleROV2Surface.ino
 Created:	06.12.2018 17:37:33
 Author:	Zinkov
*/

#include <Arduino.h>
#include "BrushlessMotor.h"
#include "RotaryCamera.h"

#define RS485_CONTROL_PIN 2

#define LEFT_MOTOR_PIN 5
#define RIGHT_MOTOR_PIN 4
#define VERTICAL_MOTOR_PIN 3

#define MANIPULATOR_PIN 6
#define CAMERA_PIN 7

#define MOTOR_PIN1 9
#define MOTOR_PIN2 10

BrushlessMotor leftMotor(LEFT_MOTOR_PIN);
BrushlessMotor rightMotor(RIGHT_MOTOR_PIN);
BrushlessMotor verticalMotor(VERTICAL_MOTOR_PIN);

RotaryCamera camera(CAMERA_PIN);
RotaryCamera manipulator(MANIPULATOR_PIN);

void setup() {
    Serial.begin(115200);
    Serial1.begin(115200);
    Serial.println("Setup");
    // Serial1.println("Setup");
    pinMode(RS485_CONTROL_PIN, OUTPUT);
    digitalWrite(RS485_CONTROL_PIN, HIGH);
    leftMotor.init();
    rightMotor.init();
    verticalMotor.init();
    camera.init();
    manipulator.init();
    delay(1000);

    digitalWrite(RS485_CONTROL_PIN, LOW);
    Serial.println("Entering loop");
}

void motor_button(int8_t data) {
  if (data > 0) {
    digitalWrite(MOTOR_PIN1, HIGH);
    digitalWrite(MOTOR_PIN2, LOW);
  } else if (data < 0) {
    digitalWrite(MOTOR_PIN1, LOW);
    digitalWrite(MOTOR_PIN2, HIGH);
  } else {
    digitalWrite(MOTOR_PIN1, LOW);
    digitalWrite(MOTOR_PIN2, LOW);
  }
}

#define START_BYTE 0xFE
#define END_BYTE 0xEF

#define DEBUG

void loop() {
    if (Serial1.available()) {
    digitalWrite(LED_BUILTIN, HIGH);
        uint8_t first_received_byte = 0;
        Serial1.readBytes(&first_received_byte, 1);
        if (first_received_byte != START_BYTE){
            Serial.println("ERROR (wrong first byte)");
            return;
        }

        uint8_t buffer[8] = {};
        buffer[0] = first_received_byte;
        Serial1.readBytes(buffer + 1, 7);

        if (buffer[0] == START_BYTE && buffer[7] == END_BYTE) {
            leftMotor.set_power(buffer[1]);
            rightMotor.set_power(-buffer[2]);
            verticalMotor.set_power(buffer[3]);
            camera.rotate(buffer[4] * 3);
            manipulator.rotate(buffer[5] * 3);
            motor_button(buffer[6]);
#ifdef DEBUG
            Serial.print((int8_t)buffer[1]); Serial.print(" ");
            Serial.print((int8_t)buffer[2]); Serial.print(" ");
            Serial.print((int8_t)buffer[3]); Serial.print(" ");
            Serial.print((int8_t)buffer[4]); Serial.print(" ");
            Serial.print((int8_t)buffer[5]); Serial.print(" ");
            Serial.println((int8_t)buffer[6]);
#endif // DEBUG
        }
        else {
            Serial.println("ERROR");
            Serial.println(Serial1.readString());
        }
    }
}
