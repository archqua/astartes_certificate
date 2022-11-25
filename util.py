import pygame as pg
def loadImage(path, scale = None):
    image = pg.image.load(path)
    if scale is not None:
        init_size = image.get_size()
        image = pg.transform.scale(
            image,
            (int(init_size[0] * scale), int(init_size[1] * scale)),
        )
    image.convert()
    return image
