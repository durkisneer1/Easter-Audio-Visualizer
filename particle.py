import math
import random
import pygame as pg
from const import *


class Particle(pg.sprite.Sprite):
    pastel_colors = (
        (226, 174, 174),  # pastel red
        (217, 210, 233),  # pastel purple
        (248, 231, 199),  # pastel yellow
        (202, 236, 229),  # pastel green
        (253, 221, 230),  # pastel pink
        (223, 234, 231),  # pastel blue
        (255, 213, 173),  # pastel orange
        (249, 238, 221),  # pastel cream
        (211, 228, 207),  # pastel sage
        (236, 221, 255),  # pastel lavender
        (207, 242, 235),  # pastel turquoise
        (255, 239, 235),  # pastel peach
    )

    def __init__(self, group: pg.sprite.Group, speed):
        super().__init__(group)

        self.color_choice = random.choice(self.pastel_colors)
        self.pos = pg.Vector2(WIN_CENTER)

        self.speed = speed
        angle = random.randint(0, 360)
        self.direction = pg.Vector2(1, 0).rotate(angle)

        self.kill_offset = 30

    def update(self, dt):
        self.pos += dt * self.direction * self.speed

        if (
            self.pos.x < -self.kill_offset
            or self.pos.x > WIN_WIDTH + self.kill_offset
            or self.pos.y < -self.kill_offset
            or self.pos.y > WIN_HEIGHT + self.kill_offset
        ):
            self.kill()

    def draw(self, screen: pg.Surface, delta_pos: float):
        size_increase = 0.04 * delta_pos
        pg.draw.circle(screen, self.color_choice, self.pos, 4 + size_increase)
