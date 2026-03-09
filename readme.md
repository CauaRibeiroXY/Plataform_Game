# 🎮 Platform Game — Jogo de Plataforma 2D em Python

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Pygame Zero](https://img.shields.io/badge/Pygame_Zero-pgzrun-green)](https://pygame-zero.readthedocs.io/)
[![License](https://img.shields.io/badge/licença-Educacional-orange)]()

---

## Descrição

**Platform Game** é um jogo de plataforma 2D desenvolvido integralmente em Python com a biblioteca **Pygame Zero**. O jogador controla um herói que percorre um nível horizontal com obstáculos, inimigos e seções aquáticas, com o objetivo de alcançar a placa de saída sem perder todas as suas vidas. O projeto demonstra a aplicação prática de conceitos de desenvolvimento de jogos — física, animação por sprites, inteligência artificial de inimigos e gerenciamento de estados — em um ambiente Python simples e acessível.

---

## Contexto do Projeto

O projeto foi criado com fins **educacionais e de portfólio**, para colocar em prática conceitos fundamentais de programação orientada a objetos, desenvolvimento de jogos e algoritmos de física e colisão. A escolha do Pygame Zero foi intencional: a biblioteca elimina o boilerplate do Pygame puro, permitindo foco total na lógica do jogo. O projeto explora desde o ciclo de atualização de frames (`update/draw`) até sistemas mais complexos como câmera seguindo o jogador e IA de inimigos com comportamentos distintos.

---

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|---|---|
| **Linguagem** | Python 3.x |
| **Framework de Jogos** | Pygame Zero (`pgzrun`) |
| **Biblioteca de Colisão** | `pygame.Rect` |
| **Áudio** | Pygame Zero (music & sounds API) |
| **Assets Visuais** | PNG sprites (pixel art) |
| **Assets de Áudio** | `.ogg` (efeitos sonoros), `.mp3` / `.wav` (música) |
| **Ferramenta de Execução** | `pgzrun` (embutido no pacote `pgzero`) |

### Dependências

```
pgzero  (inclui pygame internamente)
```

> Não há arquivo `requirements.txt` — a única dependência externa é o `pgzero`, instalável via `pip`.

---

## Arquitetura e Estrutura do Projeto

O projeto é composto por um **único arquivo principal** (`game.py`) com aproximadamente **700 linhas de código**, seguindo um modelo orientado a objetos com separação de responsabilidades por classes.

### Padrões Arquiteturais

- **Orientação a Objetos (OOP)**: Cada entidade do jogo (jogador, inimigos, plataformas, background, HUD) é encapsulada em sua própria classe com estado e comportamento independentes.
- **Máquina de Estados (State Machine)**: A variável global `game_state` controla o fluxo da aplicação (`"menu"` → `"playing"` → `"end_game"`), determinando o que é desenhado e atualizado em cada frame.
- **Game Loop com Pygame Zero**: O framework utiliza as funções globais `draw()` e `update()` chamadas automaticamente por `pgzrun.go()` a cada frame, dispensando a criação manual de um loop `while True`.
- **Sistema de Câmera por Deslocamento**: A câmera segue o jogador horizontalmente através da variável `camera_x`, que é subtraída da posição `x` de todos os objetos no momento do desenho.

### Fluxo Principal da Aplicação

```
pgzrun.go()
    │
    ├── update()  ← chamado a cada frame
    │       ├── Atualiza estado do jogo (music, camera_x)
    │       ├── enemy.update() para cada inimigo
    │       ├── player.update(platforms, enemies)
    │       ├── hud.update(player)
    │       └── Verifica condições de fim de jogo
    │
    └── draw()  ← chamado a cada frame
            ├── game_state == "menu"     → draw_menu()
            ├── game_state == "playing"  → background, player, hud, enemies, platforms
            └── game_state == "end_game" → tela preta com texto "End Game"
```

### Classes Principais

| Classe | Responsabilidade |
|---|---|
| `Player` | Movimento, física, animação por sprites, colisão com plataformas e inimigos, sistema de vidas e invulnerabilidade |
| `Platform` | Representação das plataformas (horizontais/verticais), sistema de colisão via `pygame.Rect`, plataforma final com signo de saída |
| `Enemy_frog` | Inimigo com salto físico, patrulha horizontal entre limites, IA de inversão de direção |
| `Enemy_bee` | Inimigo voador com deslocamento horizontal, animação de asa alternando frames |
| `Enemy_fish` | Inimigo aquático com movimento vertical cíclico entre limites `min_y` e `max_y` |
| `Background` | Renderização em tiles do cenário (céu, chão, água), com suporte a modo água via flag `water=True` |
| `Hud_life` | Interface gráfica de vidas com corações cheios, meio-cheios e vazios |

---

## Funcionalidades Principais

### 🕹️ Menu Principal
- Três opções interativas: **Start Game**, **Toggle Music** e **Exit**
- Detecção de clique do mouse com área de colisão calculada por proximidade às opções do menu

### 🧍 Sistema do Jogador
- **Movimento horizontal** com as setas ← →
- **Pulo** com `Espaço` ou seta ↑ (somente quando no chão)
- **Física de gravidade** com acumulação de velocidade vertical (`vy += 0.5`)
- **Animação por sprites**: idle (2 frames), caminhada (2 frames) e pulo (1 frame), com sprites espelhados para cada direção
- **Sistema de invulnerabilidade** temporária após receber dano (120 frames ≈ 2 segundos a 60 FPS)
- **Detecção de queda** — perda de vida ao sair da tela verticalmente (`y > 600`) com respawn no ponto inicial

### 👾 Inteligência Artificial dos Inimigos
- **Sapo (Frog)**: Aplica gravidade, realiza saltos periódicos (cooldown de 90 frames), inverte direção ao atingir os limites horizontais
- **Abelha (Bee)**: Voa em linha reta horizontal, inverte direção (`vx *= -1`) nos limites, alterna sprites de voo a cada 10 frames
- **Peixe (Fish)**: Move-se verticalmente entre `min_y` e `max_y`, inverte direção (`vy *= -1`), com dois estados de sprite (subindo/descendo)

### ⚔️ Sistema de Combate e Colisão
- **Pular em cima do inimigo** (detecção por sobreposição inferior) → elimina o inimigo e executa quique (`vy = -10`)
- **Colisão lateral** → empurra o jogador de volta (`vx = ±8`), deduz meia vida, ativa invulnerabilidade
- **Colisão com plataformas** → corrige posição vertical e zera `vy` ao pousar

### ❤️ HUD — Interface de Vida
- Exibe 3 corações no canto superior esquerdo
- Atualização dinâmica: coração cheio (`≥ 1 vida`), meio coração (`.5 vida`), coração vazio (`0 vida`)

### 🎵 Sistema de Áudio
- Música de fundo (`tema.mp3`) com controle de volume em 50%
- Toggle de música pelo menu principal
- Efeitos sonoros: pulo (`sfx_jump.ogg`), dano (`sfx_hurt.ogg`), eliminação de inimigo (`sfx_disappear.ogg`)

### 📷 Sistema de Câmera
- Câmera segue o jogador horizontalmente em tempo real (`camera_x = player.x - WIDTH/2`)
- Todos os objetos são renderizados com offset `- camera_x`

### 🏁 Condições de Fim de Jogo
- **Derrota**: `player.lives <= 0`
- **Vitória**: Jogador colide com a plataforma `final=True` (placa de saída)

---

## Integrações e APIs

O projeto **não utiliza APIs externas ou serviços de terceiros**. Todas as funcionalidades são implementadas localmente utilizando:

- **Pygame Zero API** — funções `draw()`, `update()`, `on_mouse_down()`, objetos globais `screen`, `keyboard`, `music`, `sounds`
- **`pygame.Rect`** — importado diretamente do Pygame para cálculo de hitboxes de plataformas
- **Sistema de arquivos local** — assets de imagem e áudio carregados automaticamente pelo Pygame Zero a partir das pastas `images/` e `sounds/`

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3.7 ou superior instalado
- `pip` disponível no terminal

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Plataform_Game
```

### 2. Instalar dependências

```bash
pip install pgzero
```

### 3. Executar o jogo

```bash
python game.py
```

> **Importante**: o comando deve ser executado **a partir da pasta raiz do projeto** (`Plataform_Game/`), pois o Pygame Zero carrega os assets relativamente às pastas `images/`, `sounds/` e `music/`.

### Controles

| Tecla | Ação |
|---|---|
| `← Seta Esquerda` | Mover para a esquerda |
| `→ Seta Direita` | Mover para a direita |
| `Espaço` / `↑ Seta Cima` | Pular |
| `Click (menu)` | Selecionar opção |

---

## Estrutura de Pastas

```
Plataform_Game/
│
├── game.py                        # Arquivo principal — toda a lógica do jogo
├── check_sizes.py                 # Script auxiliar (vazio / reservado)
├── README.md                      # Documentação do projeto
│
├── images/                        # Assets visuais (carregados automaticamente pelo pgzero)
│   ├── player/                    # 32 sprites do jogador + HUD de corações
│   │   ├── player_idle.png        # Sprite idle direita
│   │   ├── player_walk1/2.png     # Animação de caminhada (direita)
│   │   ├── player_left_*.png      # Sprites espelhados (esquerda)
│   │   ├── player_jump.png        # Sprite de pulo
│   │   ├── hud_heart.png          # Coração cheio
│   │   ├── hud_heart_half.png     # Meio coração
│   │   └── hud_heart_empty.png    # Coração vazio
│   │
│   ├── enemy/
│   │   ├── frog/                  # 6 sprites: idle, jump, rest (ambas direções)
│   │   ├── bee/                   # 6 sprites: rest, fly_a, fly_b (ambas direções)
│   │   ├── fish/                  # 5 sprites: up, up2, down, idle_up, idle_down
│   │   └── boss/                  # 3 sprites (reservados para futuro boss)
│   │
│   ├── background/                # 5 imagens de fundo (céu, chão, terra, água)
│   └── level/                     # 2 tiles: bricks_grey.png, sign_exit.png
│
├── sounds/                        # Efeitos sonoros (.ogg)
│   ├── sfx_jump.ogg
│   ├── sfx_hurt.ogg
│   └── sfx_disappear.ogg
│
└── music/                         # Música de fundo
    ├── tema.mp3
    └── music.wav
```

---

## Possíveis Melhorias

- 🆕 **Múltiplos níveis**: Criar um sistema de mapas para progressão entre fases
- 👹 **Boss**: Os assets do boss já existem na pasta `images/enemy/boss/` — implementar a classe e a lógica de batalha
- 💾 **Sistema de Save/Highscore**: Salvar pontuação e progresso em arquivo local (JSON ou SQLite)
- 🔁 **Tela de Game Over e Retry**: Atualmente o estado `end_game` apenas exibe texto; adicionar opções de recomeço
- 🧱 **Editor de Níveis**: Sistema para configurar plataformas e inimigos via arquivo externo (JSON/YAML) em vez de código hardcoded
- ⚡ **Otimização de renderização**: Instanciar `Actor` apenas uma vez em vez de recriá-los a cada frame no método `draw()` da `Platform`
- 🎯 **Sistema de pontuação**: Pontos por inimigos eliminados e tempo de conclusão
- 📱 **Suporte a gamepad**: Integração com controles via `pygame.joystick`
- 🔊 **Volume ajustável**: Controle deslizante de volume no menu
- 🌊 **Animação de água**: A imagem `background_water_moving.png` existe mas a animação não está totalmente implementada no código

---

## Aprendizados Técnicos

Este projeto demonstra e pratica os seguintes conhecimentos técnicos:

### Programação Orientada a Objetos
- Modelagem de entidades como classes com encapsulamento de estado (`self.vx`, `self.lives`, `self.live`)
- Polimorfismo implícito: todos os inimigos implementam os métodos `update()` e `draw()` com comportamentos distintos

### Física e Matemática para Jogos
- Implementação de **gravidade** com acumulação de velocidade (`vy += gravity`)
- **Detecção de colisão AABB** (Axis-Aligned Bounding Box) entre retângulos
- **Resolução de colisão** com correção de posição e zeragem de velocidade
- Cálculo de **overlap** para distinguir colisão de pisão (matar inimigo) de colisão lateral (dano)

### Animação por Sprites
- Alternância de frames baseada em contador de frames (`frame_count % N`)
- Seleção de sequência de sprites conforme estado do personagem (idle, walk, jump)
- Suporte a sprites espelhados para direção esquerda/direita

### Máquina de Estados
- Controle de fluxo da aplicação com estados explícitos (`menu`, `playing`, `end_game`)

### Sistema de Câmera 2D
- Câmera que segue o jogador com deslocamento horizontal aplicado na renderização

### Gerenciamento de Áudio
- Reprodução de música com controle de volume
- Sistema de efeitos sonoros sincronizados com eventos do jogo

### Game Loop
- Separação entre lógica (`update`) e renderização (`draw`) — padrão fundamental em desenvolvimento de jogos

---

## Palavras-chave Técnicas (Importante para ATS)

`Python` · `Pygame Zero` · `Pygame` · `Desenvolvimento de Jogos` · `Game Development` · `Programação Orientada a Objetos` · `OOP` · `Game Loop` · `Máquina de Estados` · `State Machine` · `Animação por Sprites` · `Sprite Animation` · `Física de Jogos` · `Game Physics` · `Detecção de Colisão` · `Collision Detection` · `AABB` · `Câmera 2D` · `2D Camera` · `Inteligência Artificial` · `IA de Inimigos` · `Enemy AI` · `HUD` · `Pixel Art` · `Jogo 2D` · `Plataforma 2D` · `Side-Scroller` · `Gerenciamento de Estado` · `Programação de Jogos` · `Assets de Áudio` · `Efeitos Sonoros` · `Música de Fundo`

---

> Projeto desenvolvido com fins educacionais e de portfólio. Todos os assets de imagem e áudio foram utilizados para fins não comerciais.