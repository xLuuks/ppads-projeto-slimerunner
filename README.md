# 🏃 Slime Runner – Corrida na Floresta
### Projeto de Prática Profissional em ADS
---

## 📝 Descrição do Projeto

O **Slime Runner** é um jogo no estilo *endless runner*, desenvolvido em **Python** utilizando a biblioteca **Pygame**. O jogador controla um slime que deve desviar de obstáculos, coletar power-ups, sobreviver pelo maior tempo possível e acumular pontuação progressiva.

Este projeto foi desenvolvido dentro da disciplina **Prática Profissional em ADS**, seguindo um processo iterativo. A **Iteração 2 (AC5)** trouxe melhorias significativas na jogabilidade, arquitetura, interface e organização do código, incluindo:

*   **Melhorias Visuais:** Implementação completa do efeito **Parallax** com múltiplas camadas para maior profundidade no cenário.
*   **Mecânicas de Jogo:** Introdução de **Power-Ups** com geração aleatória (RNG), efeitos temporários e duração controlada.
*   **Estrutura:** Implementação de um sistema de **Estados do Jogo (GameStates)** para gerenciar o fluxo (Menu, Jogando, Game Over).
*   **Interface:** Atualização do HUD (Head-Up Display) para exibir informações dinâmicas, como pontuação e Power-Ups ativos.
*   **Correções:** Ajustes na velocidade e correção de bugs gerais de movimento e colisão.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
| :--- | :--- | :--- |
| **Python** | 3.10+ | Linguagem de programação principal. |
| **Pygame** | 2.5+ | Biblioteca para desenvolvimento de jogos 2D. |
| **Git** | - | Sistema de controle de versão. |
| **GitHub** | - | Hospedagem do repositório. |

---

## 🚀 Instruções Detalhadas para Execução

Para rodar o **Slime Runner** em seu computador pessoal, siga os passos abaixo:

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.10+** instalado em seu sistema.

### 2. Clonar o Repositório

Abra o terminal ou prompt de comando e clone o projeto:

```bash
git clone https://github.com/xLuuks/ppads-projeto-slimerunner.git
cd ppads-projeto-slimerunner
```

### 3. Instalar as Dependências

Com o Python instalado, utilize o `pip` para instalar a biblioteca Pygame:

```bash
pip install pygame
```

### 4. Executar o Jogo

Após a instalação, execute o arquivo principal do jogo:

```bash
python main.py
```

O jogo será iniciado no estado de **Menu**.

---

## 📂 Estrutura de Pastas

A estrutura do projeto está organizada da seguinte forma para garantir a modularidade e manutenibilidade do código:

```
ppads-projeto-slimerunner/
├── models/             # Classes e lógica de entidades do jogo (Player, Obstacle, PowerUp)
├── ui/                 # Componentes de interface do usuário (HUD, Menus)
├── Imagens Jogo/       # Assets gráficos e imagens do jogo
├── tests/              # Arquivos de testes unitários e de integração
├── main.py             # Ponto de entrada principal do jogo
├── game.py             # Lógica central do loop do jogo e gerenciamento de entidades
├── settings.py         # Variáveis de configuração e constantes globais
├── states.py           # Definição e gerenciamento dos estados do jogo (GameStates)
└── README.md           # Este arquivo
```

---

## 👥 Integrantes do Grupo

| Nome | Função |
| :--- | :--- |
| Eduardo Afonso P. Ferreira | Desenvolvedor / Analista |
| Bruno Otavio Ramos | Desenvolvedor / Analista |
| João Rinaldo França Neris | Desenvolvedor / Analista |
| Lucas Augusto Correia Alves | Desenvolvedor / Analista |
| Rodrigo Luiz Gomes da Silva | Desenvolvedor / Analista |

---

## 🔗 Links do Projeto

| Recurso | Link |
| :--- | :--- |
| **Repositório GitHub** | `https://github.com/xLuuks/ppads-projeto-slimerunner` |
| **Quadro de Acompanhamento (Trello)** | `https://trello.com/b/94FQtY1H/projeto-slime-runner` |
| **Release da Iteração 2 (Tag v2)** | `https://github.com/xLuuks/ppads-projeto-slimerunner/releases/tag/v2` |
| **Documento de Especificação** | `https://docs.google.com/document/d/1UqacSleu4xvELOUO9Nx33Oy0VybCQs3tF7A5_9G-jVM/edit?tab=t.0` |
|**Link do Video de Apresentação**|`https://drive.google.com/file/d/17PK3Hqmxg6t2IFCy6YQrczqHEXO4p2oi/view?usp=drivesdk`|
|**Link do Video de Apresentação**|`https://drive.google.com/file/d/1CE2aKGGxvH2TJuZzJSBpKhU-kFD_e2I8/view?usp=drive_link`|
