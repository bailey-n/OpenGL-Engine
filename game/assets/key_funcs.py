import pygame as pg
import math


class KeyFuncs:
    def move(self, *key_args):
        keys = key_args[0]
        vec = [0.0, 0.0]
        if pg.K_a in keys:
            vec[0] -= 0.01
        if pg.K_d in keys:
            vec[0] += 0.01
        if pg.K_w in keys:
            vec[1] += 0.01
        if pg.K_s in keys:
            vec[1] -= 0.01
        if hasattr(self, 'moveByScr'):
            self.moveByScr(tuple(vec))

    def party(self, *key_args):
        keys = key_args[0]
        if pg.K_v in keys:
            if hasattr(self, 'switch_to_texture') and hasattr(self, 'textures') and hasattr(self, 'current_texture'):
                current_texture = self.current_texture
                current_texture += 1
                if current_texture == len(self.textures):
                    current_texture = 0
                self.switch_to_texture(current_texture)


