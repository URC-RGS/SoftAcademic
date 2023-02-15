import os
import pygame
from time import sleep
from distutils import util

class RovController():
    def __init__(self, config):

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.pygame = pygame
        self.pygame.init()

        self.joi_config = config

        joysticks = []
        for i in range(self.pygame.joystick.get_count()):
            joysticks.append(self.pygame.joystick.Joystick(i))
        for self.joystick in joysticks:
            self.joystick.init()

        self.logi = config['logger']

        self.data_pult = {'j1_val_y': 0, 'j1_val_x': 0,
                         'j2_val_y': 0, 'j2_val_x': 0,
                         'man': 90, 'servo_cam': 90,
                         'led': 0}

        self.camera_up = int(self.joi_config[self.joi_config['camera_up']])

        self.camera_down = int(self.joi_config[self.joi_config['camera_down']])

        self.arm_up =  int(self.joi_config[self.joi_config['arm_up']])

        self.arm_down =  int(self.joi_config[self.joi_config['arm_down']])

        self.led_up = int(self.joi_config[self.joi_config['led_up']])

        self.led_down = int(self.joi_config[self.joi_config['led_down']])

        self.sleep_listen = float(self.joi_config['time_sleep_joi'])

        self.power_motor = float(self.joi_config['power_motor'])

        self.forward_back = float(self.joi_config['forward_back_defolt']) * self.power_motor * 32767

        self.cor_forward_back = float(self.joi_config['cor_forward_back_defolt'])

        self.min_value = float(self.joi_config['min_value'])

        self.move_forward_back = int(self.joi_config[self.joi_config['move_forward_back']])

        self.left_right = float(self.joi_config['left_right_defolt']) * self.power_motor * 32767

        self.cor_left_right = float(self.joi_config['cor_left_right_defolt'])

        self.move_left_right = int(self.joi_config[self.joi_config['move_left_right']])

        self.move_up_down = int(self.joi_config[self.joi_config['move_up_down']])

        self.up_down = float(self.joi_config['up_down_defolt']) * self.power_motor * 32767

        self.cor_up_down = float(self.joi_config['cor_up_down_defolt'])

        self.move_turn_left_turn_righ = int(self.joi_config[self.joi_config['move_turn_left_turn_righ']])

        self.turn_left_turn_righ = float(self.joi_config['turn_left_turn_righ_defolt']) * self.power_motor * 32767

        self.cor_turn_left_turn_righ = float(self.joi_config['cor_turn_left_turn_righ_defolt'])

        self.reverse_forward_back = bool(util.strtobool(self.joi_config['reverse_forward_back']))

        self.reverse_left_right = bool(util.strtobool(self.joi_config['reverse_left_right']))

        self.reverse_up_down = bool(util.strtobool(self.joi_config['reverse_up_down']))

        self.reverse_turn_left_turn_righ = bool(util.strtobool(self.joi_config['reverse_turn_left_turn_righ']))

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
                        self.data_pult['led'] = 160

                    if event.button == self.arm_down:
                        self.data_pult['led'] = 100

                    if event.button == self.led_up:
                        self.data_pult['man'] = 1

                    if event.button == self.led_down:
                        self.data_pult['man'] = 0

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == self.camera_up:
                        cor_servo_cam = 0

                    if event.button == self.camera_down:
                        cor_servo_cam = 0

                # опрос стиков
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == self.move_forward_back:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_forward_back:
                            self.data_pult['j1_val_y'] = int(round(event.value, 2) * self.forward_back * -1) - self.cor_forward_back
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_forward_back:
                            self.data_pult['j1_val_y'] = int(round(event.value, 2) * self.forward_back) - self.cor_forward_back

                        else:
                            self.data_pult['j1_val_y'] = 0

                    if event.axis == self.move_left_right:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_left_right:
                            self.data_pult['j1_val_x'] = int(round(event.value, 2) * self.left_right * -1) - self.cor_left_right

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_left_right:
                            self.data_pult['j1_val_x'] = int(round(event.value, 2) * self.left_right) - self.cor_left_right

                        else:
                            self.data_pult['j1_val_x'] = 0

                    if event.axis == self.move_up_down:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_up_down:
                            self.data_pult['j2_val_y'] = int(round(event.value, 2) * self.up_down * -1) - self.cor_up_down

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_up_down:
                            self.data_pult['j2_val_y'] = int(round(event.value, 2) * self.up_down) - self.cor_up_down

                        else:
                            self.data_pult['j2_val_y'] = 0

                    if event.axis == self.move_turn_left_turn_righ:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_turn_left_turn_righ:
                            self.data_pult['j2_val_x'] = int(round(event.value, 2) * self.turn_left_turn_righ * -1) - self.cor_turn_left_turn_righ

                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_turn_left_turn_righ:
                            self.data_pult['j2_val_x'] = int(round(event.value, 2) * self.turn_left_turn_righ) - self.cor_turn_left_turn_righ

                        else:
                            self.data_pult['j2_val_x'] = 0

                else:
                    self.data_pult['j1_val_y'], self.data_pult['j2_val_y'], self.data_pult['j1_val_x'], self.data_pult['j2_val_x'] = 0, 0, 0, 0

                # повторная инициализация джойстика после отключения
                joysticks = []
                for i in range(self.pygame.joystick.get_count()):
                    joysticks.append(self.pygame.joystick.Joystick(i))
                for self.joystick in joysticks:
                    self.joystick.init()
                    break

            # рассчет положения положения полезной нагрузки
            self.data_pult['servo_cam'] += cor_servo_cam
            
            # проверка на корректность значений 
            if self.data_pult['servo_cam'] >= 180:
                self.data_pult['servo_cam'] = 180

            elif self.data_pult['servo_cam'] <= 0:
                self.data_pult['servo_cam'] = 0

            sleep(self.sleep_listen)

    def stop_listen(self):
        self.running = False

