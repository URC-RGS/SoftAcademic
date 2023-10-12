import threading
import json
from time import sleep
from sys import platform
from RovCommunication import Rov_SerialPort, Rov_SerialPort_Gebag
from RovJoystick import RovJoystick
from RovLogging import RovLogger
from pprint import pprint


# # запуск на одноплатном пк rock
# PATH_CONFIG = '/home/rock/SoftAcademic/upperAcademic/config_pult.ini'
# PATH_LOG = '/home/rock/SoftAcademic/upperAcademic/.log/'

# # запуск на компьютере в офисе 
PATH_CONFIG = 'C:/Users/Yarik/Documents/SoftAcademic/upperAcademic/config_control_box.json'
PATH_LOG = 'C:/Users/Yarik/Documents/SoftAcademic/upperAcademic/.log/'


class Control_Box:
    def __init__(self):
        '''Основной класс поста управления'''
        # считываем конфиг 
        with open(PATH_CONFIG, 'r') as self.file_config:
            self.config = json.load(self.file_config)
        self.config_control_box = self.config['CONTROL_BOX']

        # конфиг для логера 
        self.config_logi = {'path_log' : PATH_LOG,
                           'log_level' : self.config_control_box['log_level']}
        self.logi = RovLogger(self.config_logi)

        # конфиг для сериал порта 
        self.config_serial  = {'logger' : self.logi,
                                'port' : self.config_control_box['port'],
                                'bitrate' : self.config_control_box['bitrate'],
                                'timeout' : self.config_control_box['timeout_serial'],
                                'debag' : self.config_control_box['local_serial_debag']}

        # создаем экземпляр класса отвечающий за связь с аппаратом
        if self.config_control_box['local_serial_debag']:
            self.serial_port = Rov_SerialPort_Gebag(self.config_serial)
        else:
            self.serial_port = Rov_SerialPort(self.config_serial)  

        # конфиг для джойстика в зависимости от системы 
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            self.config_joystick = self.config['JOYSTICK_LIN']
            self.config_joystick['logger'] = self.logi
            self.logi.info('OC: Lin or Mac')
            
        elif platform == "win32":
            self.config_joystick = self.config['JOYSTICK_WIN']
            self.config_joystick['logger'] = self.logi
            self.logi.info('OC: Win')
            
        self.joystick_ps4 = RovJoystick(self.config_joystick)
        
        # подтягиваем настройки для робота 
        self.config_rov = self.config['ROV']

        # подтягиваем начальные данные с джойстика 
        self.value_joystick = self.joystick_ps4.value

        # частота оптправки
        self.sleep_time = self.config_control_box['sleep_time']

        # флаг проверки подключения 
        self.check_connect = False

        self.logi.info('Control box init')
        
    # запуск прослушивания джойстика 
    def run_joystick(self):
        self.joystick_ps4.listen()

    def run_controller(self):
        # запуск основного цикла
        self.logi.info('Controller run')
               
        def math_three_motors_off_PID(value_joi: dict, value_out: list):
            # сложение векторов и преобразование в частот шим 
            # [M0, M1, M2, M3, M4, M5, M6, M7, CAM(8), GRIPPER(9), LED(10)]
            # математика моторов 2000 - вперед (для манипулятора закрыть) (для светильника включить); 1000 - назад (для манипулятора открыть) (для светильника выключить)
            value_out[0] = int((1500 + value_joi['linear_x'] * 500) + (1500 + value_joi['rotate_y'] * 500) - 1500)
            value_out[1] = int((1500 + value_joi['linear_x'] * 500) - (1500 + value_joi['rotate_y'] * 500) + 1500)
            value_out[2] = int(1500 + value_joi['linear_y'] * 500)

            # математика полезной нагрузки 
            # value_out[8] = # дописать обработку сервопривода 
            value_out[9] = int(1500 - value_joi['gripper'] * 500)
            value_out[10] = int(1000 + value_joi['led'] * 1000)
            
            return value_out
      
        # TODO протестировать на академике 
        def math_four_motors_off_PID(value_joi: dict, value_out: list):
            # сложение векторов и преобразование в частот шим 
            # [M0, M1, M2, M3, M4, M5, M6, M7, CAM(8), GRIPPER(9), LED(10)]
            # математика моторов 2000 - вперед (для манипулятора закрыть) (для светильника включить); 1000 - назад (для манипулятора открыть) (для светильника выключить)
            value_out[0] = int((1500 + value_joi['linear_x'] * 500) + (1500 + value_joi['rotate_y'] * 500) - 1500)
            value_out[1] = int((1500 + value_joi['linear_x'] * 500) - (1500 + value_joi['rotate_y'] * 500) + 1500)
            value_out[2] = int(1500 + value_joi['linear_y'] * 500 + (1500 + value_joi['rotate_x'] * 500) - 1500)
            value_out[3] = int(1500 + value_joi['linear_y'] * 500 - (1500 + value_joi['rotate_x'] * 500) + 1500)
            # математика полезной нагрузки 
            # value_out[8] = # дописать обработку сервопривода 
            value_out[9] = int(1500 - value_joi['gripper'] * 500)
            value_out[10] = int(1000 + value_joi['led'] * 1000)
            
            return value_out

        # TODO протестировать 
        def math_six_motors_off_PID(value_joi: dict, value_out: list):  
            # сложение векторов и преобразование в частот шим 
            # [M0, M1, M2, M3, M4, M5, M6, M7, CAM(8), GRIPPER(9), LED(10)]
            # математика моторов 2000 - вперед (для манипулятора закрыть) (для светильника включить); 1000 - назад (для манипулятора открыть) (для светильника выключить)   
            value_out[0] = int((1500 + value_joi['linear_x'] * 500) + (1500 + value_joi['rotate_y'] * 500) + (1500 + value_joi['linear_z'] * 500) - 3000)
            value_out[1] = int((1500 + value_joi['linear_x'] * 500) - (1500 + value_joi['rotate_y'] * 500) - (1500 + value_joi['linear_z'] * 500) + 3000)
            value_out[2] = int(-1 * (1500 + value_joi['linear_x'] * 500) - (1500 + value_joi['rotate_y'] * 500) + (1500 + value_joi['linear_z'] * 500) + 3000)
            value_out[3] = int(-1 * (1500 + value_joi['linear_x'] * 500) + (1500 + value_joi['rotate_y'] * 500) - (1500 + value_joi['linear_z'] * 500) + 3000) 
            value_out[4] = int(1500 + value_joi['linear_y'] * 500 + (1500 + value_joi['rotate_x'] * 500) - 1500)
            value_out[5] = int(1500 + value_joi['linear_y'] * 500 - (1500 + value_joi['rotate_x'] * 500) + 1500)

            # математика полезной нагрузки 
            # value_out[8] = # дописать обработку сервопривода 
            value_out[9] = int(1500 - value_joi['gripper'] * 500)
            value_out[10] = int(1000 + value_joi['led'] * 1000)
            
            return value_out
        
        # TODO дописать, взять за основу протеус 
        def math_eight_motors_off_PID(value_joi: dict, value_out: list):
            pass
        
        def check_reverse_motor(config_rov : dict, value : list):
            if config_rov["reverse_motor_0"]:
                value[0] = 3000 - value[0]
                
            if config_rov["reverse_motor_1"]:
                value[1] = 3000 - value[1]
                
            if config_rov["reverse_motor_2"]:
                value[2] = 3000 - value[2]

            if config_rov["reverse_motor_3"]:
                value[3] = 3000 - value[3]

            if config_rov["reverse_motor_4"]:
                value[4] = 3000 - value[4]

            if config_rov["reverse_motor_5"]:
                value[5] = 3000 - value[5]

            if config_rov["reverse_motor_6"]:
                value[6] = 3000 - value[6]

            if config_rov["reverse_motor_7"]:
                value[7] = 3000 - value[7]
            
            return value
                
        while True:
            # [M0, M1, M2, M3, M4, M5, M6, M7, CAM(8), GRIPPER(9), LED(10)]
            # математика моторов 2000 - вперед (для манипулятора закрыть) (для светильника включить); 1000 - назад (для манипулятора открыть) (для светильника выключить)   
            self.value_out_pwm = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1000]
            
            value_joi = self.joystick_ps4.value

            self.logi.debug(f'Data pult: {value_joi}')
            
            # обработка различных схем 
            if self.config_rov['motor_scheme'] == 3:
                self.value_out_pwm = math_three_motors_off_PID(value_joi, self.value_out_pwm)
                
            elif self.config_rov['motor_scheme'] == 4:
                self.value_out_pwm = math_four_motors_off_PID(value_joi, self.value_out_pwm)
                
            elif self.config_rov['motor_scheme'] == 6:
                self.value_out_pwm = math_six_motors_off_PID(value_joi, self.value_out_pwm)
                
            elif self.config_rov['motor_scheme'] == 8:
                self.value_out_pwm = math_eight_motors_off_PID(value_joi, self.value_out_pwm)
                        
            else:
                self.logi.critical('Error motor scheme support scheme 3, 4, 6, 8 motors')
            
            self.value_out_pwm = check_reverse_motor(self.config_rov, self.value_out_pwm)
            
            self.serial_port.send_data(self.value_out_pwm)

            sleep(self.sleep_time)

    def run_main(self):
        '''запуск псевдопотоков опроса джойстика и основного цикла программы'''
        self.thread_joystick = threading.Thread(target=self.run_joystick)
        self.thread_controller = threading.Thread(target=self.run_controller)

        self.thread_joystick.start()
        self.thread_controller.start()


if __name__ == '__main__':
    control_box = Control_Box()
    control_box.run_main()
