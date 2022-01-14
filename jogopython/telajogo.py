from random import randint
import pygame
import os


# ------------------------------------------------------------------------
def npc_aleatório():
    carro_npc = {'1': 'image\car_pc1.png', '2': 'image\car_pc2.png', '3': 'image\car_pc3.png',
                 '4': 'image\car_pc4.png', '5': 'image\car_pc5.png', '6': 'image\car_pc6.png',
                 '7': 'image\car_pc7.png', '8': 'image\car_pc8.png', '9': 'image\car_pc9.png',
                 '10': 'image\car_pc10.png', '11': 'image\car_pc11.png', '12': 'image\car_pc12.png'}
    carro = str(randint(1, 12))
    return carro_npc[carro]


# ------------------------------------------------------------------------
def velocidade_npc():
    vl = (randint(8, 12))
    vfinal = vl / 10
    return vfinal


# ------------------------------------------------------------------------
def escolhe_musica(musica):
    audio = {1: 'audio\m1.mp3', 2: 'audio\m2.mp3',
             3: 'audio\m3.mp3', 4: 'audio\m4.mp3'}
    return audio[musica]


# ------------------------------------------------------------------------
def escolhefundo(contfundo):
    opcao = {1: 'image\pista1.png', 2: 'image\pista2.png', 3: 'image\pista3.png'}
    return opcao[contfundo]


# ------------------------------------------------------------------------
def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


# ------------------------------------------------------------------------
def cria_tela():
    janela = pygame.display.set_mode((1080, 720))  # cria janela do jogo
    return janela


# ------------------------------------------------------------------------
def jogar():
    musica1 = randint(1, 4)
    musica = musica1 + 1
    pygame.init()
    # variáveis de posicionamento dos objetos------------------------------------------
    xp = 486  # carro jogador
    yp = 500
    x1 = 195  # carro npc esquerda
    y1 = randint(-2000, -500)
    x2 = 340  # carro npc meio esquerda
    y2 = randint(-2000, -500)
    x3 = 486  # carro npc meio
    y3 = randint(-2000, -500)
    x4 = 630  # carro npc meio direita
    y4 = randint(-2000, -500)
    x5 = 775  # carro npc direita
    y5 = randint(-2000, -500)
    xpista = 0
    ypista = -720
    xcmd = 5
    ycmd = 100
    # variáveis de tempo e placar--------------------------------------------------------
    timer = 0
    tempo_segundo = 0
    multiplicador = 1
    placar = 0
    contfundo = 1
    tempo_fundo = 0
    # variáveis de velocidade de deslocamento do objeto (círculo)-----------------------
    veloc_xp = 20  # valor em pixels - velocidade do carro do jogador
    veloc_x1 = veloc_x2 = veloc_x3 = veloc_x4 = veloc_x5 = 20  # velocidade dos carros npc
    veloc_pista = 30  # valor em pixels - velocidade da pista
    # carrega imagens--------------------------------------------------------------------
    fundo = pygame.image.load(escolhefundo(contfundo))
    carro = pygame.image.load(npc_aleatório())
    carro_pc = pygame.image.load(npc_aleatório())
    carro_pc2 = pygame.image.load(npc_aleatório())
    carro_pc3 = pygame.image.load(npc_aleatório())
    carro_pc4 = pygame.image.load(npc_aleatório())
    carro_pc5 = pygame.image.load(npc_aleatório())
    cmd = pygame.image.load('image\cmd.png')
    # janela com placar de pontos-------------------------------------------------------
    font = pygame.font.SysFont('arial', 30)
    texto = font.render('Placar: ' + str(placar), True, (255, 255, 255), (0, 0, 0))
    pos_texto = texto.get_rect()
    pos_texto.center = (50, 50)
    # cria janela do jogo---------------------------------------------------------------
    janela = cria_tela()
    pygame.display.set_caption('Corrida em Python -> Jogar')  # mostra nome do jogo na janela
    # cria laço de repetição para manter janela aberta---------------------------------
    janela_aberta = True
    while janela_aberta:
        pygame.time.delay(50)  # delay para atualizar a janela
        for event in pygame.event.get():  # captura eventos do jogo
            if event.type == pygame.QUIT:
                janela_aberta = False

                # comandos para movimentação do objeto e trocar música-------------------------------
        comandos = pygame.key.get_pressed()
        if (comandos[pygame.K_RIGHT] or comandos[pygame.K_d]) and xp < 750:
            xp += veloc_xp
        if (comandos[pygame.K_LEFT] or comandos[pygame.K_a]) and xp > 210:  # 190 - 540 - 780
            xp -= veloc_xp
        if comandos[pygame.K_m]:
            pygame.mixer.music.load(escolhe_musica(musica))
            pygame.mixer.music.play()
            if musica == 4:
                musica = 1
            else:
                musica += 1
                # domínio de colisão-----------------------------------------------------------------
        # colisão
        if ((xp + 100 > x5 and yp < y5 + 169)):  # colisão com carro npc 5
            # pygame.quit() # encerra o pygame e sai do shell
            return [int(placar), int(tempo_segundo)]

        if ((xp < x1 + 100 and yp < y1 + 169)):  # colisão com carro npc 1
            # pygame.quit() # encerra o pygame e sai do shell
            return [int(placar), int(tempo_segundo)]

        if (xp < x3 + 100 and yp < y3 + 169) and (xp + 100 > x3 and yp < y3 + 169):  # colisão com carro npc 3
            # pygame.quit() # encerra o pygame e sai do shell
            return [int(placar), int(tempo_segundo)]

        if (xp < x2 + 100 and yp < y2 + 169) and (xp + 100 > x2 and yp < y2 + 169):  # colisão com carro npc 2
            # pygame.quit() # encerra o pygame e sai do shell
            return [int(placar), int(tempo_segundo)]

        if (xp < x4 + 100 and yp < y4 + 169) and (xp + 100 > x4 and yp < y4 + 169):  # colisão com carro npc 4
            # pygame.quit() # encerra o pygame e sai do shell
            return [int(placar), int(tempo_segundo)]

        # -----------------------------------------------------------------------------------
        y1 += veloc_x1
        if y1 > 680:
            y1 = randint(-5000, -500)
            carro_pc = pygame.image.load(npc_aleatório())
            if tempo_segundo >= 1:
                veloc_x1 = velocidade_npc() * 10 * (1 + tempo_segundo / 10)
            else:
                veloc_x1 = velocidade_npc() * 10
        y2 += veloc_x2
        if y2 > 680:
            y2 = randint(-5000, -500)
            carro_pc2 = pygame.image.load(npc_aleatório())
            if tempo_segundo >= 1:
                veloc_x2 = velocidade_npc() * 10 * (1 + tempo_segundo / 10)
            else:
                veloc_x2 = velocidade_npc() * 10
        y3 += veloc_x3
        if y3 > 680:
            y3 = randint(-5000, -500)
            carro_pc3 = pygame.image.load(npc_aleatório())
            if tempo_segundo >= 1:
                veloc_x3 = velocidade_npc() * 10 * (1 + tempo_segundo / 10)
            else:
                veloc_x3 = velocidade_npc() * 10
        y4 += veloc_x4
        if y4 > 680:
            y4 = randint(-5000, -500)
            carro_pc4 = pygame.image.load(npc_aleatório())
            if tempo_segundo >= 1:
                veloc_x4 = velocidade_npc() * 10 * (1 + tempo_segundo / 10)
            else:
                veloc_x4 = velocidade_npc() * 10
        y5 += veloc_x5
        if y5 > 680:
            y5 = randint(-5000, -500)
            carro_pc5 = pygame.image.load(npc_aleatório())
            if tempo_segundo >= 1:
                veloc_x5 = velocidade_npc() * 10 * (1 + tempo_segundo / 10)
            else:
                veloc_x5 = velocidade_npc() * 10
        ypista += veloc_pista

        if ypista >= 0:
            ypista = -720

        if timer < 20:
            timer += 1
        else:
            tempo_segundo += 1
            tempo_fundo += 1
            placar += 1 + multiplicador
            multiplicador += 0.5
            texto = font.render('Placar: ' + str(int(placar)), True, (255, 255, 255), (0, 0, 0))
            timer = 0
            if veloc_pista < 100:
                veloc_pista = veloc_pista * (1 + tempo_segundo / 500)
        if tempo_fundo > 16:
            tempo_fundo = 0
            contfundo += 1
            if contfundo > 3:
                contfundo = 1
            fundo = pygame.image.load(escolhefundo(contfundo))
        janela.blit(fundo, (int(xpista), int(ypista)))  # posiciona imagem no fundo da tela
        janela.blit(cmd, (xcmd, ycmd))
        janela.blit(carro, (xp, yp))
        janela.blit(carro_pc, (int(x1), int(y1)))
        janela.blit(carro_pc2, (int(x2), int(y2)))
        janela.blit(carro_pc3, (int(x3), int(y3)))
        janela.blit(carro_pc4, (int(x4), int(y4)))
        janela.blit(carro_pc5, (int(x5), int(y5)))
        janela.blit(texto, pos_texto)
        pygame.display.update()  # atualiza a janela
    # pygame.quit() # encerra o pygame e sai do shell