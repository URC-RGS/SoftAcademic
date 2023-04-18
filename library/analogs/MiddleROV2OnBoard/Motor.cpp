#include "Motor.h"

bool Motor::get_inverse()
{
	return m_is_inverse;
}

void Motor::set_inverse(bool inverse)
{
	m_is_inverse = inverse;
}

int8_t Motor::get_power()
{
	return m_power;
}
