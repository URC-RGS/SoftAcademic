#include "BrushlessMotor.h"

BrushlessMotor::BrushlessMotor(uint8_t pin)
{
	m_pin = pin;
}

void BrushlessMotor::init()
{
	m_driver.attach(m_pin);
	m_driver.writeMicroseconds(1500);
}

void BrushlessMotor::set_power(int8_t power)
{
	m_power = constrain(power, -100, 100);
	m_power = m_is_inverse ? m_power * -1 : m_power;
	int pulse = map(m_power, -100, 100, 1000, 2000);
	m_driver.writeMicroseconds(pulse);
}
