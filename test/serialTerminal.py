import sys
import glob
import os
from time import sleep
from serial import Serial, SerialException
from serial.serialutil import PortNotOpenError
from datetime import datetime
from threading import Thread
import logging
from verboselogs import VerboseLogger, SPAM
from logging import Logger
from typing import List, NoReturn, Optional
import coloredlogs




RECIVESLEEP = 0.001


class SerialLogger:
    '''Класс отвечающий за логирование. Логи пишуться в файл, так же выводться в консоль'''
    def __init__(self, deviceName="Serial",  path: str = "") -> NoReturn:
        self.mylogs = VerboseLogger(__name__)
        self.mylogs.setLevel(SPAM)
        self.deviceName = deviceName
        self.path = path
        
        self.history = []
        
        # обработчик вывода в консоль лог файла
        self.stream = logging.StreamHandler()
        self.streamformat = logging.Formatter(
            "%(asctime)s [%(levelname)s]\t%(message)s")

        self.stream.setLevel(logging.SPAM)
        self.stream.setFormatter(self.streamformat)

        # инициализация обработчиков
        self.mylogs.addHandler(self.stream)

        coloredlogs.install(level=SPAM, logger=self.mylogs,
                            fmt='%(asctime)s [%(levelname)s]\t%(message)s')

    def initFileLogger(self):        
        if self.path != "":
            if not os.path.exists(self.path):
                os.mkdir(self.path)

        # обработчик записи в лог-файл
        name = datetime.now().strftime(f"{self.deviceName}_%d-%m-%Y_%H-%M-%S") + ".log"
        name = os.path.join(self.path, name)
        
        self.file = logging.FileHandler(name)
        self.fileformat = logging.Formatter(
            "%(asctime)s [%(levelname)s]\t%(message)s")
        
        self.file.setLevel(logging.SPAM)
        self.file.setFormatter(self.fileformat)
        
        self.mylogs.addHandler(self.file)

    def debug(self, message) -> NoReturn:
        '''Debugging Information'''
        self.mylogs.debug(message)


    def info(self, message) -> NoReturn:
        '''сообщения информационного уровня'''
        self.mylogs.info(message)


    def warning(self, message) -> NoReturn:
        '''Something went wrong'''
        self.mylogs.warning(message)
        
        
    def error(self, message) -> NoReturn:
        '''Something broke'''
        self.mylogs.error(message)
        
        
    def recived(self, message) -> NoReturn:
        '''Data recived from device'''
        self.mylogs.notice(message)
        print("\n> ", end="")

    
    def sended(self, message) -> NoReturn:
        '''Data sended to device'''
        self.mylogs.verbose(message)
        print("\n> ", end="")
        
    
    def critical(self, message) -> NoReturn:
        '''We all will die'''
        self.mylogs.critical(message)


class SerialTerminal:
    def __init__(self, port: str = "Not selected", baudrate : int = 115200, deviceName : str = "Serial", timeout: int = 1, logger: Logger = SerialLogger, logPath: str = "") -> NoReturn:
        self.logger = logger(deviceName, logPath)
        self.baudrate = baudrate
        self.timeout = timeout
        self.port = port
        self.status = "disconnected"
        
        self.reciveThread = None
        self.device = None
        self.deviceName = None
    
    
    def setPort(self, port: str) -> bool:
        try:
            s = Serial(port)
            self.port = port
                
            s.close()
            
            self.logger.info(f"{port} - selected")
            
            return True
            
        except Exception as e:
            print(e)
            self.logger.error(f"{port} - not avalible")
            
            return False
    
    
    def setBaudrate(self, baudrate: int) -> bool:
        self.bitrate = baudrate
        
        return True
    

    def setTimeout(self, timeout: int) -> bool:
        self.timeout = timeout
        
        return True        
    
            
    def findSerials(self) -> List[str]:
        if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
            
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
            
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
            
        else:
            self.logger.critical("Unsupported platform. Exit")
            exit()
            
        result = []
            
        for port in ports:
            try:
                s = Serial(port)
                s.close()
                result.append(port)
                
            except (OSError, SerialException):
                pass
            
        if not len(result):
            self.logger.info("Serial devices not found. Exit")
            return []
        
        return result
    
    
    def connect(self) -> bool:
        self.logger.initFileLogger()
        try:
            self.device = Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout)
                      
            self.status = "connected"
            self.deviceName = self.device.name
            
            self.logger.info(f"Device {self.deviceName} successful connected")
            self.logger.info(f"\t| Port: {self.port}")
            self.logger.info(f"\t| Baundrate: {self.baudrate}")
            self.logger.info(f"\t| Timeout: {self.timeout}")
            
            return True
                      
        except:            
            self.status = "disconnected"
            
            self.logger.error(f"Device {self.deviceName} failed to connect")
            self.logger.error(f"\t| Port: {self.port}")
            self.logger.error(f"\t| Baundrate: {self.baudrate}")
            self.logger.error(f"\t| Timeout: {self.timeout}")
            
            return False
            
    
    def disconnect(self) -> bool:
        if self.status == "disconnected":
            return False
        
        if self.device == None:
            self.status = "disconnected"
            self.logger.error("Port did not open")
            return False
        
        self.status = "disconnected"
        self.device.close()
        
        self.logger.info(f"Device {self.deviceName} disconnected")
        
        self.deviceName = None
        self.isLoopRunned = False
        return True
        
        
    def send(self, message: str) -> bool:
        if self.status == "disconnected":
            return False
        
        if self.device == None:
            self.status = "disconnected"
            self.logger.error("Port did not open")
            return False
        
        try:            
            self.device.write((message + "\n").encode("UTF-8"))
            self.logger.sended(message)
            return True
            
            
        except PortNotOpenError:
            self.logger.error(f"{self.port} has been closed")
            self.status = "disconnected"
            
            return False
    
    
    def recive(self) -> Optional[str]:
        
        if self.status == "disconnected":
            return False
        
        if self.device == None:
            self.status = "disconnected"
            self.logger.error("Port did not open")
            return False
            
        try:
            data = b''
            while data == b'':
                data = self.device.readline()

                try:
                    dataout = data.decode("UTF-8").strip()
                    if dataout not in ("", "\n"):
                        self.logger.recived(dataout)
                    
                    return dataout

                except:
                    self.logger.warning('Error converting recived data')
            
                    return None
                
        except PortNotOpenError:
            self.logger.error(f"{self.port} has been closed")
            self.status = "disconnected"
            
            return None
        
    
    def reciveLoop(self) -> NoReturn:
        attempts = 1
        while attempts < 4:
            while self.status == "connected":
                self.recive()
                sleep(RECIVESLEEP)
                
            self.logger.warning(f"{self.port} - try {attempts} connect")
            sleep(5)
            
            if self.connect():
                attempts = 1
                
            else:
                attempts += 1  
        
        if isinstance(self.reciveThread, Thread):
            self.logger.info("Recive daemon has been stoped")
            
                
            
    def reciveDaemon(self) -> Thread:
        daemon = Thread(target=self.reciveLoop)
        daemon.setDaemon(True)
        daemon.start()
        
        self.reciveThread = daemon
        
        return daemon
        
        
    def __del__(self) -> NoReturn:
        try:
            self.device.close()
            self.isLoopRunned = False
            self.logger.info(f"{self.port} - port closed")
            
        except:
            pass


if __name__ == "__main__":
        
    term = SerialTerminal(deviceName="planum-serial", logPath="logs")
    print("Start find devices:\n")
    ports = term.findSerials()
    
    if not len(ports):
        exit()
        
    for i in range(len(ports)):
        print(f"{i}\t-\t{ports[i]}")
        
    print(f"{len(ports)}\t-\texit()")
        
    port = -1
        
    while port == -1:
        try:
            port = int(input("Select serial port: "))
            if port == len(ports):
                exit()
                
            if not (port > -1 and port < len(ports)):
                port = -1
                
        except KeyboardInterrupt:
            print("Exit")
            exit()
        
        except SystemExit:
            print("Exit")
            exit()  
            
        except:
            pass
    
    if term.setPort(ports[port]):
    
        if term.connect():
            term.reciveDaemon()
            mes = ""
            while mes != "$exit()":
                if mes != "":
                    term.send(mes)
                
                mes = input("\n> ")
                #print("\r" + len(mes) * " " + "\r")
            
            term.disconnect()
    
    