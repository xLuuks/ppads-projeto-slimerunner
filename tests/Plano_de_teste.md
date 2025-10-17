# Plano e Scripts de Teste de Cenário – Slime Runner
**Componente Curricular:** Práticas Profissionais em Análise e Desenvolvimento de Sistemas  
**Equipe:** Eduardo Afonso P. Ferreira, Bruno Otavio Ramos, João Rinaldo França Neris, Lucas Augusto Correia Alves, Rodrigo Luiz Gomes da Silva  
**Versão:** 2.0   
**Linguagem:** Python 3.12+  
**Bibliotecas:** Pygame  

---

## Objetivo do Documento
Este plano tem como objetivo validar as **funcionalidades centrais do jogo _Slime Runner – Corrida na Floresta_**, com base nos **casos de uso definidos** e no comportamento do sistema durante a execução.  
Os testes aqui descritos seguem o modelo de **testes de cenário (release testing)** conforme Sommerville (2018), avaliando o comportamento funcional do sistema e sua conformidade com os requisitos definidos no código-fonte.  

Cada **script de teste (TST)** contém a preparação, passos, resultado esperado, observações técnicas e espaço para o resultado obtido.  

---

## TST001 – Início Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC001 – Iniciar Jogo |
| **Cenário** | Fluxo principal |
| **Preparação (condição inicial)** | O jogo está na tela inicial (`ESTADO_MENU`) definida em `states.py`. |
| **Passos para execução do teste** | 1. Executar `main.py`.<br>2. Pressionar **ENTER** ou **ESPAÇO**.<br>3. Aguardar a transição para o estado de jogo. |
| **Resultado esperado** | O método `_processar_eventos()` em `game.py` muda o estado de `MENU` para `JOGANDO`, iniciando o loop principal (`run()`). |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Código relacionado: `game._processar_eventos()` e `states.ESTADO_JOGANDO`.
- O jogador (`Player`) é instanciado no início do estado de jogo.  

---

## TST002 – Movimento Lateral
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está em execução (`ESTADO_JOGANDO`). |
| **Passos para execução do teste** | 1. Pressionar **→** (direita).<br>2. Pressionar **←** (esquerda). |
| **Resultado esperado** | O método `Player.mover_horizontal()` em `models/player.py` atualiza a posição `x` do personagem sem sair da tela. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- A velocidade horizontal é definida em `settings.py` (`VEL_HORIZONTAL`).  
- A atualização ocorre no método `Player.atualizar()`, chamado a cada frame.  

---

## TST003 – Pulo Bem-Sucedido
| Informação | Descrição |
|-------------|------------|
| **Caso de uso em que se baseia** | UC002 – Controlar Slime |
| **Cenário** | Fluxo principal |
| **Preparação** | O slime está em contato com o chão (`Player.no_chao = True`). |
| **Passos para execução do teste** | 1. Pressionar **ESPAÇO** ou **W**.<br>2. Observar o movimento vertical do personagem. |
| **Resultado esperado** | O método `Player.pular()` aplica `FORCA_PULO` e `GRAVIDADE`, alterando a variável `vel_y`. O slime sobe e retorna ao solo. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Constantes usadas: `FORCA_PULO` e `GRAVIDADE` em `settings.py`.  
- A posição é atualizada por `Player.atualizar()` a cada frame.  

---

## TST004 – Dano por Colisão
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador possui 3 vidas e um obstáculo ativo na tela. |
| **Passos** | 1. Aproximar o slime de um obstáculo.<br>2. Colidir com ele.<br>3. Observar a redução de vidas. |
| **Resultado esperado** | O método `verificar_colisoes()` em `game.py` detecta colisão e chama `Status.sofrer_dano()` em `models/status.py`, reduzindo 1 vida. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Classes envolvidas: `Obstaculo` (models/obstaculos.py), `Status` (models/status.py).  
- Após o dano, o HUD é atualizado por `Hud.desenhar()` (ui/hud.py).  

---

## TST005 – Fim de Jogo Após Colisões Sucessivas
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC003 – Colidir com Obstáculo |
| **Cenário** | Fluxo alternativo |
| **Preparação** | O jogador possui 1 vida restante. |
| **Passos** | 1. Colidir novamente com um obstáculo.<br>2. Observar o encerramento da partida. |
| **Resultado esperado** | Ao atingir 0 vidas, `Status.sofrer_dano()` retorna `False`, acionando o estado `ESTADO_GAMEOVER` em `game.py`. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- O método `_reiniciar_partida()` é chamado quando o jogador decide recomeçar.  
- `Hud.desenhar()` exibe a pontuação final e a mensagem “Pressione Enter para reiniciar”.  

---

## TST006 – Power-Up de Velocidade
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo principal |
| **Preparação** | Um item de power-up de velocidade aparece no cenário. |
| **Passos** | 1. Colidir com o item `PowerUp`.<br>2. Observar o aumento de velocidade. |
| **Resultado esperado** | O método `PowerUp.coletar()` ativa o efeito `VEL_MAIOR`, alterando temporariamente a variável `vel_x` do jogador. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Código relacionado: `models/powerUp.py` e `Status.conceder_powerup()`.  
- O HUD exibe o ícone do efeito ativo enquanto durar o status.  

---

## TST007 – Power-Up de Invencibilidade
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC004 – Coletar Power-Up |
| **Cenário** | Fluxo alternativo |
| **Preparação** | Um item de invencibilidade está disponível. |
| **Passos** | 1. Coletar o power-up.<br>2. Colidir com obstáculo durante o efeito ativo. |
| **Resultado esperado** | `Status.invulneravel = True`, o dano é ignorado e o HUD exibe o status ativo. Após o tempo de duração, o efeito é removido. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Implementado em `PowerUp.coletar()` e `Status.verificar_powerups()`.  
- O cronômetro de duração é decrementado a cada frame.  

---

## TST008 – Exibição de Pontuação Final
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC005 – Exibir Pontuação Final |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogador termina a partida após colisão fatal. |
| **Passos** | 1. Jogar até o estado `GAME_OVER`.<br>2. Observar a tela final. |
| **Resultado esperado** | O método `Hud.desenhar()` exibe corretamente a pontuação final, usando o valor retornado de `Status.pontos`. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- A pontuação é gerenciada por `Status.adicionar_pontos()` e atualizada a cada obstáculo superado.  
- O método `pygame.display.flip()` é usado para atualizar o frame final.  

---

## TST009 – Reinício Após Game Over
| Informação | Descrição |
|-------------|------------|
| **Caso** | UC001 – Reiniciar Partida |
| **Cenário** | Fluxo principal |
| **Preparação** | O jogo está no estado `ESTADO_GAMEOVER`. |
| **Passos** | 1. Pressionar **ENTER** ou **ESPAÇO**.<br>2. Aguardar reinicialização do jogo. |
| **Resultado esperado** | O método `_reiniciar_partida()` em `game.py` restaura as variáveis: vidas, pontos e velocidade, voltando para `ESTADO_JOGANDO`. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** | ____________ |
| **Data da execução** | ___ / ___ / 2025 |

### Observações técnicas
- Função `_reiniciar_partida()` redefine `Status`, `Player`, `Obstaculo` e `PowerUp`.  
- A tela volta ao loop principal de `Jogo.run()`.  

---

### Referências
- LARMAN, Craig. *Utilizando UML e Padrões.* Porto Alegre: Bookman, 2011.  
- PRESSMAN, Roger S. *Engenharia de Software: uma abordagem profissional.* 8. ed. Porto Alegre: AMGH, 2016.  
- SOMMERVILLE, Ian. *Engenharia de Software.* 10. ed. São Paulo: Pearson, 2019.  
