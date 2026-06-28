import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-038",
    title: "SpriteFrames data-driven a partir do manifest + AnimatedSprite2D dirigido por turn_events",
    context:
      "Os 4 personagens têm sprite-sheets com animações (idle/walk/attack|cast|shoot/hurt/death, 48x48) descritas no anim/manifest.json. Hoje a apresentação usa sprites estáticos (já trocados pelo swap zero-código). É preciso ANIMAR de forma data-driven (RF-160/163), sem espalhar caminhos nem lógica de cena, e acionar a animação pelos turn_events já existentes — sem tocar regra.",
    decision:
      "Estender o registro de assets (linhagem EntityAssetRegistry/asset_paths) com um AnimatedEntityRegistry que LÊ o manifest e constrói os SpriteFrames de cada personagem (nome→animação→frames/fw/fh). As entidades na cena passam a usar AnimatedSprite2D alimentado por esses SpriteFrames; um mapeamento turn_event→animação (MOVED→walk, ATTACKED→attack/cast, SHOT→shoot, DAMAGED→hurt, DIED→death, senão idle) seleciona a animação a tocar. A presentation só LÊ eventos/estado; o domínio é intocado.",
    consequences:
      "Re-skin animado fiel e ajustável (trocar arte/anim = trocar arquivo/entrada do manifest); reusa o padrão data-driven (RNF-060). Custo: o builder de SpriteFrames do manifest e a fiação do mapa evento→animação. Acoplado ao fluxo de animação da 013 (AnimationSequencer) — a animação por evento entra como o beat visual.",
    status: "accepted",
    requirementKeys: ["RF-160", "RF-163"],
    rejectedAlternatives: [
      {
        alternative: "Hardcode dos SpriteFrames/animações por personagem em cada cena",
        reason: "Viola RNF-060 (data-driven) e espalha a fonte; trocar arte exigiria mexer em código/cena.",
      },
    ],
  },
  {
    key: "ADR-039",
    title: "TileMap 32px consumindo os tiles do pack (só apresentação)",
    context:
      "A arena deve usar um TileMap 32px com tile_floor/tile_wall/tile_stairs do pack (RF-161), substituindo o desenho atual, sem mudar as dimensões lógicas nem a regra do nível.",
    decision:
      "Renderizar o piso/parede/escada via um TileMapArena (TileMapLayer 32px) cujo TileSet referencia os tiles do pack; a montagem do tilemap deriva do estado/dimensões do nível (já expostos pelo domínio), mapeando célula→tile. Nenhuma regra migra para a cena.",
    consequences:
      "Arena fiel ao pack, escala de tile consistente (Nearest/pixel-art já setado). Custo: montar o TileSet e o mapeamento célula→tile a partir do estado do nível.",
    status: "accepted",
    requirementKeys: ["RF-161"],
    rejectedAlternatives: [
      {
        alternative: "Continuar desenhando chão/parede manualmente sem TileMap",
        reason: "Não atende o brief (TileMap 32px) e dificulta a fidelidade/escala.",
      },
    ],
  },
  {
    key: "ADR-040",
    title: "Sistema de botões de 4 estados (normal/hover/pressed/disabled) data-driven dos ui_*",
    context:
      "A UI precisa de botões com 4 estados visuais a partir dos assets ui_* (RF-162), reutilizáveis nos controles existentes (Run/Reset/Ref/Debug, menu), com o estado refletindo a interação real.",
    decision:
      "Um componente FourStateButton (cena/recurso de UI reutilizável) cujo StyleBox/textura por estado vem dos ui_* via o registro data-driven; os botões existentes passam a usar esse componente. Os 4 estados são verificáveis (normal/hover/pressed/disabled refletem a interação).",
    consequences:
      "UI coesa e fiel ao pack; estados consistentes em todos os botões. Custo: o componente + a migração dos botões atuais para ele. Não altera a lógica dos controles (apenas a aparência por estado).",
    status: "accepted",
    requirementKeys: ["RF-162"],
    rejectedAlternatives: [
      {
        alternative: "Cada botão estiliza seus 4 estados isoladamente",
        reason: "Duplicação e divergência; viola a fonte data-driven única (RNF-060).",
      },
    ],
  },
  {
    key: "ADR-041",
    title: "9 telas fiéis aos mockups via cenas Theme-driven reusando os sistemas visuais",
    context:
      "O brief exige 9 telas FIÉIS aos mockups HTML de design_files/v1 (RubyWarrior 42 - Asset Pack), com tipografia Press Start 2P (títulos/HUD pixel) + JetBrains Mono (código/texto). As telas já existem (ScreenManager da 006) mas não fiéis ao pack nem com a tipografia do brief.",
    decision:
      "Cada tela é uma cena ajustada ao seu mockup, montada por um ScreenComposer que aplica o Theme ÚNICO (paleta + fontes) e REUSA os sistemas AnimatedEntityRegistry (personagens), TileMapArena (arena) e FourStateButton (controles) — tudo data-driven (RNF-060). A fidelidade de cada tela é verificada por PROVA DE RENDER (render-rule, RNF-160). Nenhuma regra de jogo muda; opera sobre o ScreenManager existente.",
    consequences:
      "Telas fiéis e visualmente consistentes; reuso máximo dos sistemas; trocar arte/fonte = trocar arquivo/Theme. Custo: ajuste de layout por tela + Theme das fontes. Acoplado ao ScreenManager (006).",
    status: "accepted",
    requirementKeys: ["RF-164", "RF-163"],
    rejectedAlternatives: [
      {
        alternative: "Estilizar cada tela isoladamente, sem Theme único",
        reason: "Diverge da fonte data-driven única (RNF-060), duplica estilo e dificulta a fidelidade/consistência entre telas.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "ScreenComposer",
    responsibility:
      "Apresentação: monta/ajusta as 9 telas (cenas) fiéis aos mockups HTML de design_files/v1 — layout + tipografia (Press Start 2P / JetBrains Mono) via Theme único — reusando AnimatedEntityRegistry (personagens), TileMapArena (arena) e FourStateButton (controles), tudo data-driven. Opera sobre o ScreenManager (006); não altera regra. Cada tela tem prova de render.",
    dependsOn: ["AnimatedEntityRegistry", "TileMapArena", "FourStateButton"],
    requirementKeys: ["RF-164", "RF-163", "RNF-160"],
  },
  {
    name: "AnimatedEntityRegistry",
    responsibility:
      "Apresentação (linhagem EntityAssetRegistry): lê o anim/manifest.json e constrói os SpriteFrames dos 4 personagens (nome→animação→frames 48x48); fornece o mapeamento turn_event→animação (MOVED/ATTACKED/SHOT/DAMAGED/DIED→walk/attack|cast/shoot/hurt/death, senão idle). Fonte data-driven única; pontos de troca documentados.",
    dependsOn: [],
    requirementKeys: ["RF-160", "RF-163", "RNF-160"],
  },
  {
    name: "TileMapArena",
    responsibility:
      "Apresentação: renderiza piso/parede/escada via TileMapLayer 32px com TileSet dos tiles do pack, mapeando célula→tile a partir do estado/dimensões do nível. Não contém regra.",
    dependsOn: [],
    requirementKeys: ["RF-161"],
  },
  {
    name: "FourStateButton",
    responsibility:
      "Apresentação: componente de botão reutilizável com 4 estados visuais (normal/hover/pressed/disabled) resolvidos data-driven dos ui_*; usado pelos controles existentes. Não altera a lógica dos controles.",
    dependsOn: [],
    requirementKeys: ["RF-162"],
  },
];
