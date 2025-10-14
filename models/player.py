import pygame
from settings import ALTURA, GRAVIDADE, FORCA_PULO, VEL_HORIZONTAL, COR_PLAYER

class Player:
    LARG = 60
    ALT = 60
    CHAO_Y = ALTURA - 100

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, self.LARG, self.ALT)
        self.vel_y = 0.0
        self.no_chao = False
        self.imagemPlayer = pygame.image.load("")

    # ação de pulo (acionada uma vez no KEYDOWN)
    def pular(self):
        if self.no_chao:
            self.vel_y = FORCA_PULO
            self.no_chao = False

    # movimento horizontal contínuo via teclas pressionadas
    def mover_horizontal(self, tempo_decorrido: float, dir_x: float):
        self.rect.x += int(dir_x * VEL_HORIZONTAL * tempo_decorrido)

    def atualizar(self, tempo_decorrido: float):
        # gravidade + chão
        self.vel_y += GRAVIDADE * tempo_decorrido
        self.rect.y += int(self.vel_y * tempo_decorrido)
        if self.rect.bottom >= self.CHAO_Y:
            self.rect.bottom = self.CHAO_Y
            self.vel_y = 0.0
            self.em_chao = True

        # limitar à tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 960:  # usa largura fixa daqui para simplificar
            self.rect.right = 960

    def desenhar(self, tela):
        pygame.draw.rect(tela, COR_PLAYER, self.rect, border_radius=12)