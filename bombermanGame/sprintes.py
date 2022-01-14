import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 1.1, TILESIZE * 1.1))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.last_bomb = 0
        self.time = pg.time.get_ticks()

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_bomb > BOMB_RATE:
                    self.last_bomb = now
                    Bomb(self.game, self.pos.x, self.pos.y, self.pos)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_fire(self):
        hits = pg.sprite.spritecollide(self, self.game.fire, False)
        if hits:
            self.game.redScore += 1
            pg.time.wait(2000)
            pg.event.clear()
            self.time = pg.time.get_ticks()
            self.game.new()

    def update(self):
        self.get_keys()
        # self.collide_with_fire()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        if pg.time.get_ticks() - self.time > INVULNERABILITY:
            self.collide_with_fire()


class Player2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 1.1, TILESIZE * 1.1))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.last_bomb = 0
        self.time = pg.time.get_ticks()

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.vel.y = PLAYER_SPEED

        if keys[pg.K_SLASH]:
            now = pg.time.get_ticks()
            if now - self.last_bomb > BOMB_RATE:
                    self.last_bomb = now
                    Bomb(self.game, self.pos.x, self.pos.y, self.pos)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_fire(self):
        hits = pg.sprite.spritecollide(self, self.game.fire, False)
        if hits:
            self.game.blueScore += 1
            pg.time.wait(2000)
            pg.event.clear()
            self.time = pg.time.get_ticks()
            self.game.new()

    def update(self):
        self.get_keys()
        # self.collide_with_fire()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        if pg.time.get_ticks() - self.time > INVULNERABILITY:
            self.collide_with_fire()


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


class Bomb(pg.sprite.Sprite):
    def __init__(self, game, x, y, pos):
        self.groups = game.all_sprites, game.bombs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.bombPos = pos
        self.rect.x = self.bombPos.x
        self.rect.y = self.bombPos.y
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery

        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > BOMB_LIFETIME:
            self.kill()
            VFire(self.game, self.pos.x, self.pos.y)
            HFire(self.game, self.pos.x, self.pos.y)

    def explode(self):
        pass


class VFire(pg.sprite.Sprite):
    def __init__(self, game, posx, posy):
        self.groups = game.all_sprites, game.fire
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.HFire_img
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FIRE_LIFETIME:
            self.kill()


class HFire(pg.sprite.Sprite):
    def __init__(self, game, posx, posy):
        self.groups = game.all_sprites, game.fire
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.VFire_img
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FIRE_LIFETIME:
            self.kill()