from __future__ import annotations
from game.assets import StaticImage
from game.assets.animation import Animation, Animations
from typing import Union, Optional
from dataclasses import dataclass, field
import math
import time


@dataclass
class Sprite(StaticImage, Animations):
    time: float = field(init=False, default_factory=time.process_time)
    isAnimated: bool = field(init=False, default=False)
    animations: list = field(init=False, default_factory=list)

    def __post_init__(self):
        super().__post_init__()

    def __copy__(self, name: str) -> Sprite:
        new_sprite = Sprite(app=self.app,
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
                            kdfs={key: self.kdfs[key].__name__ if self.kdfs[key] is not None else '' for key in
                                  self.kdfs} if self.kdfs is not None else None,
                            khfs={key: self.khfs[key].__name__ if self.khfs[key] is not None else '' for key in
                                  self.khfs} if self.khfs is not None else None,
                            kufs={key: self.kufs[key].__name__ if self.kufs[key] is not None else '' for key in
                                  self.kufs} if self.kufs is not None else None,
                            )
        return new_sprite

    def moveByScr(self, direction_vec: Union[tuple[float, float], tuple[int, int]]) -> None:
        self.pos = tuple(sum(components) for components in zip(self.pos, direction_vec))
        self.posPx = self.scr_to_px(self.pos)
        self.update()

    def moveByPx(self, direction_vec: Union[tuple[float, float], tuple[int, int]]) -> None:
        self.posPx = tuple(sum(components) for components in zip(self.posPx, direction_vec))
        self.pos = self.px_to_scr(self.posPx)
        self.update()

    def moveToScr(self, position_vec: Union[tuple[float, float], tuple[int, int]]) -> None:
        self.pos = position_vec
        self.posPX = self.scr_to_px(self.pos)
        self.update()

    def moveToPx(self, position_vec: Union[tuple[float, float], tuple[int, int]]) -> None:
        self.posPx = position_vec
        self.pos = self.px_to_scr(self.posPx)
        self.update()

    def rotateByDeg(self, degrees: Union[float, int]) -> None:
        rads = math.radians(degrees)
        self.rot += rads
        self.update()

    def rotateBy(self, radians: Union[float, int]) -> None:
        self.rot += radians
        self.update()

    def rotateToDeg(self, degrees: Union[float, int]) -> None:
        rads = math.radians(degrees)
        self.rot = rads
        self.update()

    def rotateTo(self, radians: Union[float, int]) -> None:
        self.rot = radians
        self.update()

    def animate(self) -> None:
        for animation in self.animations:
            animation.run_animation()

    def glide_to_scr(self, new_pos_scr: Union[tuple[float, float], tuple[int, int]], time: Union[float, int]) -> None:
        animation = Animation(self,
                              self.app.time,
                              time,
                              self.linear_interpolation,
                              init_pos=self.pos,
                              end_pos=new_pos_scr)
        self.animations.append(animation)
        self.isAnimated = True

    def glide_to_px(self, new_pos_px: Union[tuple[float, float], tuple[int, int]], time: Union[float, int]) -> None:
        new_pos_scr = self.px_to_scr(new_pos_px)
        animation = Animation(self,
                              self.app.time,
                              time,
                              self.linear_interpolation,
                              init_pos=self.pos,
                              end_pos=new_pos_scr)
        self.animations.append(animation)
        self.isAnimated = True
