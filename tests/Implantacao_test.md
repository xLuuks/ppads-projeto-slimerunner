#  Plano e Scripts de Teste – Slime Runner

**Componente Curricular:** Práticas Profissionais em Análise e Desenvolvimento de Sistemas  
**Equipe:** Eduardo Afonso P. Ferreira, Bruno Otavio Ramos, João Rinaldo França Neris, Lucas Augusto Correia Alves, Rodrigo Luiz Gomes da Silva  
**Versão:** 1.0  
**Data:** 16/10/2025  
**Ferramentas:** Python 3.13+, Pygame, PyInstaller, Inno Setup

---

## 1. Script de Teste – TST001 Instalação do Jogo

| Informação | Exemplo |
|-------------|----------|
| **Identificação única** | TST001 – Instalação do Jogo |
| **Caso de uso em que se baseia** | UC001 – Instalar o jogo Slime Runner |
| **Cenário** | Instalação completa do executável gerado |
| **Preparação (condição do sistema antes do teste)** | O arquivo `SlimeRunner-Setup.exe` deve estar disponível no diretório de testes. O PC deve possuir Windows 10/11 (64-bit) e 100 MB livres. |
| **Passos para execução do teste** | 1. Executar o instalador.<br>2. Aceitar os termos e prosseguir.<br>3. Selecionar diretório padrão de instalação.<br>4. Finalizar e criar atalho na área de trabalho. |
| **Resultado esperado** | O jogo deve ser instalado em `C:\Program Files\Slime Runner\` e o atalho criado no Desktop. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** |  |
| **Data da última execução do teste** |  |

---

## 2. Script de Teste – TST002 Execução do Jogo

| Informação | Exemplo |
|-------------|----------|
| **Identificação única** | TST002 – Execução do Jogo |
| **Caso de uso em que se baseia** | UC002 – Executar o jogo Slime Runner |
| **Cenário** | Inicialização e funcionamento do executável |
| **Preparação** | O jogo deve estar instalado e o atalho criado. |
| **Passos para execução do teste** | 1. Clicar no atalho “Slime Runner”.<br>2. Verificar se a tela inicial é exibida.<br>3. Testar o início da partida.<br>4. Fechar o jogo com ESC. |
| **Resultado esperado** | O jogo deve abrir em resolução 960x540 @ 60FPS, apresentando a tela inicial e funcionando sem erros. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** |  |
| **Data da última execução do teste** |  |

---

## 3. Script de Teste – TST003 Build e Distribuição

| Informação | Exemplo |
|-------------|----------|
| **Identificação única** | TST003 – Build e Publicação |
| **Caso de uso em que se baseia** | UC003 – Gerar e distribuir o executável |
| **Cenário** | Compilação e envio do instalador |
| **Preparação** | O código-fonte deve estar versionado no GitHub e o PyInstaller configurado. |
| **Passos para execução do teste** | 1. Executar o comando `pyinstaller SlimeRunner.py --onefile`.<br>2. Verificar geração do `.exe`.<br>3. Criar instalador no Inno Setup.<br>4. Publicar arquivo no GitHub/Drive. |
| **Resultado esperado** | O arquivo `SlimeRunner-Setup.exe` deve ser gerado (25–40 MB) e publicado corretamente. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** |  |
| **Data da última execução do teste** |  |

---

## 4. Script de Teste – TST004 Desempenho do Jogo

| Informação | Exemplo |
|-------------|----------|
| **Identificação única** | TST004 – Desempenho e FPS |
| **Caso de uso em que se baseia** | UC004 – Avaliar desempenho do jogo |
| **Cenário** | Avaliação de FPS durante execução |
| **Preparação** | O jogo deve estar em execução em modo normal (sem depuração). |
| **Passos para execução do teste** | 1. Iniciar o jogo.<br>2. Medir o FPS médio durante 60 segundos.<br>3. Registrar variações. |
| **Resultado esperado** | O FPS deve se manter estável em **60 FPS** com variação máxima de ±5 FPS. |
| **Resultado do teste** | ☐ NÃO EXECUTADO ☐ SUCESSO ☐ FALHA ☐ CANCELADO |
| **Descrição do resultado obtido** |  |
| **Data da última execução do teste** |  |

---
