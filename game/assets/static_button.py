from __future__ import annotations
from typing import Union, Optional
from .button_base import ButtonBase
from .static_image import StaticImage
from dataclasses import dataclass, field
import logging
import numpy as np
import math


@dataclass
class StaticButton(ButtonBase, StaticImage):
    def __post_init__(self):
        StaticImage.__post_init__(self)
        ButtonBase.__post_init__(self)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()

    def __copy__(self, name: str) -> StaticButton:
        new_static_button = StaticButton(app=self.app,
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
                                         cafs={button: self.cafs[button].__name__ if self.cafs[button] is not None else '' for button in self.cafs} if self.cafs is not None else None,
                                         cdfs={button: self.cdfs[button].__name__ if self.cdfs[button] is not None else '' for button in self.cdfs} if self.cdfs is not None else None,
                                         chfs={button: self.chfs[button].__name__ if self.chfs[button] is not None else '' for button in self.chfs} if self.chfs is not None else None,
                                         # Returns the name of the hover function if it is not None, otherwise will set to None (default value)
                                         haf=self.haf.__name__ if self.haf is not None else None,
                                         hdf=self.haf.__name__ if self.haf is not None else None,
                                         hhf=self.haf.__name__ if self.haf is not None else None,
                                         strictBounding=self.strictBounding
                                         )
        return new_static_button

    def get_corners(self) -> list[np.ndarray]:
        bottom_left = [-0.5 * self.dimensionsPx[0], -0.5 * self.dimensionsPx[1]]
        top_right = [0.5 * self.dimensionsPx[0], 0.5 * self.dimensionsPx[1]]
        top_left = [bottom_left[0], top_right[1]]
        bottom_right = [top_right[0], bottom_left[1]]
        # Create list of corners, convert them to numpy vectors
        corners = [top_left, top_right, bottom_left, bottom_right]
        corners = [np.array([[corner[0]], [corner[1]]], dtype=float) for corner in corners]

        scaling_matrix = np.array([[self.scale[0], 0],
                                   [0, self.scale[1]]], dtype=float)

        # Rotate backwards if in top-left mode
        if self.app.mode_2d == 'TL':
            sint = math.sin(-self.rot)
            cost = math.cos(-self.rot)
        elif self.app.mode_2d == 'CC':
            sint = math.sin(self.rot)
            cost = math.cos(self.rot)
        rotation_matrix = np.array([[cost, -sint],
                                    [sint, cost]], dtype=float)

        # create translation vector
        if self.app.mode_2d == 'TL':
            translation_vector = np.array([[self.posPx[0] + 0.5 * self.scale[0] * self.dimensionsPx[0]],
                                           [self.posPx[1] + 0.5 * self.scale[1] * self.dimensionsPx[1]]], dtype=float)
        elif self.app.mode_2d == 'CC':
            translation_vector = np.array([[self.posPx[0]],
                                           [self.posPx[1]]], dtype=float)

        # Compute corners from matrix mult
        for corner in corners:
            np.matmul(scaling_matrix, corner, out=corner)
            np.matmul(rotation_matrix, corner, out=corner)
            np.add(translation_vector, corner, out=corner)

        # Output corners as 1d arrays, flip top and bottom coords if using top-left mode (top has lower y coord)
        if self.app.mode_2d == 'TL':
            corners = [corners[2], corners[3], corners[0], corners[1]]
            return [corner.flatten() for corner in corners]
        elif self.app.mode_2d == 'CC':
            return [corner.flatten() for corner in corners]

    def get_bounds(self) -> list[
        list[Union[tuple, int], Union[tuple, int]], list[Union[tuple, int], Union[tuple, int]]]:
        x_bounds = [min(corner[0] for corner in self.bb_corners), max(corner[0] for corner in self.bb_corners)]
        y_bounds = [min(corner[1] for corner in self.bb_corners), max(corner[1] for corner in self.bb_corners)]
        return [x_bounds, y_bounds]

    def list_collision_boundaries(self) -> None:
        if self.strictBounding:
            self.app.mainloop.angled_boundaries.append(self)
        else:
            self.app.mainloop.rectangular_boundaries.append(self)

    def delist_collision_boundaries(self) -> None:
        if self in self.app.mainloop.angled_boundaries:
            self.app.mainloop.angled_boundaries.remove(self)
        if self in self.app.mainloop.rectangular_boundaries:
            self.app.mainloop.rectangular_boundaries.remove(self)

    def add_to_scene(self, scene_layer: int = None) -> None:
        if not self.isViewable:
            self.isViewable = True
            self.list_collision_boundaries()
            if not scene_layer:
                self.app.scene.add_object(self.model)
            else:
                self.app.scene.insert(scene_layer, self.model)
        else:
            logging.warning(
                f' failed to add {self.__class__.__name__} object \'{self.name}\' to scene: already viewable in scene')

    def remove_from_scene(self) -> None:
        if self.isViewable:
            self.isViewable = False
            self.delist_collision_boundaries()
            self.app.scene.remove_object(self.model)
        else:
            logging.warning(
                f' failed to remove {self.__class__.__name__} object \'{self.name}\' to scene: object not viewable in scene')

    def update(self) -> None:
        StaticImage.update(self)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()

    def updateTo(self, model) -> None:
        StaticImage.updateTo(self, model)
        self.bb_corners = self.get_corners()
        self.rectangular_bounds = self.get_bounds()
