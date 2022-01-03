import pygame

BLACK = (0, 0, 0)


class Brick(pygame.sprite.Sprite):
    # Esta classe representa um tijolo. Ele deriva da classe "Sprite" do Pygame.

    def __init__(self, color, width, height):
        # Chame o construtor da classe pai (Sprite)
        super().__init__()

        # Passe a cor do tijolo e sua posição xey, largura e altura.
        # Defina a cor de fundo e defina-a como transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Desenhe o tijolo (um retângulo!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Busque o objeto retângulo que tem as dimensões da imagem.
        self.rect = self.image.get_rect()