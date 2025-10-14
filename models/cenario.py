import pygame
from settings import LARGURA, ALTURA, COR_BG, COR_CHAO

class Camada:
    """
    Representa uma camada do cenário para efeito de parallax.
    Pode usar cor sólida ou imagem (opcional).
    """
    def __init__(self, velocidade_mult: float = 1.0, imagem: pygame.Surface | None = None, cor=(40, 40, 60)):
        self.imagem = imagem
        self.cor = cor
        self.velocidade_mult = velocidade_mult
        self.x1 = 0
        self.x2 = LARGURA

    def atualizar(self, tempo_decorrido: float, velocidade_base: float):
        deslocamento = velocidade_base * self.velocidade_mult * tempo_decorrido
        self.x1 -= deslocamento
        self.x2 -= deslocamento

        # reposiciona quando sai da tela (loop infinito)
        if self.x1 <= -LARGURA:
            self.x1 = self.x2 + LARGURA
        if self.x2 <= -LARGURA:
            self.x2 = self.x1 + LARGURA

    def desenhar(self, tela: pygame.Surface):
        if self.imagem:
            tela.blit(self.imagem, (self.x1, 0))
            tela.blit(self.imagem, (self.x2, 0))
        else:
            pygame.draw.rect(tela, self.cor, (self.x1, 0, LARGURA, ALTURA))
            pygame.draw.rect(tela, self.cor, (self.x2, 0, LARGURA, ALTURA))


class Cenario:
    """
    Controla todas as camadas e o chão do jogo.
    """
    def __init__(self):
        # Cria duas camadas com velocidades diferentes (efeito de profundidade)
        self.camadas = [
            Camada(velocidade_mult=0.3, cor=(25, 25, 35)),  # fundo distante
            Camada(velocidade_mult=0.6, cor=(35, 35, 50))   # camada frontal
        ]

    def atualizar(self, tempo_decorrido: float, velocidade_base: float = 300):
        for camada in self.camadas:
            camada.atualizar(tempo_decorrido, velocidade_base)

    def desenhar(self, tela: pygame.Surface):
        # Desenha as camadas do fundo
        for camada in self.camadas:
            camada.desenhar(tela)

        # Desenha o chão
        from models.player import Player  # import tardio para evitar ciclo
        pygame.draw.rect(
            tela,
            COR_CHAO,
            (0, Player.CHAO_Y, LARGURA, ALTURA - Player.CHAO_Y)
        )