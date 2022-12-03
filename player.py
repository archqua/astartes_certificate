from geom import Point2d
import unit
import armory
import util
import pygame as pg

def prelude(): # should be called after display.set_mode()
    Player.loadImage("pic/ultramarine_default.png", scale=0.5)

ultramarine = (64, 0, 255)

class Player(unit.Armed):
    image = None
    accel_time = 500
    max_velocity = 0.3

    def __init__(self, image=None, groups=tuple(), armor_restore_time=3000):
        unit.Armed.__init__(self, image = image or Player.image, groups = groups, max_health = 2, max_armor=2)
        self.armor_restore_time = armor_restore_time
        self.armor_restore_time_remain = armor_restore_time

    def loadImage(path, scale = None):
        Player.image = util.loadImage(path, scale)

    # movements are rather clumsy but it kinda gives spacemarine come weight
    def accelerate(self, dt, direction):
        # assume direction.norm == 1.0 or 0.0
        vel_abs_value = self.linear_velocity.norm()
        if vel_abs_value > 1e-05:
            vel_abs_value -= Player.max_velocity * dt / Player.accel_time
            vel_abs_value = max(vel_abs_value, 0.0)
            self.linear_velocity = self.linear_velocity.renormalize(vel_abs_value)
        if direction.norm() > 1e-05:
            vel_along_direction = direction.dot(self.linear_velocity)
            self.linear_velocity -= direction * vel_along_direction
            # 2.0 to compensate for previous decay
            vel_along_direction += 2.0 * Player.max_velocity * dt / Player.accel_time
            vel_along_direction = min(vel_along_direction, Player.max_velocity)
            self.linear_velocity += direction * vel_along_direction
        # else:
        #     self.linear_velocity = Point2d(0.0, 0.0)

    def update(self, dt, direction, cursor_pos):
        self.accelerate(dt, direction)
        self.move(dt)
        aiming_direction = cursor_pos - self.posf
        holding_direction = aiming_direction
        unit.Armed.update(self, dt, holding_direction, aiming_direction)
        if self.armor < self.max_armor:
            if self.armor_restore_time_remain < 0:
                self.restoreArmor()
                print("restoring armor", self.armor)
                self.armor_restore_time_remain = self.armor_restore_time
            else:
                self.armor_restore_time_remain -= dt

    def receiveDamage(self, damage=1):
        unit.Armed.receiveDamage(self, damage)
        self.armor_restore_time_remain = self.armor_restore_time

    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)
        self.drawWeapon(surface)

    # def fire(self, cursor_pos):
    #     if self.weapon is not None:
    #         self.weapon.fire(cursor_pos)

