import random
import pygame
from typing import Optional, Tuple, List, Dict
from settings import LARGURA, COR_OBST
from models.player import Player

# nomes oficiais
INVENCIVEL = "invencibilidade"
TAM_MAIOR  = "aumento_tamanho"
TAM_MENOR  = "reducao_tamanho"
VEL_MENOR  = "reducao_velocidade"
VEL_MAIOR  = "aumento_velocidade"

# catálogo: só duração (cor vem de COR_OBST para ficar igual ao obstáculo)
CATALOGO_DUR: Dict[str, float] = {
    INVENCIVEL: 4.0,    # i-frames um pouco maiores
    TAM_MAIOR:  10.0,   # ↑ tamanho dura mais
    TAM_MENOR:  10.0,   # ↓ tamanho dura mais
    VEL_MENOR:  6.0,    # mundo mais lento
    VEL_MAIOR:  6.0,    # mundo mais rápido
}
TODOS_EFEITOS = [INVENCIVEL, TAM_MAIOR, TAM_MENOR, VEL_MENOR, VEL_MAIOR]


class PowerUp:
    """Coletável genérico: visual igual ao obstáculo; efeito é decidido no momento da coleta (RNG)."""
    RADIUS = 16

    def __init__(self, x: int):
        y = Player.CHAO_Y - 60
        self.rect = pygame.Rect(x - self.RADIUS, y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)
        self.ativo = True
        # velocidade é sincronizada pelo game.py a cada frame (não fixa aqui)
        self.vel_x = 0.0

    def atualizar(self, dt: float):
        self.rect.x -= int(self.vel_x * dt)
        if self.rect.right < 0:
            self.ativo = False

    def desenhar(self, tela: pygame.Surface):
        # mesma cor dos obstáculos
        pygame.draw.circle(tela, COR_OBST, self.rect.center, self.RADIUS)

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