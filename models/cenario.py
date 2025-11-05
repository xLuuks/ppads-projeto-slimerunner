import pygame
from settings import LARGURA, ALTURA


class Camada:
    """
    Representa uma camada do cenário para efeito de parallax.
    Pode usar cor sólida ou imagem (opcional).
    """
    def __init__(
        self,
        velocidade_mult: float = 1.0,
        imagem: pygame.Surface | None = None,
        cor=(40, 40, 60),
    ):
        self.imagem = imagem
        self.cor = cor
        self.velocidade_mult = velocidade_mult
        self.x1 = 0
        self.x2 = LARGURA

    def atualizar(self, tempo_decorrido: float, velocidade_base: float):
        deslocamento = velocidade_base * self.velocidade_mult * tempo_decorrido
        self.x1 -= deslocamento
        self.x2 -= deslocamento

        # Reposiciona quando sai da tela (loop infinito)
        if self.x1 <= -LARGURA:
            self.x1 = self.x2 + LARGURA
        if self.x2 <= -LARGURA:
            self.x2 = self.x1 + LARGURA

    def desenhar(self, tela: pygame.Surface):
        """
        Desenha a camada duas vezes (x1 e x2) para fazer o loop horizontal.
        Se houver imagem, usa a imagem; senão, usa um retângulo colorido.
        """
        if self.imagem is not None:
            tela.blit(self.imagem, (self.x1, 0))
            tela.blit(self.imagem, (self.x2, 0))
        else:
            pygame.draw.rect(tela, self.cor, (self.x1, 0, LARGURA, ALTURA))
            pygame.draw.rect(tela, self.cor, (self.x2, 0, LARGURA, ALTURA))


class Cenario:
    def __init__(self):
        # Camada de fundo (mais lenta) e camada frontal (igual aos obstáculos)
        self.camadas = [
            Camada(velocidade_mult=0.5, cor=(25, 25, 35)),  # fundo distante
            Camada(velocidade_mult=0.9, cor=(35, 35, 50)),  # camada frontal (igual obstáculos)
        ]

    def usar_imagens(self, img_longe: pygame.Surface, img_perto: pygame.Surface):
        """
        Define as imagens das duas camadas:
        - img_longe: plano de fundo (mais lento)
        - img_perto: camada frontal (mesma velocidade dos obstáculos)
        """
        self.camadas[0].imagem = img_longe
        self.camadas[1].imagem = img_perto

    def atualizar(self, tempo_decorrido: float, velocidade_base: float = 300):
        for camada in self.camadas:
            camada.atualizar(tempo_decorrido, velocidade_base)

    def desenhar(self, tela: pygame.Surface):
        # Desenha cada camada na ordem certa (fundo primeiro, frente depois)
        for camada in self.camadas:
            camada.desenhar(tela)