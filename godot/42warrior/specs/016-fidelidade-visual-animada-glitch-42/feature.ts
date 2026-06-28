import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "016-fidelidade-visual-animada-glitch-42",
  name: "Fidelidade visual animada glitch 42",
  problem:
    "O Usuário forneceu o asset-pack glitch/42 e o PO já fez o swap zero-código dos 9 sprites/tiles ESTÁTICOS em uso. Mas o brief pede o RE-SKIN ANIMADO fiel: os 4 personagens (hero, enemy_cadet, enemy_dev, boss_director) têm sprite-sheets de animação (idle/walk/attack|cast|shoot/hurt/death) no manifest, a arena deve usar um TileMap 32px consumindo os tile_*, e a UI precisa de um sistema de botões de 4 estados (ui_*). Hoje a apresentação é estática (sprites simples, sem AnimatedSprite2D/SpriteFrames, sem TileMap, botões sem estados) — não atinge a fidelidade de apresentação do brief.",
  productRequirementKeys: ["PR-007", "PR-012"],
  goals: [
    "AnimatedSprite2D/SpriteFrames data-driven para os 4 personagens a partir dos sheets do manifest: hero (idle 4 / walk 6 / attack 5 / hurt 4 / death 6), enemy_cadet (idle/walk/cast/hurt/death), enemy_dev (idle/walk/shoot/hurt/death), boss_director (idle/cast/hurt/death) — todos frames 48x48; animação por evento de turno (walk/attack/hurt/death) acoplada aos turn_events existentes.",
    "TileMap 32px na arena consumindo os tiles do pack (tile_floor/tile_wall/tile_stairs), substituindo o desenho atual de chão/parede, sem mudar regra.",
    "Sistema de botões de 4 estados (normal/hover/pressed/disabled) a partir dos ui_*, reutilizável nos controles existentes (Run/Reset/Ref/Debug etc.).",
    "Tudo DATA-DRIVEN via o registro existente (RNF-060): trocar/ajustar arte = trocar arquivo/entrada do manifest, ZERO lógica de cena nova fora do registro; pontos de troca documentados.",
  ],
  outOfScope: [
    "Alterar regra/domínio: é PURA apresentação (consome turn_events e estado; não decide nada).",
    "Inventar estética: segue o manifest/README do pack; não altera paleta nem cria arte.",
    "Fidelidade pixel-perfect das 9 telas e tipografia fiel (Press Start 2P/JetBrains Mono): GATED — faltam o mockup HTML das telas e os arquivos de fonte; ficam como item aguardando o Usuário (specados como fonte/layout data-driven com placeholder, não como RF verificável agora).",
    "Re-implementar o comportamento glitch (overlay/pós-processo/corrupção de UI): isso é a feature 015 (separada por coesão).",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
