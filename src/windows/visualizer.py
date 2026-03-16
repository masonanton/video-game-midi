import random
import math
import glfw
from OpenGL.GL import *

class Visualizer:
    def __init__(self, width, height):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.window = glfw.create_window(width, height, "Visualizer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        self.width = width
        self.height = height

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  

        self.points = [
            (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(10000)
        ]

        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.idle_yaw_speed = 0.00
        self.idle_pitch_speed = 0.00

        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

        self.wave_x = 0.0
        self.wave_y = 0.0
        self.wave_time = 0.0

        self.color = (1.0, 1.0, 1.0)
        self.flash = 0.0

    def update(self, controller_state):
        self.yaw += self.idle_yaw_speed
        self.pitch += self.idle_pitch_speed
        self.wave_time += 0.05

        if controller_state is None:
            return

        buttons = controller_state.get("buttons", set())
        hats = controller_state.get("hats", (0,0))
        joystick = controller_state.get("joystick", (0.0, 0.0))
        
        if "A" in buttons:
            self.angle_x += 2.0
        if "B" in buttons:
            self.angle_x -= 2.0
        if "Z" in buttons:
            self.angle_z -= 2.0
        if "R" in buttons:
            self.angle_z += 2.0
        if "CUP" in buttons:
            self.angle_y += 2.0
        if "CDOWN" in buttons:
            self.angle_y -= 2.0
        if "CLEFT" in buttons:
            self.angle_y -= 2.0
        if "CRIGHT" in buttons:
            self.angle_y += 2.0
        if "START" in buttons:
            self.angle_x = 0.0
            self.angle_y = 0.0
            self.angle_z = 0.0

        if hats[1] == 1:
            self.color = (1.0, 1.0, 1.0)
            self.flash = 1.0
        elif hats[1] == -1:
            self.color = (0.2, 0.4, 1.0)
            self.flash = 1.0
        if hats[0] == -1:
            self.color = (1.0, 0.2, 0.2)
            self.flash = 1.0
        elif hats[0] == 1:
            self.color = (0.2, 1.0, 0.3)
            self.flash = 1.0
            
        self.flash = max(0.0, self.flash - 0.05)
        self.wave_x = joystick[0]
        self.wave_y = joystick[1]

    def render(self):
        glfw.make_context_current(self.window)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.width / self.height
        glFrustum(-aspect * 0.1, aspect * 0.1, -0.1, 0.1, 0.2, 10.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -3.0)

        glRotatef(self.pitch + self.angle_x, 1, 0, 0)
        glRotatef(self.yaw + self.angle_y, 0, 1, 0)
        glRotatef(self.roll + self.angle_z, 0, 0, 1)

        brightness = min(1.0, 0.75 + self.flash * 0.25)
        r = self.color[0] * brightness
        g = self.color[1] * brightness
        b = self.color[2] * brightness

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glPointSize(2.0)

        glBegin(GL_POINTS)
        for (px, py, pz) in self.points:
            distort_y = self.wave_x * 0.3 * math.sin(pz * 4.0 + self.wave_time)
            distort_x = self.wave_y * 0.3 * math.sin(py * 4.0 + self.wave_time)
            glColor4f(r, g, b, 1.0)
            glVertex3f(px + distort_x, py + distort_y, pz)
        glEnd()

        glfw.swap_buffers(self.window)

    def tick(self):
        glfw.poll_events()
        if glfw.window_should_close(self.window):
            glfw.terminate()
            return
        self.render()