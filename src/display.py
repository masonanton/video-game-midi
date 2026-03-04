import pygame
import os
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

IMAGE_PATH = "imgs"

IMAGE_MAPPINGS = {
    "outline": "outline.png",
    "A": "a.png",
    "B": "b.png",
    "CDOWN": "cdown.png",
    "CRIGHT": "cright.png",
    "CUP": "cup.png",
    "CLEFT": "cleft.png",
    "START": "start.png",
    "L": "l.png",
    "R": "r.png",
    "Z": "z.png",
    "DOWNHAT": "downhat.png",
    "RIGHTHAT": "righthat.png",
    "UPHAT": "uphat.png",
    "LEFTHAT": "lefthat.png",
    "AXIS": "axis.png"
}

def create_image(item):
    return pygame.image.load(os.path.join(IMAGE_PATH, IMAGE_MAPPINGS[item])).convert_alpha()
class Display:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.width = screen_width
        self.height = screen_height
        self.top_left = (
            (screen_width - 700) // 2, 
            (screen_height - 400) // 2
        )
        pygame.display.set_caption("Video Game MIDI Controller")

    def write_text(self, text):
        font = pygame.font.SysFont('ocraextended',30)
        alert = font.render(text, 1, WHITE)
        self.screen.blit(alert, (0, 0))

    def display_image(self, name, location = (0,0)):
        image = create_image(name)
        if location == (0,0):
            self.screen.blit(image, self.top_left)
        else:
            # this is not a perfect solution to locating the joystick on the display
            # it simply multiplies the location by a factor to place it within the larger circle
            # in reality, this factor should change based on x, y angle (think a triangle)
            # for now we will keep it
            new_x = self.top_left[0] + 15 * location[0]
            new_y = self.top_left[1] + 15 * location[1]
            self.screen.blit(image, (new_x, new_y))

    def update_state(self, state):
        self.display_image("outline")
        self.display_buttons(state["buttons_on"])
        self.display_hats(state["hats"])
        self.display_axis(state["axis"])

    def clear(self):
        self.screen.fill(BLACK)
    
    def display_buttons(self, buttons_on):
        for button_name in buttons_on:
            self.display_image(button_name)

    def display_hats(self, hats):
        if hats[0] == 1:
            self.display_image("RIGHTHAT")
        elif hats[0] == -1:
            self.display_image("LEFTHAT")
        if hats[1] == 1:
            self.display_image("UPHAT")
        elif hats[1] == -1:
            self.display_image("DOWNHAT")

    def display_axis(self, axis):
        x,y = axis
        self.display_image("AXIS", (x,y))



    


