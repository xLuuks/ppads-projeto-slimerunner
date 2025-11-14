import random
import pygame
from typing import Optional, Tuple, List, Dict

from settings import *
from models.player import Player

# Ícone global usado para desenhar TODOS os power-ups no cenário.
# O game.py deve fazer: power_mod.ICON_POWERUP = self.power_icon
ICON_POWERUP: pygame.Surface | None = None

# nomes oficiais dos efeitos
INVENCIVEL = "invencibilidade"
TAM_MAIOR  = "aumento_tamanho"
TAM_MENOR  = "reducao_tamanho"
VEL_MENOR  = "reducao_velocidade"
VEL_MAIOR  = "aumento_velocidade"

# =========================
# CONFIGURAÇÃO RÁPIDA 👇
# =========================
# Tamanho e posição vertical do ícone de power-up.
POWERUP_CONF: Dict[str, int] = {
    "w": 60,     # largura do ícone
    "h": 60,     # altura do ícone
    "y_offset": 10,  # distância do centro do power-up até o chão (Player.CHAO_Y - y_offset)
}

# catálogo: só duração (cor vem de COR_POWERUP / COR_OBST para ficar consistente)
CATALOGO_DUR: Dict[str, float] = {
    INVENCIVEL: 4.0,   # i-frames um pouco maiores
    TAM_MAIOR:  10.0,  # ↑ tamanho dura mais
    TAM_MENOR:  10.0,  # ↓ tamanho dura mais
    VEL_MENOR:  6.0,   # mundo mais lento
    VEL_MAIOR:  6.0,   # mundo mais rápido
}

TODOS_EFEITOS = [INVENCIVEL, TAM_MAIOR, TAM_MENOR, VEL_MENOR, VEL_MAIOR]


class PowerUp:
    """Coletável genérico: visual (ícone) + efeito decidido na coleta (RNG)."""

    def __init__(self, x: int):
        w = POWERUP_CONF["w"]
        h = POWERUP_CONF["h"]
        y_offset = POWERUP_CONF["y_offset"]

        # centro do power-up um pouco acima do chão
        y_centro = Player.CHAO_Y - y_offset

        self.rect = pygame.Rect(
            x - w // 2,
            y_centro - h // 2,
            w,
            h,
        )

        self.ativo = True
        # velocidade é sincronizada pelo game.py a cada frame (não fixa aqui)
        self.vel_x = 0.0

    def atualizar(self, dt: float):
        self.rect.x -= int(self.vel_x * dt)
        if self.rect.right < 0:
            self.ativo = False

    def desenhar(self, tela: pygame.Surface):
        # Usa o ícone global se estiver configurado; senão, desenha bolinha
        global ICON_POWERUP

        if ICON_POWERUP is not None:
            w = POWERUP_CONF["w"]
            h = POWERUP_CONF["h"]
            img = pygame.transform.smoothscale(ICON_POWERUP, (w, h))
            tela.blit(img, self.rect.topleft)
        else:
            # fallback: círculo simples no centro do rect
            raio = min(self.rect.width, self.rect.height) // 2
            pygame.draw.circle(tela, COR_POWERUP, self.rect.center, raio)

    def coletar(self, status, player) -> Optional[Tuple[float, float]]:
        """
        Decide um efeito aleatório e aplica.
        Retorna (world_speed_mult, duracao) se for power de velocidade, senão None.
        """
        tipo = random.choice(TODOS_EFEITOS)
        dur = CATALOGO_DUR[tipo]

        # Registra para HUD/Status
        status.conceder_powerup(tipo, dur)

        if tipo == INVENCIVEL:
            status.invulneravel = True
            status._invuln_restante = max(status._invuln_restante, dur)
            return None

        if tipo == TAM_MAIOR:
            mult = getattr(player, "size_mult", 1.0) * 1.3
            if hasattr(player, "set_size_mult"):
                player.set_size_mult(mult)
            return None

        if tipo == TAM_MENOR:
            mult = getattr(player, "size_mult", 1.0) * 0.75
            if hasattr(player, "set_size_mult"):
                player.set_size_mult(mult)
            return None

        if tipo == VEL_MENOR:
            return (0.75, dur)

        if tipo == VEL_MAIOR:
            return (1.25, dur)

        return None


class SpawnerPowerUp:
    """Spawna power-ups com baixa frequência. O efeito só é decidido na coleta."""
    def __init__(self, intervalo_base: float = 9.0):
        self.intervalo_base = intervalo_base
        self.timer = 0.0

    def atualizar(self, dt: float, lista_powerups: List[PowerUp]):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.intervalo_base + random.uniform(3, 6)
            x = LARGURA + random.randint(220, 420)
            lista_powerups.append(PowerUp(x))