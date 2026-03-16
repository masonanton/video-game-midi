import pygame
from pygame.locals import *
from controllers.n64_controller import N64Controller
from controllers.keyboard_controller import KeyboardController
from windows.display import Display
from windows.visualizer import Visualizer

try:
    pygame.init()
except:
    print("Error in intialization.")

display = Display(700, 400)
visualizer = Visualizer(800, 600)
keyboard_controller = KeyboardController()

clock = pygame.time.Clock()

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
            case pygame.KEYDOWN:
                keyboard_controller.process_button_down(event)
            case pygame.KEYUP:
                keyboard_controller.process_button_up(event)

    display.clear()

    if not controller:
        display.write_text('no controller detected. using keyboard.')
        controller_state = keyboard_controller.get_state()
    else:
        display.write_text('n64 controller in use.')
        controller_state = controller.get_state()
    display.update_state(controller_state)
    visualizer.update(controller_state)

    pygame.display.flip()
    visualizer.tick()
    clock.tick(60)

pygame.quit()








