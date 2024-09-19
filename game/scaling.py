

class ScalingFuncs:
    @staticmethod
    def scale_gui(app):
        base_xt_ratio = 16 / 9
        x, y = app.WIN_SIZE
        if x >= base_xt_ratio * y:
            # Widescreen monitors, prioritize fitting to screen's y scale
            base_scale = y
            if base_scale >= 2160:
                # 2160 +
                scale = 2
            elif base_scale >= 1440:
                # 1440, 1600
                scale = 4 / 3
            elif base_scale >= 1080:
                # 1080, 1200
                scale = 1
            elif base_scale >= 900:
                # 900, 1024, 1050
                scale = 5 / 6
            elif base_scale >= 768:
                # 768, 800
                scale = 2 / 3
            elif base_scale >= 720:
                # 720
                scale = 2 / 3
            else:
                # 400 -
                scale = 1 / 2
        else:
            # Square/non wide-screen monitors, prioritize fitting to screen's x scale
            base_scale = x
            if base_scale >= 3440:
                # 3440, 3840 +
                scale = 2
            elif base_scale >= 2560:
                # 2560
                scale = 4 / 3
            elif base_scale >= 1920:
                # 1920
                scale = 1
            elif base_scale >= 1600:
                # 1600, 1680
                scale = 5 / 6
            elif base_scale >= 1360:
                # 1360, 1366, 1440
                scale = 3 / 4
            elif base_scale >= 1280:
                # 1280
                scale = 2 / 3
            elif base_scale >= 960:
                # 960, 1024
                scale = 1 / 2
            else:
                # 600 -
                scale = 5 / 16
        return scale