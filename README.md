# SoftAcademic

Состав аппарата:
Минимально необходимый функционал для аппарата:

        - управление 4 бесколлекторными двигателями 
        (частота шим 50 герц, длина импулься 1000 - 1500 - 2000
        1000 польный назад, 1500 среднее положение, 2000 полный вперед)

        - уравление сервоприводом поворота камеры
        (частота шим 50 герц, длина импульсов 1000 - 2000)

        - управление сервоприводом манипулятора 
        (частота шим 50 герц, длина импульсов 1000 - 2000)

        - общение по UART с постом управления 
        (скорость 57600 либо 115200)

        - опрос вольтметра с фильтрацией значеней кальманом 

Дополнительный функционал:

        - опрос датчика глубины и температуры MS5837

        - опрос датчика ориентации bno055

        - реализация алгоритмов стабилизации по глубине и по курсу 

        (скорее всего для начала бедет PID контроллер)

        
Общие источники:

https://alexgyver.ru/arduino-algorithms/
https://alexgyver.ru/lessons/parsing/
https://alexgyver.ru/lessons/filters/
https://github.com/GyverLibs/GyverPID
https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/arduino-code
https://github.com/bluerobotics/BlueRobotics_MS5837_Library

Версия 2.0 манипулятор:
- https://wiki.iarduino.ru/page/actuator-linear/
- https://wiki.iarduino.ru/page/current_sensor/
- https://www.chipdip.ru/product/tps5450ddar-2
- https://www.youtube.com/watch?v=qXS617cC6Bw&t=1s
- https://alexgyver.ru/lessons/naked-chip/
- https://alexgyver.ru/lessons/intro/

