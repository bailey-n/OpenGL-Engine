import pygame as pg
import moderngl as mgl
import numpy as np
import math
import glm


class BaseModel:
    def __init__(self, app, vao_name, texture_name,
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(theta) for theta in rot])
        self.scale = scale
        self.model_matrix = self.get_model_matrix()
        self.texture_name = texture_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def get_model_matrix(self):
        model_matrix = glm.mat4()

        # Account for initial coordinate translation
        model_matrix = glm.translate(model_matrix, self.pos)

        # Account for initial rotation
        model_matrix = glm.rotate(model_matrix, self.rot.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.z, glm.vec3(0, 0, 1))

        # Account for scaling
        model_matrix = glm.scale(model_matrix, self.scale)
        return model_matrix

    def update(self): ...

    def render(self):
        self.update()
        self.vao.render()


class BaseModel2D:
    def __init__(self, app, vao_name, texture_name,
                 pos=(0, 0), dimensions=(0, 0), scale=(1, 1), rot=0):
        self.app = app
        self.pos = pos
        self.scale = scale
        self.rot = rot

        self.width, self.height = dimensions

        self.texture_name = texture_name
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program

        self.model_matrix = self.get_model_matrix()

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        screen_width, screen_height = self.app.WIN_SIZE

        # Apply 2d translation
        if self.app.mode_2d == 'TL':
            offset_x = self.width * self.scale[0] / screen_width
            offset_y = self.height * self.scale[1] / screen_height
        elif self.app.mode_2d == 'CC':
            offset_x = 0
            offset_y = 0
        pos = (self.pos[0] + offset_x, self.pos[1] - offset_y, 0)
        model_matrix = glm.translate(model_matrix, pos)

        # scale down vertex coords (written in pixels) to be relative to screen
        relative_width = 1 / screen_width
        relative_height = 1 / screen_height
        pixel_rescale = (relative_width, relative_height, 1.0)
        model_matrix = glm.scale(model_matrix, pixel_rescale)

        # Apply rotation
        model_matrix = glm.rotate(model_matrix, self.rot, glm.vec3(0, 0, 1))

        return model_matrix

    def update(self): ...

    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', texture_name='crate',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_name, pos, rot, scale)
        self.on_init()

    def update(self):
        # model_matrix = glm.rotate(self.model_matrix, self.app.time, glm.vec3(0, 1, 0))
        self.texture.use()
        self.program['view_matrix'].write(self.app.camera.view_matrix)
        self.program['model_matrix'].write(self.model_matrix)

    def on_init(self):
        # Send texture data to shader
        self.texture = self.app.mesh.texture.textures[self.texture_name]
        self.program['u_texture_0'] = 0
        self.texture.use()

        # Send matrix data to shader
        self.program['projection_matrix'].write(self.app.camera.projection_matrix)
        self.program['view_matrix'].write(self.app.camera.view_matrix)
        self.program['model_matrix'].write(self.model_matrix)


class GUI(BaseModel2D):
    def __init__(self, app, vao_name='gui_vao', texture_name='stretch',
                 pos=(0, 0), dimensions=(0, 0), scale=(1, 1), rot=0):
        super().__init__(app, vao_name, texture_name, pos, dimensions, scale, rot)
        self.on_init()

    def update(self):
        self.texture.use()
        self.model_matrix = self.get_model_matrix()
        self.program['model_matrix'].write(self.model_matrix)

    def on_init(self):
        # Send texture data to shader
        self.texture = self.app.mesh.texture.textures[self.texture_name]
        self.program['u_texture_0'] = 0
        self.texture.use()

        # Send matrix data to shader
        self.program['model_matrix'].write(self.model_matrix)
