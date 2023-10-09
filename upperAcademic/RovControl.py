import os
import pygame
from time import sleep

class RovController():
    def __init__(self, config):

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.pygame = pygame
        self.pygame.init()

        self.config_joi = config

        # подключение джойтика 
        joysticks = []
        for i in range(self.pygame.joystick.get_count()):
            joysticks.append(self.pygame.joystick.Joystick(i))
        for self.joystick in joysticks:
            self.joystick.init()

        # ссылаемся на основной обьект логера 
        self.logi = config['logger']

        # текущие значение с пульта управления 
        self.value_pult = {
                          'value_j1_y': 0,
                          'value_j1_x': 0,
                          
                          'value_j2_y': 0,
                          'value_j2_x': 0,
                          
                          'man': 0,
                          'led': 0,
                          'servo_cam': 90
                          }
        
        # назначение кнопок камеры
        self.camera_up = self.config_joi[self.config_joi['camera_up']]
        self.camera_down = self.config_joi[self.config_joi['camera_down']]

        # назначение кнопок манипулятора
        self.arm_up =  self.config_joi[self.config_joi['arm_up']]
        self.arm_down =  self.config_joi[self.config_joi['arm_down']]

        # назначение кнопок светильника
        self.led_up = self.config_joi[self.config_joi['led_up']]
        self.led_down = self.config_joi[self.config_joi['led_down']]
        
        # задержка между опросами джойстика 
        self.sleep_listen = self.config_joi['time_sleep_joi']
        
        # минимальное значение управляющего воздействия стика
        self.min_value = self.config_joi['min_value']

        # назначение стиков 
        self.stick_linear_x = self.config_joi['']
        self.stick_linear_y = self.config_joi['']
        self.stick_linear_z = self.config_joi['']
        
        self.stick_rotate_x = self.config_joi['']
        self.stick_rotate_y = self.config_joi['']
        self.stick_rotate_z = self.config_joi['']
        
        # коэфиценты 
        self.power_linear_x = self.config_joi['']
        self.power_linear_y = self.config_joi['']
        self.power_linear_z = self.config_joi['']
        
        self.power_rotate_x = self.config_joi['']
        self.power_rotate_y = self.config_joi['']
        self.power_rotate_z = self.config_joi['']

        # реверс управления 
        self.reverse_linear_x = self.config_joi['']
        self.reverse_linear_y = self.config_joi['']
        self.reverse_linear_z = self.config_joi['']
        
        self.reverse_rotate_x = self.config_joi['']
        self.reverse_rotate_y = self.config_joi['']
        self.reverse_rotate_z = self.config_joi['']

        self.running = True

        self.logi.info('Controller PS4 init')

    def listen(self):
        self.logi.info('Controller PS4 listen')

        # сдвиг камеры 
        cor_servo_cam = 0

        while self.running:
            for event in self.pygame.event.get():
                # опрос нажания кнопок
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.camera_up:
                        cor_servo_cam = -1

                    if event.button == self.camera_down:
                        cor_servo_cam = 1

                    if event.button == self.arm_up:
                        self.value_pult['man'] = 180

                    if event.button == self.arm_down:
                        self.value_pult['man'] = 0

                    if event.button == self.led_up:
                        self.value_pult['led'] = 180

                    if event.button == self.led_down:
                        self.value_pult['led'] = 0

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.camera_up:
                        cor_servo_cam = 0

                    if event.button == self.camera_down:
                        cor_servo_cam = 0

                # опрос стиков
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == self.move_forward_back:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_forward_back:
                            self.value_pult['j1_val_y'] = int(round(event.value, 2) * self.forward_back * -1) - self.cor_forward_back
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_forward_back:
                            self.value_pult['j1_val_y'] = int(round(event.value, 2) * self.forward_back) - self.cor_forward_back

                        else:
                            self.value_pult['j1_val_y'] = 0

                    if event.axis == self.move_left_right:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_left_right:
                            self.value_pult['j1_val_x'] = int(round(event.value, 2) * self.left_right * -1) - self.cor_left_right

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_left_right:
                            self.value_pult['j1_val_x'] = int(round(event.value, 2) * self.left_right) - self.cor_left_right

                        else:
                            self.value_pult['j1_val_x'] = 0

                    if event.axis == self.move_up_down:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_up_down:
                            self.value_pult['j2_val_y'] = int(round(event.value, 2) * self.up_down * -1) - self.cor_up_down

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_up_down:
                            self.value_pult['j2_val_y'] = int(round(event.value, 2) * self.up_down) - self.cor_up_down

                        else:
                            self.value_pult['j2_val_y'] = 0

                    if event.axis == self.move_turn_left_turn_righ:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_turn_left_turn_righ:
                            self.value_pult['j2_val_x'] = int(round(event.value, 2) * self.turn_left_turn_righ * -1) - self.cor_turn_left_turn_righ

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_turn_left_turn_righ:
                            self.value_pult['j2_val_x'] = int(round(event.value, 2) * self.turn_left_turn_righ) - self.cor_turn_left_turn_righ

                        else:
                            self.value_pult['j2_val_x'] = 0

                else:
                    self.value_pult['j1_val_y'], self.value_pult['j2_val_y'], self.value_pult['j1_val_x'], self.value_pult['j2_val_x'] = 0, 0, 0, 0

                # повторная инициализация джойстика после отключения
                joysticks = []
                for i in range(self.pygame.joystick.get_count()):
                    joysticks.append(self.pygame.joystick.Joystick(i))
                for self.joystick in joysticks:
                    self.joystick.init()
                    break

            # рассчет положения положения полезной нагрузки
            self.value_pult['servo_cam'] += cor_servo_cam
            
            # проверка на корректность значений 
            if self.value_pult['servo_cam'] >= 180:
                self.value_pult['servo_cam'] = 180

            elif self.value_pult['servo_cam'] <= 0:
                self.value_pult['servo_cam'] = 0

            sleep(self.sleep_listen)

    def stop_listen(self):
        self.running = False

