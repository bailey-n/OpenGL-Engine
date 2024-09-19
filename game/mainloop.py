from .scaling import ScalingFuncs
import pygame as pg
import random
import math
import time
from .assets import *
from .stages import *


class MainLoop:
    def __init__(self, app, compute_fps):
        pg.init()
        self.app = app
        self.app.mainloop = self
        self.FPS = compute_fps
        self.run = False

        self.gameClock = pg.time.Clock()

        self.game_objects = []
        self.stages = []
        self.rectangular_boundaries = []
        self.angled_boundaries = []
        # Creates dict of key indexes in pg.key.get_pressed with a corresponding array of functions which react to that key
        self.key_down_func_dict = {index: [] for index in range(len(pg.key.get_pressed()))}
        self.key_hold_func_dict = {index: [] for index in range(len(pg.key.get_pressed()))}
        self.key_up_func_dict = {index: [] for index in range(len(pg.key.get_pressed()))}
        self.key_hold_times = [0 for index in range(len(pg.key.get_pressed()))]

        self.mbs_down = [False, False, False, False, False]
        self.keys_down = []
        self.keys_pressed = []
        self.keys_up = []

        self.on_init()

    def on_init(self):
        '''width = 20
        height = 20
        SPACE = 2
        for x in range(width):
            for z in range(height):
                self.game_objects.append(CubeObj(app=self.app,
                                                 name=f'Cube_{(x*z) + z}',
                                                 texture_name='img.png',
                                                 pos=(SPACE*x, SPACE, -SPACE*z),
                                                 vbo_name='cube',
                                                 vao_name='cube',
                                                 ))'''
        static_images = []
        sprites = []
        static_buttons = []
        button_sprites = []
        static_images.append(StaticImage(app=self.app,
                                         name=f'test_image_0',
                                         textures=['test.png'],
                                         posPx=(0, 0),
                                         dimensionsPx=(200, 200),
                                         scale=(1 / 2, 1 / 2),
                                         rot=0))
        static_images.append(StaticImage(app=self.app,
                                         name=f'test_image_1',
                                         textures=['test.png'],
                                         posPx=(0, 700),
                                         dimensionsPx=(200, 200),
                                         scale=(1, 1),
                                         rot=0))
        static_images.append(StaticImage(app=self.app,
                                         name=f'test_image_2',
                                         textures=['test.png'],
                                         posPx=(1500, 0),
                                         dimensionsPx=(200, 200),
                                         scale=(3 / 2, 3 / 2),
                                         rot=0))
        static_images.append(StaticImage(app=self.app,
                                         name=f'test_image_3',
                                         textures=['test.png'],
                                         posPx=(1400, 500),
                                         dimensionsPx=(200, 200),
                                         scale=(2, 2),
                                         rot=0))

        static_images.append(StaticImage(app=self.app,
                                         name=f'test_image_4',
                                         textures=['test.png'],
                                         pos=(0.95, -0.95),
                                         dimensionsPx=(200, 200),
                                         scale=(1, 1),
                                         rot=0))
        sprites.append(Sprite(app=self.app,
                              name='test_image',
                              textures=['stretch.png', 'img.png', 'img_2.png'],
                              pos=(-0.5, -0.5),
                              dimensionsPx=(200, 200),
                              scale=(1, 2),
                              rot=0,
                              khfs={pg.K_a: 'move', pg.K_d: 'move', pg.K_s: 'move', pg.K_w: 'move'},
                              kufs={pg.K_v: 'party'}
                              ))
        button_sprites.append(ButtonSprite(app=self.app,
                                           name='test_button',
                                           textures=['test.png', 'img.png', 'img_1.png', 'img_2.png'],
                                           posPx=(200, 200),
                                           dimensionsPx=(150, 300),
                                           scale=(2, 1 / 2),
                                           rot=math.radians(15),
                                           haf='switch_to_secondary_texture',
                                           hhf='rotate',
                                           hdf='switch_to_default_texture',
                                           cafs={0: 'switch_to_tertiary_texture', 2: 'switch_to_quaternary_texture'},
                                           cdfs={0: 'switch_to_secondary_texture',
                                                 2: 'switch_to_secondary_texture'}))
        test_stage = Stage(name='test_stage',
                           mainloop=self,
                           app=self.app,
                           static_images=static_images,
                           sprites=sprites,
                           static_buttons=static_buttons,
                           button_sprites=button_sprites,
                           stage_func='test_scene',
                           kdfs={pg.K_ESCAPE: 'quit'}
                           )
        self.stages.append(test_stage)
        self.stages[0].load()

    def check_game_updates(self) -> None:
        self.keys_down=[]
        self.keys_up=[]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app.close()
            if event.type == pg.KEYDOWN:
                self.keys_down.append(event.key)
            if event.type == pg.KEYUP:
                self.keys_up.append(event.key)
            if event.type == pg.MOUSEWHEEL:
                self.app.scrolling = event.y

        # Handle camera movement
        keys = pg.key.get_pressed()
        self.app.camera.move(keys)

    def handle_key_inputs(self) -> None:
        # Takes newly released keys and runs key up funcs
        if any(self.keys_up):
            asset_up_set = []
            for key in self.keys_up:
                self.keys_pressed.remove(key)
                self.key_hold_times[key] = 0
                for asset in self.key_up_func_dict[key]:
                   if asset not in asset_up_set: asset_up_set.append(asset)
            for asset in asset_up_set:
                asset.keys_up(self.keys_up)

        # Handles persistent keys
        if any(self.keys_pressed):
            asset_hold_set = []
            for key in self.keys_pressed:
                if key not in self.keys_down:
                    self.key_hold_times[key] += self.app.delta_time
                    for asset in self.key_hold_func_dict[key]:
                        if asset not in asset_hold_set: asset_hold_set.append(asset)
            for asset in asset_hold_set:
                asset.keys_hold(self.keys_pressed, self.key_hold_times)

        # Take newly pressed keys and runs key down funcs
        if any(self.keys_down):
            asset_down_set = []
            for key in self.keys_down:
                self.keys_pressed.append(key)
                for asset in self.key_down_func_dict[key]:
                    if asset not in asset_down_set: asset_down_set.append(asset)
            for asset in asset_down_set:
                asset.keys_down(self.keys_down)

    def check_asset_updates(self) -> None:
        for object in self.game_objects:
            if hasattr(object, 'isAnimated') and object.isViewable:
                if object.isAnimated:
                    object.animate()

    def do_collisions(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        clicks = pg.mouse.get_pressed(num_buttons=5)

        for interactive_object in self.rectangular_boundaries:
            x_bounds, y_bounds = interactive_object.rectangular_bounds
            if (x_bounds[0] <= mouse_pos[0] <= x_bounds[1] and
                    y_bounds[0] <= mouse_pos[1] <= y_bounds[1]):
                self.handle_hovering(clicks, interactive_object)
            elif interactive_object.isHovered:
                # Run hover deactivate function if leaving hover
                interactive_object.hover_deactivate()

        for interactive_object in self.angled_boundaries:
            corners = interactive_object.bb_corners
            if self.collision_is_detected(corners, mouse_pos):
                self.handle_hovering(clicks, interactive_object)
            elif interactive_object.isHovered:
                # Run hover deactivate function if leaving hover
                interactive_object.hover_deactivate()

        # Record mouse states for next frame
        self.mbs_down = clicks

    def handle_hovering(self, clicks: tuple[bool, bool, bool, bool, bool], interactive_object) -> None:
        # Run hover hold if continued hovering, hover activate if start of hover
        if interactive_object.isHovered:
            interactive_object.hover_hold(self.app.delta_time)
        else:
            interactive_object.hover_activate()

        if any(clicks):
            # Sets activated buttons to buttons which were not active last frame but active this frame, then runs funcs
            activated_buttons = [index for index, key_pair in enumerate(zip(self.mbs_down, clicks)) if
                                 key_pair[1] and not key_pair[0]]
            if activated_buttons: interactive_object.click_activate(activated_buttons)

            # Sets held buttons to buttons which were active both last frame and this frame for buttons already clicked, then runs funcs
            held_buttons = [index for index, key_trio in
                            enumerate(zip(self.mbs_down, clicks, interactive_object.isClicked)) if all(key_trio)]
            if held_buttons: interactive_object.click_hold(held_buttons, self.app.delta_time)

        if any(self.mbs_down):
            # Sets deactivated keys to buttons which were activate last frame but not this frame, then runs funcs
            deactivated_buttons = [index for index, key_pair in enumerate(zip(self.mbs_down, clicks)) if
                                   key_pair[0] and not key_pair[1]]
            if deactivated_buttons: interactive_object.click_deactivate(deactivated_buttons)

    def collision_is_detected(self, corners, mouse_pos):
        x, y = mouse_pos
        x0, y0 = corners[0]
        x1, y1 = corners[1]
        x2, y2 = corners[2]
        x3, y3 = corners[3]

        # Computes twice the area of the two triangles which constitute the rectangle
        t1A = self.compute_area(x1 - x0, y1 - y0,
                                x2 - x0, y2 - y0)
        t2A = self.compute_area(x2 - x1, y2 - y1,
                                x3 - x1, y3 - y1)

        # Calculates the difference between all corner positions and mouse position
        dx0 = x0 - x
        dy0 = y0 - y
        dx1 = x1 - x
        dy1 = y1 - y
        dx2 = x2 - x
        dy2 = y2 - y
        dx3 = x3 - x
        dy3 = y3 - y

        # Computes mutually overlapping area, adds non-overlapping area to form mouse-triangle areas
        shared_area = self.compute_area(dx1, dy1, dx2, dy2)

        m1A = shared_area + self.compute_area(dx0, dy0, dx1, dy1) + self.compute_area(dx2, dy2, dx0, dy0)
        m2A = shared_area + self.compute_area(dx3, dy3, dx1, dy1) + self.compute_area(dx2, dy2, dx3, dy3)

        return (True if round(m1A, 8) == round(t1A, 8) or round(m2A, 8) == round(t2A, 8) else False)

    @staticmethod
    def compute_area(x1, y1, x2, y2):
        # Returns |x1y2 - x2y1|; det(v1, v2)
        return abs(x1 * y2 - x2 * y1)

    def get_time(self) -> None:
        self.time = pg.time.get_ticks() * 0.001

    def execute(self) -> None:
        while self.run:
            self.check_game_updates()
            self.handle_key_inputs()
            self.check_asset_updates()
            self.do_collisions()
            self.app.render_frame()
            self.gameClock.tick()
