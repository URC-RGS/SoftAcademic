#include "Timer.h"
#include <Arduino.h>

Timer::Timer()
{
	m_isStarted = false;
}

void Timer::start()
{
	m_isStarted = true;
	m_start = millis();
}

long Timer::elapsed()
{
	return m_isStarted ? millis() - m_start : 0;
}

bool Timer::is_started()
{
	return m_isStarted;
}

void Timer::stop()
{
	m_isStarted = false;
}
