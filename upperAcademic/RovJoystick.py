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
                      'linear_x': 0,
                      'linear_y': 0,
                      'linear_z': 0,
                          
                      'rotate_x': 0,
                      'rotate_y': 0,
                      'rotate_z': 0,           
                      
                      'servo_cam': 0,             
                      'gripper': 0,
                      'led': 0,
                      
                      'stabilization_depth' : 0,
                      'stabilization_course' : 0
                    }
        
        # назначение кнопок камеры
        self.index_camera_up = self.config_joystick[self.config_joystick['camera_up']]
        self.index_camera_down = self.config_joystick[self.config_joystick['camera_down']]

        # назначение кнопок манипулятора
        self.index_gripper_up =  self.config_joystick[self.config_joystick['gripper_up']]
        self.index_gripper_down =  self.config_joystick[self.config_joystick['gripper_down']]

        # назначение кнопки светильника
        self.index_led_check = self.config_joystick[self.config_joystick['led_check']]
        
        # назначение кнопки автоглубины
        self.index_stabilization_depth = self.config_joystick[self.config_joystick['stabilization_depth']]
        
        # назначение кнопки автокурса 
        self.index_stabilization_course = self.config_joystick[self.config_joystick['stabilization_course']]
        
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
        
        self.check_options_stick_jl_x = 0
        self.check_options_stick_jl_y = 0
        self.check_options_stick_jr_x = 0
        self.check_options_stick_jr_y = 0
        self.check_options_stick_L = 0
        self.check_options_stick_R = 0

        self.reverse_stick_jl_x = self.config_joystick["reverse_stick_jl_x"]
        self.reverse_stick_jl_y = self.config_joystick["reverse_stick_jl_y"]
        self.reverse_stick_jr_x = self.config_joystick["reverse_stick_jr_x"]
        self.reverse_stick_jr_y = self.config_joystick["reverse_stick_jr_y"]
        self.reverse_stick_L = self.config_joystick["reverse_stick_L"]
        self.reverse_stick_R = self.config_joystick["reverse_stick_R"]
        
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
                    
                    # либо открываем (1), либо закрываем (-1), либо ничего не делаем (0)
                    if event.button == self.index_camera_up:
                        self.value['servo_cam'] = 1

                    elif event.button == self.index_camera_down:
                        self.value['servo_cam'] = -1
                        
                    # либо открываем (1), либо закрываем (-1), либо ничего не делаем (0)
                    if event.button == self.index_gripper_up:
                        self.value['gripper'] = 1
                        
                    elif event.button == self.index_gripper_down:
                        self.value['gripper'] = -1

                    if event.button == self.index_led_check:
                        self.value['led'] = int(not bool(self.value['led']))
                    
                    if event.button == self.index_stabilization_depth:
                        self.value['stabilization_depth'] = int(not bool(self.value['stabilization_depth']))
                        
                    if event.button == self.index_stabilization_course:
                        self.value['stabilization_course'] = int(not bool(self.value['stabilization_course']))
                    
                    if event.button == self.index_options_stick_jl_x:
                        self.check_options_stick_jl_x = 1

                    if event.button == self.index_options_stick_jl_y:
                        self.check_options_stick_jl_y = 1

                    if event.button == self.index_options_stick_jr_x:
                        self.check_options_stick_jr_x = 1

                    if event.button == self.index_options_stick_jr_y:
                        self.check_options_stick_jr_y = 1 

                    if event.button == self.index_options_stick_L:
                        self.check_options_stick_L = 1

                    if event.button == self.index_options_stick_R:
                        self.check_options_stick_R = 1
                        
                        
                if event.type == pygame.JOYBUTTONUP:
                    
                    if event.button == self.index_options_stick_jl_x:
                        self.check_options_stick_jl_x = 0

                    if event.button == self.index_options_stick_jl_y:
                        self.check_options_stick_jl_y = 0

                    if event.button == self.index_options_stick_jr_x:
                        self.check_options_stick_jr_x = 0

                    if event.button == self.index_options_stick_jr_y:
                        self.check_options_stick_jr_y = 0

                    if event.button == self.index_options_stick_L:
                        self.check_options_stick_L = 0

                    if event.button == self.index_options_stick_R:
                        self.check_options_stick_R = 0
                    
                    if event.button == self.index_camera_up:
                        self.value['servo_cam'] = 0
                        
                    if event.button == self.index_camera_down:
                        self.value['servo_cam'] = 0
                        
                    if event.button == self.index_gripper_up:
                        self.value['gripper'] = 0
                        
                    if event.button == self.index_gripper_down:
                        self.value['gripper'] = 0
                        
                # опрос стиков с учетом дополнительного функционала 
                if event.type == pygame.JOYAXISMOTION:
        
                    # обработка оси X левого джойстика
                    # основной функционал без инвертирования 
                    if event.axis == self.index_stick_jl_x and (not bool(self.check_options_stick_jl_x)) and (not self.reverse_stick_jl_x):
                        self.value["rotate_y"] = round(event.value * self.power_rotate_y, 2)
                               
                    # основной фунционал инвертированный 
                    elif event.axis == self.index_stick_jl_x and (not bool(self.check_options_stick_jl_x)) and self.reverse_stick_jl_x:
                        self.value["rotate_y"] = round(event.value * self.power_rotate_y * -1, 2)
                        
                    # дополнительный функционал без инвертирования 
                    elif event.axis == self.index_stick_jl_x and bool(self.check_options_stick_jl_x) and (not self.reverse_stick_jl_x):
                        self.value["rotate_x"] = round(event.value * self.power_rotate_x, 2)
                        
                    # дополнительный функционал инвертированный 
                    elif event.axis == self.index_stick_jl_x and bool(self.check_options_stick_jl_x) and self.reverse_stick_jl_x:
                        self.value["rotate_x"] = round(event.value * self.power_rotate_x * -1, 2)
                        
                    # обработка оси Y левого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_stick_jl_y and (not bool(self.check_options_stick_jl_y)) and (not self.reverse_stick_jl_y):
                        self.value["linear_x"] = round(event.value * self.power_linear_x, 2)
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_stick_jl_y and (not bool(self.check_options_stick_jl_y)) and self.reverse_stick_jl_y:
                        self.value["linear_x"] = round(event.value * self.power_linear_x * -1, 2)
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_stick_jl_y and bool(self.check_options_stick_jl_y) and (not self.reverse_stick_jl_y):
                        self.value["rotate_z"] = round(event.value * self.power_rotate_z, 2)
                        
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_stick_jl_y and bool(self.check_options_stick_jl_y) and self.reverse_stick_jl_y:
                        self.value["rotate_z"] = round(event.value * self.power_rotate_z * -1, 2)
                    
                    # обработка оси X правого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_stick_jr_x and not bool(self.check_options_stick_jr_x) and not self.reverse_stick_jr_x:
                        self.value["linear_z"] = round(event.value * self.power_linear_z, 2)
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_stick_jr_x and not bool(self.check_options_stick_jr_x) and self.reverse_stick_jr_x:
                        self.value["linear_z"] = round(event.value * self.power_linear_z * -1, 2)
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_stick_jr_x and bool(self.check_options_stick_jr_x) and not self.reverse_stick_jr_x:
                        pass
    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_stick_jr_x and bool(self.check_options_stick_jr_x) and self.reverse_stick_jr_x:
                        pass
                    
                    # обработка оси Y правого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_stick_jr_y and not bool(self.check_options_stick_jr_y) and not self.reverse_stick_jr_y:
                        self.value['linear_y'] = round(event.value * self.power_linear_y, 2)
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_stick_jr_y and not bool(self.check_options_stick_jr_y) and self.reverse_stick_jr_y:
                        self.value['linear_y'] = round(event.value * self.power_linear_y * -1, 2)
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_stick_jr_y and bool(self.check_options_stick_jr_y) and not self.reverse_stick_jr_y:
                        pass

                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_stick_jr_y and bool(self.check_options_stick_jr_y) and self.reverse_stick_jr_y:
                        pass
                        
                    # обработка левого курка
                    # основной функционал без инвертирования
                    if event.axis == self.index_stick_L and not bool(self.check_options_stick_L) and not self.reverse_stick_L:
                        pass
                    
                    # основной функционал инвертированный
                    elif event.axis == self.index_stick_L and not bool(self.check_options_stick_L) and self.reverse_stick_L:
                        pass
                    
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_stick_L and bool(self.check_options_stick_L) and not self.reverse_stick_L:
                        pass
                    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_stick_L and bool(self.check_options_stick_L) and self.reverse_stick_L:
                        pass

                    # обработка правого курка
                    # основной функционал без инвертирования
                    if event.axis == self.index_stick_R and not bool(self.check_options_stick_R) and not self.reverse_stick_R:
                        pass
                    
                    # основной функционал инвертированный
                    elif event.axis == self.index_stick_R and not bool(self.check_options_stick_R) and self.reverse_stick_R:
                        pass
                    
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_stick_R and bool(self.check_options_stick_R) and not self.reverse_stick_R:
                        pass
                    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_stick_R and bool(self.check_options_stick_R) and self.reverse_stick_R:
                        pass
                
                else:
                    self.value['linear_x'] = 0
                    self.value['linear_y'] = 0
                    self.value['linear_z'] = 0
                    self.value['rotate_x'] = 0
                    self.value['rotate_y'] = 0
                    self.value['rotate_z'] = 0

            # повторная инициализация джойстика 
            joysticks = []
            for i in range(self.pygame.joystick.get_count()):
                joysticks.append(self.pygame.joystick.Joystick(i))
            for self.joystick in joysticks:
                self.joystick.init()
                break
            
            # засыпаем на некоторое время между опросами 
            sleep(self.sleep_time)

    def stop_listen(self):
        self.running = False

