import random
import pygame
from settings import LARGURA, COR_OBST
from models.player import Player

# Catálogo simples (ajuste tamanhos se quiser)
CATALOGO_OBST = {
    "tronco_baixo": {"w": 70, "h": 40, "y_offset": 0},
    "pedra":        {"w": 50, "h": 50, "y_offset": 0},
    "tronco_alto":  {"w": 60, "h": 90, "y_offset": 0},
}

class Obstaculo:
    def __init__(self, tipo: str, x_inicial: int, velocidade: float):
        if tipo not in CATALOGO_OBST:
            raise ValueError(f"Tipo de obstáculo desconhecido: {tipo}")
        spec = CATALOGO_OBST[tipo]
        w, h = spec["w"], spec["h"]
        y = Player.CHAO_Y - h - spec.get("y_offset", 0)

        self.tipo = tipo
        self.rect = pygame.Rect(x_inicial, y, w, h)
        self.velocidade = float(velocidade)

    def atualizar(self, dt: float):
        # IMPORTANTE: usa self.velocidade (injeção do game.py)
        self.rect.x -= int(self.velocidade * dt)

    def desenhar(self, tela: pygame.Surface):
        pygame.draw.rect(tela, COR_OBST, self.rect, border_radius=6)

    def saiu_da_tela(self) -> bool:
        return self.rect.right < 0


class SpawnerObstaculos:
    """Controla o spawn e garante espaçamento mínimo."""
    def __init__(self, intervalo_base: float = 1.4, gap_base_px: int = 200):
        self.intervalo_base = intervalo_base
        self.timer = 0.0
        self.tipos = list(CATALOGO_OBST.keys())
        self.gap_base_px = gap_base_px
        self.grace_timer = 0.0
        self.ultimo_tipo = None

    def bloquear(self, segundos: float):
        self.grace_timer = max(self.grace_timer, segundos)

    def _ultimo_right(self, lista: list[Obstaculo]) -> int:
        return max((o.rect.right for o in lista), default=-10_000)

    def atualizar(self, dt: float, escala: float, lista: list[Obstaculo]):
        # pausa temporária
        if self.grace_timer > 0:
            self.grace_timer -= dt
            return

        # intervalo diminui com a escala (mais difícil = mais spawn)
        self.timer -= dt
        intervalo = max(0.5, self.intervalo_base / max(0.8, min(2.5, escala)))

        if self.timer <= 0:
            if self._tentar_spawn(escala, lista):
                self.timer = intervalo
            else:
                self.timer = 0.15  # tenta de novo rapidinho

    def _tentar_spawn(self, escala: float, lista: list[Obstaculo]) -> bool:
        ultimo_right = self._ultimo_right(lista)

        # gap mínimo cresce levemente com a escala
        gap_min = int(self.gap_base_px * (0.9 + 0.2 * max(1.0, escala)))
        if ultimo_right > LARGURA - gap_min:
            return False

        # escolhe tipo evitando repetição de "alto" em sequência
        tipo = random.choice(self.tipos)
        if self.ultimo_tipo == "tronco_alto" and tipo == "tronco_alto":
            tipo = "pedra"
        self.ultimo_tipo = tipo

        # VELOCIDADE do obstáculo = 300 * escala recebida do game.py
        velocidade = 300 * max(0.5, escala)

        start_x = max(LARGURA + 40, ultimo_right + gap_min, LARGURA + random.randint(0, 220))
        lista.append(Obstaculo(tipo, start_x, velocidade))
        return True


def verificar_colisoes(player, obstaculos: list[Obstaculo]) -> bool:
    pr = player.rect
    for o in obstaculos:
        if pr.colliderect(o.rect):
            return True
    return False