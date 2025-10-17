# 🧪 TC-003 – Colidir com Obstáculo
**Caso de Uso:** UC-003 – Colidir com Obstáculo  
**Objetivo:** Verificar se o jogador perde vida ao colidir com um obstáculo e se o jogo encerra quando as vidas acabam.  
**Arquivo principal:** `game.py` – função `verificar_colisoes()`  

---

## 🎮 TST-004 – Dano por colisão
**Cenário:** Fluxo principal  
**Preparação:**
- O jogador possui 3 vidas  
- Um obstáculo está posicionado à frente  

**Passos:**
1. Mover o slime até encostar no obstáculo  
2. Observar o HUD  

**Resultado Esperado:**
- A vida é reduzida em 1 unidade  
- O som de dano é reproduzido  
- O HUD é atualizado  

**Resultado do Teste:** ☐ Não Executado ☐ Sucesso ☐ Falha ☐ Cancelado  
**Data:** ___ / ___ / 2025  

---

## 💀 TST-005 – Fim de jogo após colisões sucessivas
**Cenário:** Fluxo alternativo  
**Preparação:**
- O jogador possui apenas 1 vida  

**Passos:**
1. Causar uma colisão com obstáculo  
2. Aguardar o estado do jogo mudar  

**Resultado Esperado:**
- O jogo muda para `ESTADO_GAMEOVER`  
- A tela exibe o menu de reinício com a pontuação final  

**Resultado do Teste:** ☐ Não Executado ☐ Sucesso ☐ Falha ☐ Cancelado  
**Data:** ___ / ___ / 2025  
