import sys
import pygame

# Importa os módulos de outras classes
from settings import *
from states import *
from models.player import Player
from models.cenario import Cenario
from models.obstaculos import Obstaculos
from models.powerUp import PowerUp
from models.status import Status
from ui.hud import Hud


class Jogo:
    def __init__(self, titulo="Slime Runner – Base"):
        pygame.init()
        pygame.display.set_caption(titulo)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()

        # Estados
        self.estado = ESTADO_MENU
        self.pause = False

        # Entidades
        self.player = Player()
        self.cenario = Cenario()
        self.hud = Hud()

        # Controle de movimento
        self.dir_x = 0.0  # direção horizontal (−1 = esq, +1 = dir)

    # ---------------- LOOP PRINCIPAL ----------------
    def run(self):
        while True:
            tempo_decorrido = self.clock.tick(FPS) / 1000.0

            # Processa entrada, atualiza e desenha
            self._processar_eventos()
            self._atualizar(tempo_decorrido)
            self._desenhar()

    # ---------------- EVENTOS ----------------
    def _processar_eventos(self):
        # Eventos únicos (tecla pressionada ou solta)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # MENU → iniciar jogo
                if self.estado == ESTADO_MENU and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_JOGANDO

                # GAME OVER → voltar ao menu
                elif self.estado == ESTADO_GAMEOVER and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_MENU

                # JOGANDO → ações únicas
                elif self.estado == ESTADO_JOGANDO:
                    # Pular
                    if e.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.player.pular()

                    # Pausar
                    if e.key == pygame.K_p:
                        self.pause = not self.pause

            # Detectar quando soltar teclas, para parar o movimento
            if e.type == pygame.KEYUP and self.estado == ESTADO_JOGANDO:
                if e.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
                    self.dir_x = 0.0

        # Detectar teclas pressionadas continuamente (movimento)
        if self.estado == ESTADO_JOGANDO and not self.pause:
            teclas = pygame.key.get_pressed()
            self.dir_x = 0.0
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                self.dir_x -= 1.0
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                self.dir_x += 1.0

    # ---------------- LÓGICA ----------------
    def _atualizar(self, tempo_decorrido: float):
        if self.estado != ESTADO_JOGANDO or self.pause:
            return

        # Atualiza entidades
        self.player.mover_horizontal(tempo_decorrido, self.dir_x)
        self.player.atualizar(tempo_decorrido)

        # (futuro) colisões e lógica do cenário
        # self.cenario.atualizar(tempo_decorrido)

    # ---------------- DESENHO ----------------
    def _desenhar(self):
        # Fundo
        self.tela.fill(COR_BG)
        pygame.draw.rect(self.tela, COR_CHAO, (0, Player.CHAO_Y, LARGURA, ALTURA - Player.CHAO_Y))

        # Desenhar entidades
        # self.cenario.renderizar(self.tela)
        self.player.desenhar(self.tela)
        # self.hud.renderizar(self.tela, vidas, pontos, status)

        # Atualiza frame
        pygame.display.flip()