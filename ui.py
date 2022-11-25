import pygame as pg

class Cursor:
    size = (10, 10)
    pos = (0, 0)
    color = (255, 255, 255)
    def defaultDrawer(surface):
        return pg.draw.circle(
            surface, Cursor.color,
            center = Cursor.pos, radius = Cursor.size[0] // 2,
        )
    drawer = defaultDrawer


def drawUI(surface):
    Cursor.drawer(surface)
