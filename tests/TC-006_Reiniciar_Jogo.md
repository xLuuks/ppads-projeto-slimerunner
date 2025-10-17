
# 🧪 Plano de Teste — TC-006 Reiniciar Jogo

**Projeto:** Slime Runner  
**Versão:** 1.0  
**Data:** 16/10/2025  
**Caso de Uso:** UC011 – Reiniciar Jogo 
---

| **Informação** | **Descrição** |
|-----------------|----------------|
| **Identificação única** | TST-012 Reiniciar o jogo após tela de Game Over |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogo está em estado `ESTADO_GAMEOVER`, após o jogador perder todas as vidas. A tela exibe a mensagem “Game Over” e a pontuação final. |
| **Passos para execução** | 1. Aguardar o estado `ESTADO_GAMEOVER`.<br>2. Pressionar a tecla **ENTER** (ou **ESPACO**, conforme mapeado no código).<br>3. Observar a reinicialização do jogo e o retorno ao estado de jogo ativo (`ESTADO_JOGANDO`). |
| **Resultado esperado** | - O evento de tecla `pygame.KEYDOWN` para ENTER/ESPAÇO é capturado.<br>- O jogo redefine `status.vidas = 3`, `status.pontos = 0` e `status.game_over = False`.<br>- O estado é alterado para `ESTADO_JOGANDO` e o cenário é reiniciado (função `reiniciar_jogo()` é chamada).<br>- A nova partida começa normalmente. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | 
