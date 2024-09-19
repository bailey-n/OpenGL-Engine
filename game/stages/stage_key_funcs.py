import pygame as pg


class StageKeyFuncs:
    def quit(self, *key_args):
        keys = key_args[0]
        if pg.K_ESCAPE in keys:
            if hasattr(self, 'app'):
                self.app.close()
