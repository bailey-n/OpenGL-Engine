import numpy as np
import moderngl as mgl
# from engine import Graphics
from typing import Union


class VBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbos = {}
        # self.vbos['cube'] = CubeVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

    def generate_vbo(self, name, VBO_class, *args):
        self.vbos[name] = VBO_class(self.ctx, *args)

    def generate_2d_vbo(self, aspect_ratio):
        self.vbos[f'gui_vbo_{len(self.vbos)}'] = GUI_VBO(self.ctx, aspect_ratio)


class BaseVBO:
    def __init__(self, ctx, *vbo_args):
        self.ctx = ctx
        self.vbo = self.get_vbo(vbo_args)
        self.format: str = None
        self.attrib: list = None

    def get_vertex_data(self): ...

    def get_vbo(self, vbo_args) -> None:
        vertex_data = self.get_vertex_data(*vbo_args)
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class GUI_VBO(BaseVBO):
    def __init__(self, ctx, px_width: Union[float, int], px_height: Union[float, int]):
        super().__init__(ctx, px_width, px_height)
        self.format = '2f 3f'
        self.attributes = ['in_texture_coord_0', 'in_position']

    @staticmethod
    def get_data(vertices: Union[list[tuple[float, ...], ...], list[tuple[int, ...], ...]],
                 indices: list[tuple[int, ...], ...]) -> np.array:

        data = [vertices[index] for triangle in indices for index in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self, px_width: Union[float, int], px_height: Union[float, int]):
        vertices = [(-1.0 * px_width, -1.0 * px_height, 0.0),
                    (1.0 * px_width, -1.0 * px_height, 0.0),
                    (1.0 * px_width, 1.0 * px_height, 0.0),
                    (-1.0 * px_width, 1.0 * px_height, 0.0)]
        indices = [(0, 2, 3), (0, 1, 2)]

        vertex_data = self.get_data(vertices, indices)

        texture_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_indices = [(0, 2, 3), (0, 1, 2)]

        texture_data = self.get_data(texture_vertices, texture_indices)

        vertex_data = np.hstack([texture_data, vertex_data])
        return vertex_data


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f'
        self.attributes = ['in_texture_coord_0', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[index] for triangle in indices for index in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6 ,7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        vertex_data = self.get_data(vertices, indices)

        texture_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_coord_indices = [(0, 2, 3), (0, 1, 2),
                                 (0, 2, 3), (0, 1, 2),
                                 (0, 1, 2), (2, 3, 0),
                                 (2, 3, 0), (2, 0, 1),
                                 (0, 2, 3), (0, 1, 2),
                                 (3, 1, 2), (3, 0 ,1)]
        texture_coord_data = self.get_data(texture_coord, texture_coord_indices)

        vertex_data = np.hstack([texture_coord_data, vertex_data])
        return vertex_data