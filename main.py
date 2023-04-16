import pygame as pg
from const import *
from support import remap
from visualizer import Visualizer
from music_player import MusicPlayer

pg.mixer.pre_init(frequency=SAMPLE_RATE)
pg.init()

screen = pg.display.set_mode(WIN_SIZE)
pg.display.set_icon(pg.image.load("assets/pg_egg.png"))
pg.display.set_caption("Easter Music Visualizer")
clock = pg.time.Clock()

visual = Visualizer()
bg_index = 0
bg_img = pg.transform.scale(
    pg.image.load(f"assets/{bg_index}.png").convert(),
    WIN_SIZE,
)
tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
tint.fill((0, 0, 0, 135))


def main():
    global bg_index, bg_img
    cd_player = None
    run = True
    while run:
        events = pg.event.get()
        for ev in events:
            if ev.type == pg.QUIT or (ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE):
                run = False
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_r:
                    bg_index = (bg_index + 1) % 5
                    bg_img = pg.transform.scale(
                        pg.image.load(f"assets/{bg_index}.png").convert(), WIN_SIZE
                    )

                if cd_player is not None:
                    if ev.key == pg.K_SPACE:
                        cd_player.play()
                    elif ev.key == pg.K_q:
                        cd_player.pause()
                        visual.clear()
                        visual.resize()

            elif ev.type == pg.DROPFILE:
                try:
                    cd_player = MusicPlayer(pg.mixer.Sound(ev.file))
                except pg.error:
                    print("Invalid file")

        screen.blit(bg_img, (0, 0))
        if cd_player is not None:
            cd_player.tick()
            raw_amp = cd_player.get_amp_level() / 1000 if cd_player.busy() else 1
            remapped_amp = remap(0, 5, 1, 2.5, raw_amp)
            dt = clock.tick() / (1000 / remapped_amp)

            if cd_player.busy():
                visual.update(remapped_amp, dt)

                scaled_bg_img = pg.transform.scale_by(
                    bg_img, remap(0, 5, 1, 1.1, raw_amp)
                )
                bg_rect = scaled_bg_img.get_rect(center=WIN_CENTER)
                screen.blit(scaled_bg_img, bg_rect)
        else:
            clock.tick()

        screen.blit(tint, (0, 0))
        visual.draw(screen)

        pg.display.flip()


if __name__ == "__main__":
    main()
