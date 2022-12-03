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

class Player:
    health = 0
    armor = 0
    pos = (0, 0)

    armor_color = (192, 192, 255)
    armor_radii = [22, 25]
    def update(player):
        Player.health = player.health
        Player.armor = player.armor
        Player.pos = player.pos()

    def defaultDrawer(surface):
        for i in range(Player.armor):
            pg.draw.circle(
                surface, Player.armor_color,
                center=Player.pos, radius=Player.armor_radii[i],
                width=1,
            )
    drawer = defaultDrawer


def drawBack(surface):
    Player.drawer(surface)
def drawFront(surface):
    Cursor.drawer(surface)
    
# def drawUI(surface):
#     Player.drawer(surface)
#     Cursor.drawer(surface)

