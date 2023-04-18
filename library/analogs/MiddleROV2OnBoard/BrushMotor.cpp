#include "BrushMotor.h"

BrushMotor::BrushMotor(uint8_t pin_left, uint8_t pin_right)
{
	m_driver_left = pin_left;
	m_driver_right = pin_right;
}

void BrushMotor::init()
{
	pinMode(m_driver_right, OUTPUT);
	pinMode(m_driver_left, OUTPUT);
}
void BrushMotor::set_power(int8_t power)
{
	m_power = constrain(power, -100, 100);
	m_power = m_is_inverse ? m_power * -1 : m_power;
	if (m_power < 0)
	{
		analogWrite(m_driver_left, map(abs(m_power), 0, 100, 0, 255));
		analogWrite(m_driver_right, 0);
	}
	else
	{
		analogWrite(m_driver_right, map(abs(m_power), 0, 100, 0, 255));
		analogWrite(m_driver_left, 0);
	}
}
