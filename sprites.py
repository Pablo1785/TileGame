import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.standing_frames_r[0]
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.current_frame = 0
        self.last_update = 0
        self.running = False

    def get_keys(self):
        self.vel = vec(0, 0)
        self.running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.running = True

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.running = True

        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.running = True

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.running = True

    def load_images(self):
        self.standing_frames_r = []
        for f in self.game.player_idle:
            self.standing_frames_r.append(pg.transform.scale(f, (PLAYER_SIZE, PLAYER_SIZE)))

        self.standing_frames_l = []
        for f in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(f, True, False))

        self.running_frames_r = []
        for f in self.game.player_run:
            self.running_frames_r.append(pg.transform.scale(f, (PLAYER_SIZE, PLAYER_SIZE)))

        self.running_frames_l = []
        for f in self.running_frames_r:
            self.running_frames_l.append(pg.transform.flip(f, True, False))

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel != vec(0, 0):
            self.running = True
        else:
            self.running = False

        # running animation:
        if self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.running_frames_r[self.current_frame]
                else:
                    self.image = self.running_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # idle animation:
        if not self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                bottom = self.rect.bottom
                self.image = self.standing_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom



    def wall_coll(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.wall_coll('x')
        self.rect.y = self.pos.y
        self.wall_coll('y')


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

    def update(self):
        pass




class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE