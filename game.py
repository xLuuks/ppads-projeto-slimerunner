import sys
import pygame

# Importa os módulos de outras classes
from settings import *
from states import *
from models.player import Player
from models.cenario import Cenario
from models.obstaculos import Obstaculo, SpawnerObstaculos, verificar_colisoes
from models.status import Status
from models.powerUp import (
    PowerUp, SpawnerPowerUp,
    INVENCIVEL, TAM_MAIOR, TAM_MENOR, VEL_MENOR, VEL_MAIOR
)
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

        # Power-ups (em cena) e controlador
        self.powerups_ativos = []
        self.spawner_power = SpawnerPowerUp()

        # Controle de movimento
        self.dir_x = 0.0  # direção horizontal (−1 = esq, +1 = dir)

        # Status do jogo
        self.status = Status(vidas_iniciais=3)

        # Timer CRESCENTE (runner infinito)
        self.timer_crescente = 0.0

        # Dificuldade baseada no tempo da PARTIDA
        self.t0_ms = pygame.time.get_ticks()
        self.dificuldade = 1.0

        # Velocidades
        self.world_speed_mult = 1.0     # power-ups
        self.progress_mult = 1.0        # cresce com o tempo

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

                if self.estado == ESTADO_MENU and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._reiniciar_partida()
                    self.estado = ESTADO_JOGANDO

                elif self.estado == ESTADO_GAMEOVER and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.estado = ESTADO_MENU

                elif self.estado == ESTADO_JOGANDO:
                    if e.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        self.player.pular()
                    if e.key == pygame.K_p:
                        self.pause = not self.pause

            if e.type == pygame.KEYUP and self.estado == ESTADO_JOGANDO:
                if e.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT):
                    self.dir_x = 0.0

        if self.estado == ESTADO_JOGANDO and not self.pause:
            teclas = pygame.key.get_pressed()
            self.dir_x = 0.0
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                self.dir_x -= 1.0
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                self.dir_x += 1.0

    # ---------------- LÓGICA ----------------
    def _atualizar(self, dt: float):
        if self.estado != ESTADO_JOGANDO or self.pause:
            return

        # Dificuldade (spawn) e progressão (velocidade)
        elapsed_min = (pygame.time.get_ticks() - self.t0_ms) / 60000.0
        self.dificuldade = max(1.0, 1.0 + elapsed_min)
        # aceleração perceptível (~60%/min) com teto
        self.progress_mult = min(2.4, 1.0 + 0.60 * elapsed_min)
        speed_scalar = self.progress_mult * self.world_speed_mult

        # CENÁRIO
        self.cenario.atualizar(dt, velocidade_base=300 * speed_scalar)

        # PLAYER
        self.player.mover_horizontal(dt, self.dir_x)
        self.player.atualizar(dt)

        # OBSTÁCULOS (spawner usa escala; cada obstáculo move com self.velocidade)
        self.spawner.atualizar(dt, self.dificuldade * speed_scalar, self.obstaculos)
        for obst in self.obstaculos[:]:
            obst.velocidade = 300 * speed_scalar
            obst.atualizar(dt)
            if obst.saiu_da_tela():
                self.obstaculos.remove(obst)
                self.status.adicionar_pontos(10)

        # POWER-UPS (mesma velocidade do mundo; efeito RNG na coleta)
        self.spawner_power.atualizar(dt, self.powerups_ativos)
        for pu in self.powerups_ativos[:]:
            pu.vel_x = 300 * speed_scalar
            pu.atualizar(dt)
            if pu.rect.colliderect(self.player.rect):
                efeito = pu.coletar(self.status, self.player)
                pu.ativo = False
                if efeito is not None:
                    mult, dur = efeito
                    self.world_speed_mult = mult
            if not pu.ativo:
                self.powerups_ativos.remove(pu)

        # TIMER crescente
        self.timer_crescente += dt

        # STATUS + reversões
        self.status.atualizar(dt)
        ativos = self.status.powerups.keys()

        if TAM_MAIOR not in ativos and TAM_MENOR not in ativos:
            if getattr(self.player, "size_mult", 1.0) != 1.0:
                self.player.reset_size()

        if VEL_MENOR not in ativos and VEL_MAIOR not in ativos:
            if self.world_speed_mult != 1.0:
                self.world_speed_mult = 1.0

        # COLISÃO com obstáculos (depois de aplicar power-ups)
        if verificar_colisoes(self.player, self.obstaculos):
            if self.status.sofrer_dano(1, iframes=0.8):
                self.obstaculos.clear()
                if hasattr(self.spawner, "bloquear"):
                    self.spawner.bloquear(0.8)
            if self.status.game_over:
                self.estado = ESTADO_GAMEOVER

    # ---------------- DESENHO ----------------
    def _desenhar(self):
        self.cenario.desenhar(self.tela)

        for obst in self.obstaculos:
            obst.desenhar(self.tela)

        for pu in self.powerups_ativos:
            pu.desenhar(self.tela)

        if self.status.invulneravel and int(pygame.time.get_ticks() * 0.01) % 2 == 0:
            pass
        else:
            self.player.desenhar(self.tela)

        self.hud.desenhar(
            self.tela,
            vidas=self.status.vidas,
            pontos=int(self.status.pontos),
            timer_seg=self.timer_crescente,
            powerups=list(self.status.powerups.keys())
        )

        # (opcional) Debug da velocidade
        # fonte_dbg = pygame.font.SysFont("consolas", 16)
        # dbg = fonte_dbg.render(f"progress={self.progress_mult:.2f}x world={self.world_speed_mult:.2f}x", True, (200,200,200))
        # self.tela.blit(dbg, (10, ALTURA - 24))

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
        self.powerups_ativos.clear()

        self.status.resetar()
        self.pause = False
        self.timer_crescente = 0.0

        self.t0_ms = pygame.time.get_ticks()
        self.dificuldade = 1.0

        self.spawner.timer = 0.0
        if hasattr(self.spawner, "grace_timer"):
            self.spawner.grace_timer = 0.0
        if hasattr(self.spawner, "ultimo_tipo"):
            self.spawner.ultimo_tipo = None
        if hasattr(self.spawner, "bloquear"):
            self.spawner.bloquear(0.8)

        # velocidades
        self.world_speed_mult = 1.0
        self.progress_mult = 1.0

        self.dir_x = 0.0
