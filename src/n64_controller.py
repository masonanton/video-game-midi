class N64Controller:
    def __init__(self, joystick):
        self.joystick = joystick

        self.button_map = {
            2: "A",
            1: "B",
            3: "CDOWN",
            8: "CRIGHT",
            9: "CUP",
            0: "CLEFT",
            12: "START",
            4: "L",
            5: "R",
            6: "Z"
        }

        self.state = {
            "buttons_on": set(),
            "axis": [0,0],
            "hats": (0,0)
        }

    def process_axis_movement(self):
        x = self.joystick.get_axis(0)
        y = self.joystick.get_axis(1)
        self.state["axis"] = [x,y]

    def process_button_down(self, event):
        button_name = self._event_to_button_name(event)
        self.state["buttons_on"].add(button_name)
    
    def process_button_up(self, event):
        button_name = self._event_to_button_name(event)
        if button_name in self.state["buttons_on"]:
            self.state["buttons_on"].remove(button_name)

    def process_hats_movement(self):
        self.state["hats"] = self.joystick.get_hat(0)
    
    def get_state(self):
        return self.state

    def _event_to_button_name(self, event):
        button_num = event.dict["button"]
        return self.button_map[button_num]


