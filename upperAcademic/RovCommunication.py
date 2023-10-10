from random import randint
import serial


class Rov_SerialPort:
    def __init__(self, config_serial : dict):
        '''`Класс для работы с последовательным портом'''

        self.check_connect = False
        self.logi = config_serial['logger']

        # открытие порта
        self.serial_port = serial.Serial(
                                        port=config_serial['port'],
                                        baudrate=config_serial['bitrate'],
                                        timeout=config_serial['timeout']
                                        )
                                        
        self.check_cor = False

        self.logi.info(f'Serial port init: {config_serial}')

    def receiver_data(self):
        #прием информации с аппарата
        data = None

        while data == None or data == b'':
            data = self.serial_port.readline()

        try:
            self.logi.debug(f'Receiver data: {str(data)}')
            
            # print(str(data))
            
            # mass_data = str(data)[2:-3].split(', ')
            
            # dataout = list(map(lambda x: float(x), mass_data[:-1]))

        except:
            self.logi.warning('Error converting data')
            return None

        return data

    def send_data(self, data : list):
        #отправка массива на аппарат
        try:
            data = (f'{str(data)[1:-1]}\n').replace(', ', ' ').encode()
            
            self.serial_port.write(data)

            self.logi.debug(f'Send data: {data}')

        except:
            self.logi.warning('Error send data')


class Rov_SerialPort_Gebag:
    def __init__(self, config_serial : dict):
        '''`Класс для работы с последовательным портом'''
        self.check_connect = False
        self.logi = config_serial['logger']

        # открытие порта
        self.logi.info(f'''PORT: {config_serial['port']}    BITRATE: {config_serial['bitrate']}    TIMEOUT_SERIAL: {config_serial['timeout']}''')

        self.check_cor = False

        self.logi.info(f'Serial port init: {config_serial}')

    def receiver_data(self):
        #прием информации с аппарата
        
        data = [12.6,randint(0,2), randint(25,27), randint(0,5), randint(180,210)]

        self.logi.debug(f'Receiver data : {str(data)}')
            
        return data

    def send_data(self, data: list):
        #отправка массива на аппарат
        
        self.logi.debug(f'Send data: {str(data)}')


