#pragma once

#include "Motor.h"
#include <Servo.h>

class BrushlessMotor :public Motor {
public:
	BrushlessMotor(uint8_t pin);
	void init();
	void set_power(int8_t power);
private:
	uint8_t m_pin;
	Servo m_driver;
};
