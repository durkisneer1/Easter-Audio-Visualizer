import time
import numpy as np
import pygame as pg
from const import *


class MusicPlayer:
    def __init__(self, sound: pg.mixer.Sound):
        self.sound = sound
        self.snd_array = pg.sndarray.array(self.sound)
        self.length = self.snd_array.size
        self.size = len(self.snd_array)

        self.start_time = 0
        self.current_time = 0

        self.start_index = 0
        self.end_index = 0
        self.window_length = 0.1

    def play(self):
        self.sound.stop()
        self.sound.play()
        self.start_time = time.time()

    def pause(self):
        self.sound.stop()
        self.start_time = 0
        self.current_time = 0

    def busy(self):
        return pg.mixer.get_busy()

    def get_amp_level(self):
        start_index = max(
            0, int(SAMPLE_RATE * (self.current_time - self.window_length))
        )
        end_index = min(
            self.size,
            int(SAMPLE_RATE * (self.current_time + self.window_length)),
        )

        sliced_data = self.snd_array[start_index:end_index]
        rms = np.mean(np.abs(sliced_data))

        return rms

    def tick(self):
        self.current_time = time.time() - self.start_time
