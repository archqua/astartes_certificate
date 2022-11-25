from geom import Point2d


class Weapon:
    def __init__(self):
        self.launched_projectiles = []

    def fire(src, dst):
        raise NotImplementedError("Abstract weapon can't fire")


class Bullet:
    def __init__(pos, vel):
        self.posf = pos.floats()
        self.vel = vel.floats()
    
    def move(self, dt, lin_vel_abs_value = 2.0):
        self.posf += self.vel * lin_vel_abs_value * dt


class Bolter:
    def fire(src, dst, bullet_vel = 2.0):
        Bullet = Bolter.Bullet
        self.launched_projectiles.add(
            Bullet(src, (dst - src).renorm(bullet_vel))
        )
