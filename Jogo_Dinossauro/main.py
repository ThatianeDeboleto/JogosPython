import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange

pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480

BRANCO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagens_dinossauro.append(img)
#96 valor altura do dino
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = ALTURA - 64 - 96//2
        self.rect.center = (100, ALTURA - 64)
        self.pulo = False

    def pular(self):
        self.pulo = True
#self.rect.y -= 20 dino voa, subtrai para sempre -criar condicao para parar de subir e descer (else)
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_dinossauro[int(self.index_lista)]


class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)
#nuvem ir e voltar loop tela
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 10
#IMAGEM CACTO como vai se apresentar no jogo --- colicao mask
class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (LARGURA, ALTURA - 64)
    #cacto voltar tela
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

#add metodo ao dino
todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(LARGURA * 2 // 64):
    chao = Chao(i)
    todas_as_sprites.add(chao)
#objeto cacto --- adicionar
    cacto = Cacto()
    todas_as_sprites.add(cacto)
#add cacto (objeto ao  grupo)
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)

#evento adicionar pulo a tecla espaço --- if event.type == KEYDOWN (QUALQUER TECLA)
relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            #para o dinossauro nao ficar pulando eternamente quando clica espaco
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
    #chamar colisao metodo  --- enquanto nao ouver colisao LISTA VAZIA, quando ocorrer lista recebe objeto - exemplo cacto
    #True cacto some - False permanece
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)
    #objeto contem sprites
  #se colidir -
    if colisoes:
        pass
    else:
        todas_as_sprites.update()

    pygame.display.flip()