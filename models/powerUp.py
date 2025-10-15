# models/powerUp.py
import random
import pygame
from typing import Optional, Dict, List, Tuple
from settings import LARGURA
from models.player import Player

# -------- nomes oficiais (use para aparecer no HUD) --------
INVENCIVEL = "invencibilidade"
TAM_MAIOR  = "aumento_tamanho"
TAM_MENOR  = "reducao_tamanho"
VEL_MENOR  = "reducao_velocidade"
VEL_MAIOR  = "aumento_velocidade"

# catálogo (cores só para fallback visual; troque por ícones quando quiser)
CATALOGO_POWER: Dict[str, Dict] = {
    INVENCIVEL: {"dur": 3.0, "cor": (80, 200, 255)},     # i-frames
    TAM_MAIOR:  {"dur": 6.0, "cor": (255, 150, 60)},     # ~+30% tamanho
    TAM_MENOR:  {"dur": 6.0, "cor": (160, 200, 255)},    # ~-25% tamanho
    VEL_MENOR:  {"dur": 5.0, "cor": (255, 210, 90)},     # mundo 0.75x
    VEL_MAIOR:  {"dur": 5.0, "cor": (120, 255, 120)},    # mundo 1.25x
}

class PowerUp:
    """
    Item coletável.
    - Efeitos de tamanho são aplicados direto no Player (usam set_size_mult/reset).
    - Invencibilidade é aplicada no Status (i-frames).
    - Efeitos de velocidade retornam um multiplicador para o game.py aplicar no "mundo".
    """
    RADIUS = 16
    VEL_X = 250.0  # px/s

    def __init__(self, tipo: str, x: int):
        if tipo not in CATALOGO_POWER:
            raise ValueError(f"PowerUp desconhecido: {tipo}")
        self.tipo = tipo
        self.duracao = float(CATALOGO_POWER[tipo]["dur"])
        self.cor = CATALOGO_POWER[tipo]["cor"]
        # flutua um pouco acima do chão
        y = Player.CHAO_Y - 60
        self.rect = pygame.Rect(x - self.RADIUS, y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)
        self.ativo = True

    # --------------- ciclo ---------------
    def atualizar(self, dt: float):
        self.rect.x -= int(self.VEL_X * dt)
        if self.rect.right < 0:
            self.ativo = False

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.circle(tela, self.cor, self.rect.center, self.RADIUS)

    # --------------- coleta / efeito ---------------
    def coletar(self, status, player) -> Optional[Tuple[float, float]]:
        """
        Aplica efeitos imediatos.
        Retorna (world_speed_mult, duracao) para o game.py aplicar no mundo
        quando o power-up for de velocidade; caso contrário retorna None.
        """
        # todos aparecem no HUD via Status
        status.conceder_powerup(self.tipo, self.duracao)

        if self.tipo == INVENCIVEL:
            # invulnerável (i-frames) controlado pelo Status
            status.invulneravel = True
            status._invuln_restante = max(status._invuln_restante, self.duracao)

        elif self.tipo == TAM_MAIOR:
            # ~+30% do tamanho atual
            mult = getattr(player, "size_mult", 1.0) * 1.3
            if hasattr(player, "set_size_mult"):
                player.set_size_mult(mult)

        elif self.tipo == TAM_MENOR:
            # ~-25% do tamanho atual
            mult = getattr(player, "size_mult", 1.0) * 0.75
            if hasattr(player, "set_size_mult"):
                player.set_size_mult(mult)

        elif self.tipo == VEL_MENOR:
            return (0.75, self.duracao)  # mundo mais lento (dur segundos)

        elif self.tipo == VEL_MAIOR:
            return (1.25, self.duracao)  # mundo mais rápido (dur segundos)

        # para os demais, nada a retornar
        return None


class SpawnerPowerUp:
    """Spawna power-ups com baixa frequência e posição segura."""
    def __init__(self, intervalo_base: float = 9.0):
        self.intervalo_base = intervalo_base
        self.timer = 0.0
        self.tipos: List[str] = list(CATALOGO_POWER.keys())

    def atualizar(self, dt: float, lista_powerups: List[PowerUp]):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.intervalo_base + random.uniform(3, 6)
            tipo = random.choice(self.tipos)
            x = LARGURA + random.randint(220, 420)
            lista_powerups.append(PowerUp(tipo, x))