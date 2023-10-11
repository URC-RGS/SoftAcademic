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
        
        self.check_options_stick_jl_x = False
        self.check_options_stick_jl_y = False
        self.check_options_stick_jr_x = False
        self.check_options_stick_jr_y = False
        self.check_options_stick_L = False
        self.check_options_stick_R = False

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
                        self.value['servo_cam'] = -1

                    if event.button == self.index_led_check:
                        self.value['led_check'] = int(not bool(self.value['led_check']))
                    
                    if event.button == self.index_stabilization_depth:
                        self.value['stabilization_depth'] = int(not bool(self.value['stabilization_depth']))
                        
                    if event.button == self.index_stabilization_course:
                        self.value['stabilization_course'] = int(not bool(self.value['stabilization_course']))
                    
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
                        
                # опрос стиков с учетом дополнительного функционала 
                if event.type == pygame.JOYAXISMOTION:
                    # обработка оси X левого джойстика
                    # основной функционал без инвертирования 
                    if event.axis == self.index_options_stick_jl_x and not self.check_options_stick_jl_x and not self.reverse_stick_jl_x:
                        self.value["rotate_axis_y"] = event.value 
                        
                    # основной фунционал инвертированный 
                    elif event.axis == self.index_options_stick_jl_x and not self.check_options_stick_jl_x and self.reverse_stick_jl_x:
                        self.value["rotate_axis_y"] = event.value * -1
                        
                    # дополнительный функционал без инвертирования 
                    elif event.axis == self.index_options_stick_jl_x and self.check_options_stick_jl_x and not self.reverse_stick_jl_x:
                        pass
                    
                    # дополнительный функционал инвертированный 
                    elif event.axis == self.index_options_stick_jl_x and self.check_options_stick_jl_x and self.reverse_stick_jl_x:
                        pass
                    
                    # обработка оси Y левого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_options_stick_jl_y and not self.check_options_stick_jl_y and not self.reverse_stick_jl_y:
                        self.value["linear_axis_x"] = event.value
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_options_stick_jl_y and not self.check_options_stick_jl_y and self.reverse_stick_jl_y:
                        self.value["linear_axis_x"] = event.value * -1
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_options_stick_jl_y and self.check_options_stick_jl_y and not self.reverse_stick_jl_y:
                        pass
                    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_options_stick_jl_y and self.check_options_stick_jl_y and self.reverse_stick_jl_y:
                        pass
                    
                    # обработка оси X правого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_options_stick_jr_x and not self.check_options_stick_jr_x and not self.reverse_stick_jr_x:
                        self.value["linear_axis_z"] = event.value
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_options_stick_jr_x and not self.check_options_stick_jr_x and self.reverse_stick_jr_x:
                        self.value["linear_axis_z"] = event.value * -1
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_options_stick_jr_x and self.check_options_stick_jr_x and not self.reverse_stick_jr_x:
                        self.value["rotate_axis_x"] = event.value
    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_options_stick_jr_x and self.check_options_stick_jr_x and self.reverse_stick_jr_x:
                        self.value["rotate_axis_x"] = event.value * -1
                    
                    # обработка оси Y правого джойстика
                    # основной функционал без инвертирования
                    if event.axis == self.index_options_stick_jr_y and not self.check_options_stick_jr_y and not self.reverse_stick_jr_y:
                        self.value['linear_axis_y'] = event.value
                        
                    # основной функционал инвертированный
                    elif event.axis == self.index_options_stick_jr_y and not self.check_options_stick_jr_y and self.reverse_stick_jr_y:
                        self.value['linear_axis_y'] = event.value * -1
                        
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_options_stick_jr_y and self.check_options_stick_jr_y and not self.reverse_stick_jr_y:
                        self.value["rotate_axis_z"] = event.value

                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_options_stick_jr_y and self.check_options_stick_jr_y and self.reverse_stick_jr_y:
                        self.value["rotate_axis_z"] = event.value * -1
                        
                    # обработка левого курка
                    # основной функционал без инвертирования
                    if event.axis == self.index_options_stick_L and not self.check_options_stick_L and not self.reverse_stick_L:
                        pass
                    
                    # основной функционал инвертированный
                    elif event.axis == self.index_options_stick_L and not self.check_options_stick_L and self.reverse_stick_L:
                        pass
                    
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_options_stick_L and self.check_options_stick_L and not self.reverse_stick_L:
                        pass
                    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_options_stick_L and self.check_options_stick_L and self.reverse_stick_L:
                        pass

                    # обработка правого курка
                    # основной функционал без инвертирования
                    if event.axis == self.index_options_stick_R and not self.check_options_stick_R and not self.reverse_stick_R:
                        pass
                    
                    # основной функционал инвертированный
                    elif event.axis == self.index_options_stick_R and not self.check_options_stick_R and self.reverse_stick_R:
                        pass
                    
                    # дополнительный функционал без инвертирования
                    elif event.axis == self.index_options_stick_R and self.check_options_stick_R and not self.reverse_stick_R:
                        pass
                    
                    # дополнительный функционал инвертированный
                    elif event.axis == self.index_options_stick_R and self.check_options_stick_R and self.reverse_stick_R:
                        pass
                
                else:
                    self.value['linear_axis_x'],
                    self.value['linear_axis_y'],
                    self.value['linear_axis_z'],
                    self.value['rotate_axis_x'],
                    self.value['rotate_axis_y'], 
                    self.value['rotate_axis_z'] = 0, 0, 0, 0, 0, 0

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

