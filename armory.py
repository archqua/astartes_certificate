from geom import Point2d
import pygame as pg

# def prelude():
#     Bolter.loadImage("")

def arm(unit, weapon_ctor, groups=tuple(), weapon_image=None):
    assert type(groups) is tuple, "please, pass groups as tuple"
    if unit.weapon is not None:
        unit.weapon.kill()
    unit.weapon = weapon_ctor(image=weapon_image, groups=groups)

class Weapon(pg.sprite.Sprite):
    def __init__(self, image=None, groups=tuple()):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = None

    def fire(self, dst):
        raise NotImplementedError("Abstract weapon can't fire")


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, vel, groups=tuple()):
        pg.sprite.Sprite.__init__(self, *groups)
        self.posf = pos.floated()
        self.vel = vel.floated()
    
    def move(self, dt):
        self.posf += self.vel * lin_vel_abs_value * dt

    def update(self, dt):
        self.posf += self.vel * dt

    def draw(self, surface):
        return pg.draw.circle(
            surface, (255, 255, 255),
            center = self.posf.ints(), radius = 10,
        )


class Bolter(Weapon):
    image = None
    def __init__(self, cooldown=160, image=None, groups=tuple()):
        Weapon.__init__(self, image)
        self.bullets_groups = groups
        self.image = image or Bolter.image
        self.point_to = None
        self.outlet = None
        self.cooldown = cooldown
        self.remain_cooldown = 0

    def update(self, dt, holding_pos, aiming_pos):
        if self.remain_cooldown > 0:
            self.remain_cooldown -= dt
        self.pos = holding_pos
        point_to = aiming_pos - holding_pos
        n = point_to.norm()
        if n > 1e-05:
            self.point_to = point_to / n
            self.outlet = self.pos + self.point_to * 10

    def draw(self, sufrace):
        pass

    def fire(self, where, bullet_vel = 4.0):
        if self.remain_cooldown <= 0:
            Bullet(self.outlet, (where - self.outlet).renormalize(bullet_vel), groups=self.bullets_groups)
            self.remain_cooldown = self.cooldown
