import pygame
from pygame.locals import *
from time import sleep
from n64_controller import N64Controller
from display import Display

try:
    pygame.init()
except:
    print("Error in intialization.")

display = Display(700, 400)

controller = None

running = True
while running:

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                controller = N64Controller(joystick)
            case pygame.JOYDEVICEREMOVED:
                if controller and event.instance_id == controller.joystick.get_instance_id():
                    controller = None
            case pygame.JOYAXISMOTION:
                controller.process_axis_movement()
            case pygame.JOYBUTTONDOWN:
                controller.process_button_down(event)
            case pygame.JOYBUTTONUP:
                controller.process_button_up(event)
            case pygame.JOYHATMOTION:
                controller.process_hats_movement()

        display.clear()

        if not controller:
            display.write_text('No controller detected.')

pygame.quit()








