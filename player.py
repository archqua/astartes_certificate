from geom import Point2d
import armory
import util
import pygame as pg

def prelude(): # should be called after display.set_mode()
    Player.loadImage("pic/ultramarine_default.png", scale=0.5)

ultramarine = (64, 0, 255)

class Player(pg.sprite.Sprite):
    image = None
    accel_time = 500
    max_velocity = 0.3

    def __init__(self, image=None, groups=tuple()):
        pg.sprite.Sprite.__init__(self, *groups)
        self.linear_velocity = Point2d(0.0, 0.0)
        self.posf = Point2d(0.0, 0.0)
        self.image = image or Player.image
        if self.image is not None:
            self.setImage(self.image)
        self.color = ultramarine
        self.weapon = None
        self.aiming_direction = Point2d(1.0, 0.0)

    def loadImage(path, scale = None):
        Player.image = util.loadImage(path, scale)

    def setImage(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.posf.ints()

    def pos(self):
        return self.posf.ints()

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
    def move(self, dt):
        self.posf += self.linear_velocity * dt
        self.rect.center = self.posf.ints()

    def update(self, dt, direction, cursor_pos):
        self.accelerate(dt, direction)
        self.move(dt)
        player_pos = self.posf.inted()
        aiming_direction = cursor_pos - player_pos
        n = aiming_direction.norm()
        if n > 1e-05:
            self.aiming_direction = aiming_direction / n
            self.weapon.update(
                dt,
                player_pos + self.aiming_direction * 32,
                player_pos + self.aiming_direction * 64,
            )

    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)

    def fire(self, cursor_pos):
        if self.weapon is not None:
            self.weapon.fire(cursor_pos)

