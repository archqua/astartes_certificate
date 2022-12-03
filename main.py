#!/bin/env python3
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
pg.init() # pygame is anyway inited in modules, so no point to postpone

import random

import user_io
from user_io import KeyboardInput, MouseInput
import ui
from geom import Point2d
import player
from player import Player
import armory
import enemy
from enemy import OrcShooter


# I don't wish to check if cursor pos assignment is necessary in clickers
def clickCb(event):
    ui.Cursor.size = (14, 14)
    ui.Cursor.pos = event.pos
    # TODO discriminate between buttons
    MouseInput.lmb_pressed = True
def unclickCb(event):
    ui.Cursor.size = (10, 10)
    ui.Cursor.pos = event.pos
    # TODO discriminate between buttons
    MouseInput.lmb_pressed = False
def cursorCb(event):
    ui.Cursor.pos = event.pos
    user_io.MouseInput.cursor_pos = Point2d(*event.pos)

def keyCb(event):
    down_callbacks = keeb_callbacks[key_down_key]
    if event.key in down_callbacks:
        down_callbacks[event.key]()
def unkeyCb(event):
    up_callbacks = keeb_callbacks[key_up_key]
    if event.key in up_callbacks:
        up_callbacks[event.key]()


event_callbacks = {
    pg.MOUSEBUTTONDOWN: clickCb,
    pg.MOUSEBUTTONUP:   unclickCb,
    pg.MOUSEMOTION:     cursorCb,
    pg.KEYDOWN:         keyCb,
    pg.KEYUP:           unkeyCb,
}
key_down_key = 0
key_up_key = 1
keeb_callbacks = (
    {
        pg.K_s: KeyboardInput.fwdCb,
        pg.K_a: KeyboardInput.leftCb,
        pg.K_w: KeyboardInput.bwdCb,
        pg.K_d: KeyboardInput.rightCb,
        pg.K_UP:    KeyboardInput.bwdCb,
        pg.K_LEFT:  KeyboardInput.leftCb,
        pg.K_DOWN:  KeyboardInput.fwdCb,
        pg.K_RIGHT: KeyboardInput.rightCb,
    },
    {
        pg.K_s: KeyboardInput.unfwdCb,
        pg.K_a: KeyboardInput.unleftCb,
        pg.K_w: KeyboardInput.unbwdCb,
        pg.K_d: KeyboardInput.unrightCb,
        pg.K_UP:    KeyboardInput.unbwdCb,
        pg.K_LEFT:  KeyboardInput.unleftCb,
        pg.K_DOWN:  KeyboardInput.unfwdCb,
        pg.K_RIGHT: KeyboardInput.unrightCb,
    },
)


class AstartesCertificate:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.NOFRAME)
        self.background = (0, 96, 0)

        # modules need to finish initialization after pg.display.set_mode()
        player.prelude()
        enemy.prelude()
        armory.prelude()

        self.player = Player()
        # self.player.setImage(Player.image)

        screen_width, screen_height = self.screen.get_size()
        xspawnspace = screen_width - 200
        yspawnspace = screen_height - 200
        self.enemy_spawn_positions = [
            Point2d(100.0,                       100.0),
            Point2d(100.0 + xspawnspace / 3,     100.0),
            Point2d(100.0 + xspawnspace * 2 / 3, 100.0),
            Point2d(100.0 + xspawnspace,         100.0),
            Point2d(100.0 + xspawnspace,         100.0 + yspawnspace / 2),
            Point2d(100.0 + xspawnspace,         100.0 + yspawnspace),
            Point2d(100.0 + xspawnspace * 2 / 3, 100.0 + yspawnspace),
            Point2d(100.0 + xspawnspace / 3,     100.0 + yspawnspace),
            Point2d(100.0,                       100.0 + yspawnspace),
            Point2d(100.0,                       100.0 + yspawnspace / 2)
        ]
        # TIMER_RESOLUTION == 0 for some reason
        # self.max_framerate = int(1 / pg.TIMER_RESOLUTION)
        self.max_framerate = 63
        # 1000 / 60 == 16.67, 1000 / 63 = 15.87

        self.ready = False

    def deinit(self):
        pg.quit()

    def prelude(self): # is called at the beginning of mainLoop()
        pg.mouse.set_visible(False)

        self.player.posf = Point2d(
            self.screen.get_width() * 0.5,
            self.screen.get_height() * 0.5,
        )

        # create empty groups
        self.projectiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        # arm units
        armory.arm(self.player, armory.Bolter, groups=(self.projectiles,))

        self.time_before_enemy_spawn = 2120
        self.time_before_enemy_spawn_remain = 2120
        self.min_time_before_enemy_spawn = 800
        self.enemy_spawn_period_dec = 120
        self.kills_before_spawn_mode_update = 1
        self.kills_before_spawn_mode_update_remain = 1
        self.kills_before_spawn_mode_inc = 5

        # last thing to do in prelude
        self.clock = pg.time.Clock()
        self.clock.tick()

        self.ready = True

    def mainLoop(self, skip_prelude = False):
        if not skip_prelude:
            self.prelude()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type in event_callbacks:
                    event_callbacks[event.type](event)

            # time change independent stuff

            accel_direction = user_io.normalizedMovement()
            # self.player.linear_velocity = user_io.normalizedMovement()

            self.screen.fill(self.background)

            # time change dependent stuff
            self.clock.tick(self.max_framerate)
            dt = self.clock.get_time()

            self.projectiles.update(dt)
            
            screen_width, screen_height = self.screen.get_size()
            for projectile in self.projectiles:
                # TODO change to projectile.rect.center checks
                # TODO get actual window dimensions???
                if projectile.posf.x > screen_width + 100 or projectile.posf.x < -100:
                    projectile.kill()
                if projectile.posf.y > screen_height + 100 or projectile.posf.y < -100:
                    projectile.kill()
                for enemy in self.enemies.sprites():
                    if enemy.posf.distToSegment(projectile.posf, projectile.prev_posf) < enemy.size:
                        enemy.receiveDamage()
                        if enemy.mustDie():
                            enemy.kill()
                            self.kills_before_spawn_mode_update_remain -= 1
                            if self.kills_before_spawn_mode_update_remain <= 0:
                                self.time_before_enemy_spawn -= self.enemy_spawn_period_dec
                                self.time_before_enemy_spawn = max(
                                        self.time_before_enemy_spawn,
                                        self.min_time_before_enemy_spawn
                                    )
                                self.kills_before_spawn_mode_update += self.kills_before_spawn_mode_inc
                                self.kills_before_spawn_mode_inc += 1
                                self.kills_before_spawn_mode_update_remain = self.kills_before_spawn_mode_update
                                print("now enemies spawn each", self.time_before_enemy_spawn, "ms")
                            # self.time_before_enemy_spawn = 2000
                            # self.time_before_enemy_spawn_remain = 2000
                            # self.min_time_before_enemy_spawn = 800
                            # self.enemy_spawn_period_dec = 120
                            # self.kills_before_spawn_mode_update = 1
                            # self.kills_before_spawn_mode_update_remain = 1
                if self.player.posf.distToSegment(projectile.posf, projectile.prev_posf) < self.player.size:
                    self.player.receiveDamage()
                    if self.player.health == 1:
                        self.background = (32, 64, 0)

            if not self.player.mustDie():
                if self.player.posf.x < 0:
                    self.player.posf.x *= -1
                    self.player.linear_velocity.x *= -1
                    accel_direction.x *= -1
                elif self.player.posf.x > screen_width:
                    self.player.posf.x = 2*screen_width - self.player.posf.x
                    self.player.linear_velocity.x *= -1
                    accel_direction.x *= -1
                if self.player.posf.y < 0:
                    self.player.posf.y *= -1
                    self.player.linear_velocity.y *= -1
                    accel_direction.y *= -1
                elif self.player.posf.y > screen_height:
                    self.player.posf.y = 2*screen_height - self.player.posf.y
                    self.player.linear_velocity.y *= -1
                    accel_direction.y *= -1
                self.player.update(dt, accel_direction, user_io.MouseInput.cursor_pos)
                if user_io.MouseInput.lmb_pressed:
                    self.player.fire(user_io.MouseInput.cursor_pos)

            self.time_before_enemy_spawn_remain -= dt
            if self.time_before_enemy_spawn_remain <= 0:
                self.spawnOrcShooter()
                self.time_before_enemy_spawn_remain = self.time_before_enemy_spawn
            for enemy in self.enemies.sprites():
                enemy.update(dt, self.player.posf)
                enemy.fire(self.player.posf)

            # drawing
            ui.Player.update(self.player)
            ui.drawBack(self.screen)

            self.projectiles.draw(self.screen)
            # self.enemies.draw(self.screen)
            for enemy in self.enemies.sprites():
                enemy.draw(self.screen)
                enemy.drawCircle(self.screen)
            if not self.player.mustDie():
                self.player.draw(self.screen)
                self.player.drawCircle(self.screen)
            # print(self.enemies)
            # TODO
            # for sprite in self.projectiles.sprites():
            #     sprite.draw(self.screen)

            ui.drawFront(self.screen)

            pg.display.update()

    def spawnOrcShooter(self, pos=None):
        if pos is None:
            pos = self.enemy_spawn_positions[
                random.randint(0, len(self.enemy_spawn_positions) - 1)
            ]
            xoffset = (random.random() - 0.5) * 100 # +- 50
            yoffset = (random.random() - 0.5) * 100 # +- 50
            pos.x += xoffset
            pos.y += yoffset
        orc = OrcShooter.spawn(pos.ints(), groups=(self.enemies,))
        armory.arm(orc, armory.Bolter, groups=(self.projectiles,), init_cooldown=500, cooldown=240)
        

if __name__ == "__main__":
    game = AstartesCertificate()
    game.mainLoop()
    game.deinit()
