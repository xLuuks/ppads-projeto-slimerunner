# 🧪 TC-004 – Coletar Power-Up
**Caso de Uso:** UC-004 – Coletar Power-Up  
**Objetivo:** Verificar se o slime ativa o efeito correto ao coletar um power-up.  
**Arquivo principal:** `game.py` – função `verificar_colisoes()`  

---

## ⚡ TST-006 – Power-Up de Velocidade
**Cenário:** Fluxo principal  
**Preparação:**
- Um power-up de velocidade aparece no cenário  

**Passos:**
1. Mover o slime até o power-up  
2. Coletar o item  

**Resultado Esperado:**
- A velocidade do slime aumenta (`VEL_HORIZONTAL` × 1.5)  
- O HUD exibe um ícone de efeito ativo  
- O efeito dura até o tempo configurado (`duracao`)  

**Resultado do Teste:** ☐ Não Executado ☐ Sucesso ☐ Falha ☐ Cancelado  
**Data:** ___ / ___ / 2025  

---

## 💫 TST-007 – Power-Up de Invencibilidade
**Cenário:** Fluxo alternativo  
**Preparação:**
- Power-up de invencibilidade disponível  

**Passos:**
1. Coletar o item  
2. Colidir com obstáculo  

**Resultado Esperado:**
- O slime não perde vida durante o efeito  
- O HUD exibe o ícone de invencibilidade  
- O status é desativado após o tempo de duração  

**Resultado do Teste:** ☐ Não Executado ☐ Sucesso ☐ Falha ☐ Cancelado  
**Data:** ___ / ___ / 2025  
