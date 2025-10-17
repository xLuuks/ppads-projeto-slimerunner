---

| **Informação** | **Descrição** |
|-----------------|----------------|
| **Identificação única** | TST-012 Reiniciar o jogo após tela de Game Over |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogo está em estado `ESTADO_GAMEOVER`, após o jogador perder todas as vidas. A tela exibe a mensagem “Game Over” e a pontuação final. |
| **Passos para execução** | 1. Aguardar o estado `ESTADO_GAMEOVER`.<br>2. Pressionar a tecla **ENTER** (ou **ESPACO**, conforme mapeado no código).<br>3. Observar a reinicialização do jogo e o retorno ao estado de jogo ativo (`ESTADO_JOGANDO`). |
| **Resultado esperado** | - O evento de tecla `pygame.KEYDOWN` para ENTER/ESPAÇO é capturado.<br>- O jogo redefine `status.vidas = 3`, `status.pontos = 0` e `status.game_over = False`.<br>- O estado é alterado para `ESTADO_JOGANDO` e o cenário é reiniciado (função `reiniciar_jogo()` é chamada).<br>- A nova partida começa normalmente. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | __________________________________ |
| **Data da execução** | ___ / ___ / 2025 |

---

### **Observações técnicas**
- O comportamento de reinício é definido na função principal do jogo (`game.py`), dentro do bloco de eventos `if estado == ESTADO_GAMEOVER:`.  
- Ao pressionar ENTER, o sistema deve reinicializar os objetos do jogador, obstáculos e power-ups.  
- Confirmar que o fundo, sons e variáveis de status retornam ao estado inicial.  
- Após a reinicialização, a pontuação deve ser exibida novamente iniciando de 0.
