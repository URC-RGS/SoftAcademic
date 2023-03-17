#include "LevelMotor.h"

LevelMotor::LevelMotor(uint8_t pin_left, uint8_t pin_right)
{
	m_driver_right = pin_right;
	m_driver_left = pin_left;
}
void LevelMotor::init()
{
	pinMode(m_driver_left, OUTPUT);
	pinMode(m_driver_right, OUTPUT);
}
void LevelMotor::set_power(int8_t power)
{
	m_power = constrain(power, -100, 100);
	m_power = m_is_inverse ? m_power * -1 : m_power;
	if (m_power == 0)
	{
		digitalWrite(m_driver_left, LOW);
		digitalWrite(m_driver_right, LOW);
	}
	else if (m_power > 0)
	{
		digitalWrite(m_driver_left, HIGH);
		digitalWrite(m_driver_right, LOW);
	}
	else
	{
		digitalWrite(m_driver_left, LOW);
		digitalWrite(m_driver_right, HIGH);
	}
}
