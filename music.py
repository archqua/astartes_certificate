import pygame as pg
import os
import random

playlist = []
rareness = 10
def loadPlaylist(path="./sound/music/", topdown=False):
    global playlist
    global rareness

    playlist = []
    raw_playlist = []
    for file in os.listdir(path):
        if "ogg" in file:
            raw_playlist.append(os.path.join(path, file))

    rare_playlist = []
    rare_path = os.path.join(path, "rare")
    for file in os.listdir(rare_path):
        if "ogg" in file:
            rare_playlist.append(os.path.join(rare_path, file))

    random.shuffle(raw_playlist)
    playlist.extend(raw_playlist)
    for _ in range(len(rare_playlist) * max(1, rareness // len(raw_playlist))):
        random.shuffle(raw_playlist)
        playlist.extend(raw_playlist)

    for rare_song in rare_playlist:
        i = random.randint(1, len(playlist)) - 1
        playlist.insert(i, rare_song)

song_finished = pg.event.custom_type()
next_song = 0
def start(volume=0.2):
    global song_finished

    pg.mixer.music.set_volume(volume)
    pg.mixer.music.set_endevent(song_finished)

    loadSong(0)
    queueNextSong()
    pg.mixer.music.play()

def stop():
    pg.mixer.music.stop()

def loadSong(idx):
    # should be called once
    global playlist
    global next_song
    next_song = (idx + 1) % len(playlist)
    pg.mixer.music.load(playlist[idx])

def queueNextSong():
    global next_song
    global playlist
    pg.mixer.music.queue(playlist[next_song])
    next_song += 1
    next_song %= len(playlist)


