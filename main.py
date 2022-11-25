#!/bin/env python3
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

import user_io
from user_io import KeyboardInput

import ui

from geom import Point2d
from player import Player


# I don't wish to check if cursor pos assignment is necessary in clickers
def clickCb(event):
    ui.Cursor.size = (14, 14)
    ui.Cursor.pos = event.pos
def unclickCb(event):
    ui.Cursor.size = (10, 10)
    ui.Cursor.pos = event.pos
def cursorCb(event):
    ui.Cursor.pos = event.pos

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
        self.background = (0, 0, 0)

        pg.mouse.set_visible(False)

        # TIMER_RESOLUTION == 0 for some reason
        # self.max_framerate = int(1 / pg.TIMER_RESOLUTION)
        self.max_framerate = 60
        self.player = Player()

    def deinit(self):
        pg.quit()

    def prelude(self):
        self.screen = pg.display.set_mode((0, 0), pg.RESIZABLE)
        self.player.posf = Point2d(
            self.screen.get_width() * 0.5,
            self.screen.get_height() * 0.5,
        )
        # last thing to do in prelude
        self.clock = pg.time.Clock()
        self.clock.tick()

    def mainLoop(self):
        self.prelude()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type in event_callbacks:
                    event_callbacks[event.type](event)

            # time change independent stuff

            self.player.linear_velocity = user_io.normalizedMovement()

            self.screen.fill(self.background)

            # time change dependent stuff
            self.clock.tick(self.max_framerate)
            dt = self.clock.get_time()

            self.player.move(dt)
            player_pos = self.player.pos()
            pg.draw.circle(
                self.screen,
                self.player.color,
                center = player_pos,
                radius = 20,
            )

            # drawing ui
            ui.drawUI(self.screen)

            pg.display.update()


if __name__ == "__main__":
    game = AstartesCertificate()
    game.mainLoop()
    game.deinit()
