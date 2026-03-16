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
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)
        glViewport(0, 0, width, height)

        self.points = [
            (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(10000)
        ]

        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

        # Angular velocities
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.vel_z = 0.0

        self.acceleration = 0.4
        self.max_speed = 6.0
        self.friction = 0.92

        self.wave_x = 0.0
        self.wave_y = 0.0
        self.wave_time = 0.0

        self.color = (1.0, 1.0, 1.0)
        self.flash = 0.0

    def _on_resize(self, window, width, height):
        self.width = width
        self.height = height
        glfw.make_context_current(self.window)
        glViewport(0, 0, width, height)

    def update(self, controller_state):
        self.wave_time += 0.05

        if controller_state is None:
            self._apply_physics()
            return

        buttons = controller_state.get("buttons_on", set())
        hats = controller_state.get("hats", (0, 0))
        axis = controller_state.get("axis", [0.0, 0.0])

        if "START" in buttons:
            self.vel_x = 0.0
            self.vel_y = 0.0
            self.vel_z = 0.0

        if "A" in buttons:
            self.vel_x = min(self.vel_x + self.acceleration, self.max_speed)
        if "B" in buttons:
            self.vel_x = max(self.vel_x - self.acceleration, -self.max_speed)
        if "R" in buttons:
            self.vel_z = min(self.vel_z + self.acceleration, self.max_speed)
        if "Z" in buttons:
            self.vel_z = max(self.vel_z - self.acceleration, -self.max_speed)
        if "CUP" in buttons:
            self.vel_y = min(self.vel_y + self.acceleration, self.max_speed)
        if "CDOWN" in buttons:
            self.vel_y = max(self.vel_y - self.acceleration, -self.max_speed)
        if "CLEFT" in buttons:
            self.vel_y = max(self.vel_y - self.acceleration, -self.max_speed)
        if "CRIGHT" in buttons:
            self.vel_y = min(self.vel_y + self.acceleration, self.max_speed)

        # Build color by averaging all active hat directions
        hat_colors = []
        if hats[1] == 1:
            hat_colors.append((0.78, 0.52, 0.52))  # up: white
        if hats[1] == -1:
            hat_colors.append((0.35, 0.45, 0.62))  # down: blue
        if hats[0] == -1:
            hat_colors.append((0.72, 0.38, 0.18))  # left: red
        if hats[0] == 1:
            hat_colors.append((0.45, 0.58, 0.42))  # right: green

        if hat_colors:
            r = sum(c[0] for c in hat_colors) / len(hat_colors)
            g = sum(c[1] for c in hat_colors) / len(hat_colors)
            b = sum(c[2] for c in hat_colors) / len(hat_colors)
            self.color = (r, g, b)
            self.flash = 1.0

        self.flash = max(0.0, self.flash - 0.05)
        self.wave_x = axis[0]
        self.wave_y = axis[1]

        self._apply_physics()

    def _apply_physics(self):
        self.angle_x += self.vel_x
        self.angle_y += self.vel_y
        self.angle_z += self.vel_z
        self.vel_x *= self.friction
        self.vel_y *= self.friction
        self.vel_z *= self.friction

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
        glTranslatef(0.0, 0.0, -5.0)

        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        glRotatef(self.angle_z, 0, 0, 1)

        brightness = min(1.0, 0.75 + self.flash * 0.25)
        r = self.color[0] * brightness
        g = self.color[1] * brightness
        b = self.color[2] * brightness

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glPointSize(2.0)

        glBegin(GL_POINTS)
        for (px, py, pz) in self.points:
            distort_y = self.wave_x * 0.6 * math.sin(pz * 4.0 + self.wave_time)
            distort_x = self.wave_y * 0.6 * math.sin(py * 4.0 + self.wave_time)
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