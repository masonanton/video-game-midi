import pygame

class KeyboardController:
    def __init__(self):
        self.state = {
            "buttons_on": set(),
            "axis": [0.0, 0.0],
            "hats": (0, 0)
        }

        self.key_button_map = {
            pygame.K_a: "A",
            pygame.K_b: "B",
            pygame.K_z: "Z",
            pygame.K_r: "R",
            pygame.K_l: "L",
            pygame.K_s: "START",
            pygame.K_u: "CUP",
            pygame.K_d: "CDOWN",
            pygame.K_q: "CLEFT",
            pygame.K_e: "CRIGHT",
        }

    def process_button_down(self, event):
        button_name = self.key_button_map.get(event.key)
        if button_name:
            self.state["buttons_on"].add(button_name)

    def process_button_up(self, event):
        button_name = self.key_button_map.get(event.key)
        if button_name and button_name in self.state["buttons_on"]:
            self.state["buttons_on"].remove(button_name)

    def process_axis_movement(self):
        keys = pygame.key.get_pressed()
        x = (1.0 if keys[pygame.K_RIGHT] else 0.0) - (1.0 if keys[pygame.K_LEFT] else 0.0)
        y = (-1.0 if keys[pygame.K_UP] else 0.0) + (1.0 if keys[pygame.K_DOWN] else 0.0)
        self.state["axis"] = [x, y]

    def process_hats_movement(self):
        keys = pygame.key.get_pressed()
        x = (1 if keys[pygame.K_1] else 0) - (1 if keys[pygame.K_2] else 0)
        y = (1 if keys[pygame.K_3] else 0) - (1 if keys[pygame.K_4] else 0)
        self.state["hats"] = (x, y)

    def get_state(self):
        self.process_axis_movement()
        self.process_hats_movement()
        return self.state