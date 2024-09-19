from engine.model import GUI


class Animation:
    def __init__(self, asset, start_time, animation_time, func, **kwargs):
        self.asset = asset
        self.start_time = start_time
        self.animation_time = animation_time
        self.end_time = start_time + animation_time
        self.func = func
        self.kwargs = kwargs
        self.time = 0

    def run_animation(self) -> None:
        self.time = (self.asset.app.time - self.start_time) / self.animation_time
        if not self.asset.app.time > self.end_time:
            self.func(self, self.time)
        else:
            self.func(self, 1)
            self.destroy()

    def destroy(self):
        self.asset.animations.remove(self)
        if len(self.asset.animations) == 0:
            self.asset.isAnimated = False


class Animations:
    @staticmethod
    def linear_interpolation(anim, time):
        # Extract required information
        asset = anim.asset
        kwargs_dict = anim.kwargs

        # Interpolate position
        init_pos = kwargs_dict['init_pos']
        end_pos = kwargs_dict['end_pos']
        new_pos = (time * (end_pos[0] - init_pos[0]) + init_pos[0],
                   time * (end_pos[1] - init_pos[1]) + init_pos[1])

        # Update display model
        new_model = GUI(app=asset.app,
                        vao_name=asset.vao_name,
                        texture_name=asset.texture_name,
                        pos=new_pos,
                        dimensions=asset.dimensionsPx,
                        scale=asset.scale,
                        rot=asset.rot)
        asset.updateTo(new_model)

        # End state func
        if time == 1:
            asset.pos = end_pos
            asset.posPx = asset.scr_to_px(end_pos)
