import pygame as pg
from geom import Point2d

class Unit(pg.sprite.Sprite):
    def __init__(self, image, groups, size=15.0):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.size = size
        self.linear_velocity = Point2d(0.0, 0.0)
        self.posf = Point2d(0.0, 0.0)
        if self.image is not None:
            self.setImage(self.image)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.posf.ints()

    def pos(self):
        return self.posf.ints()

    def move(self, dt):
        self.posf += self.linear_velocity * dt
        self.rect.center = self.posf.ints()

    def drawCircle(self, surface):
        pg.draw.circle(
            surface, (255, 0, 0),
            center=self.posf.ints(), radius=int(self.size),
            width=2,
        )


class Healthy(Unit):
    def __init__(self, image, groups, size=15.0, max_health=1):
        Unit.__init__(self, image, groups, size)
        self.max_health = max_health
        self.health = max_health

    def receiveDamage(self, damage=1):
        self.health -= damage

    def restoreHealth(self, amount=1):
        self.health += amount
        self.health = min(self.health, self.max_health)

    def mustDie(self):
        return self.health <= 0


# TODO class Armor similar to Weapon
class Armored(Healthy):
    def __init__(self, image, groups, size=15.0, max_health=1, max_armor=1):
        Healthy.__init__(self, image, groups, size, max_health)
        self.max_armor = max_armor
        self.armor = max_armor

    def receiveDamage(self, damage=1):
        if self.armor > 0:
            absorbed = min(self.armor, damage)
            self.armor -= absorbed
            damage -= absorbed
        Healthy.receiveDamage(self, damage)

    def restoreArmor(self, amount=1):
        self.armor += amount
        self.armor = min(self.armor, self.max_armor)


class Armed(Armored):
    def __init__(self, image, groups, size=15.0, max_health=1, max_armor=0, hold_dist = 10.0):
        Armored.__init__(self, image, groups, size, max_health, max_armor)
        self.weapon = None
        self.hold_dist = hold_dist
        self.hold_direction = Point2d(1.0, 0.0)
        self.aim_direction = Point2d(1.0, 0.0)

    def update(self, dt, holding_direction, aiming_direction):
        n = aiming_direction.norm()
        m = holding_direction.norm()
        if n > 1e-05:
            self.aim_direction = aiming_direction / n
        if m > 1e-05:
            self.hold_direction = holding_direction / m
        # posf = self.posf
        if self.weapon is not None:
            self.weapon.update(
                dt,
                (self.posf + self.hold_direction * self.hold_dist),
                (self.posf + self.aim_direction * 2 * self.hold_dist),
            )

    def fire(self, where):
        if self.weapon is not None:
            self.weapon.fire(where)

    def drawWeapon(self, surface):
        if self.weapon is not None:
            self.weapon.draw(surface)



