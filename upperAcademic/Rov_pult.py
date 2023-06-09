import threading
import configparser
from time import sleep
from distutils import util
from RovCommunication import Rov_SerialPort, Rov_SerialPort_Gebag
from RovControl import RovController
from RovLogging import RovLogger


# # запуск на одноплатном пк rock
# # путь до конфиг файла
# PATH_CONFIG = '/home/rock/SoftAcademic/raspberry-pult/config_pult.ini'

# # # путь до файлика с логами 
# PATH_LOG = '/home/rock/SoftAcademic/raspberry-pult/.log/'

# # запуск на компьютере в офисе 
# # путь до конфиг файла
PATH_CONFIG = 'C:/Users/Yarik/Documents/SoftAcademic/raspberry-pult/config_pult.ini'

# путь до файлика с логами 
PATH_LOG = 'C:/Users/Yarik/Documents/SoftAcademic/raspberry-pult/.log/'


class PULT_Main:
    def __init__(self):
        '''Основной класс поста управления'''
        self.data_input = []

        # считываем и задаем конфиги 
        self.config = configparser.ConfigParser()
        self.config.read(PATH_CONFIG)

        self.pult_conf = dict(self.config['RovPult'])

        # конфиг для логера 
        self.log_config = {'path_log':PATH_LOG,
                           'log_level': str(self.pult_conf['log_level'])}

        # создаем экземпляр класса отвечающий за логирование 
        self.logi = RovLogger(self.log_config)

        # конфиг для сериал порта 
        self.serial_config  = {'logger': self.logi,
                                'port': str(self.pult_conf['serial_port']),
                                'bitrate': int(self.pult_conf['bitrate']),
                                'timeout': float(self.pult_conf['timeout_serial']),
                                'debag' : util.strtobool(self.pult_conf['local_serial_debag'])}

        # создаем экземпляр класса отвечающий за связь с аппаратом по последовательному порту
        if util.strtobool(self.pult_conf['local_serial_debag']):
            self.serial_port = Rov_SerialPort_Gebag(self.serial_config)
        else:
            self.serial_port = Rov_SerialPort(self.serial_config)  

        # конфиг для джойстика 
        self.joi_config = dict(self.config['JOYSTICK'])
        self.joi_config['logger'] = self.logi
        
        # конфиг учитывающий особеннсти аппарата
        self.rov_conf = {'motor_scheme': int(self.config['Rov']['motor_scheme']),
                         'reverse_motor_0': util.strtobool(self.config['Rov']['reverse_motor_0']),
                         'reverse_motor_1': util.strtobool(self.config['Rov']['reverse_motor_1']),
                         'reverse_motor_2': util.strtobool(self.config['Rov']['reverse_motor_2']),
                         'reverse_motor_3': util.strtobool(self.config['Rov']['reverse_motor_3']),
                         'reverse_motor_4': util.strtobool(self.config['Rov']['reverse_motor_4']),
                         'reverse_motor_5': util.strtobool(self.config['Rov']['reverse_motor_5']),
                         'reverse_motor_6': util.strtobool(self.config['Rov']['reverse_motor_4']),
                         'reverse_motor_7': util.strtobool(self.config['Rov']['reverse_motor_5'])}
        
        # создаем экземпляр класса отвечающий за управление и взаимодействие с джойстиком 
        self.controll_ps4 = RovController(self.joi_config)  

        # подтягиваем данные с джойстика 
        self.data_pult = self.controll_ps4.data_pult

        # частота оптправки
        self.rate_command_out = float(self.pult_conf['rate_command_out'])

        # проверка подключения 
        self.check_connect = False

        self.correct = True

        self.logi.info('Main post init')

    def run_controller(self):
        # запуск прослушивания джойстика 
        self.controll_ps4.listen()

    def run_command(self):
        # запуск основного цикла
        self.logi.info('Pult run')
        
        '''
        Описание протокола передачи:
            С поста управлеия:
                    [motor0, motor1, motor2, motor3, motor4, motor5, motor6, motor7, ServoCam, Arm, GPIO-OUT1, GPIO-OUT2]
                по умолчанию:
                    [50, 50, 50, 50, 50, 50, 50, 50, 90, 90, 0, 0]
            C аппарата:
                    [напряжение(V), курс(градусы), глубина(м)]
                по умолчанию:
                    [0,0,0,0]
        '''
        def transformation(value: int):
            #Функция перевода значений АЦП с джойстика в проценты

            return (32768 - value) // 655

        def defense(value: int):
            #Функция защиты от некорректных данных§

            if value >= 100:
                value = 100

            elif value <= 0:
                value = 0
                
            return value

        def calculation_for_three_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            # Подготовка массива для отправки на аппарат
            # математика преобразования значений с джойстика в значения для моторов
            # j1_val_y - вперед\назад 
            # j1_val_x - разворот направо\налево
            # j2_val_y - всплытие\погружение
            # j2_val_x - не используются
            
            dataout = []
            
            if config['reverse_motor_0']:
                dataout.append(defense(50 + j1_val_y - j1_val_x))
            else:
                dataout.append(defense(50 - j1_val_y + j1_val_x))
                
            if config['reverse_motor_1']:
                dataout.append(defense(-50 + j1_val_y + j1_val_x))
            else:
                dataout.append(defense(150 - j1_val_y - j1_val_x))
            
            if config['reverse_motor_2']:
                dataout.append(defense(100 - (j2_val_y)))
            else:
                dataout.append(defense(j2_val_y))
                
            if config['reverse_motor_3']:
                dataout.append(50)
            else:
                dataout.append(50)

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
      
        def calculation_for_four_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            
            # Подготовка массива для отправки на аппарат
            # математика преобразования значений с джойстика в значения для моторов
            # j1_val_y - вперед\назад 
            # j1_val_x - разворот направо\налево
            # j2_val_y - всплытие\погружение
            # j2_val_x - не используются
                    
            dataout = []
            
            if config['reverse_motor_0']:
                dataout.append(defense(50 + j1_val_y - j1_val_x))
            else:
                dataout.append(defense(50 - j1_val_y + j1_val_x))
                
            if config['reverse_motor_1']:
                dataout.append(defense(-50 + j1_val_y + j1_val_x))
            else:
                dataout.append(defense(150 - j1_val_y - j1_val_x))
            
            if config['reverse_motor_2']:
                dataout.append(defense(100 - (j2_val_y)))
            else:
                dataout.append(defense(j2_val_y))
                
            if config['reverse_motor_3']:
                dataout.append(defense(100 - (j2_val_y)))
            else:
                dataout.append(defense(j2_val_y))

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
     
        def calculation_for_six_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            dataout = []
            
            if self.rov_conf['reverse_motor_0']:
                dataout.append(defense(100 - (j1_val_y + j1_val_x + j2_val_x - 100)))
            else:
                dataout.append(defense(j1_val_y + j1_val_x + j2_val_x - 100))
                
            if self.rov_conf['reverse_motor_1']:
                dataout.append(defense(100 - (j1_val_y - j1_val_x - j2_val_x + 100)))
            else:
                dataout.append(defense(j1_val_y - j1_val_x - j2_val_x + 100))
            
            if self.rov_conf['reverse_motor_2']:
                dataout.append(defense(100 - ((-1 * j1_val_y) - j1_val_x + j2_val_x + 100)))
            else:
                dataout.append(defense((-1 * j1_val_y) - j1_val_x + j2_val_x + 100))
                
            if self.rov_conf['reverse_motor_3']:
                dataout.append(defense(100 - ((-1 * j1_val_y) + j1_val_x - j2_val_x + 100)))
            else:
                dataout.append(defense((-1 * j1_val_y) + j1_val_x - j2_val_x + 100))

            if self.rov_conf['reverse_motor_4']:
                dataout.append(defense(100 - j2_val_y))
            else:
                dataout.append(defense(j2_val_y))
            
            if self.rov_conf['reverse_motor_5']:
                dataout.append(defense(100 - j2_val_y))
            else:
                dataout.append(defense(j2_val_y))

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
        
        def calculation_for_eight_motors(config,j1_val_y,j1_val_x,j2_val_y,j2_val_x):
            # TODO посчитать математику для векторной 8 движительной схемы 
            pass
        
        while True:
            dataout = []
            # запрос данный из класса пульта (потенциально слабое место)
            data = self.data_pult
            
            self.logi.debug(f'Data pult: {data}')

            j1_val_y = transformation(data['j1_val_y'])
            j1_val_x = transformation(data['j1_val_x'])
            j2_val_y = transformation(data['j2_val_y'])
            j2_val_x = transformation(data['j2_val_x'])
            
            if self.rov_conf['motor_scheme'] == 3:
                dataout = calculation_for_three_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                
            elif self.rov_conf['motor_scheme'] == 4:
                dataout = calculation_for_four_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
                
            elif self.rov_conf['motor_scheme'] == 6:
                dataout = calculation_for_six_motors(self.rov_conf, j1_val_y, j1_val_x, j2_val_y, j2_val_y)
            
            else:
                self.logi.critical('Error motor scheme support scheme 3, 4, 6 motors')
                
            if data['servo_cam'] >= float(self.joi_config['max_value_cam']):
                data['servo_cam'] = float(self.joi_config['max_value_cam'])
            if data['servo_cam'] <= float(self.joi_config['min_value_cam']):
                data['servo_cam'] = float(self.joi_config['min_value_cam'])
            
            # необходимо привести все к int 
            dataout.append(int(round(data['servo_cam'])))

            if data['man'] >= float(self.joi_config['max_value_man']):
                data['man'] = float(self.joi_config['max_value_man'])
            if data['man'] <= float(self.joi_config['min_value_man']):
                data['man'] = float(self.joi_config['min_value_man'])

            # необходимо привести все к int 
            dataout.append(int(round(data['man'])))
            
            # необходимо привести все к int 
            dataout.append(int(round(data['led'])))

            # отправка пакета на аппарат 
            self.serial_port.send_data_new(dataout)

            # # прием данных с дитчиков с аппарата 
            self.data_input = self.serial_port.receiver_data_new()
            
            self.logi.info(self.data_input)

            # if self.data_input == None:
            #     self.check_connect = False
            #     self.logi.warning('Receiver data: None')
            # else:
            #     self.check_connect = True
            
            # # TODO сделать вывод телеметрии на инжинерный экран 
            # print(self.data_input)

            # sleep(self.rate_command_out)

    def run_main(self):
        '''запуск процессов опроса джойстика и основного цикла программы'''
        self.ThreadJoi = threading.Thread(target=self.run_controller)
        self.ThreadCom = threading.Thread(target=self.run_command)

        self.ThreadJoi.start()
        self.ThreadCom.start()


if __name__ == '__main__':
    post = PULT_Main()
    post.run_main()
