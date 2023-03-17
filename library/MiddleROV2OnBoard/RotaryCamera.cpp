#include "RotaryCamera.h"

RotaryCamera::RotaryCamera(int8_t pin)
{
	m_pin = pin;
	m_defAngle = 90;
}

void RotaryCamera::init()
{
	m_driver.attach(m_pin);
	m_timer.start();
	m_driver.write(m_defAngle);
	m_angle = m_defAngle;
}

RotaryCamera::~RotaryCamera()
{
	m_driver.detach();
}

void RotaryCamera::rotate(int8_t angle)
{	
	m_lastangle = angle != m_lastangle ? angle : m_lastangle;
	if (m_timer.elapsed() > 30)
	{
		m_angle += m_lastangle;
		m_timer.start();
		m_angle = constrain(m_angle, 25, 165);
		m_driver.write(m_angle);
	}
}
