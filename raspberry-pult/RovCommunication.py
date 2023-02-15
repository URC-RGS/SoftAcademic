import socket
from ast import literal_eval  
from RovLogging import RovLogger
from datetime import datetime
from random import randint
import serial


class RovServer:
    def __init__(self, server_config: dict):
        '''Класс отвечающий за создание сервера'''

        self.logi = server_config['logger']
        
        # выбор режима: Отладка\Запуск на реальном аппарате
        if server_config['local_host_start']:
            self.host = server_config['local_host']
            self.port = server_config['port_local_host']
        else:
            self.host = server_config['real_host']
            self.port = server_config['port_real_host']
            
            
        # настройка сервера
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
        self.server.bind((self.host, self.port))
        self.logi.info('ROV waiting for connection')
        self.server.listen(1)
        self.user_socket, self.address = self.server.accept()
        self.check_connect = True

        self.logi.info(f'ROV Connected {self.user_socket}')

    def receiver_data(self):
        #Прием информации с аппарата
        if self.check_connect:
            data = self.user_socket.recv(512)
            if len(data) == 0:
                self.server.close()
                self.check_connect = False
                self.logi.info(f'ROV disconnection {self.user_socket}')
                return None

            data = dict(literal_eval(str(data.decode('utf-8'))))
            self.logi.debug(f'Receiver data : {str(data)}')
            return data

    def send_data(self, data: dict):
        #Отправка массива на аппарат
        if self.check_connect:
            self.user_socket.send(str(data).encode('utf-8'))
            self.logi.debug(f'Send data : {str(data)}')


class RovClient:
    def __init__(self, server_config: dict):
        '''Класс ответсвенный за связь с постом'''
        self.logi = server_config['logger']
        
        if server_config['local_host_start']:
            self.host = server_config['local_host']
            self.port = server_config['port_local_host']

        else:
            self.host = server_config['real_host']
            self.port = server_config['port_real_host']

        self.check_connect = True      

        # Настройки клиента 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
        self.client.connect((self.host, self.port))

    def receiver_data(self):
        #Прием информации с поста управления 
        if self.check_connect:
            data = self.client.recv(512).decode('utf-8')

            if len(data) == 0:
                self.check_connect = False
                self.logi.info('Rov disconect')
                self.client.close()
                return None

            data = dict(literal_eval(str(data)))
            self.logi.debug(f'Receiver data : {str(data)}')
            return data

    def send_data(self, data:dict):
        #Функция для  отправки пакетов на пульт 
        if self.check_connect:
            data['time'] = str(datetime.now())

            self.logi.debug(f'Send data : {str(data)}')

            data_output = str(data).encode("utf-8")
            self.client.send(data_output)


class Rov_SerialPort:
    def __init__(self, serial_config:dict):
        '''`Класс для работы с последовательным портом'''

        self.check_connect = False
        self.logi = serial_config['logger']

        # открытие порта
        self.serial_port = serial.Serial(
                                        port=serial_config['port'],
                                        baudrate=serial_config['bitrate'],
                                        timeout=serial_config['timeout']
                                        )
                                        
        self.check_cor = False

        self.logi.info(f'Serial port init: {serial_config}')

    def receiver_data(self):
        #прием информации с аппарата
        data = None

        while data == None or data == b'':
            data = self.serial_port.readline()

        try:
            self.logi.debug(f'Receiver data: {str(data)}')
            
            mass_data = str(data)[3:-4].split(', ')
            
            dataout = list(map(lambda x: float(x), mass_data[:-1]))

        except:
            self.logi.warning('Error converting data')
            return None

        return dataout

    def send_data(self, data: list = [50, 50, 50, 50, 50, 50, 90, 0, 0, 0]):
        #отправка массива на аппарат
        try:
            data = (f'{str(data)}\n').encode()
            
            self.serial_port.write(data)

            self.logi.debug(f'Send data: {data}')

        except:
            self.logi.warning('Error send data')


class Rov_SerialPort_Gebag:
    def __init__(self, serial_config:dict):
        '''`Класс для работы с последовательным портом'''
        self.check_connect = False
        self.logi = serial_config['logger']

        # открытие порта
        self.logi.info(f'''PORT: {serial_config['port']}    BITRATE: {serial_config['bitrate']}    TIMEOUT_SERIAL: {serial_config['timeout']}''')

        self.check_cor = False

        self.logi.info(f'Serial port init: {serial_config}')

    def receiver_data(self):
        #прием информации с аппарата
        
        data = [12.6,randint(0,2), randint(25,27), randint(0,5), randint(180,210), str(datetime.now())]

        self.logi.debug(f'Receiver data : {str(data)}')
            
        return data

    def send_data(self, data: list = [50, 50, 50, 50, 50, 50, 90, 0, 0, 0]):
        #отправка массива на аппарат

        self.logi.debug(f'Send data: {str(data)}')


