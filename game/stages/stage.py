from __future__ import annotations
from game.stages.stage_funcs import StageFuncs
from game.stages.stage_key_funcs import StageKeyFuncs
import logging
from typing import Union, Optional


class Stage(StageFuncs, StageKeyFuncs):
    def __init__(self, name, mainloop, app,
                 static_images: list, sprites: list,
                 static_buttons: list, button_sprites: list,
                 stage_func: str = None,
                 kdfs: Optional[dict] = None,
                 khfs: Optional[dict] = None,
                 kufs: Optional[dict] = None):
        # Identifying data
        self.name = name
        self.mainloop = mainloop
        self.app = app

        # Set stage func
        if stage_func is None:
            self.stage_func = getattr(self, f'{self.name}', None)
            if self.stage_func is None:
                logging.critical(f' Failed to load stage function \'{self.name}\' for stage \'{self.name}\': StageFunc does not exist')
        else:
            self.stage_func = getattr(self, stage_func, None)
            if self.stage_func is None:
                logging.critical(f' Failed to load stage function \'{stage_func}\' for stage \'{self.name}\': StageFunc does not exist')

        # Turn key functions dict into callable funcs
        self.stage_button_func = getattr(self, f'{self.name}', None)
        if self.stage_func is None:
            logging.critical(f' Failed to load stage button function \'{self.name}\' for stage \'{self.name}\': StageButtonFunc does not exist')

        # Important stage objects
        self.static_images = static_images
        self.sprites = sprites
        self.static_buttons = static_buttons
        self.button_sprites = button_sprites

        self.assets = static_images + sprites + static_buttons + button_sprites

        # Set object stages to self
        for asset in self.assets:
            asset.stage = self

        # Internal state variables
        self.state = 0

        # Set key func dicts
        self.kdfs = kdfs
        self.khfs = khfs
        self.kufs = kufs

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

    def __copy__(self, name: str) -> Stage:
        new_stage = Stage(name=name,
                          mainloop=self.mainloop,
                          app=self.app,
                          static_images=self.static_images[:],
                          sprites=self.sprites[:],
                          static_buttons=self.static_buttons[:],
                          button_sprites=self.button_sprites[:],
                          stage_func=self.stage_func.__name__ if self.stage_func is not None else None,
                          # Returns name of function in dict if it is not None, blank string otherwise (to be converted to None in initialization)
                          # Will return None (default dict value) if the original dict is None
                          kdfs={key: self.kdfs[key].__name__ if self.kdfs[key] is not None else '' for key in
                                self.kdfs} if self.kdfs is not None else None,
                          khfs={key: self.khfs[key].__name__ if self.khfs[key] is not None else '' for key in
                                self.khfs} if self.khfs is not None else None,
                          kufs={key: self.kufs[key].__name__ if self.kufs[key] is not None else '' for key in
                                self.kufs} if self.kufs is not None else None,
                          )
        return new_stage

    def load(self) -> None:
        self.state = 0
        # Append game objects to mainloop game object list
        for asset in self.assets:
            asset.load()
        self.stage_func()
        # Load key funcs
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
        self.state = -1
        for asset in self.assets:
            asset.unload()
        self.stage_func()
        # Unload key funcs
        for asset_list in self.app.mainloop.key_down_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)
        for asset_list in self.app.mainloop.key_hold_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)
        for asset_list in self.app.mainloop.key_up_func_dict.values():
            if self in asset_list:
                asset_list.remove(self)

    def update(self, new_state: int) -> None:
        self.state = new_state
        self.stage_func()

    def make_copy_of(self, asset, new_name: str) -> None:
        asset_copy = asset.copy(new_name)
        self.assets.append(asset_copy)
        if asset.__class__.__name__ == 'StaticImage':
            self.static_images.append(asset_copy)
        if asset.__class__.__name__ == 'Sprite':
            self.sprites.append(asset_copy)
        if asset.__class__.__name__ == 'StaticButton':
            self.static_buttons.append(asset_copy)
        if asset.__class__.__name__ == 'ButtonSprite':
            self.button_sprites.append(asset_copy)

    def keys_down(self, keys):
        for key in keys:
            self.kdfs[key](keys)

    def keys_hold(self, keys, hold_times):
        for key in keys:
            self.khfs[key](keys, hold_times)

    def keys_up(self, keys):
        for key in keys:
            self.kufs[key](keys)
