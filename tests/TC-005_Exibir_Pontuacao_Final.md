
#  Plano de Teste — TC-005 Exibir Pontuação Final

**Projeto:** Slime Runner  
**Versão:** 1.0  
**Data:** 16/10/2025  
**Caso de Uso:** UC010 – Exibir Pontuação Final  

---

| **Informação** | **Descrição** |
|-----------------|----------------|
| **Identificação única** | TST-011 Exibir pontuação final ao encerrar o jogo |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogador inicia o jogo normalmente, com `status.pontos` aumentando durante a partida. O jogo está configurado para transicionar ao estado `ESTADO_GAMEOVER` quando `status.vidas = 0`. |
| **Passos para execução** | 1. Iniciar o jogo e jogar normalmente.<br>2. Colidir com obstáculos até que todas as vidas (`status.vidas`) sejam perdidas.<br>3. Aguardar a transição automática para o estado de `GAME_OVER`.<br>4. Observar a exibição da pontuação final na tela. |
| **Resultado esperado** | - O jogo entra no estado `GAME_OVER`.<br>- A pontuação total (`status.pontos`) acumulada é exibida na tela de fim de jogo.<br>- O texto da pontuação deve ser renderizado usando a função `desenhar_texto()` (localizada em `game.py`), indicando “Pontuação Final: X pontos”. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | __________________________________ |
| **Data da execução** | ___ / ___ / 2025 |

---

### **Observações técnicas**
- O valor mostrado é obtido de `status.pontos`, atualizado durante o loop principal (`Status.adicionar_pontos()`).  
- A função de exibição é chamada durante o estado `ESTADO_GAMEOVER`, antes da reinicialização.  
- Deve-se confirmar que o texto é centralizado na tela (`pygame.display`) e atualizado com `pygame.display.flip()`.

