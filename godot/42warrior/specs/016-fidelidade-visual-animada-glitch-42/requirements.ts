import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-160",
    kind: "functional",
    description:
      "Os 4 personagens (hero, enemy_cadet, enemy_dev, boss_director) são renderizados com AnimatedSprite2D/SpriteFrames data-driven a partir do anim/manifest.json: cada um com suas animações (idle/walk/attack|cast|shoot/hurt/death, frames 48x48). A animação correta é acionada pelos turn_events existentes (movimento→walk, ataque→attack/shoot/cast, dano→hurt, morte→death), sem decidir regra.",
    priority: "highest",
    rationale: "CLR-002: re-skin animado fiel ao pack, acoplado aos eventos de turno; pura apresentação.",
  },
  {
    key: "RF-161",
    kind: "functional",
    description:
      "A arena usa um TileMap 32px que consome os tiles do pack (tile_floor, tile_wall, tile_stairs), substituindo o desenho atual de chão/parede/escada, sem alterar a regra nem as dimensões lógicas do nível.",
    priority: "high",
    rationale: "CLR-002: tilemap fiel ao pack (32px), só apresentação.",
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
    key: "RNF-160",
    kind: "non_functional",
    description:
      "A entrega é provada por PROVA DE RUNTIME DE CENA além de GUT: um smoke-test headless instancia game.tscn com os AnimatedSprite2D e o TileMap reais carregados (sem erro), e a suíte permanece 100% verde com 0 regressão das features 001–006. (Instanciar a cena sem carregar a arte real NÃO basta.)",
    priority: "high",
    rationale: "Condição de aceite do PO (cmqxmkkrl): prova de runtime de cena + 4-estados verificáveis + sem regressão.",
  },
];
