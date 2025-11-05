import pygame
from settings import ALTURA, GRAVIDADE, FORCA_PULO, VEL_HORIZONTAL, COR_PLAYER, LARGURA

class Player:
    LARG = 90
    ALT = 90
    CHAO_Y = ALTURA - 80

    def __init__(self):
        # multiplicadores (power-ups)
        self.size_mult = 1.0
        self.jump_mult = 1.0

        # posição/velocidade em float
        self.pos = pygame.Vector2(150, Player.CHAO_Y - Player.ALT)
        self.vel = pygame.Vector2(0.0, 0.0)

        # rect para colisão/desenho (tamanho ajustado em _sincronizar_rect)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.LARG, self.ALT)

        # estado
        self.no_chao = True  # inicia no chão

        # animação (opcional)
        self.frames = []          # lista de Surfaces
        self.frame_idx = 0.0
        self.fps_anim = 10.0      # frames por segundo
        self.image = None         # frame atual

        self._sincronizar_rect()

    # --------- ações ---------
    def pular(self):
        if self.no_chao:
            self.vel.y = FORCA_PULO * self.jump_mult
            self.no_chao = False

    def mover_horizontal(self, tempo_decorrido: float, dir_x: float):
        # velocidade horizontal “lógica” (para animação) e deslocamento
        self.vel.x = dir_x * VEL_HORIZONTAL
        self.pos.x += self.vel.x * tempo_decorrido

    # --------- atualização ---------
    def atualizar(self, tempo_decorrido: float):
        # gravidade
        self.vel.y += GRAVIDADE * tempo_decorrido
        self.pos.y += self.vel.y * tempo_decorrido

        # chão
        altura_atual = int(self.ALT * self.size_mult)
        if self.pos.y + altura_atual >= self.CHAO_Y:
            self.pos.y = self.CHAO_Y - altura_atual
            self.vel.y = 0.0
            self.no_chao = True

        # limites laterais considerando a largura atual
        largura_atual = int(self.LARG * self.size_mult)
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x + largura_atual > LARGURA:
            self.pos.x = LARGURA - largura_atual

        # animação simples (opcional)
        if self.frames:
            andando = abs(self.vel.x) > 1e-3 and self.no_chao
            velocidade_anim = self.fps_anim * (1.5 if andando else 1.0)
            self.frame_idx = (self.frame_idx + velocidade_anim * tempo_decorrido) % len(self.frames)
            self.image = self.frames[int(self.frame_idx)]

        self._sincronizar_rect()

    # --------- desenho ---------
    def desenhar(self, tela):
        if self.image:
            # se usar sprites, ideal redimensionar a imagem pelo size_mult
            img = self.image
            if self.size_mult != 1.0:
                w = int(self.LARG * self.size_mult)
                h = int(self.ALT * self.size_mult)
                img = pygame.transform.smoothscale(self.image, (w, h))
            tela.blit(img, self.rect.topleft)
        else:
            pygame.draw.rect(tela, COR_PLAYER, self.rect, border_radius=12)

    # --------- utilitários ---------
    def _sincronizar_rect(self):
        """Atualiza o rect a partir de pos + size_mult, mantendo o topo-esquerdo."""
        w = int(self.LARG * self.size_mult)
        h = int(self.ALT * self.size_mult)
        self.rect.width = w
        self.rect.height = h
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def set_size_mult(self, mult: float):
        """
        Ajusta o tamanho preservando a base no chão e o centro-x.
        Clampa para evitar valores extremos.
        """
        mult = max(0.5, min(1.8, mult))
        base_y = self.rect.bottom
        cx = self.rect.centerx
        self.size_mult = mult
        # aplica novo tamanho e restaura base/centro
        self._sincronizar_rect()
        self.rect.centerx = cx
        self.rect.bottom = base_y
        # atualiza pos coerente com o rect
        self.pos.x = float(self.rect.x)
        self.pos.y = float(self.rect.y)

    def reset_size(self):
        self.set_size_mult(1.0)

    def set_pos(self, x: float, y: float):
        self.pos.update(x, y)
        self._sincronizar_rect()

    def get_pos(self):
        return self.pos.x, self.pos.y