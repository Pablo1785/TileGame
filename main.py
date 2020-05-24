# GRAPHICS BY: Robert AKA "0x72" on https://0x72.itch.io

import pygame as pg
import sys
from os import path
import random as r
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.running = True
        self.playing = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(250, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map3.txt'))

        self.player_idle = []
        for i in range(4):
            self.player_idle.append(
                pg.image.load(path.join(img_folder, "knight_f_idle_anim_f{}.png".format(i))).convert_alpha())

        self.player_run = []
        for i in range(4):
            self.player_run.append(
                pg.image.load(path.join(img_folder, "knight_f_run_anim_f{}.png".format(i))).convert_alpha())

        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

    def new_game(self):
        self.show_start_screen()

        # level setup
        self.setup()

        # gameplay
        self.game_loop()

        # end screen
        self.show_go_screen()

    def game_loop(self):
        self.playing = True

        while self.playing:
            # time passes
            self.dt = self.clock.tick(FPS) / 1000  # delta t will make movement independent of fps

            # user input
            self.events()

            # process input, collisions, move sprites etc
            self.update()

            # draw sprites, text and flip the display
            self.draw()

    def events(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BROWN)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()

    def setup(self):
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):  # row is index of list item, tiles is its value
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()

while g.running:
    g.new_game()
