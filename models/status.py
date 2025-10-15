from __future__ import annotations

class Status:
    """
    Controla vidas, pontos, invulnerabilidade (i-frames) e power-ups temporários.
    """
    def __init__(self, vidas_iniciais: int = 3):
        self.vidas_iniciais = vidas_iniciais
        self.resetar()

    # ---------- ciclo de vida ----------
    def resetar(self):
        self.vidas: int = self.vidas_iniciais
        self.pontos: float = 0.0
        self.invulneravel: bool = False
        self._invuln_restante: float = 0.0
        # powerups: nome -> segundos restantes
        self.powerups: dict[str, float] = {}

    def atualizar(self, dt: float):
        # i-frames
        if self.invulneravel:
            self._invuln_restante -= dt
            if self._invuln_restante <= 0:
                self.invulneravel = False
                self._invuln_restante = 0.0

        # power-ups temporários
        if self.powerups:
            expirados = []
            for nome, t in self.powerups.items():
                t -= dt
                if t <= 0:
                    expirados.append(nome)
                else:
                    self.powerups[nome] = t
            for nome in expirados:
                del self.powerups[nome]

    # ---------- eventos ----------
    def sofrer_dano(self, dano: int = 1, iframes: float = 0.8) -> bool:
        """
        Aplica dano se não estiver invulnerável. Retorna True se aplicou dano.
        """
        if self.invulneravel:
            return False
        self.vidas -= dano
        if iframes > 0:
            self.invulneravel = True
            self._invuln_restante = iframes
        return True

    def adicionar_pontos(self, qtd: float):
        self.pontos += qtd

    def conceder_powerup(self, nome: str, duracao_seg: float):
        if duracao_seg > 0:
            self.powerups[nome] = duracao_seg

    def remover_powerup(self, nome: str):
        self.powerups.pop(nome, None)

    # ---------- consultas ----------
    @property
    def game_over(self) -> bool:
        return self.vidas <= 0