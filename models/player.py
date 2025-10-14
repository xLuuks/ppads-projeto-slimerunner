import pygame
from settings import ALTURA, GRAVIDADE, FORCA_PULO, VEL_HORIZONTAL, COR_PLAYER

class Player:
    LARG = 60
    ALT = 60
    CHAO_Y = ALTURA - 100

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, self.LARG, self.ALT)
        self.vel_y = 0.0
        self.em_chao = False

    # ação de pulo (acionada uma vez no KEYDOWN)
    def pular(self):
        if self.em_chao:
            self.vel_y = FORCA_PULO
            self.em_chao = False

    # movimento horizontal contínuo via teclas pressionadas
    def mover_horizontal(self, dt: float, dir_x: float):
        self.rect.x += int(dir_x * VEL_HORIZONTAL * dt)

    def atualizar(self, dt: float):
        # gravidade + chão
        self.vel_y += GRAVIDADE * dt
        self.rect.y += int(self.vel_y * dt)
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