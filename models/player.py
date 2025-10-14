import pygame
from settings import ALTURA, GRAVIDADE, FORCA_PULO, VEL_HORIZONTAL, COR_PLAYER, LARGURA

class Player:
    LARG = 60
    ALT = 60
    CHAO_Y = ALTURA - 100

    def __init__(self):
        # POSIÇÃO E VELOCIDADE EM FLOAT (suave)
        self.pos = pygame.Vector2(150, Player.CHAO_Y - Player.ALT)
        self.vel = pygame.Vector2(0.0, 0.0)

        # Rect só para colisão/desenho, sincronizado com self.pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.LARG, self.ALT)

        self.no_chao = False

        # --- (opcional) ANIMAÇÃO ---
        self.frames = []          # liste de Surfaces se tiver sprites
        self.frame_idx = 0.0
        self.fps_anim = 10.0      # velocidade da animação (frames/s)
        self.image = None         # frame atual

        # # Exemplo se quiser carregar um PNG único:
        # self.image = pygame.image.load("assets/slime.png").convert_alpha()

    # ação de pulo (acionada no KEYDOWN)
    def pular(self):
        if self.no_chao:
            self.vel.y = FORCA_PULO
            self.no_chao = False

    # movimento horizontal contínuo via teclas pressionadas
    def mover_horizontal(self, tempo_decorrido: float, dir_x: float):
        self.pos.x += (dir_x * VEL_HORIZONTAL) * tempo_decorrido

    def _sincronizar_rect(self):
        # posiciona o rect de acordo com a pos float
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def atualizar(self, tempo_decorrido: float):
        # gravidade
        self.vel.y += GRAVIDADE * tempo_decorrido
        self.pos.y += self.vel.y * tempo_decorrido

        # chão
        if self.pos.y + self.ALT >= self.CHAO_Y:
            self.pos.y = self.CHAO_Y - self.ALT
            self.vel.y = 0.0
            self.no_chao = True

        # limitar à tela (usa LARGURA do settings)
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x + self.LARG > LARGURA:
            self.pos.x = LARGURA - self.LARG

        # animação simples (opcional)
        if self.frames:
            andando = abs(self.vel.x) > 1e-3 and self.no_chao
            velocidade_anim = self.fps_anim * (1.5 if andando else 1.0)
            self.frame_idx = (self.frame_idx + velocidade_anim * tempo_decorrido) % len(self.frames)
            self.image = self.frames[int(self.frame_idx)]

        self._sincronizar_rect()

    def desenhar(self, tela):
        if self.image:
            tela.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(tela, COR_PLAYER, self.rect, border_radius=12)

    # (opcional) setters/gets úteis
    def set_pos(self, x: float, y: float):
        self.pos.update(x, y)
        self._sincronizar_rect()

    def get_pos(self):
        return self.pos.x, self.pos.y