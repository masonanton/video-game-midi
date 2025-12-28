import pygame
from pygame.locals import *
from time import sleep
from n64_controller import N64Controller

try:
    pygame.init()
except:
    print("Error in intialization.")

while pygame.joystick.get_count() == 0:
    pygame.event.pump()
    print("No joystick detected.")
    sleep(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()
controller = N64Controller(joystick)


print("hats", joystick.get_numhats())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if event.type == pygame.JOYAXISMOTION:
        controller.process_axis_movement()
    elif event.type == pygame.JOYBUTTONDOWN:
        controller.process_button_down(event)
    elif event.type == pygame.JOYBUTTONUP:
        controller.process_button_up(event)
    elif event.type == pygame.JOYHATMOTION:
        controller.process_hats_movement()
    
    print(controller.get_state())








