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

        # Ícones de HUD básicos
        self.icon_coracao: pygame.Surface | None   = None   # coração (vidas)
        self.icon_ampulheta: pygame.Surface | None = None   # ampulheta do timer

        # Ícones de power-ups: nome_do_powerup -> Surface
        self.icons: Dict[str, pygame.Surface] = {}

    # Registrar imagens para os power-ups da HUD
    def set_icons(self, mapping: Dict[str, pygame.Surface]):
        self.icons = dict(mapping) if mapping else {}

    def desenhar(self, tela: pygame.Surface,
             vidas: int,
             pontos: int,
             timer_seg: Optional[float] = None,
             powerups: Optional[List[str]] = None,
             xp_mult: Optional[float] = None):
        
        margin = 20
        spacing = 10

        # 1) Pontuação — topo ESQUERDO
        txt_pts = self.fonte_media.render(f"Pontuação: {pontos}", True, VERDE_TXT)
        tela.blit(txt_pts, (margin, margin))
        
        # 1.1) Multiplicador XP
        if xp_mult is not None:
            txt_mult = self.fonte_pequena.render(f"x{xp_mult:.2f}", True, (255, 255, 100))
            # canto inferior direito
            x = LARGURA - txt_mult.get_width() - 20
            y = ALTURA - txt_mult.get_height() - 20
            tela.blit(txt_mult, (x, y))
        # 2) Timer — CENTRO superior (mm:ss)
        if timer_seg is not None:
            t = max(0, int(timer_seg))
            mm, ss = divmod(t, 60)
            txt_timer = self.fonte_media.render(f"{mm:02d}:{ss:02d}", True, VERDE_TXT)

            # posição do texto
            x_txt = LARGURA // 2 - txt_timer.get_width() // 2
            y_txt = margin
            tela.blit(txt_timer, (x_txt, y_txt))

            # desenhar ampulheta ao lado do timer (se existir)
            
            if self.icon_ampulheta is not None:
                tam_icon = txt_timer.get_height() + 20
                surf_amp = pygame.transform.smoothscale(
                    self.icon_ampulheta, (tam_icon, tam_icon)
                )
                # coloca a ampulheta à esquerda do texto, centralizada verticalmente
                x_amp = x_txt - tam_icon - 8
                y_amp = y_txt + (txt_timer.get_height() - tam_icon) // 2
                tela.blit(surf_amp, (x_amp, y_amp))
            else:
                # fallback antigo: círculo marrom atrás do timer
                cx = LARGURA // 2
                cy = margin + txt_timer.get_height() // 2 + 2
                pygame.draw.circle(
                    tela,
                    (70, 50, 20),
                    (cx - txt_timer.get_width() // 2 - 18, cy),
                    16,
                )

        # 3) Vidas — topo DIREITO (alinhado à direita)
        cor_coracao = (255, 70, 70)
        heart_size = 30  # tamanho do coração/ícone
        total_w = vidas * heart_size + (vidas - 1) * spacing if vidas > 0 else 0
        start_x = LARGURA - margin - total_w
        y = margin + 2

        for i in range(vidas):
            x = start_x + i * (heart_size + spacing)
            if self.icon_coracao is not None:
                # usa o PNG de coração
                surf_coracao = pygame.transform.smoothscale(
                    self.icon_coracao, (heart_size, heart_size)
                )
                tela.blit(surf_coracao, (x, y))
            else:
                # fallback: coração desenhado por polígonos
                self._draw_heart(tela, x, y, heart_size, cor_coracao)

        # 4) Power-ups — linha ABAIXO das vidas, alinhados à direita
        if powerups:
            icon_size = 32  # tamanho do ícone na HUD
            y_icons = y + heart_size + 10
            total_pw = len(powerups) * icon_size + (len(powerups) - 1) * 8
            x_icons = LARGURA - margin - total_pw

            for i, nome in enumerate(powerups):
                x = x_icons + i * (icon_size + 8)

                if nome in self.icons:
                    surf_icon = pygame.transform.smoothscale(
                        self.icons[nome], (icon_size, icon_size)
                    )
                    tela.blit(surf_icon, (x, y_icons))
                else:
                    # fallback: badge circular com a inicial do efeito
                    pygame.draw.circle(
                        tela,
                        OURO,
                        (x + icon_size // 2, y_icons + icon_size // 2),
                        icon_size // 2,
                    )
                    letra = self.fonte_pequena.render(
                        nome[:1].upper(), True, (60, 40, 10)
                    )
                    tela.blit(
                        letra,
                        (
                            x + (icon_size - letra.get_width()) // 2,
                            y_icons + (icon_size - letra.get_height()) // 2,
                        ),
                    )

    # ----- util (fallback de coração desenhado) -----
    def _draw_heart(self, tela, x, y, size, cor):
        r = size // 2
        pygame.draw.circle(tela, cor, (x + r // 2, y + r // 2), r // 2)
        pygame.draw.circle(tela, cor, (x + r + r // 2, y + r // 2), r // 2)
        pts = [(x, y + r // 2), (x + r, y + size), (x + size, y + r // 2)]
        pygame.draw.polygon(tela, cor, pts)