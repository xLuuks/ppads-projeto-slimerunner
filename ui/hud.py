import pygame
from typing import List, Optional, Dict
from settings import LARGURA, ALTURA

VERDE_TXT = (0, 230, 0)
BRANCO    = (255, 255, 255)
OURO      = (240, 200, 80)

class Hud:
    def __init__(self):
        self.fonte_grande  = pygame.font.SysFont("consolas", 32, bold=True)
        self.fonte_media   = pygame.font.SysFont("consolas", 24, bold=True)
        self.fonte_pequena = pygame.font.SysFont("consolas", 18)

        # se quiser usar imagens, injete via set_icons({'escudo': Surface, ...})
        self.icons: Dict[str, pygame.Surface] = {}

    # opcional: registrar imagens reais para power-ups
    def set_icons(self, mapping: Dict[str, pygame.Surface]):
        self.icons = mapping or {}

    def desenhar(self, tela: pygame.Surface,
                 vidas: int,
                 pontos: int,
                 timer_seg: Optional[float] = None,
                 powerups: Optional[List[str]] = None):
        margin = 20
        spacing = 10

        # 1) Pontuação — topo ESQUERDO
        txt_pts = self.fonte_media.render(f"Pontuação: {pontos}", True, VERDE_TXT)
        tela.blit(txt_pts, (margin, margin))

        # 2) Timer — CENTRO superior (mm:ss)
        if timer_seg is not None:
            t = max(0, int(timer_seg))
            mm, ss = divmod(t, 60)
            txt_timer = self.fonte_media.render(f"{mm:02d}:{ss:02d}", True, VERDE_TXT)
            tela.blit(txt_timer, (LARGURA // 2 - txt_timer.get_width() // 2, margin))

            # (opcional) “medalhão” atrás do timer
            cx = LARGURA // 2
            cy = margin + txt_timer.get_height() // 2 + 2
            pygame.draw.circle(tela, (70, 50, 20), (cx - txt_timer.get_width() // 2 - 18, cy), 16)

        # 3) Vidas — topo DIREITO (alinhado à direita)
        cor_coracao = (255, 70, 70)
        heart_w = 22
        total_w = vidas * heart_w + (vidas - 1) * spacing if vidas > 0 else 0
        start_x = LARGURA - margin - total_w
        y = margin + 2
        for i in range(vidas):
            x = start_x + i * (heart_w + spacing)
            self._draw_heart(tela, x, y, heart_w, cor_coracao)

        # 4) Power-ups — linha ABAIXO das vidas, alinhados à direita
        if powerups:
            icon_size = 28
            y_icons = y + heart_w + 10
            total_pw = len(powerups) * icon_size + (len(powerups) - 1) * 8
            x_icons = LARGURA - margin - total_pw
            for i, nome in enumerate(powerups):
                x = x_icons + i * (icon_size + 8)
                if nome in self.icons:
                    surf = pygame.transform.smoothscale(self.icons[nome], (icon_size, icon_size))
                    tela.blit(surf, (x, y_icons))
                else:
                    # fallback: badge circular com letra
                    pygame.draw.circle(tela, OURO, (x + icon_size // 2, y_icons + icon_size // 2), icon_size // 2)
                    letra = self.fonte_pequena.render(nome[:1].upper(), True, (60, 40, 10))
                    tela.blit(letra, (x + (icon_size - letra.get_width())//2, y_icons + (icon_size - letra.get_height())//2))

    # ----- util -----
    def _draw_heart(self, tela, x, y, size, cor):
        r = size // 2
        pygame.draw.circle(tela, cor, (x + r//2, y + r//2), r//2)
        pygame.draw.circle(tela, cor, (x + r + r//2, y + r//2), r//2)
        pts = [(x, y + r//2), (x + r, y + size), (x + size, y + r//2)]
        pygame.draw.polygon(tela, cor, pts)