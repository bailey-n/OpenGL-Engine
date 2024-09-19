from .graphics import Graphics


def create_app(win_size, fps):
    app = Graphics(win_size=win_size,
                   FPS=fps)
    return app