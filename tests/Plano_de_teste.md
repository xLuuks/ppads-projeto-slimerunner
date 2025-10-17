# Plano e Scripts de Teste – Slime Runner
**Componente Curricular:** Práticas Profissionais em Análise e Desenvolvimento de Sistemas  
**Equipe:** Eduardo Afonso P. Ferreira, Bruno Otavio Ramos, João Rinaldo França Neris, Lucas Augusto Correia Alves, Rodrigo Luiz Gomes da Silva  
**Versão:** 1.0  
**Data:** 17/10/2025  
**Ferramentas:** Python 3.12+, Pygame  

---

## 1. Script de Teste – TST001 Início Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC001 – Iniciar Jogo |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogo está na tela inicial (`ESTADO_MENU`). |
| **Passos para execução do teste** | 1. Executar `main.py`.<br>2. Pressionar **ENTER** ou **ESPAÇO**.<br>3. Aguardar o início da partida. |
| **Resultado esperado** | O estado do jogo muda para `ESTADO_JOGANDO` e o slime aparece na tela, iniciando a corrida. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 2. Script de Teste – TST002 Movimento Lateral
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está em execução (`ESTADO_JOGANDO`). |
| **Passos para execução do teste** | 1. Pressionar **→** (direita).<br>2. Pressionar **←** (esquerda). |
| **Resultado esperado** | O slime se move suavemente nas direções correspondentes, sem travamentos. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 3. Script de Teste – TST003 Pulo Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O slime está no chão e pode realizar um salto. |
| **Passos para execução do teste** | 1. Pressionar **ESPAÇO** ou **W**.<br>2. Observar o movimento vertical. |
| **Resultado esperado** | O slime sobe e desce suavemente com a física do jogo (`FORCA_PULO`, `GRAVIDADE`). |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 4. Script de Teste – TST004 Dano por Colisão
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador possui 3 vidas e há um obstáculo à frente. |
| **Passos para execução do teste** | 1. Mover o slime até encostar no obstáculo.<br>2. Observar o HUD. |
| **Resultado esperado** | A vida do jogador é reduzida em 1 unidade e o som de dano é reproduzido. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 5. Script de Teste – TST005 Fim de Jogo Após Colisões
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo alternativo |
| **Preparação** | O jogador possui apenas 1 vida. |
| **Passos para execução do teste** | 1. Colidir com um obstáculo.<br>2. Aguardar o estado do jogo mudar. |
| **Resultado esperado** | O jogo muda para `ESTADO_GAMEOVER` e exibe o menu de reinício. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 6. Script de Teste – TST006 Power-Up de Velocidade
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo principal |
| **Preparação** | Um power-up de velocidade aparece no cenário. |
| **Passos para execução do teste** | 1. Mover o slime até o item.<br>2. Coletar o power-up. |
| **Resultado esperado** | A velocidade horizontal do slime aumenta e o HUD exibe o ícone de efeito ativo. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 7. Script de Teste – TST007 Power-Up de Invencibilidade
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo alternativo |
| **Preparação** | Um power-up de invencibilidade está disponível. |
| **Passos para execução do teste** | 1. Coletar o item.<br>2. Colidir com obstáculo. |
| **Resultado esperado** | O slime não perde vida durante o efeito e o HUD mostra o ícone de invencibilidade. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 8. Script de Teste – TST008 Exibição de Pontuação Final
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC005 – Exibir Pontuação Final |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador finaliza a partida após colisão fatal. |
| **Passos para execução do teste** | 1. Jogar até o estado `GAME_OVER`.<br>2. Observar tela final. |
| **Resultado esperado** | A pontuação final é exibida corretamente e o texto “Game Over” aparece. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---

## 9. Script de Teste – TST009 Reinício Após Game Over
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC001 – Reiniciar Partida |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está no estado `ESTADO_GAMEOVER`. |
| **Passos para execução do teste** | 1. Pressionar **ENTER** ou **ESPAÇO**.<br>2. Aguardar reinício. |
| **Resultado esperado** | O jogo retorna para o estado `ESTADO_JOGANDO` com vidas, pontos e tempo reiniciados. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Data da execução** | ___ / ___ / 2025 |

---
