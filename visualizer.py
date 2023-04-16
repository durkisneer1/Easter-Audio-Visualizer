import time
import pygame as pg
from const import *
from particle import Particle


class Visualizer:
    def __init__(self):
        self.surf = pg.image.load("assets/pg_egg.png").convert_alpha()
        self.scaled_surf = pg.transform.scale_by(self.surf, 0.3)
        self.pos = pg.Vector2(WIN_CENTER)
        self.rect = self.scaled_surf.get_rect(center=self.pos)

        self.particles = pg.sprite.Group()
        self.spawn_time = time.time() + 0.01

    def update(self, scalar, dt):
        self.scaled_surf = pg.transform.scale_by(self.surf, scalar * 0.3)
        self.rect = self.scaled_surf.get_rect(center=WIN_CENTER)

        if time.time() > self.spawn_time and scalar > 1.25:
            Particle(self.particles, scalar * 100)
            self.spawn_time = time.time() + 0.01

        [p.update(dt) for p in self.particles]

    def clear(self):
        self.particles.empty()

    def resize(self):
        self.scaled_surf = pg.transform.scale_by(self.surf, 0.3)
        self.rect = self.scaled_surf.get_rect(center=WIN_CENTER)

    def draw(self, screen):
        particle_list = self.particles.sprites()
        particle_list.reverse()
        for p in particle_list:
            delta_pos = p.pos.distance_to(self.pos)
            p.draw(screen, delta_pos)

        screen.blit(self.scaled_surf, self.rect)
