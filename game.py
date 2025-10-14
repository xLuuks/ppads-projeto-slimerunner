import sys
import pygame

# Importa os módulos de outras classes
from settings import *
from states import *
from models.player import Player
from models.cenario import Cenario
from models.obstaculos import Obstaculo, SpawnerObstaculos, verificar_colisoes
# from models.powerup import PowerUp   # (quando implementar)
# from models.status import Status      # (quando implementar)
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

        # Obstáculos
        self.obstaculos = []
        self.spawner = SpawnerObstaculos()

        # Controle de movimento
        self.dir_x = 0.0  # direção horizontal (−1 = esq, +1 = dir)

        # Variáveis do jogo
        self.vidas = 3
        self.pontos = 0.0

        # HUD extras
        self.timer_total = 90.0
        self.timer_restante = self.timer_total
        self.powerups = []

        # ----- NOVO: controle da dificuldade por partida -----
        self.t0_ms = pygame.time.get_ticks()   # timestamp de início desta PARTIDA
        self.dificuldade = 1.0                 # valor base

    # ---------------- LOOP PRINCIPAL ----------------
    def run(self):
        while True:
            tempo_decorrido = self.clock.tick(FPS) / 1000.0
            self._processar_eventos()
            self._atualizar(tempo_decorrido)
            self._desenhar()

    # ---------------- EVENTOS ----------------
    def _processar_eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                # MENU → iniciar jogo
                if self.estado == ESTADO_MENU and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._reiniciar_partida()
                    self.estado = ESTADO_JOGANDO

                # GAME OVER → voltar ao menu
                elif self.estado == ESTADO_GAMEOVER and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_MENU

                # JOGANDO → ações únicas
                elif self.estado == ESTADO_JOGANDO:
                    if e.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.player.pular()
                    if e.key == pygame.K_p:
                        self.pause = not self.pause

            # parar movimento ao soltar teclas
            if e.type == pygame.KEYUP and self.estado == ESTADO_JOGANDO:
                if e.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
                    self.dir_x = 0.0

        # movimento contínuo
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

        # cenário + player
        self.cenario.atualizar(tempo_decorrido, velocidade_base=300)
        self.player.mover_horizontal(tempo_decorrido, self.dir_x)
        self.player.atualizar(tempo_decorrido)

        # ----- NOVO: dificuldade baseada no tempo da PARTIDA -----
        elapsed_min = (pygame.time.get_ticks() - self.t0_ms) / 60000.0  # minutos desde o início desta partida
        self.dificuldade = max(1.0, 1.0 + elapsed_min)

        # obstáculos
        self.spawner.atualizar(tempo_decorrido, self.dificuldade, self.obstaculos)
        for obst in self.obstaculos[:]:
            obst.atualizar(tempo_decorrido)
            if obst.saiu_da_tela():
                self.obstaculos.remove(obst)
                self.pontos += 10

        # colisão
        if verificar_colisoes(self.player, self.obstaculos):
            self.vidas -= 1
            self.obstaculos.clear()  # “limpa” após dano

            # (opcional) dá um respiro de spawn se seu Spawner tiver bloquear()
            if hasattr(self.spawner, "bloquear"):
                self.spawner.bloquear(0.8)

            if self.vidas <= 0:
                self.estado = ESTADO_GAMEOVER

        # timer da fase (central no HUD)
        self.timer_restante = max(0.0, self.timer_restante - tempo_decorrido)
        # if self.timer_restante <= 0: self.estado = ESTADO_GAMEOVER

    # ---------------- DESENHO ----------------
    def _desenhar(self):
        # fundo + chão
        self.cenario.desenhar(self.tela)

        # obstáculos
        for obst in self.obstaculos:
            obst.desenhar(self.tela)

        # player
        self.player.desenhar(self.tela)

        # HUD no layout da arte
        self.hud.desenhar(
            self.tela,
            vidas=self.vidas,
            pontos=int(self.pontos),
            timer_seg=self.timer_restante,
            powerups=self.powerups
        )

        # overlays
        if self.estado == ESTADO_MENU:
            self._overlay("SLIME RUNNER", "Enter/Espaço para iniciar")
        elif self.estado == ESTADO_GAMEOVER:
            self._overlay("GAME OVER", "Enter/Espaço para voltar ao menu")
        elif self.pause:
            self._overlay("PAUSADO", "P para continuar")

        pygame.display.flip()

    # ---------------- OVERLAY ----------------
    def _overlay(self, titulo, subtitulo):
        s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        self.tela.blit(s, (0, 0))
        fonte_titulo = pygame.font.SysFont("consolas", 38, bold=True)
        fonte_msg = pygame.font.SysFont("consolas", 22)
        t1 = fonte_titulo.render(titulo, True, (255, 255, 255))
        t2 = fonte_msg.render(subtitulo, True, (200, 200, 200))
        self.tela.blit(t1, (LARGURA // 2 - t1.get_width() // 2, ALTURA // 2 - 80))
        self.tela.blit(t2, (LARGURA // 2 - t2.get_width() // 2, ALTURA // 2 - 20))

    # ---------------- REINICIAR ----------------
    def _reiniciar_partida(self):
        self.player = Player()
        self.obstaculos.clear()

        # reset de estado
        self.vidas = 3
        self.pontos = 0
        self.pause = False
        self.timer_restante = self.timer_total
        self.powerups = []

        # ----- NOVO: reset da dificuldade e do relógio da partida -----
        self.t0_ms = pygame.time.get_ticks()
        self.dificuldade = 1.0

        # reset do spawner (evita spawn colado ao recomeçar)
        self.spawner.timer = 0.0
        if hasattr(self.spawner, "grace_timer"):
            self.spawner.grace_timer = 0.0
        if hasattr(self.spawner, "ultimo_tipo"):
            self.spawner.ultimo_tipo = None
        # (opcional) pequeno respiro inicial
        if hasattr(self.spawner, "bloquear"):
            self.spawner.bloquear(0.8)

        # movimento
        self.dir_x = 0.0