import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-009",
    title: "TileMap2D para o corredor da masmorra; entidades como Sprite2D filhos",
    context:
      "O corredor da masmorra precisa de tiles reais de pedra e sprites distintos por entidade (RF-020, RF-021), substituindo o render procedural via _draw. A grade já existe no domínio (LevelState); a apresentação precisa refletir esse grid sem duplicar lógica.",
    decision:
      "DungeonView usa um TileMap2D (Godot 4) cujas células correspondem 1:1 a posições do LevelState. Tiles de piso e de parede provêm de um atlas CC0 (Kenney/0x72). Cada entidade presente no estado (warrior, inimigos, captive, escada) é um nó Sprite2D instanciado como filho de DungeonView, posicionado via TileMap.map_to_local(). Ao receber um novo LevelState a cena atualiza apenas os nós afetados, sem recriar o tilemap inteiro.",
    consequences:
      "Visual de grade imediato com assets CC0; swap de sprites = trocar arquivos res://assets/ (RF-025). A lógica de turno permanece exclusivamente no domínio. Custo: mapear posições de LevelState para coordenadas de TileMap na borda de apresentação.",
    status: "accepted",
    requirementKeys: ["RF-020", "RF-021", "RF-025", "RF-026", "RNF-001"],
    rejectedAlternatives: [
      {
        alternative: "Nós individuais (Node2D/Control) posicionados manualmente para cada célula",
        reason:
          "TileMap é a API canônica do Godot para grades; o approach Node2D manual exige coordenadas pixel a mão e não aproveita a pipeline de batching de tiles do motor.",
      },
      {
        alternative: "Manter o render procedural via _draw e apenas adicionar sprites sobrepostos",
        reason:
          "Manteria dois sistemas de renderização paralelos; CLR-001 exige substituição completa do render procedural.",
      },
    ],
  },
  {
    key: "ADR-010",
    title: "TurnEvents → AnimationPlayer/Tween por sprite; DungeonView como observador de TurnResult",
    context:
      "Cada turno produz uma lista de TurnEvent (RF-022). A cena precisa reproduzir animações correspondentes (moved→walk, attacked→attack, took_damage→hurt, etc.) sem conhecer a lógica de jogo; e o TurnResolver deve permanecer independente das animações (RNF-002).",
    decision:
      "Após cada resolve(), o GameFlowController passa o TurnResult (next_state + events) para a DungeonView. A DungeonView itera os eventos em ordem e despacha animações para os sprites afetados via AnimationPlayer (para frames de sprite sheet) ou Tween (para interpolação de posição/alpha). Cada animação tem duração ≤ 0,4 s; elas são enfileiradas e executadas via await de sinal 'animation_finished' — sem bloquear o TurnResolver. O TurnResolver é chamado somente após o conjunto de animações do turno anterior ter concluído (ou após um timeout de segurança).",
    consequences:
      "Feedback visual por turno claro e fiel à referência; TurnResolver permanece síncrono e <16 ms (RNF-002). Custo: a DungeonView mantém um mapeamento entity_id → Sprite2D e a lógica de enfileiramento de animações.",
    status: "accepted",
    requirementKeys: ["RF-022", "RNF-001", "RNF-002"],
    rejectedAlternatives: [
      {
        alternative: "Sinais Godot emitidos diretamente pelo TurnResolver para a cena",
        reason:
          "Acoplaria o domínio à engine Godot (viola CONV-002/RNF-001). TurnEvents já são o contrato de saída do domínio; a cena consome o TurnResult, não o contrário.",
      },
    ],
  },
  {
    key: "ADR-011",
    title: "HUD em CanvasLayer (layer 1) sobreposto ao mundo; atualizado via LevelState",
    context:
      "O HUD (HP coração, turno, descrição do nível, score) precisa ser sempre visível mesmo com câmera scrollando (RF-023). Implementar como filho direto da cena de jogo causaria que o HUD scrollasse junto com a câmera.",
    decision:
      "HudView é um nó CanvasLayer com layer = 1, filho raiz da cena de jogo mas fora do viewport da Camera2D. Ele expõe um método update_hud(state: LevelState, score: Score) chamado pelo GameFlowController após cada turno. Labels e ícone de coração são filhos diretos do HudView como nós Control/Label.",
    consequences:
      "HUD sempre visível independentemente da posição da câmera; atualização trivial via chamada de método com dados puros. Custo: a cena de jogo precisa manter referência ao HudView e chamar update_hud após cada turno.",
    status: "accepted",
    requirementKeys: ["RF-023", "RNF-001"],
    rejectedAlternatives: [
      {
        alternative: "HUD como filho da DungeonView posicionado na câmera",
        reason:
          "Requer reposicionamento manual do HUD a cada frame de câmera; CanvasLayer é a API canônica do Godot para overlays de UI invariantes à câmera.",
      },
    ],
  },
  {
    key: "ADR-012",
    title: "Camera2D com position_smoothing seguindo o warrior; zoom automático em níveis curtos",
    context:
      "O corredor precisa ser enquadrado completo em níveis curtos, e seguir o warrior com suavização em níveis longos (RF-024). A câmera não pode cortar a escada ou outras unidades visíveis.",
    decision:
      "Uma Camera2D filha de DungeonView tem position_smoothing_enabled = true e position_smoothing_speed ≈ 5.0. A câmera segue o Sprite2D do warrior. Em níveis cujo comprimento total em pixels cabe na viewport, o zoom é ajustado automaticamente para enquadrar todo o corredor (zoom = min(viewport_size / dungeon_pixel_size)). Em níveis mais longos, o zoom fixo + smoothing garantem acompanhamento fluido.",
    consequences:
      "Jogador sempre vê o warrior e contexto próximo; níveis curtos são mostrados completos sem scroll. Custo: lógica de ajuste de zoom na inicialização do nível (função pura de tamanho de grade vs. viewport).",
    status: "accepted",
    requirementKeys: ["RF-024"],
    rejectedAlternatives: [
      {
        alternative: "Câmera fixa centrada no corredor",
        reason:
          "Não funciona em níveis maiores que a viewport — parte do corredor ficaria fora da tela.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "DungeonView",
    responsibility:
      "Cena raiz da apresentação do jogo. Contém o TileMap2D do corredor, os Sprite2D das entidades e a Camera2D. Recebe TurnResult do GameFlowController e coordena a atualização do tilemap, o reposicionamento/animação dos sprites e a chamada ao HudView.",
    dependsOn: ["HudView", "EntitySpriteRegistry"],
    requirementKeys: ["RF-020", "RF-021", "RF-022", "RF-024", "RF-026", "RNF-001"],
  },
  {
    name: "EntitySpriteRegistry",
    responsibility:
      "Mapeamento entre entity_id (string) e o Sprite2D/AnimationPlayer correspondente na cena. Cria o Sprite2D na primeira vez que a entidade aparece no LevelState e remove quando desaparece. Encapsula o despacho de animações por tipo de TurnEvent.",
    dependsOn: [],
    requirementKeys: ["RF-021", "RF-022", "RNF-002"],
  },
  {
    name: "HudView",
    responsibility:
      "CanvasLayer (layer 1) com Labels de HP (ícone coração + valor), número de turno, descrição textual do nível e pontuação. Método público update_hud(state, score) usado pelo GameFlowController após cada turno.",
    dependsOn: [],
    requirementKeys: ["RF-023", "RNF-001"],
  },
  {
    name: "AssetPaths",
    responsibility:
      "Constantes dos caminhos res://assets/ para tiles e sprites CC0, centralizadas para que o swap pela arte definitiva da 42 exija alterar apenas este módulo.",
    dependsOn: [],
    requirementKeys: ["RF-025"],
  },
];
