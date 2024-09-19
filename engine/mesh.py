from .vao import VAO
from .vbo import VBO
from .shader_program import ShaderProgram
from .texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.vbo = self.vao.vbo
        self.program = self.vao.program
        self.texture = Texture(app.ctx)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()