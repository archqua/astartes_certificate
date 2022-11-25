from geom import Point2d
import armory

ultramarine = (64, 0, 255)

class Player:
    def __init__(self):
        self.linear_velocity = Point2d(0.0, 0.0)
        self.posf = Point2d(0.0, 0.0)
        self.color = ultramarine
        self.weapon = armory.Bolter()

    def pos(self):
        # return int(self.posf[0]), int(self.posf[1])
        return self.posf.ints()

    def move(self, dt, lin_vel_abs_value = 1.0):
        # posf = (
        #     self.posf[0] + dt * self.linear_velocity[0],
        #     self.posf[1] + dt * self.linear_velocity[1],
        # )
        # self.posf = posf
        self.posf += self.linear_velocity * lin_vel_abs_value * dt

