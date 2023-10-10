import os
import pygame
from time import sleep

class RovJoystick():
    def __init__(self, config):

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.pygame = pygame
        self.pygame.init()

        self.config_joystick = config

        # подключение джойтика 
        joysticks = []
        for i in range(self.pygame.joystick.get_count()):
            joysticks.append(self.pygame.joystick.Joystick(i))
        for self.joystick in joysticks:
            self.joystick.init()

        # ссылаемся на основной обьект логера 
        self.logi = config['logger']

        # текущие значение с пульта управления 
        self.value = {  
                      'linear_axis_x': 0,
                      'linear_axis_y': 0,
                      'linear_axis_z': 0,
                          
                      'rotate_axis_x': 0,
                      'rotate_axis_y': 0,
                      'rotate_axis_z': 0,           
                                   
                      'gripper': 0,
                      'led': 0,
                      'servo_cam': 0,
                      
                      'stabilization_depth' : 0,
                      'stabilization_course' : 0
                    }
        
        # назначение кнопок камеры
        self.index_camera_up = self.config_joystick[self.config_joystick['camera_up']]
        self.index_camera_down = self.config_joystick[self.config_joystick['camera_down']]

        # назначение кнопок манипулятора
        self.index_gripper_up =  self.config_joystick[self.config_joystick['arm_up']]
        self.index_gripper_down =  self.config_joystick[self.config_joystick['arm_down']]

        # назначение кнопок светильника
        self.index_led_check = self.config_joystick[self.config_joystick['led_check']]
        
        # задержка между опросами джойстика 
        self.sleep_time = self.config_joystick['sleep_time']
        
        # минимальное значение управляющего воздействия стика
        self.min_value = self.config_joystick['min_value']

        # назначение индексов стиков 
        self.index_stick_jl_x = self.config_joystick["stick_jl_x"]
        self.index_stick_jl_y = self.config_joystick["stick_jl_y"]
        self.index_stick_jr_x = self.config_joystick["stick_jr_x"]
        self.index_stick_jr_y = self.config_joystick["stick_jr_y"]
        self.index_stick_L = self.config_joystick["stick_L"]
        self.index_stick_R = self.config_joystick["stick_R"]

        self.index_options_stick_jl_x = self.config_joystick[self.config_joystick["options_stick_jl_x"]]
        self.index_options_stick_jl_y = self.config_joystick[self.config_joystick["options_stick_jl_y"]]
        self.index_options_stick_jr_x = self.config_joystick[self.config_joystick["options_stick_jr_x"]]
        self.index_options_stick_jr_y = self.config_joystick[self.config_joystick["options_stick_jr_y"]]
        self.index_options_stick_L = self.config_joystick[self.config_joystick["options_stick_L"]]
        self.index_options_stick_R = self.config_joystick[self.config_joystick["options_stick_R"]]
        
        self.check_options_stick_jl_x = False
        self.check_options_stick_jl_y = False
        self.check_options_stick_jr_x = False
        self.check_options_stick_jr_y = False
        self.check_options_stick_L = False
        self.check_options_stick_R = False
        
        # коэфиценты 
        self.power_linear_x = self.config_joystick['power_linear_x']
        self.power_linear_y = self.config_joystick['power_linear_y']
        self.power_linear_z = self.config_joystick['power_linear_z']
        
        self.power_rotate_x = self.config_joystick['power_rotate_x']
        self.power_rotate_y = self.config_joystick['power_rotate_y']
        self.power_rotate_z = self.config_joystick['power_rotate_z']

        # реверс управления 
        self.reverse_linear_x = self.config_joystick['reverse_linear_x']
        self.reverse_linear_y = self.config_joystick['reverse_linear_y']
        self.reverse_linear_z = self.config_joystick['reverse_linear_z']
        
        self.reverse_rotate_x = self.config_joystick['reverse_rotate_x']
        self.reverse_rotate_y = self.config_joystick['reverse_rotate_y']
        self.reverse_rotate_z = self.config_joystick['reverse_rotate_z']

        self.running = True

        self.logi.info('Controller PS4 init')

    def listen(self):
        self.logi.info('Controller PS4 listen')
        
        while self.running:
            for event in self.pygame.event.get():
                # опрос нажания кнопок
                if event.type == pygame.JOYBUTTONDOWN:
                    
                    # обработка камеры, либо увеличиваем на 1 градус за каждый проход, либо уменьшаем 
                    if event.button == self.index_camera_up:
                        self.value['servo_cam'] = 1
                    elif event.button == self.index_camera_down:
                        self.value['servo_cam'] = -1
                        
                    # обработка манипулятора, либо открываем (1), либо закрываем (-1), либо ничего не делаем (0)
                    if event.button == self.index_gripper_up:
                        self.value['gripper'] = 1
                    elif event.button == self.index_gripper_down:
                        self.value['servo_cam'] = -1

                    if event.button == self.index_led_check:
                        self.value['led_check'] = int(not bool(self.value['led_check']))
                    
                    
                    if event.button == self.index_options_stick_jl_x:
                        self.check_options_stick_jl_x = True

                    if event.button == self.index_options_stick_jl_y:
                        self.check_options_stick_jl_y = True

                    if event.button == self.index_options_stick_jr_x:
                        self.check_options_stick_jr_x = True

                    if event.button == self.index_options_stick_jr_y:
                        self.check_options_stick_jr_y = True

                    if event.button == self.index_options_stick_L:
                        self.check_options_stick_L = True

                    if event.button == self.index_options_stick_R:
                        self.check_options_stick_R = True
                        
                if event.type == pygame.JOYBUTTONUP:
                    
                    if event.button == self.index_options_stick_jl_x:
                        self.value_rotate_pushbutton_x = False

                    if event.button == self.index_options_stick_jl_y:
                        self.value_rotate_pushbutton_x = False

                    if event.button == self.index_options_stick_jr_x:
                        self.value_rotate_pushbutton_x = False

                    if event.button == self.index_options_stick_jr_y:
                        self.value_rotate_pushbutton_x = False

                    if event.button == self.index_options_stick_L:
                        self.value_rotate_pushbutton_x = False

                    if event.button == self.index_options_stick_R:
                        self.value_rotate_pushbutton_x = False
                    
                    if event.button == self.index_camera_up:
                        self.value['servo_cam'] = 0
                    if event.button == self.index_camera_down:
                        self.value['servo_cam'] = 0
                        
                    if event.button == self.index_gripper_up:
                        self.value['gripper'] = 0
                    if event.button == self.index_gripper_down:
                        self.value['servo_cam'] = 0
                        
                # опрос стиков
                if event.type == pygame.JOYAXISMOTION:
                    # обработка линейного движения 
                    if event.axis == self.index_options_stick_jl_x and not self.:
                        
                        
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_linear_x:
                            self.value['linear_x'] = int(round(event.value, 3) * self.power_linear_x * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_linear_x:
                            self.value['linear_x'] = int(round(event.value, 3) * self.power_linear_x) 
                            
                        else:
                            self.value['linear_x'] = 0
                            
                if event.axis == self.linear_x and self.value_rotate_pushbutton_x:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_linear_x:
                            self.value['linear_x'] = int(round(event.value, 3) * self.power_linear_x * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_linear_x:
                            self.value['linear_x'] = int(round(event.value, 3) * self.power_linear_x) 
                            
                        else:
                            self.value['linear_x'] = 0
                    
                    
                    if event.axis == self.linear_y:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_linear_y:
                            self.value['linear_y'] = int(round(event.value, 3) * self.power_linear_y * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_linear_y:
                            self.value['linear_y'] = int(round(event.value, 3) * self.power_linear_y) 
                            
                        else:
                            self.value['linear_y'] = 0
                        
                    
                    if event.axis == self.linear_z:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_linear_z:
                            self.value['linear_z'] = int(round(event.value, 3) * self.power_linear_z * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_linear_z:
                            self.value['linear_z'] = int(round(event.value, 3) * self.power_linear_z) 
                            
                        else:
                            self.value['linear_z'] = 0
                            
                    if event.axis == self.rotate_x:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_rotate_x:
                            self.value['rotate_x'] = int(round(event.value, 3) * self.power_rotate_x * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_rotate_x:
                            self.value['rotate_x'] = int(round(event.value, 3) * self.power_rotate_x) 
                            
                        else:
                            self.value['rotate_x'] = 0

                    if event.axis == self.rotate_y:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_rotate_x:
                            self.value['rotate_y'] = int(round(event.value, 3) * self.power_rotate_x * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_rotate_x:
                            self.value['rotate_y'] = int(round(event.value, 3) * self.power_rotate_x) 
                            
                        else:
                            self.value['rotate_y'] = 0

                    if event.axis == self.rotate_x:
                        if abs(round(event.value, 3)) >= self.min_value and self.reverse_rotate_x:
                            self.value['rotate_x'] = int(round(event.value, 3) * self.power_rotate_x * -1) 
                        
                        elif abs(round(event.value, 3)) >= self.min_value and not self.reverse_rotate_x:
                            self.value['rotate_x'] = int(round(event.value, 3) * self.power_rotate_x) 
                            
                        else:
                            self.value['rotate_x'] = 0




                else:
                    self.value['j1_val_y'], self.value['j2_val_y'], self.value['j1_val_x'], self.value['j2_val_x'] = 0, 0, 0, 0

                # повторная инициализация джойстика после отключения
                joysticks = []
                for i in range(self.pygame.joystick.get_count()):
                    joysticks.append(self.pygame.joystick.Joystick(i))
                for self.joystick in joysticks:
                    self.joystick.init()
                    break
                
            
            # проверка на корректность значений 
            if self.value['servo_cam'] >= 180:
                self.value['servo_cam'] = 180

            elif self.value['servo_cam'] <= 0:
                self.value['servo_cam'] = 0

            sleep(self.sleep_listen)

    def stop_listen(self):
        self.running = False

