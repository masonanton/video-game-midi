import pygame
from pygame.locals import *
from time import sleep

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

print("hats", joystick.get_numhats())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if event.type == pygame.JOYAXISMOTION:
        print(
            "Axis 0:", joystick.get_axis(0),
            "Axis 1:", joystick.get_axis(1),
            "Axis 2:", joystick.get_axis(2),
            "Axis 3:", joystick.get_axis(3)
        )

    if event.type == pygame.JOYBUTTONDOWN:
        print(
            event.dict
        )

    if event.type == pygame.JOYHATMOTION:
        print(
            "Hat 0:", joystick.get_hat(0)
        )








