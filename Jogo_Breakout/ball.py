import pygame
from random import randint

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    # Esta classe representa uma bola. Ele deriva da classe "Sprite" do Pygame.

    def __init__(self, color, width, height):
        # Chame o construtor da classe pai (Sprite)
        super().__init__()

        #Passe a cor da bola, suas posições xey, largura e altura.
        # Defina a cor de fundo e defina-a como transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Desenhe a bola
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 8), randint(-8, 8)]

        # Busque o objeto retângulo que tem as dimensões da imagem.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)