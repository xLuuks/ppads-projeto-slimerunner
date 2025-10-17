# 🧪 TC-001 – Iniciar Jogo
**Caso de Uso:** UC-001 – Iniciar Jogo  
**Objetivo:** Verificar se o jogo inicia corretamente a partir do menu principal.  
**Arquivo principal:** `game.py` – método `_processar_eventos()`  

---

## 🎮 TST-001 – Início bem-sucedido
**Cenário:** Fluxo principal  
**Preparação:**
- O jogo está na tela inicial (`ESTADO_MENU`)

**Passos:**
1. Executar `main.py`
2. Pressionar **ENTER** ou **ESPAÇO**
3. Aguardar o início da partida

**Resultado Esperado:**
- O estado do jogo muda para `ESTADO_JOGANDO`
- O slime aparece na tela e o fundo começa a se mover

**Resultado do Teste:** ☐ Não Executado ☐ Sucesso ☐ Falha ☐ Cancelado  
**Data:** ___ / ___ / 2025  
