#!/bin/env python3
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
pg.init() # pygame is anyway inited in modules, so no point to postpone

import user_io
from user_io import KeyboardInput, MouseInput
import ui
from geom import Point2d
import player
from player import Player
import armory


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
        pg.K_UP:    KeyboardInput.fwdCb,
        pg.K_LEFT:  KeyboardInput.leftCb,
        pg.K_DOWN:  KeyboardInput.bwdCb,
        pg.K_RIGHT: KeyboardInput.rightCb,
    },
    {
        pg.K_s: KeyboardInput.unfwdCb,
        pg.K_a: KeyboardInput.unleftCb,
        pg.K_w: KeyboardInput.unbwdCb,
        pg.K_d: KeyboardInput.unrightCb,
        pg.K_UP:    KeyboardInput.unfwdCb,
        pg.K_LEFT:  KeyboardInput.unleftCb,
        pg.K_DOWN:  KeyboardInput.unbwdCb,
        pg.K_RIGHT: KeyboardInput.unrightCb,
    },
)


class AstartesCertificate:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((0, 0), pg.RESIZABLE)
        self.background = (0, 128, 0)

        # modules need to finish initialization after pg.display.set_mode()
        player.prelude()

        self.player = Player()
        # self.player.setImage(Player.image)

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

        # arm units
        armory.arm(self.player, armory.Bolter, groups=(self.projectiles,))

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

            for projectile in self.projectiles:
                # TODO change to projectile.rect.center checks
                # TODO get actual window dimensions???
                if projectile.posf.x > 2000 or projectile.posf.x < -100:
                    projectile.kill()
                if projectile.posf.y > 1200 or projectile.posf.y < -100:
                    projectile.kill()

            self.player.update(dt, accel_direction, user_io.MouseInput.cursor_pos)
            if user_io.MouseInput.lmb_pressed:
                self.player.fire(user_io.MouseInput.cursor_pos)


            self.player.draw(self.screen)
            # TODO
            # self.projectiles.draw(self.screen)
            for sprite in self.projectiles.sprites():
                sprite.draw(self.screen)

            # drawing ui
            ui.drawUI(self.screen)

            pg.display.update()


if __name__ == "__main__":
    game = AstartesCertificate()
    game.mainLoop()
    game.deinit()
