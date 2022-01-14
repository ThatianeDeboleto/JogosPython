import sys
from os import path
from sprites import *
import pygame as pg

# define cores (R, G, B)
from sprintes import Wall, Player1, Player2

WHITE = (242, 242, 242)
BLACK = (33, 33, 33)
DARK_GREY = (66, 66, 66)
LIGHT_GREY = (100, 100, 100)
GREEN = (165, 214, 167)
RED = (244, 67, 54)
YELLOW = (255, 255, 0)
BLUE = (33, 150, 243)
WALL = (158, 158, 158)
TEAL = (0, 188, 212)
PURPLE = (103, 58, 183)
LIGHT_BLUE = (144, 202, 249)
ORANGE = (255, 152, 0)

# game tela
WIDTH = 512   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 512  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 144
TITLE = "BomberMan"
BG_COLOR = DARK_GREY
FINAL_WIN = 3
INVULNERABILITY = 2000

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Configurações do player
PLAYER_SPEED = 250

# Configurações da bomba
BOMB_LIFETIME = 2500
BOMB_RATE = 1000

FIRE_LIFETIME = 1000
FIRE_RATE = 2000

FIRE_IMG = 'Fire.png'
HFIRE_IMG = 'HFire.png'
VFIRE_IMG = "VFire.png"

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.redScore = 0
        self.blueScore = 0
        self.blueWin = False
        self.redWin = False
        self.tie = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.score_font = path.join(img_folder, 'Basic-Regular.ttf')
        self.my_font = pg.font.SysFont("monospace", 10, True)
        self.HFire_img = pg.image.load(path.join(img_folder, HFIRE_IMG)).convert()
        self.VFire_img = pg.image.load(path.join(img_folder, VFIRE_IMG)).convert()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # inicialize todas as variáveis e faça toda a configuração para um novo jogo
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bombs = pg.sprite.Group()
        self.fire = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player1(self, col, row)
                if tile == 'E':
                    self.enemy = Player2(self, col, row)

    def run(self):
        # loop do jogo - defina self.playing = False para terminar o jogo
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # atualizar parte do loop do jogo
        self.all_sprites.update()

        if self.blueScore == FINAL_WIN:
            self.playing = False
            self.blueWin = True
        if self.redScore == FINAL_WIN:
            self.playing = False
            self.redWin = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.blueScore), self.score_font, 22, BLUE, (WIDTH / 2) - 16, 0, align="n")
        self.draw_text(str(self.redScore), self.score_font, 22, RED, (WIDTH / 2) + 16, 0, align="n")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        self.screen.fill(BG_COLOR)

        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

        self.draw_text("BOMBER MAN", self.score_font, 75, WHITE, WIDTH / 2, HEIGHT * 1/4, align="center")
        self.draw_text("PRESS ANY KEY", self.score_font, 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BG_COLOR)

        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

        self.draw_text(str(self.blueScore), self.score_font, 22, BLUE, (WIDTH / 2) - 16, 0, align="n")
        self.draw_text(str(self.redScore), self.score_font, 22, RED, (WIDTH / 2) + 16, 0, align="n")
        if self.blueWin:
            self.draw_text("BLUE WINS", self.score_font, 100, BLUE, WIDTH / 2, HEIGHT / 2, align="center")
            pg.display.flip()
        if self.redWin:
            self.draw_text("RED WINS", self.score_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")

        self.draw_text("press any key to replay", self.score_font, 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.clear()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.redScore = 0
                    self.blueScore = 0
                    return


g = Game()

g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()