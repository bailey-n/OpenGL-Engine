from __future__ import annotations
import pygame as pg
from dataclasses import dataclass, field
from typing import Union, Optional
from engine import Graphics
from engine.vbo import GUI_VBO
from engine.model import GUI
from game.stages.stage import Stage
from game.assets.key_funcs import KeyFuncs
import glm
import logging


@dataclass
class StaticImage(KeyFuncs):
    # Identifying properties
    app: Graphics
    name: str
    stage: Stage = None
    # Physical properties
    textures: Union[tuple[str, ...], list[str, ...]] = field(default_factory=dict)
    pos: Optional[Union[tuple[float, float], tuple[int, int]]] = None
    posPx: Optional[Union[tuple[float, float], tuple[int, int], None]] = None
    dimensions: Optional[Union[tuple[float, float], tuple[int, int], None]] = None
    dimensionsPx: Optional[Union[tuple[float, float], tuple[int, int]]] = None
    scale: Optional[Union[tuple[float, float], tuple[int, int], None]] = field(default=(1, 1))
    rot: Optional[Union[float, int]] = field(default=0)
    # Key functions: key down functions, key hold functions, key up functions
    kdfs: Optional[dict] = None
    khfs: Optional[dict] = None
    kufs: Optional[dict] = None
    # Internal variables
    program_name: str = field(init=False, default='gui')
    current_texture: int = field(init=False, default=0)
    isViewable: bool = field(init=False, default=False)


    def __post_init__(self):
        logging.info(f' Generating StaticImage data for {self.__class__.__name__} object \'{self.name}\'')
        scr_width, scr_height = self.app.WIN_SIZE
        # Convert screen scale <-> pixels
        if self.dimensionsPx is not None:
            if self.dimensions:
                logging.warning(f' Creating {self.__class__.__name__} object \'{self.name}\' with both specified screen dimensions and pixel dimensions; defaulting to pixel dimensions')
            self.dimensions = (self.dimensionsPx[0] / scr_width,
                               self.dimensionsPx[1] / scr_height)

        elif self.dimensions is not None:
            self.dimensionsPx = (self.dimensions[0] * scr_width,
                                 self.dimensions[1] * scr_height)
            # Compute aspect ratio for later
            self.aspect_ratio = self.dimensionsPx[0] / self.dimensionsPx[1]

        # Compute position conversion based on 2D graphing mode
        if self.posPx is not None:
            if self.pos is not None:
                logging.warning(f' Creating {self.__class__.__name__} object \'{self.name}\' with both a specified screen position and pixel position; defaulting to pixel position')
            self.pos = self.px_to_scr(self.posPx)
        elif self.pos is not None:
            self.posPx = self.scr_to_px(self.pos)

        # Establish default pos and dim values if none are given
        if self.pos is None and self.posPx is None:
            if self.app.mode_2d == 'TL':
                self.pos = (-1, 1)
                self.posPx = (0, 0)
            elif self.app.mode_2d == 'CC':
                self.pos = (0, 0)
                self.posPx = (0, 0)
                logging.warning(f' Creating {self.__class__.__name__} object \'{self.name}\' without a specified initial position')
        if self.dimensions is None and self.dimensionsPx is None:
            self.dimensions = (0, 0)
            self.dimensionsPx = (0, 0)
            # Set aspect ratio to 0 for later, will make it impossible for image to render
            self.aspect_ratio = 0
            logging.warning(f' Creating {self.__class__.__name__} object \'{self.name}\' without specified initial dimensions; image will not render upon rescaling')

        # Create vars for initial width and height
        self.width, self.height = self.dimensionsPx

        # Ensure that program name and texture files exist
        if not self.program_name in self.app.mesh.program.programs:
            self.app.mesh.program.generate_program(self.program_name)

        for texture_name in self.textures:
            if not texture_name in self.app.mesh.texture.textures:
                self.app.mesh.texture.generate_texture(texture_name)

        # Set default/initial texture to first texture in array
        self.texture_name = self.textures[0]

        # Rescale to establish initial scale and gain initial model
        self.rescale(self.scale)
        
        # Turn key function strings into callable funcs
        if self.kdfs is not None:
            for key in self.kdfs:
                func = getattr(self, self.kdfs[key], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set key down function to \'{self.kdfs[key]}\', but \'{self.kdfs[key]}\' does not exist '
                                    f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.kdfs[key] = func

        if self.khfs is not None:
            for key in self.khfs:
                func = getattr(self, self.khfs[key], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set key-hold function to \'{self.khfs[key]}\', but \'{self.khfs[key]}\' does not exist '
                                    f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.khfs[key] = func

        if self.kufs is not None:
            for key in self.kufs:
                func = getattr(self, self.kufs[key], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set key up function to \'{self.kufs[key]}\', but \'{self.kufs[key]}\' does not exist '
                                    f'as any key funcs or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.kufs[key] = func

    def __copy__(self, name: str) -> StaticImage:
        new_static_image = StaticImage(app=self.app,
                                       name=name,
                                       stage=self.stage if self.stage is not None else None,
                                       textures=self.textures[:],
                                       pos=self.pos[:],
                                       posPx=self.posPx[:],
                                       dimensions=self.dimensions[:],
                                       dimensionsPx=self.dimensionsPx[:],
                                       scale=self.scale[:],
                                       rot=self.rot,
                                       # Returns name of function in dict if it is not None, blank string otherwise (to be converted to None in initialization)
                                       # Will return None (default dict value) if the original dict is None
                                       kdfs = {key: self.kdfs[key].__name__ if self.kdfs[key] is not None else '' for key in self.kdfs} if self.kdfs is not None else None,
                                       khfs = {key: self.khfs[key].__name__ if self.khfs[key] is not None else '' for key in self.khfs} if self.khfs is not None else None,
                                       kufs = {key: self.kufs[key].__name__ if self.kufs[key] is not None else '' for key in self.kufs} if self.kufs is not None else None,
                                       )
        return new_static_image

    def rescale(self, scale: Union[tuple[float, float], tuple[int, int]]) -> None:
        # Establish temp scales
        self.scale = scale
        x_scale, y_scale = scale
        scaled_width = self.dimensionsPx[0] * x_scale
        scaled_height = self.dimensionsPx[1] * y_scale

        # Create new VBO fork, delete old one if necessary
        self.vbo_name = f'gui_vbo_{self.texture_name}_{self.name}'
        if self.vbo_name in self.app.mesh.vbo.vbos:
            del self.app.mesh.vbo.vbos[self.vbo_name]
            logging.info(f' Replacing old VBO fork of \'{self.name}\', \'{self.vbo_name}\'')

        self.app.mesh.vbo.generate_vbo(self.vbo_name, GUI_VBO, scaled_width, scaled_height)

        # Create new VAO fork, delete old one if necessary
        self.vao_name = f'gui_vao_{self.texture_name}_{self.name}'
        if self.vao_name in self.app.mesh.vao.vaos:
            del self.app.mesh.vao.vaos[self.vao_name]
            logging.info(f' Replacing old VAO fork of \'{self.name}\', \'{self.vao_name}\'')

        self.app.mesh.vao.generate_vao(name=self.vao_name,
                                       vbo_name=self.vbo_name,
                                       program_name=self.program_name)

        # Update model in scene if object is viewable
        self.update()

    def switch_to_texture(self, texture_index: int) -> None:
        num_textures = len(self.textures)
        if (-num_textures) <= texture_index < num_textures:
            self.current_texture = texture_index
            self.texture_name = self.textures[texture_index]
            self.update()
        else:
            logging.warning(f' failed to switch {self.__class__.__name__} object \'{self.name}\'s texture to texture [{texture_index}]: '
                            f'texture index is not in range of textures array')

    def generate_model(self) -> GUI:
        model = GUI(app=self.app,
                    vao_name=self.vao_name,
                    texture_name=self.texture_name,
                    pos=self.pos,
                    dimensions=self.dimensionsPx,
                    scale=self.scale,
                    rot=self.rot)
        return model

    def update(self) -> None:
        new_model = self.generate_model()
        if self.isViewable:
            scene_layer = self.app.scene.objects.index(self.model)
            self.app.scene.objects[scene_layer] = new_model
        self.model = new_model

    def updateTo(self, model) -> None:
        if self.isViewable:
            scene_layer = self.app.scene.objects.index(self.model)
            self.app.scene.objects[scene_layer] = model
        self.model = model
        
    def load(self) -> None:
        self.app.mainloop.game_objects.append(self)
        if self.kdfs is not None:
            for key in self.kdfs:
                if self.kdfs is not None:
                    self.app.mainloop.key_down_func_dict[key].append(self)
        if self.khfs is not None:
            for key in self.khfs:
                if self.khfs is not None:
                    self.app.mainloop.key_hold_func_dict[key].append(self)
        if self.kufs is not None:
            for key in self.kufs:
                if self.kufs is not None:
                    self.app.mainloop.key_up_func_dict[key].append(self)
                    
    def unload(self) -> None:
        self.app.mainloop.game_objects.remove(self)
        for asset_list in self.app.mainloop.key_down_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)
        for asset_list in self.app.mainloop.key_hold_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)
        for asset_list in self.app.mainloop.key_up_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)
        

    def add_to_scene(self, scene_layer: int = None) -> None:
        if not self.isViewable:
            self.isViewable = True
            if not scene_layer:
                self.app.scene.add_object(self.model)
            else:
                self.app.scene.insert(scene_layer, self.model)
        else:
            logging.warning(f' failed to add {self.__class__.__name__} object \'{self.name}\' to scene: already viewable in scene')

    def move_to_scene_layer(self, scene_layer: int) -> None:
        if self.isViewable:
            scene_objects = len(self.app.scene.objects)
            if (-scene_objects) <= scene_layer < scene_objects:
                self.remove_from_scene()
                self.add_to_scene(scene_layer)
            else:
                logging.warning(f' failed to move {self.__class__.__name__} object \'{self.name}\' to scene layer [{scene_layer}]: scene layer index not in range of scene object array')
        else:
            logging.warning(f' failed to move {self.__class__.__name__} object \'{self.name}\' to scene layer [{scene_layer}]: object is not viewable in scene')

    def remove_from_scene(self) -> None:
        if self.isViewable:
            self.isViewable = False
            self.app.scene.remove_object(self.model)
        else:
            logging.warning(f' failed to remove {self.__class__.__name__} object \'{self.name}\' to scene: object not viewable in scene')

    def px_to_scr(self, posPx: Union[tuple[float, float], tuple[int, int]]) -> Union[tuple[float, float], tuple[int, int]]:
        scr_width, scr_height = self.app.WIN_SIZE
        if self.app.mode_2d == 'TL':
            pos = (((posPx[0] * 2) / scr_width) - 1,
                   ((posPx[1] * -2) / scr_height) + 1)
        elif self.app.mode_2d == 'CC':
            pos = (posPx[0] / scr_height,
                   posPx[1] / scr_height)
        return pos

    def scr_to_px(self, pos: Union[tuple[float, float], tuple[int, int]]) -> Union[tuple[float, float], tuple[int, int]]:
        scr_width, scr_height = self.app.WIN_SIZE
        if self.app.mode_2d == 'TL':
            posPx = (((scr_width * (pos[0] + 1)) - self.dimensions[0] * self.scale[0]) / 2,
                    ((scr_height * (pos[1] - 1)) + self.dimensions[1] * self.scale[1]) / -2)
        elif self.app.mode_2d == 'CC':
            posPx = (pos[0] * scr_width,
                     pos[1] * scr_height)
        return posPx

    def keys_down(self, keys):
        for key in keys:
            self.kdfs[key](keys)

    def keys_hold(self, keys, hold_times):
        for key in keys:
            self.khfs[key](keys, hold_times)

    def keys_up(self, keys):
        for key in keys:
            self.kufs[key](keys)


