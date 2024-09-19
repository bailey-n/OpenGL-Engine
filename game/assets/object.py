from engine.vbo import CubeVBO
from engine.model import Cube
from dataclasses import dataclass, field
from typing import Union
from engine import Graphics


@dataclass
class CubeObj:
    app: Graphics
    name: str
    texture_name: str
    pos: Union[tuple[float, float, float], tuple[int, int, int]] = field(default=(0, 0, 0))
    rot: Union[tuple[float, float, float], tuple[int, int, int]] = field(default=(0, 0, 0))
    scale: Union[tuple[float, float, float], tuple[int, int, int]] = field(default=(1, 1, 1))
    vbo_name: str = ''
    vao_name: str = ''
    program_name: str = field(init=False, default='default')
    isViewable: bool = field(init=False, default=True)

    def __post_init__(self) -> None:
        # Create model data in app mesh
        if not self.vbo_name in self.app.mesh.vbo.vbos:
            self.app.mesh.vbo.generate_vbo(name=self.vbo_name,
                                           VBO_class=CubeVBO)
        if not self.program_name in self.app.mesh.program.programs:
            self.app.mesh.program.generate_program(name=self.program_name)
        if not self.texture_name in self.app.mesh.texture.textures:
            self.app.mesh.texture.generate_texture(name=self.texture_name)
        if not self.vao_name in self.app.mesh.vao.vaos:
            self.app.mesh.vao.generate_vao(name=self.vao_name,
                                           program_name=self.program_name,
                                           vbo_name=self.vbo_name)

        self.model = Cube(app=self.app,
                          vao_name=self.vao_name,
                          texture_name=self.texture_name,
                          pos=self.pos,
                          rot=self.rot,
                          scale=self.scale)

    def moveBy(self, direction_vec: tuple[Union[float, int], ...]) -> None:
        self.pos = tuple(sum(components) for components in zip(self.pos, direction_vec))
        self.model.update()

    def moveTo(self, pos: Union[tuple[float, float, float], tuple[int, int, int]]) -> None:
        self.pos = pos
        self.model.update()

    def add_to_scene(self) -> None:
        self.isViewable = True
        self.app.scene.add_object(self.model)

    def remove_from_scene(self) -> None:
        self.isViewable = False
        self.app.scene.remove_object(self.model)
