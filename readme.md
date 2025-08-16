# Platformer Game - Projeto Pygame Zero

Um jogo de plataforma desenvolvido em Python usando a biblioteca Pygame Zero, seguindo as diretrizes de desenvolvimento de jogos educacionais.

## 📋 Sobre o Projeto

Este é um jogo de plataforma 2D onde o jogador controla um herói que deve atravessar diferentes níveis, enfrentando inimigos e coletando vidas. O objetivo é chegar até a placa de saída sem perder todas as vidas.

## 🎮 Características do Jogo

### Menu Principal
- **Start Game**: Inicia uma nova partida
- **Toggle Music**: Liga/desliga a música de fundo
- **Exit**: Sair do jogo

### Jogabilidade
- **Movimento**: Use as setas ← → para mover o personagem
- **Pulo**: Use ESPAÇO ou seta ↑ para pular
- **Objetivo**: Chegue até a placa de saída sem perder todas as vidas
- **Vidas**: O jogador começa com 3 vidas (representadas por corações no HUD)

### Inimigos
- **Sapo (Frog)**: Se move pulando entre limites horizontais
- **Abelha (Bee)**: Voa horizontalmente com animação de batida de asas
- **Peixe (Fish)**: Se move verticalmente em áreas aquáticas

### Sistema de Combate
- **Eliminar inimigos**: Pule em cima dos inimigos para eliminá-los
- **Receber dano**: Colidir lateralmente com inimigos causa perda de vida
- **Invulnerabilidade**: Após receber dano, o jogador fica temporariamente invulnerável

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Pygame Zero** (biblioteca principal)
- **pygame.Rect** (apenas para colisões)
- **Bibliotecas padrão**: math, random

## 🎨 Recursos Visuais

### Animações de Sprites
- **Player**: Idle, caminhada e pulo (com sprites diferentes para cada direção)
- **Inimigos**: Cada inimigo possui animações específicas de movimento
- **Background**: Cenários com múltiplas camadas e elementos aquáticos

### Sistema de Câmera
- Câmera que segue o jogador em ambas as direções
- Renderização relativa à posição da câmera

## 🔧 Instalação e Execução

### Pré-requisitos
```powershell
# Verificar se Python está instalado
python --version

# Instalar Pygame Zero
pip install pgzero
```

### Executando o Jogo
```powershell
# Navegar até a pasta do projeto
cd C:\Users\seu_usuario\Pgzero\plat_game

# Executar o jogo
python game.py
```

## 📁 Estrutura de Arquivos

```
plat_game/
├── game.py                 # Arquivo principal do jogo
├── music/
│   └── tema.ogg           # Música de fundo
├── sounds/
│   ├── sfx_jump.wav       # Som de pulo
│   ├── sfx_hurt.wav       # Som de dano
│   └── sfx_disappear.wav  # Som de eliminação de inimigo
├── images/
│   ├── player/            # Sprites do jogador e HUD
│   ├── enemy/             # Sprites dos inimigos
│   ├── background/        # Imagens de fundo
│   └── level/             # Elementos do cenário
```

## 🎯 Mecânicas do Jogo

### Sistema de Vidas
- **3 vidas iniciais** representadas por corações
- **Perda de vida**: Colisão com inimigos ou queda
- **Game Over**: Quando todas as vidas são perdidas
- **Vitória**: Ao chegar na placa de saída

### Física do Jogo
- **Gravidade**: Aplicada ao jogador e alguns inimigos
- **Colisões**: Detecção precisa entre jogador, plataformas e inimigos
- **Movimento**: Controles responsivos com animações fluidas

## 🏗️ Arquitetura do Código

### Classes Principais
- **Player**: Controle do jogador, movimento e animações
- **Platform**: Sistema de plataformas e colisões
- **Enemy_frog, Enemy_bee, Enemy_fish**: Diferentes tipos de inimigos
- **Background**: Sistema de cenários e elementos visuais
- **Hud_life**: Interface de usuário para vidas

### Padrões Utilizados
- **Orientação a Objetos**: Classes bem estruturadas para cada elemento
- **Estado do Jogo**: Sistema de estados (menu, playing, end_game)
- **Animação por Sprites**: Troca de frames para animações realistas

## 🎵 Audio

- **Música de fundo**: Reprodução contínua durante o jogo
- **Efeitos sonoros**: Sons para pulo, dano e eliminação de inimigos
- **Controle de áudio**: Opção para ligar/desligar no menu

## 🚀 Funcionalidades Implementadas

- ✅ Menu principal funcional
- ✅ Sistema completo de movimento e pulo
- ✅ Múltiplos tipos de inimigos com IA
- ✅ Sistema de vidas e HUD
- ✅ Animações de sprites para todos os personagens
- ✅ Sistema de câmera que segue o jogador
- ✅ Colisões precisas
- ✅ Música e efeitos sonoros
- ✅ Condições de vitória e derrota

## 📈 Complexidade

O projeto possui aproximadamente **700 linhas de código** com:
- **6 classes principais** bem estruturadas
- **Sistema de animação** complexo por sprites
- **IA de inimigos** com comportamentos únicos
- **Sistema de física** personalizado
- **Gerenciamento de estados** do jogo

## 👥 Desenvolvimento

Projeto desenvolvido seguindo as diretrizes de:
- **PEP8** para estilo de código
- **Programação Orientada a Objetos**
- **Nomes descritivos** em inglês
- **Código original** e independente

---

**Divirta-se jogando! 🎮**