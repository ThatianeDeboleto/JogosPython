import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

# Definir cores
PINK = (255, 20, 147)
LAVENDERBLUSH = (255, 240, 245)
MISTYROSE = (255, 105, 180)
RED = (170, 216, 211)
SEASHELL = (255, 245, 238)
YELLOW = (57, 62, 70)

pontuacao = 0
vidas = 3

# abrir uma nova janela
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

# Esta será uma lista que conterá todos os sprites do jogo
all_sprites_list = pygame.sprite.Group()

# criar raquete
paddle = Paddle(MISTYROSE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

# Criar bola
ball = Ball(PINK, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(SEASHELL, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Adicione a raquete à lista de sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

#O loop continuará até que o usuário saia do jogo (por exemplo, clicar no botão Fechar).
carryOn = True

# O relógio será usado para controlar a rapidez com que a tela é atualizada
clock = pygame.time.Clock()

# -------- Main Programa Loop -----------
while carryOn:

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

    # Movendo a raquete quando o uso usa as teclas de seta
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)

    # --- A lógica do jogo deve ir aqui
    all_sprites_list.update()

    # Verifique se a bola está quicando contra qualquer uma das 4 paredes:
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.velocity[1] = -ball.velocity[1]
        vidas -= 1
        if vidas == 0:
            # Exibir mensagem de fim de jogo por 3 segundos
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, PINK)
            screen.blit(text, (250, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # parar jogo
            carryOn = False

    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]

    # Detecta colisões entre a bola e a raquete
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()

    # Verifique se a bola colide com algum dos tijolos
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        pontuacao += 1
        brick.kill()
        if len(all_bricks) == 0:
            # Exibir mensagem de nível completo por 3 segundos
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, PINK)
            screen.blit(text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # parar jogo
            carryOn = False

    # --- O código de desenho deve ir aqui
    # Primeiro, limpe a tela para azul escuro.
    screen.fill(LAVENDERBLUSH)
    pygame.draw.line(screen, PINK, [0, 38], [800, 38], 2)

    # Mostra a pontuação e o número de vidas no topo da tela
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(pontuacao), 1, PINK)
    screen.blit(text, (20, 10))
    text = font.render("Lives: " + str(vidas), 1, PINK)
    screen.blit(text, (650, 10))

    # Agora vamos desenhar todos os sprites de uma vez. (Por enquanto temos apenas 2 sprites!)
    all_sprites_list.draw(screen)

    # --- Vá em frente e atualize a tela com o que desenhamos.
    pygame.display.flip()

    # --- Limite de 60 quadros por segundo
    clock.tick(60)

# Depois de sair do loop principal do programa, podemos parar o mecanismo de jogo:
pygame.quit()