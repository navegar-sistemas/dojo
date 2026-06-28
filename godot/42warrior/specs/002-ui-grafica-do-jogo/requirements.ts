import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Renderização visual (PR-007) ──────────────────────────────────────────────
  {
    key: "RF-020",
    kind: "functional",
    description:
      "O corredor da masmorra é renderizado como um TileMap 2D de tiles de pedra provenientes de um asset pack CC0 (ex.: Kenney Dungeon Pack ou 0x72 Dungeon Tileset). Cada célula do TileMap corresponde a um espaço do LevelState; paredes preenchem o contorno superior e inferior.",
    priority: "highest",
    rationale: "CLR-001/CLR-004: substituição do render procedural (_draw) pela grade visual de masmorra exigida pela referência do Ruby Warrior.",
  },
  {
    key: "RF-021",
    kind: "functional",
    description:
      "Cada tipo de entidade possui sprite distinto: warrior (cavaleiro de armadura), sludge (slime verde), thick sludge (slime maior), archer (arqueiro), wizard (mago), captive (cativo acorrentado) e escada (dourada). Sprites vêm do mesmo pack CC0 com pontos de troca claramente identificados.",
    priority: "highest",
    rationale: "CLR-002/CLR-004: identidade visual por unidade; fidelidade à referência do Ruby Warrior.",
  },
  {
    key: "RF-022",
    kind: "functional",
    description:
      "A cada turno, os TurnEvents emitidos pelo domínio disparam animações correspondentes nas sprites: moved→walk, attacked→attack, took_damage→hurt, rested→idle/heal, rescued→rescue, shot→shoot, enemy_defeated→die, won→victory, died→death. A cena assina os eventos e aciona as animações sem conhecer a lógica de jogo.",
    priority: "highest",
    rationale: "CLR-003/CLR-004: feedback visual por turno consumido da camada de domínio via eventos; Clean Architecture.",
  },
  {
    key: "RF-023",
    kind: "functional",
    description:
      "O HUD exibe em tempo real: HP do warrior representado por ícone de coração + valor numérico (ex.: ♥ 20/20), número do turno atual, descrição textual do nível e pontuação acumulada. O HUD é atualizado após cada turno a partir do LevelState.",
    priority: "highest",
    rationale: "CLR-004: informações essenciais para o jogador acompanhar o estado do jogo.",
  },
  {
    key: "RF-024",
    kind: "functional",
    description:
      "A câmera enquadra o corredor completo do nível. Em níveis maiores que a viewport, a câmera segue o warrior com suavização (Camera2D com smoothing). O corredor nunca fica cortado parcialmente; o jogador sempre vê a escada e todas as unidades visíveis.",
    priority: "high",
    rationale: "Jogabilidade: o jogador precisa ver o estado completo do corredor para tomar decisões.",
  },
  {
    key: "RF-025",
    kind: "functional",
    description:
      "Os assets gráficos (tiles, sprites, SpriteFrames) são referenciados por caminhos e nós com nomenclatura padronizada (ex.: res://assets/sprites/warrior.png) de modo que a substituição pela arte definitiva da 42 exija apenas trocar os arquivos e não reescrever lógica de cena.",
    priority: "high",
    rationale: "CLR-002: integração com art swap para a arte da 42 sem refactor de cena.",
  },
  {
    key: "RF-026",
    kind: "functional",
    description:
      "O game_view.gd existente (render procedural com _draw) é substituído integralmente pela nova cena gráfica. A nova cena lê exclusivamente LevelState e TurnEvents da camada Application; nenhuma regra de jogo, cálculo de dano ou lógica de turno reside na apresentação.",
    priority: "highest",
    rationale: "CLR-003/CLR-004: elimina o render procedural insuficiente e garante separação de camadas (CONV-002).",
  },
  // ── Não-funcionais ────────────────────────────────────────────────────────────
  {
    key: "RNF-001",
    kind: "non_functional",
    description:
      "A camada de apresentação (cenas Godot) não importa nem instancia classes do domínio diretamente: 0 ocorrências de `load/preload` ou `new` de classes de src/domain/ em arquivos .gd de cena. Todo acesso ao estado do jogo ocorre via interfaces da camada Application (LevelState, TurnEvents, WarriorFacade).",
    priority: "highest",
    rationale: "CONV-002: domínio independente da engine; a cena é um adaptador puro de saída.",
  },
  {
    key: "RNF-002",
    kind: "non_functional",
    description:
      "Animações de sprite têm duração máxima de 0,4 s por evento de turno e são executadas assincronamente via AnimationPlayer/Tween e sinais do Godot. O TurnResolver resolve o próximo turno em menos de 16 ms independentemente do estado das animações em curso.",
    priority: "high",
    rationale: "Turno determinístico (ADR-002): a apresentação não pode adicionar latência ao ciclo de turno.",
  },
];
