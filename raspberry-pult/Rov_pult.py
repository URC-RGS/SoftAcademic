import threading
import configparser
from time import sleep
from distutils import util
from RovCommunication import Rov_SerialPort, Rov_SerialPort_Gebag
from RovControl import RovController
from RovLogging import RovLogger
from datetime import datetime



# # запуск на одноплатном пк rock
# # путь до конфиг файла
PATH_CONFIG = '/home/rock/SoftAcademic/raspberry-pult/config_pult.ini'

# # путь до файлика с логами 
PATH_LOG = '/home/rock/SoftAcademic/raspberry-pult/log/'

# запуск на одноплатном пк pi4 
# путь до конфиг файла
#PATH_CONFIG = '/home/pi/SoftSkatt/raspberry-pult/config_pult.ini'

# путь до файлика с логами 
#PATH_LOG = '/home/pi/SoftSkatt/raspberry-pult/log/'

'''
# запуск на ноутбуке 
# путь до конфиг файла
PATH_CONFIG = '/Users/yarik/Documents/SoftAcademic/raspberry-pult/config_pult.ini'

# путь до файлика с логами 
PATH_LOG =  '/Users/yarik/Documents/SoftAcademic/raspberry-pult/log/'
'''

'''
# запуск на компьютере в офисе 
# путь до конфиг файла
PATH_CONFIG = 'C:/Users/Yarik/Documents/SoftAcademic/raspberry-pult/config_pult.ini'

# путь до файлика с логами 
PATH_LOG = 'C:/Users/Yarik/Documents/SoftAcademic/raspberry-pult/log/'
'''

class PULT_Main:
    def __init__(self):
        '''Основной класс поста управления'''
        self.data_input = []

        # считываем и задаем конфиги 
        self.config = configparser.ConfigParser()
        self.config.read(PATH_CONFIG)

        self.rov_conf = dict(self.config['RovPult'])

        # конфиг для логера 
        self.log_config = {'path_log':PATH_LOG,
                           'log_level': str(self.rov_conf['log_level'])}

        # создаем экземпляр класса отвечающий за логирование 
        self.logi = RovLogger(self.log_config)

        # конфиг для сериал порта 
        self.serial_config  = {'logger': self.logi,
                                'port': str(self.rov_conf['serial_port']),
                                'bitrate': int(self.rov_conf['bitrate']),
                                'timeout': float(self.rov_conf['timeout_serial']),
                                'debag' : util.strtobool(self.rov_conf['local_serial_debag'])}

        # создаем экземпляр класса отвечающий за связь с аппаратом по последовательному порту
        if util.strtobool(self.rov_conf['local_serial_debag']):
            self.serial_port = Rov_SerialPort_Gebag(self.serial_config)
        else:
            self.serial_port = Rov_SerialPort(self.serial_config)  

        # конфиг для джойстика 
        self.joi_config = dict(self.config['JOYSTICK'])
        self.joi_config['logger'] = self.logi
        
        # создаем экземпляр класса отвечающий за управление и взаимодействие с джойстиком 
        self.controll_ps4 = RovController(self.joi_config)  

        # подтягиваем данные с джойстика 
        self.data_pult = self.controll_ps4.data_pult

        # частота оптправки
        self.rate_command_out = float(self.rov_conf['rate_command_out'])

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
        Движение вперед - (1 вперед 2 вперед 3 назад 4 назад) 
        Движение назад - (1 назад 2 назад 3 вперед 4 вперед)
        Движение лагом вправо - (1 назад 2 вперед 3 вперед 4 назад)
        Движение лагом влево - (1 вперед 2 назад 3 назад 4 вперед)
        Движение вверх - (5 вниз 6 вниз)
        Движение вниз - (5 вверх 6 вверх)

        Описание протокола передачи:
            С поста управлеия:
                [motor0, motor1, motor2, motor3, motor4, motor5, ServoCam, Arm, led0, led1]
                по умолчанию:
                [50, 50, 50, 50, 50, 50, 90, 0, 0, 0]
            C аппарата:
                [напряжение(V), ток потребления(А), курс(градусы), глубина(м)]
                [0,0,0,0]
        '''
        def transformation(value: int):
            #Функция перевода значений АЦП с джойстика в проценты

            return (32768 - value) // 655

        def defense(value: int):
            #Функция защиты от некорректных данных§

            if value > 100:
                value = 100

            elif value < 0:
                value = 0
                
            return value

        while True:
            dataout = []
            # запрос данный из класса пульта (потенциально слабое место)
            data = self.data_pult
            
            self.logi.debug(f'Data pult: {data}')

            j1_val_y = transformation(data['j1_val_y'])
            j1_val_x = transformation(data['j1_val_x'])
            j2_val_y = transformation(data['j2_val_y'])
            j2_val_x = transformation(data['j2_val_x'])

            # Подготовка массива для отправки на аппарат
            # математика преобразования значений с джойстика в значения для моторов
            dataout.append(defense(j1_val_y + j1_val_x + j2_val_x - 100))
            dataout.append(defense(j1_val_y - j1_val_x - j2_val_x + 100))
            # костыльное переопределнение двигателей надо сделать с выбором пресетов TODO
            dataout.append(defense(j2_val_y))
            dataout.append(defense(j2_val_y))
            
            dataout.append(defense((-1 * j1_val_y) - j1_val_x + j2_val_x + 100))
            dataout.append(defense((-1 * j1_val_y) + j1_val_x - j2_val_x + 100))

            

            if data['servo_cam'] >= float(self.joi_config['max_value_cam']):
                data['servo_cam'] = float(self.joi_config['max_value_cam'])
            if data['servo_cam'] <= float(self.joi_config['min_value_cam']):
                data['servo_cam'] = float(self.joi_config['min_value_cam'])

            dataout.append(data['servo_cam'])

            if data['man'] >= float(self.joi_config['max_value_man']):
                data['man'] = float(self.joi_config['max_value_man'])
            if data['man'] <= float(self.joi_config['min_value_man']):
                data['man'] = float(self.joi_config['min_value_man'])

            dataout.append(data['led'])

            dataout.append(data['man'])
            
            

            #dataout.append(str(datetime.now()))

            # отправка пакета на аппарат 
            self.serial_port.send_data(dataout)

            # прием данных с дитчиков с аппарата 
            self.data_input = self.serial_port.receiver_data()

            if self.data_input == None:
                self.check_connect = False
                self.logi.warning('Receiver data: None')
            else:
                self.check_connect = True
            
            # TODO сделать вывод телеметрии на инжинерный экран 
            print(self.data_input)

            # if util.strtobool(self.rov_conf['local_serial_debag']):
            #     delay = datetime.now() - datetime.strptime(self.data_input[-1], '%Y-%m-%d %H:%M:%S.%f')
            #     print(delay.total_seconds())
            # else:
            #     delay = datetime.now() - datetime.strptime(self.data_input[-1][3:-5], '%Y-%m-%d %H:%M:%S.%f')
            #     print(delay.total_seconds())



            sleep(self.rate_command_out)

    def run_main(self):
        '''запуск процессов опроса джойстика и основного цикла программы'''
        self.ThreadJoi = threading.Thread(target=self.run_controller)
        self.ThreadCom = threading.Thread(target=self.run_command)

        self.ThreadJoi.start()
        self.ThreadCom.start()


if __name__ == '__main__':
    post = PULT_Main()
    post.run_main()
    
