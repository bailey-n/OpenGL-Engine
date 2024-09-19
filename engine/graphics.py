import pygame as pg
import moderngl as mgl
import sys
from .model import *
from .camera import Camera
from .mesh import Mesh
from .scene import Scene
import os
import time


class Graphics:
    def __init__(self, win_size=(1600, 900), FPS=60):
        # Initialize pygame modules
        pg.init()

        # Store window size
        self.WIN_SIZE = win_size

        # Set framerate
        self.FPS = FPS

        # Set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # Create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Set existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Mouse settings
        # '''allows for mouse to be replaced by a custom mouse sprite'''
        # pg.mouse.set_visible(False)
        self.scrolling = 0

        # Set clock object for time tracking
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time_ms = 0

        # Create Camera object
        self.camera = Camera(self)

        # Create and store mesh object
        self.mesh = Mesh(self)

        # Store objects in scene variable
        self.scene = Scene(self)

        # Set 2d position mode
        self.mode_2d = 'TL'

        # Create mainloop var for later
        self.mainloop = None

    def close(self):
        self.mesh.destroy()
        pg.quit()
        sys.exit()

    def render(self):
        # Clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # Render scene
        self.scene.render()
        # Swap Buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def render_frame(self):
        self.get_time()
        self.camera.update()
        self.render()
        self.delta_time_ms = self.clock.tick(self.FPS)
        self.delta_time = self.delta_time_ms * 0.001