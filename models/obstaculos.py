import pygame
import random
from settings import LARGURA
from models.player import Player  # para saber o Y do chão

# Catálogo de obstáculos (nomes, tamanhos e cores)
CATALOGO_OBST = {
    "pedra":        {"w": 52, "h": 40, "y": lambda: Player.CHAO_Y - 40, "cor": (140, 100, 80)},
    "tronco_baixo": {"w": 80, "h": 48, "y": lambda: Player.CHAO_Y - 48, "cor": (110, 70, 40)},
    "tronco_alto":  {"w": 48, "h": 70, "y": lambda: Player.CHAO_Y - 70, "cor": (120, 80, 45)},
    "espinhos":     {"w": 64, "h": 32, "y": lambda: Player.CHAO_Y - 32, "cor": (160, 160, 160)},
}


class Obstaculo:
    """Representa um obstáculo individual no jogo."""

    def __init__(self, tipo: str, x: int, velocidade: float):
        spec = CATALOGO_OBST[tipo]
        y = spec["y"]()
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, spec["w"], spec["h"])
        self.velocidade = velocidade
        self.cor = spec["cor"]

    def atualizar(self, dt: float):
        """Move o obstáculo para a esquerda."""
        self.rect.x -= int(self.velocidade * dt)

    def desenhar(self, tela: pygame.Surface):
        """Desenha o obstáculo (forma simples)."""
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)
        # (opcional) adicione sprites aqui no futuro

    def saiu_da_tela(self) -> bool:
        """Retorna True se o obstáculo saiu da tela."""
        return self.rect.right < 0


class SpawnerObstaculos:
    """Controla o spawn de obstáculos garantindo espaçamento mínimo."""
    def __init__(self, intervalo_base: float = 1.4, gap_base_px: int = 180):
        self.intervalo_base = intervalo_base
        self.timer = 0.0
        self.tipos = list(CATALOGO_OBST.keys())
        self.gap_base_px = gap_base_px   # distância mínima na TELA entre obstáculos
        self.grace_timer = 0.0           # bloqueio temporário (ex.: após colisão)

    def bloquear(self, segundos: float):
        """Impede spawn por 'segundos' (use ao sofrer dano, por exemplo)."""
        self.grace_timer = max(self.grace_timer, segundos)

    def _ultimo_right(self, lista: list[Obstaculo]) -> int:
        """right do obstáculo mais à direita (maior X)."""
        return max((o.rect.right for o in lista), default=-10_000)

    def atualizar(self, dt: float, dificuldade: float, lista: list[Obstaculo]):
        # grace/bloqueio
        if self.grace_timer > 0:
            self.grace_timer -= dt
            return

        # timer baseado em dificuldade
        self.timer -= dt
        intervalo = max(0.5, self.intervalo_base / dificuldade)

        if self.timer <= 0:
            # tenta spawn respeitando gap; se não der, adia um pouco
            if self._tentar_spawn(dificuldade, lista):
                self.timer = intervalo
            else:
                self.timer = 0.15  # re-tenta em 150ms

    def _tentar_spawn(self, dificuldade: float, lista: list[Obstaculo]) -> bool:
        ultimo_right = self._ultimo_right(lista)

        # gap mínimo cresce um pouco com a dificuldade e com a largura típica
        # (mantém o jogo justo mesmo acelerando)
        gap_min = int(self.gap_base_px * (0.9 + 0.2 * dificuldade))
        # se ainda há obstáculo muito perto da borda direita, não spawna
        # queremos: "na tela" haja ao menos gap_min livre antes do próximo
        if ultimo_right > LARGURA - gap_min:
            return False

        # escolhe tipo e calcula velocidade
        tipo = random.choice(self.tipos)
        spec = CATALOGO_OBST[tipo]
        velocidade = 300 * dificuldade

        # posiciona garantindo que não apareça colado fora da tela
        # e que respeite gap ao último obstáculo
        start_x = max(LARGURA + 40, ultimo_right + gap_min, LARGURA + random.randint(0, 220))
        lista.append(Obstaculo(tipo, start_x, velocidade))
        return True

def verificar_colisoes(player, lista_obstaculos: list[Obstaculo]) -> bool:
    """Retorna True se houve colisão entre o player e qualquer obstáculo."""
    for obst in lista_obstaculos:
        if player.rect.colliderect(obst.rect):
            return True
    return False