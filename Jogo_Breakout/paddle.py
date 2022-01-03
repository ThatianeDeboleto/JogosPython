import pygame

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    # Esta classe representa uma raquete. Ele deriva da classe "Sprite" do Pygame.

    def __init__(self, color, width, height):

        super().__init__()

        # Passe a cor da raquete e sua posição xey, largura e altura.
        # Defina a cor de fundo e defina-a como transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Desenhe a raquete
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Busque o objeto retângulo que tem as dimensões da imagem.
        self.rect = self.image.get_rect()

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        # (fora da tela)
        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self, pixels):
        self.rect.x += pixels
        # Verifique a tela, se esta indo muito longe  (fora da tela)
        if self.rect.x > 700:
            self.rect.x = 700