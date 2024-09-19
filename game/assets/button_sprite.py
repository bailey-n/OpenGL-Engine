from __future__ import annotations
from typing import Union, Optional
from .static_button import StaticButton
from .sprite import Sprite
from dataclasses import dataclass, field
import numpy as np
import math


@dataclass
class ButtonSprite(Sprite, StaticButton):
    def __post_init__(self):
        StaticButton.__post_init__(self)

    def __copy__(self, name: str) -> ButtonSprite:
        new_button_sprite = ButtonSprite(app=self.app,
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
                                         cafs={
                                             button: self.cafs[button].__name__ if self.cafs[button] is not None else ''
                                             for button in self.cafs} if self.cafs is not None else None,
                                         cdfs={
                                             button: self.cafs[button].__name__ if self.cafs[button] is not None else ''
                                             for button in self.cafs} if self.cafs is not None else None,
                                         chfs={
                                             button: self.cafs[button].__name__ if self.cafs[button] is not None else ''
                                             for button in self.cafs} if self.cafs is not None else None,
                                         # Returns the name of the hover function if it is not None, otherwise will set to None (default value)
                                         haf=self.haf.__name__ if self.haf is not None else None,
                                         hdf=self.haf.__name__ if self.haf is not None else None,
                                         hhf=self.haf.__name__ if self.haf is not None else None,
                                         strictBounding=self.strictBounding
                                         )
        return new_button_sprite


