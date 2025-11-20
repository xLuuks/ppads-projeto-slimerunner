# Plano e Scripts de Teste de Cenário – Slime Runner
**Componente Curricular:** Práticas Profissionais em Análise e Desenvolvimento de Sistemas  
**Equipe:** Eduardo Afonso P. Ferreira, Bruno Otavio Ramos, João Rinaldo França Neris, Lucas Augusto Correia Alves, Rodrigo Luiz Gomes da Silva  
**Data:** 16/10/2025  
**Linguagem:** Python 3.12+  
**Bibliotecas:** Pygame  

---

## TST001 – Início Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC001 – Iniciar Jogo |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogo está na tela inicial (`ESTADO_MENU`) definida em `states.py`. |
| **Passos para execução do teste** | 1. Executar `main.py`.<br>2. Pressionar **ENTER** ou **ESPAÇO**.<br>3. Aguardar a transição para o estado de jogo. |
| **Resultado esperado** | O método `_processar_eventos()` em `game.py` muda o estado de `MENU` para `JOGANDO`, iniciando o loop principal (`run()`). |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | Ao pressionar ENTER, o jogo saiu corretamente da tela de menu e iniciou o estado `JOGANDO`, exibindo o player e o cenário funcionando normalmente. |
| **Data da execução** | 20/11/2025 |

---

## TST002 – Movimento Lateral
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está em execução (`ESTADO_JOGANDO`). |
| **Passos para execução do teste** | 1. Pressionar **→** (direita).<br>2. Pressionar **←** (esquerda). |
| **Resultado esperado** | O método `Player.mover_horizontal()` em `models/player.py` atualiza a posição `x` do personagem sem sair da tela. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | O slime se moveu para a direita e esquerda de forma fluida, respeitando os limites laterais da tela, sem ultrapassar as bordas. |
| **Data da execução** | 20/11/2025 |

---

## TST003 – Pulo Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O slime está em contato com o chão (`Player.no_chao = True`). |
| **Passos para execução do teste** | 1. Pressionar **ESPAÇO** ou **W**.<br>2. Observar o movimento vertical do personagem. |
| **Resultado esperado** | O método `Player.pular()` aplica `FORCA_PULO` e `GRAVIDADE`, alterando a variável `vel_y`. O slime sobe e retorna ao solo. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | O personagem realizou o salto normalmente, subindo e caindo de acordo com a gravidade configurada, sem travamentos ou saltos duplos indevidos. |
| **Data da execução** | 20/11/2025 |

---

## TST004 – Dano por Colisão
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador possui 3 vidas e um obstáculo ativo na tela. |
| **Passos** | 1. Aproximar o slime de um obstáculo.<br>2. Colidir com ele.<br>3. Observar a redução de vidas. |
| **Resultado esperado** | O método `verificar_colisoes()` em `game.py` detecta colisão e chama `Status.sofrer_dano()`, reduzindo 1 vida. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | Ao colidir com o obstáculo, a vida foi reduzida imediatamente e o HUD refletiu a mudança sem atrasos. |
| **Data da execução** | 20/11/2025 |

---

## TST005 – Fim de Jogo Após Colisões Sucessivas
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo alternativo |
| **Preparação** | O jogador possui 1 vida restante. |
| **Passos** | 1. Colidir novamente com um obstáculo.<br>2. Observar o encerramento da partida. |
| **Resultado esperado** | Ao atingir 0 vidas, `Status.sofrer_dano()` retorna `False`, acionando o estado `ESTADO_GAMEOVER`. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | Após a colisão final, o jogo entrou imediatamente no estado GAME OVER e exibiu a pontuação final corretamente. |
| **Data da execução** | 20/11/2025 |

---

## TST006 – Power-Up de Velocidade
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo principal |
| **Preparação** | Um item de power-up de velocidade aparece no cenário. |
| **Passos** | 1. Colidir com o item `PowerUp`.<br>2. Observar o aumento de velocidade. |
| **Resultado esperado** | O método `PowerUp.coletar()` ativa o efeito `VEL_MAIOR`, aumentando temporariamente a velocidade horizontal. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | A velocidade horizontal aumentou perceptivelmente e retornou ao normal após o tempo previsto do efeito. |
| **Data da execução** | 20/11/2025 |

---

## TST007 – Power-Up de Invencibilidade
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo alternativo |
| **Preparação** | Um item de invencibilidade está disponível. |
| **Passos** | 1. Coletar o power-up.<br>2. Colidir com obstáculo durante o efeito ativo. |
| **Resultado esperado** | Com invencibilidade ativa, o dano deve ser ignorado. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | Durante o efeito ativo, as colisões não reduziram vidas. Após o término, o dano voltou a ser aplicado normalmente. |
| **Data da execução** | 20/11/2025 |

---

## TST008 – Exibição de Pontuação Final
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC005 – Exibir Pontuação Final |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador termina a partida após colisão fatal. |
| **Passos** | 1. Jogar até o estado `GAME_OVER`.<br>2. Observar a tela final. |
| **Resultado esperado** | O HUD deve exibir a pontuação final corretamente. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | A pontuação final foi exibida de forma clara na tela de game over, mantendo consistência com os pontos acumulados durante a partida. |
| **Data da execução** | 20/11/2025 |

---

## TST009 – Reinício Após Game Over
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC001 – Reiniciar Partida |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está no estado `ESTADO_GAMEOVER`. |
| **Passos** | 1. Pressionar **ENTER** ou **ESPAÇO**.<br>2. Aguardar reinicialização. |
| **Resultado esperado** | `_reiniciar_partida()` deve resetar o jogo e retornar ao estado `JOGANDO`. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☒ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | Ao pressionar ENTER, o jogo reiniciou corretamente: vidas, pontos e status foram restaurados e o player voltou ao cenário pronto para jogar. |
| **Data da execução** | 20/11/2025 |
