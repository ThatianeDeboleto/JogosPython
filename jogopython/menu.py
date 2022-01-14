import pygame
import os
from random import randint
import telajogo
import score


# ----------------------------------------------------------------
def escolhe_menu(menu):
    opcao = {1: 'image\p1.png', 2: 'image\p2.png', 3: 'image\p3.png'}
    return opcao[menu]


# ----------------------------------------------------------------
def muda_placar(mudacor_placar):
    cor = {1: [(63, 72, 204), (239, 228, 176)],
           2: [(136, 0, 21), (239, 228, 176)]}
    return cor[mudacor_placar]


# ----------------------------------------------------------------
def menu(placarfinal, tempofinal):
    musica = randint(1, 4)
    tocar = telajogo.escolhe_musica(musica)
    menu = 1
    pygame.init()
    xqd = -1080
    yqd = 0
    xmc1 = -500
    ymc1 = 650
    xmc2 = 1500
    ymc2 = 60
    recorde = score.le_score()
    mudacor_placar = 2
    tempo_placar = 0
    font1 = pygame.font.SysFont('arial black', 28)
    texto0 = font1.render('< RECORDE >   ' + str(recorde) + ' pontos!', True, (63, 72, 204), (239, 228, 176))
    pos_texto0 = texto0.get_rect()
    pos_texto0.center = (540, 440)
    texto1 = font1.render('Placar: ' + str(placarfinal) + ' pontos!', True, (63, 72, 204), (239, 228, 176))
    pos_texto1 = texto1.get_rect()
    pos_texto1.center = (540, 380)
    texto2 = font1.render('Tempo de jogo: ' + str(tempofinal) + ' segundos!', True, (63, 72, 204), (239, 228, 176))
    pos_texto2 = texto2.get_rect()
    pos_texto2.center = (540, 340)
    fundoprincipal = pygame.image.load('image\principal.png')
    p1 = pygame.image.load(escolhe_menu(menu))
    mc1 = pygame.image.load('image\mc1.png')
    mc2 = pygame.image.load('image\mc2.png')
    janela = telajogo.cria_tela()
    pygame.display.set_caption('Corrida em Python -> Menu Principal')
    veloc_qd = 5
    veloc_mc = 30
    janela_aberta = True
    while janela_aberta:
        pygame.time.delay(50)  # delay para atualizar a janela
        for event in pygame.event.get():  # captura eventos do jogo
            if event.type == pygame.QUIT:
                return 2
        comandos = pygame.key.get_pressed()
        if (comandos[pygame.K_LEFT] or comandos[pygame.K_a]):
            menu -= 1
            if menu < 1:
                menu = 1
            p1 = pygame.image.load(escolhe_menu(menu))
        if (comandos[pygame.K_RIGHT] or comandos[pygame.K_d]):
            menu += 1
            if menu > 3:
                menu = 3
            p1 = pygame.image.load(escolhe_menu(menu))
        if comandos[pygame.K_SPACE]:
            return menu
        if xqd < - 40:
            xqd += veloc_qd
        else:
            xqd = -1080
        if xmc1 < 1580:
            xmc1 += veloc_mc
        else:
            xmc1 = 0
        if xmc2 > -1000:
            xmc2 -= veloc_mc
        else:
            xmc2 = 1500
        tempo_placar += 1
        if tempo_placar > 10:
            tempo_placar = 0
            opt = muda_placar(mudacor_placar)
            texto0 = font1.render('< RECORDE >   ' + str(recorde) + ' pontos!', True, opt[0], opt[1])
            texto1 = font1.render('Placar: ' + str(placarfinal) + ' pontos!', True, opt[0], opt[1])
            texto2 = font1.render('Tempo de jogo: ' + str(tempofinal) + ' segundos!', True, opt[0], opt[1])
            if mudacor_placar == 2:
                mudacor_placar = 1
            else:
                mudacor_placar = 2
        janela.blit(fundoprincipal, (xqd, yqd))  # posiciona imagem no fundo da tela
        janela.blit(mc1, (xmc1, ymc1))  # posiciona imagem no fundo da tela
        janela.blit(mc2, (xmc2, ymc2))  # posiciona imagem no fundo da tela
        janela.blit(p1, (190, 115))  # posiciona imagem no fundo da tela
        janela.blit(texto0, pos_texto0)
        if placarfinal > 1:
            janela.blit(texto1, pos_texto1)
            janela.blit(texto2, pos_texto2)

        pygame.display.update()  # atualiza a janela
    pygame.quit()  # encerra o pygame e sai do shell