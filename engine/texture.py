import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}

    def generate_texture(self, name: str) -> None:
        self.textures[name] = self.get_texture(path=f'textures/{name}')

    def get_texture(self, path: str) -> None:
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # Mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # Anisotropic Filtering
        texture.anisotropy = 32.0

        return texture

    def destroy(self) -> None:
        [texture.release() for texture in self.textures.values()]
