from geom import Point2d
import armory
import util
import pygame as pg

ultramarine = (64, 0, 255)

class Player(pg.sprite.Sprite):
    image = None
    accel_time = 500
    max_velocity = 1.0

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.linear_velocity = Point2d(0.0, 0.0)
        self.posf = Point2d(0.0, 0.0)
        self.image = Player.image
        self.color = ultramarine
        self.weapon = armory.Bolter()

    def loadImage(path, scale = None):
        Player.image = util.loadImage(path, scale)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.posf.ints()

    def pos(self):
        return self.posf.ints()

    def accelerate(self, dt, direction):
        # assume direction.norm == 1.0 or 0.0
        if direction.norm() > 1e-05:
            vel_along_direction = direction.dot(self.linear_velocity)
            self.linear_velocity -= direction * vel_along_direction
            # 2.0 to compensate for previous decay
            vel_along_direction += 2.0 * Player.max_velocity * dt / Player.accel_time
            vel_along_direction = min(vel_along_direction, Player.max_velocity)
            self.linear_velocity += direction * vel_along_direction
        vel_abs_value = self.linear_velocity.norm()
        if vel_abs_value > 1e-05:
            vel_abs_value -= Player.max_velocity * dt / Player.accel_time
            vel_abs_value = max(vel_abs_value, 0.0)
            self.linear_velocity = self.linear_velocity.renormalize(vel_abs_value)
        # else:
        #     self.linear_velocity = Point2d(0.0, 0.0)

    def move(self, dt, lin_vel_abs_value = 1.0):
        self.posf += self.linear_velocity * lin_vel_abs_value * dt
        self.rect.center = self.posf.ints()

    def draw(self, surface):
        # return pg.draw.circle(
        #     surface,
        #     self.color,
        #     center = self.posf.ints(),
        #     radius = 20,
        # )
        if self.image is not None:
            surface.blit(self.image, self.rect)

