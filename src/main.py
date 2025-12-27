import pygame
from pygame.locals import *
from time import sleep

try:
    pygame.init()
except:
    print("Error in intialization.")

while (pygame.joystick.get_count() == 0):
    pygame.event.pump()
    print("No joystick detected.")
    sleep(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()






