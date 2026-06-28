import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-160",
    kind: "functional",
    description:
      "Os 4 personagens (hero, enemy_cadet, enemy_dev, boss_director) são renderizados com AnimatedSprite2D/SpriteFrames data-driven a partir do anim/manifest.json: cada um com suas animações (idle/walk/attack|cast|shoot/hurt/death, frames 48x48). A animação correta é acionada pelos turn_events existentes (movimento→walk, ataque→attack/shoot/cast, dano→hurt, morte→death), sem decidir regra. Os sprites (48x48 personagens / 32x32 sludge) são ANCORADOS PELOS PÉS — bottom-center do sprite alinhado à célula de 32px; sprite mais alto transborda para cima (padrão de jogo).",
    priority: "highest",
    rationale: "CLR-002: re-skin animado fiel ao pack, acoplado aos eventos de turno; pura apresentação.",
  },
  {
    key: "RF-161",
    kind: "functional",
    description:
      "A arena usa um TileMap com grade NATIVA de 32px (TILE_SIZE=32, sem reamostrar a arte, filtro Nearest) consumindo os tiles do pack (tile_floor, tile_wall, tile_stairs), substituindo o desenho atual de chão/parede/escada, sem alterar a regra nem as dimensões lógicas do nível. A dimensão 32px nativa é a fonte e já está na main (reflete o hotfix 659ef14, grandfathered, que alinhou TILE_SIZE 64→32 e tile_size/texture_region_size aos tiles 32x32 do pack). A apresentação usa ESCALA INTEIRA apenas (2x/3x conforme os mockups, nunca fracionária — preserva o pixel-art), consistente com o zoom inteiro da câmera (RF da 011).",
    priority: "high",
    rationale: "CLR-002 + decisão de escala visual do PO (cmqxobe8c): tilemap fiel ao pack em 32px nativo, escala inteira; reflete o hotfix 659ef14 já na main (code-on-main passa a ter spec).",
  },
  {
    key: "RF-162",
    kind: "functional",
    description:
      "Há um sistema de botões com 4 estados visuais (normal/hover/pressed/disabled) a partir dos assets ui_*, aplicado aos controles existentes (Run/Reset/Ref/Debug e botões de menu), com o estado refletindo a interação real.",
    priority: "high",
    rationale: "CLR-002: sistema de botões 4-estados do brief, reutilizável.",
  },
  {
    key: "RF-163",
    kind: "functional",
    description:
      "Toda a arte (sprite-sheets, tiles, ui) é resolvida DATA-DRIVEN pelo registro existente (linhagem EntityAssetRegistry/asset_paths): trocar/ajustar arte ou animação = trocar arquivo ou entrada do manifest, sem nova lógica de cena fora do registro; os pontos de troca são documentados.",
    priority: "highest",
    rationale: "CLR-003/RNF-060: re-skin data-driven, fonte única, sem hardcode espalhado.",
  },
  {
    key: "RF-164",
    kind: "functional",
    description:
      "As 9 telas do jogo (menu, jogo/arena, resultado, transição, seleção de nível, sandbox, glossário, API/referência, créditos) são FIÉIS aos mockups HTML de design_files/v1 (RubyWarrior 42 - Asset Pack): layout, hierarquia visual e elementos conforme o mockup, com a TIPOGRAFIA do brief — Press Start 2P para títulos/HUD pixel e JetBrains Mono para código/texto — aplicada via Theme único. Reusa os sistemas (AnimatedSprite2D dos personagens, TileMap 32px, botões 4-estados) e o registro data-driven; nenhuma regra de jogo muda.",
    priority: "high",
    rationale: "Escopo aprovado pelo PO (cmqxpfgnv): 9 telas fiéis aos mockups HTML + tipografia Press Start 2P/JetBrains Mono; pura apresentação sobre o ScreenManager (006).",
  },
  {
    key: "RF-165",
    kind: "functional",
    description:
      "Há um Theme GLOBAL (design system) aplicado a TODAS as telas, data-driven: paleta (fundo void #0A0A0B, painéis grafite #15161A/#22242B), fontes Press Start 2P (títulos/HUD) + JetBrains Mono (corpo/código/logs) importadas de design_files/v1/fonts, e um sistema de CORES POR CONTEXTO (ZERO amarelo como base; títulos neutros em BRANCO #F2F2F2 com RGB-split (sombra ciano #00F0FF à esquerda + magenta #FF2BD6 à direita), verde #00FF66 sucesso/exit 0, rubi #FF003C perigo/morte/SIGKILL, ciano #00F0FF ativo/seleção; âmbar #FFD23F é acento MÍNIMO — somente gemas/estrelas — exceção documentada à regra zero-amarelo). Inclui overlay de glitch (fx_glitch_overlay em CanvasLayer, blend Add/Screen) em todas as telas, fundo temático (tile_void + scanlines + data-rain) e botões/sliders tematizados (primário ciano). Trocar arte/fonte/cor = trocar Theme/arquivo, sem hardcode espalhado.",
    priority: "highest",
    rationale: "Brief do Matheus (via PO cmqxr1a0d): as telas estavam com o tema default do Godot (cinza/fonte genérica/amarelo). F4 entrega o design system e SUBSUME/RESOLVE o RNF-063 da 006 (game_theme.tres criado mas nunca aplicado) — aplicar o Theme global É o RNF-063.",
  },
  {
    key: "RNF-160",
    kind: "non_functional",
    description:
      "A entrega é provada por PROVA DE RUNTIME DE CENA além de GUT, sob a REGRA DE RENDER-PROOF: um smoke-test headless instancia game.tscn, RENDERIZA ≥1 frame e checa o floor_layer com tiles REALMENTE desenhados + os AnimatedSprite2D posicionados na grade de 32px (instanciar a cena sem renderizar, ou sem a arte real carregada, NÃO basta — este é o requisito que o bug da arena preta provou). A suíte permanece 100% verde com 0 regressão das features 001–006.",
    priority: "high",
    rationale: "Condição de aceite do PO (cmqxmkkrl) + REGRA DE RENDER-PROOF adotada (cmqxobe8c): renderizar ≥1 frame e checar floor_layer com tiles+sprites posicionados; 4-estados verificáveis; sem regressão.",
  },
];
