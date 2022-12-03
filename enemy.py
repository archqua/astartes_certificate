import pygame as pg
import unit
import random
import util
from geom import Point2d

def prelude():
    OrcShooter.loadImages()

class Enemy(unit.Armed):
    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)
        self.drawWeapon(surface)

class OrcShooter(Enemy):
    images = []
    def __init__(self, image_n=None, groups=None):
        Enemy.__init__(self, image=OrcShooter.getHeadImage(image_n), groups=groups)

    def getHeadImage(img_num = None):
        return OrcShooter.images[img_num or random.randint(0, len(OrcShooter.images)-1)]

    def loadImages():
        for i in range(1, 5):
            OrcShooter.images.append(util.loadImage(f"pic/orc_face_{i}.png", scale=0.5))

    def update(self, dt, player_posf):
        self.move(dt)
        direction = (player_posf - self.posf)#.normalize()
        self.hold_direction = direction
        self.aim_direction = direction
        Enemy.update(self, dt, self.hold_direction, self.aim_direction)

    def spawn(pos, groups, image_n=None):
        assert type(groups) is tuple, "pass groups as tuple"
        orc = OrcShooter(image_n=image_n, groups=groups)
        orc.posf = Point2d(pos).floated()
        return orc

    # def draw(self, surface):
    #     Enemy.draw(self, surface)
    #     Enemy.drawWeapon(self, surface)



