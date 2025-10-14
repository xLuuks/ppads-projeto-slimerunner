import sys
import pygame

# Importa os arquivos de outras classes, que serão iniciados no jogo.

from settings import *
from states import *
from models.player import *
from models.cenario import *
from models.obstaculos import *
from models.powerUp import *
from models.status import *
from ui.hud import *

class Jogo:
    def __init__(self, titulo="Slime Runner – Base"):
        pygame.init()
        pygame.display.set_caption(titulo)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()

        # estados
        self.estado = ESTADO_MENU
        self.pause = False

        # entidades
        self.player = Player()
        self.cenario = Cenario()
        self.hud = Hud()

    def run(self):
        while True:
            tempo_decorrido = self.clock.tick(FPS) / 1000.0
            self._processar_eventos()
            self._atualizar(tempo_decorrido)
            self._desenhar()

    def _processar_eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.estado == ESTADO_MENU and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_JOGANDO
                elif self.estado == ESTADO_JOGANDO:
                    if e.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.player.pular()
                    if e.key == pygame.K_p:
                        self.pause = not self.pause
                elif self.estado == ESTADO_GAMEOVER and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_MENU

    def _atualizar(self, tempo_decorrido):
        if self.estado != ESTADO_JOGANDO or self.pause:
            return
        self.player.atualizar(tempo_decorrido)

    def _desenhar(self):
        self.tela.fill(COR_BG)
        pygame.draw.rect(self.tela, COR_CHAO, (0, Player.CHAO_Y, LARGURA, ALTURA - Player.CHAO_Y))
        self.player.desenhar(self.tela)
        pygame.display.flip()