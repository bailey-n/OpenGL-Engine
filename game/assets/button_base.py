from dataclasses import dataclass, field
from typing import Callable, Union, Optional
from game.assets.button_funcs import ButtonFuncs
import logging


@dataclass
class ButtonBase(ButtonFuncs):
    # click activate function lists
    cafs: Optional[dict] = None
    cdfs: Optional[dict] = None
    chfs: Optional[dict] = None

    # hover activate function, hover deactivate function, hover-hold function
    haf: Optional[str] = None
    hdf: Optional[str] = None
    hhf: Optional[str] = None

    # Bools for state tracking
    strictBounding: bool = True
    isClicked: list[bool, ...] = field(init=False, default_factory=list)
    isHovered: bool = field(init=False, default=False)

    # Other state tacking vars
    click_times: dict = field(init=False, default=dict)
    hover_time: Union[int, float] = field(init=False, default=0)

    def __post_init__(self):
        logging.info(f' Generating ButtonBase data for {self.__class__.__name__} object')
        # Create default args
        self.isClicked = [False, False, False, False, False]
        self.click_times = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

        # Turn function strings into callable funcs
        # CLICK DICTS
        if self.cafs is not None:
            for button in self.cafs:
                func = getattr(self, self.cafs[button], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set click activate function to \'{self.cafs[button]}\', but \'{self.cafs[button]}\' does not exist '
                                    f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.cafs[button] = func
                
        if self.cdfs is not None:
            for button in self.cdfs:
                func = getattr(self, self.cdfs[button], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set click deactivate function to \'{self.cdfs[button]}\', but \'{self.cdfs[button]}\' does not exist '
                                    f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.cdfs[button] = func
                
        if self.chfs is not None:
            for button in self.chfs:
                func = getattr(self, self.chfs[button], None)
                if func is None:
                    logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                    f'attempted to set click-hold function to \'{self.chfs[button]}\', but \'{self.chfs[button]}\' does not exist '
                                    f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                    f'Setting to \'None\' instead')
                self.chfs[button] = func
            
        # HOVER
        if self.haf is not None:
            func = getattr(self, self.haf, None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set hover activate function to \'{self.haf}\', but \'{self.haf}\' does not exist '
                                f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.haf = func

        if self.hdf is not None:
            func = getattr(self, self.hdf, None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set hover deactivate function to \'{self.hdf}\', but \'{self.hdf}\' does not exist '
                                f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.hdf = func

        if self.hhf is not None:
            func = getattr(self, self.hhf, None)
            if func is None:
                logging.warning(f' {self.__class__.__name__} object \'{self.__repr__}\' '
                                f'attempted to set hover-hold function to \'{self.hhf}\', but \'{self.hhf}\' does not exist '
                                f'as any button funcs, button base, or {self.__class__.__name__} class or parent class method. '
                                f'Setting to \'None\' instead')
            self.hhf = func

    def hover_activate(self) -> None:
        self.isHovered = True
        if self.haf is not None: self.haf()

    def hover_hold(self, delta_time: Union[float, int]) -> None:
        self.hover_time += delta_time
        if self.hhf is not None: self.hhf()

    def hover_deactivate(self) -> None:
        self.isHovered = False
        if self.hdf is not None: self.hdf()
        self.hover_time = 0

    def click_activate(self, buttons: list[int, ...]) -> None:
        for button in buttons:
            self.isClicked[button] = True
            if self.cafs is not None and button in self.cafs and self.cafs[button] is not None:
                self.cafs[button]()

    def click_hold(self, buttons: list[int, ...], delta_time: Union[float, int]) -> None:
        for button in buttons:
            self.click_times[button] += delta_time
            if self.chfs is not None and button in self.chfs and self.chfs[button] is not None:
                self.chfs[button]()

    def click_deactivate(self, buttons: list[int, ...]) -> None:
        for button in buttons:
            self.isClicked[button] = False
            if self.cdfs is not None and button in self.cdfs and self.cdfs[button] is not None:
                self.cdfs[button]()
            self.click_times[button] = 0
