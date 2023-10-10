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

        # создаем экземпляр класса отвечающий за логирование 
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
            
        elif platform == "win32":
            self.config_joystick = self.config['JOYSTICK_WIN']
            self.config_joystick['logger'] = self.logi
        
        # создаем экземпляр класса отвечающий за управление и взаимодействие с джойстиком 
        self.joystick_ps4 = RovJoystick(self.config_joystick)
        
        # подтягиваем настройки для робота 
        self.config_rov = self.config['ROV']

        # подтягиваем начальные данные с джойстика 
        self.value_joystick = self.joystick_ps4.value_joystick

        # частота оптправки
        self.sleep_time = self.config_control_box['sleep_time']

        # флаг проверки подключения 
        self.check_connect = False

        self.logi.info('Control box init')

    def run_joystick(self):
        # запуск прослушивания джойстика 
        self.joystick_ps4.listen()

    def run_controller(self):
        # запуск основного цикла
        self.logi.info('co run')
        
        def math_three_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            # Подготовка массива для отправки на аппарат
            # математика преобразования значений с джойстика в значения для моторов
            
            dataout = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
            
            if config['reverse_motor_0']:
                dataout.append(50 + j1_val_y - j1_val_x)
            else:
                dataout.append(50 - j1_val_y + j1_val_x)
                
            if config['reverse_motor_1']:
                dataout.append(-50 + j1_val_y + j1_val_x)
            else:
                dataout.append(150 - j1_val_y - j1_val_x)
            
            if config['reverse_motor_2']:
                dataout.append(100 - (j2_val_y))
            else:
                dataout.append(j2_val_y)
                
            return dataout
      
        def math_four_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            
            # Подготовка массива для отправки на аппарат
            # математика преобразования значений с джойстика в значения для моторов
            # j1_val_y - вперед\назад 
            # j1_val_x - разворот направо\налево
            # j2_val_y - всплытие\погружение
            # j2_val_x - не используются
                    
            dataout = []
            
            if config['reverse_motor_0']:
                dataout.append(50 + j1_val_y - j1_val_x)
            else:
                dataout.append(50 - j1_val_y + j1_val_x)
                
            if config['reverse_motor_1']:
                dataout.append(-50 + j1_val_y + j1_val_x)
            else:
                dataout.append(150 - j1_val_y - j1_val_x)
            
            if config['reverse_motor_2']:
                dataout.append(100 - (j2_val_y))
            else:
                dataout.append(j2_val_y)
                
            if config['reverse_motor_3']:
                dataout.append(100 - (j2_val_y))
            else:
                dataout.append(j2_val_y)

            if config['reverse_motor_4']:
                dataout.append(50)
            else:
                dataout.append(50)
            
            if config['reverse_motor_5']:
                dataout.append(50)
            else:
                dataout.append(50)
                
            if config['reverse_motor_6']:
                dataout.append(50)
            else:
                dataout.append(50)
            
            if config['reverse_motor_7']:
                dataout.append(50)
            else:
                dataout.append(50)
                
            for i in range(len(dataout)):
                dataout[i] = int(round(dataout[i]))
                
            return dataout
     
        def math_six_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            dataout = []
            
            if self.rov_conf['reverse_motor_0']:
                dataout.append(100 - (j1_val_y + j1_val_x + j2_val_x - 100))
            else:
                dataout.append(j1_val_y + j1_val_x + j2_val_x - 100)
                
            if self.rov_conf['reverse_motor_1']:
                dataout.append(100 - (j1_val_y - j1_val_x - j2_val_x + 100))
            else:
                dataout.append(j1_val_y - j1_val_x - j2_val_x + 100)
            
            if self.rov_conf['reverse_motor_2']:
                dataout.append(100 - ((-1 * j1_val_y) - j1_val_x + j2_val_x + 100))
            else:
                dataout.append((-1 * j1_val_y) - j1_val_x + j2_val_x + 100)
                
            if self.rov_conf['reverse_motor_3']:
                dataout.append(100 - ((-1 * j1_val_y) + j1_val_x - j2_val_x + 100))
            else:
                dataout.append((-1 * j1_val_y) + j1_val_x - j2_val_x + 100)

            if self.rov_conf['reverse_motor_4']:
                dataout.append(100 - j2_val_y)
            else:
                dataout.append(j2_val_y)
            
            if self.rov_conf['reverse_motor_5']:
                dataout.append(100 - j2_val_y)
            else:
                dataout.append(j2_val_y)

            if config['reverse_motor_6']:
                dataout.append(50)
            else:
                dataout.append(50)
            
            if config['reverse_motor_7']:
                dataout.append(50)
            else:
                dataout.append(50)
                
            for i in range(len(dataout)):
                dataout[i] = int(round(dataout[i]))

            return dataout
        
        def math_eight_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            # TODO посчитать математику для векторной 8 движительной схемы 
            pass
        
        while True:
            dataout = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 90, 0, 0]
            
            value = self.joystick_ps4.value_joystick
            
            self.logi.debug(f'Data pult: {value}')
            
            if self.rov_conf['motor_scheme'] == 3:
                dataout = math_three_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                
            elif self.rov_conf['motor_scheme'] == 4:
                dataout = math_four_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                
            elif self.rov_conf['motor_scheme'] == 6:
                dataout = math_six_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                
            elif self.rov_conf['motor_scheme'] == 6:
                dataout = math_eight_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                        
            else:
                self.logi.critical('Error motor scheme support scheme 3, 4, 6 motors')
                
            if value['servo_cam'] >= float(self.joi_config['max_value_cam']):
                value['servo_cam'] = float(self.joi_config['max_value_cam'])
            if value['servo_cam'] <= float(self.joi_config['min_value_cam']):
                value['servo_cam'] = float(self.joi_config['min_value_cam'])
            
            # необходимо привести все к int 
            dataout.append(int(round(value['servo_cam'])))

            # необходимо привести все к int 
            dataout.append(int(round(value['man'])))
            
            # необходимо привести все к int 
            dataout.append(int(round(value['led'])))

            # отправка пакета на аппарат 
            self.serial_port.send_data(dataout)

            sleep(self.rate_command_out)

    def run_main(self):
        '''запуск псевдопотоков опроса джойстика и основного цикла программы'''
        self.thread_joystick = threading.Thread(target=self.run_joystick)
        self.thread_controller = threading.Thread(target=self.run_controller)

        self.thread_joystick.start()
        self.thread_controller.start()


if __name__ == '__main__':
    control_box = Control_Box()
    control_box.run_main()
