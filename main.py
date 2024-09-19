import logging
import time
import multiprocessing as mp
import pygame as pg
import sys
from settings import Settings
from engine import *
from game import *


def main(win_size, fps):
    app = create_app(win_size, fps)
    mainloop = MainLoop(app, fps)

    mainloop.run = True
    mainloop.execute()


if __name__ == "__main__":
    # Start loading timer
    startTime = time.perf_counter()

    # Logging setup
    logging.basicConfig(level=logging.WARNING)
    logging.info(f" Running \'main.py\' as \'main\'")

    # Import file settings and initialize pygame
    settings_data = Settings('settings.txt')
    screensize = settings_data.widthSetting, settings_data.heightSetting
    FPS = settings_data.fpsSetting

    # Run game
    logging.info(f" Finished initialization in: {time.perf_counter() - startTime} seconds")

    main(screensize, FPS)

    logging.info(f" Program finished in: {time.perf_counter() - startTime} seconds")