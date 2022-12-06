from geom import Point2d
import pygame as pg
import util

import math

def prelude():
    Bolter.loadImages()
    Bullet.loadImages()

def arm(unit, weapon_ctor, groups=tuple(), weapon_images=None, init_cooldown=0, **weapon_kwargs):
    assert type(groups) is tuple, "please, pass groups as tuple"
    if unit.weapon is not None:
        unit.weapon.kill()
    unit.weapon = weapon_ctor(images=weapon_images, groups=groups, **weapon_kwargs)
    unit.weapon.remain_cooldown = init_cooldown

class Weapon(pg.sprite.Sprite):
    def __init__(self, images=None, groups=tuple()):
        pg.sprite.Sprite.__init__(self, *groups)
        self.images = images

    def fire(self, dst):
        raise NotImplementedError("Abstract weapon can't fire")


class Bullet(pg.sprite.Sprite):
    # TODO sane Bullet class

    images = None
    def __init__(self, pos, vel, images=None, groups=tuple()):
        pg.sprite.Sprite.__init__(self, *groups)
        self.posf = pos.floated()
        self.prev_posf = pos.floated()
        self.vel = vel.floated()
        self.vel_norm = self.vel.norm()
        self.images = images or Bullet.images
        self.image = None
        if self.images is not None:
            self.setImages(self.images)
            self.updateImage()
            self.updateRect()
    
    def move(self, dt):
        self.prev_posf = self.posf
        self.posf += self.vel * dt
        self.rect.center = self.posf.ints()

    def update(self, dt):
        self.move(dt)

    def updateImage(self):
        if self.vel.dot(Point2d(1.0, 0.0)) > 0:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        angle = -Point2d(1.0, 0.0).angNormed(self.vel / self.vel_norm) if self.vel_norm > 1e-05 else 0.0
        self.image = pg.transform.rotate(self.image, math.degrees(angle) - 90)

    # def draw(self, surface):
    #     if self.image is not None:
    #         angle = -Point2d(1.0, 0.0).angNormed(self.vel / self.vel_norm) if self.vel_norm > 1e-05 else 0.0
    #         rotated = pg.transform.rotate(self.image, math.degrees(angle) - 90)
    #         surface.blit(rotated, self.rect)
    #         return surface.blit(self.image, self.rect)
    #     else:
    #         return pg.draw.circle(
    #             surface, (255, 255, 255),
    #             center = self.posf.ints(), radius = 10,
    #         )

    def updateRect(self):
        vertices = self.getImageVertices()
        xs = tuple(map(lambda v: v.x, vertices))
        ys = tuple(map(lambda v: v.y, vertices))
        left, right = int(min(*xs)), int(max(*xs))
        top, bottom = int(min(*ys)), int(max(*ys))
        self.rect = pg.Rect(left, top, right - left, bottom - top)

    def getImageVertices(self):
        # hwidth, hheight = self.image_width / 2, self.image_height / 2
        hheight, hwidth = self.image_width / 2, self.image_height / 2
        tl0 = Point2d(-hwidth, -hheight)
        tr0 = Point2d( hwidth, -hheight)
        br0 = Point2d( hwidth,  hheight)
        bl0 = Point2d(-hwidth,  hheight)
        points0 = (tl0, tr0, br0, bl0)
        cosine, sine = Point2d(1.0, 0.0).cos_sin_normed(self.vel / self.vel_norm)
        points = tuple(map(lambda v: v.rotateByCosSin(cosine, sine) + self.posf, points0))
        return points

    def setImages(self, images, image_n = 0):
        # rotation pivot is given as offset from center
        self.images = images
        self.image = self.images[image_n]
        self.image_width, self.image_height = self.image.get_width(), self.image.get_height()
        self.updateRect()

    def loadImages():
        Bullet.images = []
        Bullet.images.append(util.loadImage("pic/default_round.png", scale=0.17))
        Bullet.images.append(pg.transform.flip(Bullet.images[0], flip_x=True, flip_y=False))


class Bolter(Weapon):
    images = None
    def __init__(self, cooldown=160, images=None, groups=tuple()):
        Weapon.__init__(self, images)
        self.bullets_groups = groups
        self.images = images or Bolter.images
        self.point_to = Point2d(1.0, 0.0)
        self.pos = Point2d(0.0, 0.0)
        self.outlet_offsets = (Point2d(70, 1), Point2d(70, -1))
        self.outlet_offset = self.outlet_offsets[0]
        self.outlet = self.outlet_offset
        if self.images is not None:
            self.setImages(self.images)
        self.cooldown = cooldown
        self.remain_cooldown = 0

    def setImages(self, images, image_n = 0, pivots = [Point2d(-50.0, -12.0), Point2d(-50.0, 12.0)]):
        # rotation pivot is given as offset from center
        self.images = images
        self.image = self.images[image_n]
        self.image_width, self.image_height = self.image.get_width(), self.image.get_height()
        self.pivots = pivots
        self.pivot = self.pivots[0]
        self.updateRect()

    def updateRect(self):
        vertices = self.getImageVertices()
        xs = tuple(map(lambda v: v.x, vertices))
        ys = tuple(map(lambda v: v.y, vertices))
        left, right = int(min(*xs)), int(max(*xs))
        top, bottom = int(min(*ys)), int(max(*ys))
        self.rect = pg.Rect(left, top, right - left, bottom - top)

    def getImageVertices(self):
        hwidth, hheight = self.image_width / 2, self.image_height / 2
        tl0 = Point2d(-hwidth, -hheight) - self.pivot
        tr0 = Point2d( hwidth, -hheight) - self.pivot
        br0 = Point2d( hwidth,  hheight) - self.pivot
        bl0 = Point2d(-hwidth,  hheight) - self.pivot
        points0 = (tl0, tr0, br0, bl0)
        cosine, sine = Point2d(1.0, 0.0).cos_sin_normed(self.point_to)
        points = tuple(map(lambda v: v.rotateByCosSin(cosine, sine) + self.pos, points0))
        return points

    def update(self, dt, holding_pos, aiming_pos):
        if self.remain_cooldown > 0:
            self.remain_cooldown -= dt
        self.pos = holding_pos
        point_to = aiming_pos - holding_pos
        n = point_to.norm()
        if n > 1e-05:
            self.point_to = point_to / n
            # cosine, sine = Point2d(1.0, 0.0).cos_sin_normed(self.point_to)
            cosine, sine = self.point_to.cos_sin_normed(Point2d(1.0, 0.0))
            self.outlet = self.pos + self.outlet_offset.rotateByCosSin(cosine, -sine)
            # self.outlet = self.pos + self.point_to * 80
        if point_to.dot(Point2d(1.0, 0.0)) > 0:
            self.image = self.images[0]
            self.pivot = self.pivots[0]
            self.outlet_offset = self.outlet_offsets[0]
        else:
            self.image = self.images[1]
            self.pivot = self.pivots[1]
            self.outlet_offset = self.outlet_offsets[1]
        self.updateRect()

    def draw(self, surface):
        angle = -Point2d(1.0, 0.0).angNormed(self.point_to)
        rotated = pg.transform.rotate(self.image, math.degrees(angle))
        surface.blit(rotated, self.rect)
        # pg.draw.circle(
        #     surface, (255, 0, 0),
        #     center = self.outlet.ints(), radius = 2,
        # )

    def fire(self, where, bullet_vel = 3.0):
        if self.remain_cooldown <= 0:
            Bullet(self.outlet, self.point_to * bullet_vel, groups=self.bullets_groups)
            self.remain_cooldown = self.cooldown

    def loadImages():
        Bolter.images = []
        Bolter.images.append(util.loadImage("pic/boltgun.png", scale=0.75))
        Bolter.images.append(pg.transform.flip(Bolter.images[0], flip_x=False, flip_y=True))
