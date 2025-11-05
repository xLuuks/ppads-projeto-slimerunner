import sys
import os
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


def carregar_imagem(rel_path, tamanho=None):
    caminho = os.path.join(os.path.dirname(__file__), rel_path)
    img = pygame.image.load(caminho).convert_alpha()
    if tamanho is not None:
        img = pygame.transform.smoothscale(img, tamanho)
    return img


class Jogo:
    def __init__(self, titulo="Slime Runner – Base"):
        pygame.init()
        pygame.display.set_caption(titulo)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.clock = pygame.time.Clock()

        # Carregar assets gráficos (imagens, ícones etc.)
        self._carregar_assets()

        # Registrar ícone global dos power-ups (aparece no cenário)
        import models.powerUp as power_mod
        power_mod.ICON_POWERUP = self.power_icon

        # Registrar imagens de obstáculos (usadas dentro de models.obstaculos)
        from models import obstaculos
        obstaculos.OBST_IMGS.clear()
        obstaculos.OBST_IMGS.update(self.obst_imgs)

        # Estados
        self.estado = ESTADO_MENU
        self.pause = False

        # Entidades
        self.player = Player()
        self.cenario = Cenario()
        self.hud = Hud()

        # Ícones de HUD básicos (vidas + ampulheta do timer)
        self.hud.icon_coracao   = self.icon_vida
        self.hud.icon_ampulheta = self.icon_tempo

        # Configurar sprites do Slime
        self.player.frames = [
            self.img_slime_parado,
            self.img_slime_correndo
        ]
        self.player.image = self.img_slime_parado

        # Configurar imagens de fundo (parallax)
        self.cenario.usar_imagens(self.img_cenario_longe, self.img_cenario_perto)

        # Power-ups exibidos na HUD (um ícone diferente para cada efeito)
        self.hud.set_icons({
            INVENCIVEL: self.icon_invencivel,
            TAM_MAIOR:  self.icon_tam_maior,
            TAM_MENOR:  self.icon_tam_menor,
            VEL_MENOR:  self.icon_vel_menor,
            VEL_MAIOR:  self.icon_vel_maior,
        })

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
        self.world_speed_mult = 1.0     # afetada por power-ups de velocidade
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
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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

        # OBSTÁCULOS
        self.spawner.atualizar(dt, self.dificuldade * speed_scalar, self.obstaculos)
        for obst in self.obstaculos[:]:
            obst.velocidade = 300 * speed_scalar
            obst.atualizar(dt)
            if obst.saiu_da_tela():
                self.obstaculos.remove(obst)

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

        # Pontuação baseada no tempo e posição horizontal
        ganho_base = 5 * dt  # base: 5 pontos por segundo (ajuste como quiser)
        mult = self._get_xp_multiplier()
        ganho_final = ganho_base * mult

        self.status.adicionar_pontos(ganho_final)


        # STATUS + reversões
        self.status.atualizar(dt)
        ativos = self.status.powerups.keys()

        # se não há power-up de tamanho ativo, volta ao normal
        if TAM_MAIOR not in ativos and TAM_MENOR not in ativos:
            if getattr(self.player, "size_mult", 1.0) != 1.0:
                self.player.reset_size()

        # se não há power-up de velocidade ativo, volta ao normal
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

        # efeito de “piscar” quando invulnerável
        if self.status.invulneravel and int(pygame.time.get_ticks() * 0.01) % 2 == 0:
            pass
        else:
            self.player.desenhar(self.tela)

        # HUD – aqui a lista de powerups ativos vira ícones conforme o mapa setado
        xp_mult = self._get_xp_multiplier()

        self.hud.desenhar(
            self.tela,
            vidas=self.status.vidas,
            pontos=int(self.status.pontos),
            timer_seg=self.timer_crescente,
            powerups=list(self.status.powerups.keys()),
            xp_mult=xp_mult,
        )

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

    # ---------------- XP Multiplicador --------------------
    def _get_xp_multiplier(self) -> float:
        
        if not hasattr(self, "player") or self.player is None:
            return 1.0

        px = self.player.rect.centerx
        frac = px / LARGURA  # 0.0 (esquerda) -> 1.0 (direita)
        frac = max(0.0, min(1.0, frac))

        centro_min = 0.10
        centro_max = 0.55
        max_bonus = 2.35  

        bonus = 0.0
        if frac < centro_min:
            # quanto mais à esquerda, maior o bônus
            t = (centro_min - frac) / centro_min
            bonus = max_bonus * t
        elif frac > centro_max:
            # quanto mais à direita, maior o bônus
            t = (frac - centro_max) / (1.0 - centro_max)
            bonus = max_bonus * t
        else:
            bonus = 0.0

        return 1.0 + bonus

    # ---------------- REINICIAR ----------------
    def _reiniciar_partida(self):
        self.player = Player()

        # reaplica as sprites do Slime
        self.player.frames = [
            self.img_slime_parado,
            self.img_slime_correndo
        ]
        self.player.image = self.img_slime_parado

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

    # ---------------- CARREGAR ASSETS ----------------
    def _carregar_assets(self):
        base = "Imagens Jogo"

        # ---- Slime ----
        slime_dir = base + "/Slime"
        tam_slime = (Player.LARG, Player.ALT)
        self.img_slime_parado   = carregar_imagem(slime_dir + "/parado_sem_fundo.png",   tam_slime)
        self.img_slime_correndo = carregar_imagem(slime_dir + "/correndo_sem_fundo.png", tam_slime)
        self.img_slime_pulando  = carregar_imagem(slime_dir + "/pulando_sem_fundo.png",  tam_slime)
        self.img_slime_dano     = carregar_imagem(slime_dir + "/dano_sem_fundo_v2.png",  tam_slime)

        # ---- Cenário ----
        cen_dir = base + "/Cenario"
        self.img_cenario_longe = carregar_imagem(cen_dir + "/PLANO_DE_FUNDO.png", (LARGURA, ALTURA))
        self.img_cenario_perto = carregar_imagem(cen_dir + "/ARVORES.png",        (LARGURA, ALTURA))

        # ---- HUD (se quiser usar depois para vidas/tempo) ----
        hud_dir = base + "/HUD"
        self.icon_vida  = carregar_imagem(hud_dir + "/pontos-vida.png", (32, 32))
        self.icon_tempo = carregar_imagem(hud_dir + "/tempo.png",       (32, 32))

        # ---- Obstáculos ----
        obst_dir = base + "/Obstaculos"
        self.obst_imgs = {
            "tronco_baixo": carregar_imagem(obst_dir + "/tronco_sem_fundo.png",   (70, 40)),
            "pedra":        carregar_imagem(obst_dir + "/rocha_sem_fundo.png",    (50, 50)),
            "tronco_alto":  carregar_imagem(obst_dir + "/pedreira_sem_fundo.png", (60, 90)),
            "arbusto_de_espinhos": carregar_imagem(obst_dir + "/espinho_sem_fundo.png", (70,40)),
            "cogumelo_venenoso": carregar_imagem(obst_dir + "/veneno_sem_fundo.png", (40,40)),
            "poca": carregar_imagem(obst_dir + "/poca_sem_fundo.png",(70,100))
        }

        # ---- Power-ups ----
        power_dir = base + "/PowerUps"

        # Ícone que aparece no cenário (cogumelo, por exemplo)
        self.power_icon = carregar_imagem(power_dir + "/power_sem_fundo.png", (40, 40))

        # Ícones específicos para cada efeito na HUD
        self.icon_invencivel = carregar_imagem(power_dir + "/escudo.png",       (40, 40))  # ex.: escudo dourado
        self.icon_tam_maior  = carregar_imagem(power_dir + "/seta_cima.png",    (40, 40))  # seta verde para cima
        self.icon_tam_menor  = carregar_imagem(power_dir + "/seta_baixo.png",   (40, 40))  # seta roxa para baixo
        self.icon_vel_menor  = carregar_imagem(power_dir + "/caracol.png",      (40, 40))  # espiral / caracol
        self.icon_vel_maior  = carregar_imagem(power_dir + "/velocimetro.png",  (40, 40))  # velocímetro / relógio

        # ---- HUD ----
        hud_dir = base + "/HUD"
        self.icon_vida  = carregar_imagem(hud_dir + "/pontos-vida.png", (32, 32))
        self.icon_tempo = carregar_imagem(hud_dir + "/tempo.png",       (32, 32))