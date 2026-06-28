import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 016 (Fidelidade visual animada glitch-42).
 * Fonte: brief de UI/visual do Usuário (asset-pack glitch/42) + GO de governança do agente-po
 * (chat cmqxmkkrl, separar da 015, derivar asset-map do manifest, gating de fontes/mockup).
 * Registradas como confirmedBy "usuario" (brief + delegação ao PO).
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Separação de concern (016 re-skin × 015 glitch)",
    questions: [
      {
        question: "O re-skin animado entra na 015 (glitch) ou numa feature separada?",
        answer:
          "Feature SEPARADA (016): 016 = APRESENTAÇÃO pura (re-skin animado, TileMap, botões 4-estados, data-driven); 015 = COMPORTAMENTO glitch (overlay/pós-processo/corrupção de UI, mecânica determinística). O invariante de determinismo da 015 não se aplica ao re-skin; separar mantém coesão (decisão do PO em cmqxmkkrl).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Escopo animado e asset-map",
    questions: [
      {
        question: "Quais personagens/animações e de onde vem o mapa de assets?",
        answer:
          "4 personagens animados via AnimatedSprite2D/SpriteFrames, derivados do anim/manifest.json (134 linhas): hero (idle 4/walk 6/attack 5/hurt 4/death 6), enemy_cadet (idle/walk/cast/hurt/death), enemy_dev (idle/walk/shoot/hurt/death), boss_director (idle/cast/hurt/death) — frames 48x48. O agente-spec DERIVA o asset-map do manifest; o PO revisa exceções (não monta à mão). + TileMap 32px consumindo tile_* e sistema de botões 4-estados (ui_*).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Data-driven e prova de runtime (critério de aceite do PO)",
    questions: [
      {
        question: "Como garantir que é re-skin fiel sem reinventar e como provar?",
        answer:
          "Data-driven via o registro existente (RNF-060): trocar/ajustar arte = trocar arquivo/entrada do manifest, ZERO lógica de cena nova fora do registro. Aceite do PO (cmqxmkkrl): (1) cadeia PR→RF→US→T verde; (2) re-skin data-driven; (3) PROVA DE RUNTIME DE CENA (smoke headless instanciando game.tscn com os AnimatedSprite2D/TileMap reais, além de GUT); (4) os 4 estados dos botões verificáveis.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Lacunas que gateiam parte do brief (fontes + mockup)",
    questions: [
      {
        question: "O que fazer com a tipografia fiel e as 9 telas pixel-perfect sem os arquivos?",
        answer:
          "GATED: as FONTES (Press Start 2P / JetBrains Mono) e o MOCKUP HTML das 9 telas NÃO vieram no pack. Então: tipografia = fonte data-driven com ponto de troca + placeholder (NÃO vira RF verificável até chegarem); '9 telas pixel-perfect' = item gated aguardando o mockup. NÃO bloqueia a 016: entrega-se o verificável agora (re-skin animado + TileMap + botões), gate-se o resto. PO aguardando o Usuário fornecer fontes+mockup.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-005",
    topic: "Resumo do entendimento da feature 016 (ratificação)",
    questions: [
      {
        question: "O entendimento geral está correto?",
        answer:
          "Sim. 016 entrega o re-skin de APRESENTAÇÃO fiel ao pack glitch/42: AnimatedSprite2D/SpriteFrames dos 4 personagens (manifest), TileMap 32px (tile_*) e botões 4-estados (ui_*), tudo data-driven via o registro (RNF-060), animação acoplada aos turn_events, sem tocar regra/domínio. Tipografia e fidelidade pixel-perfect das telas ficam gated (faltam fontes + mockup). PR-007 (apresentação) + PR-012 (identidade glitch-42). Aceite exige prova de runtime de cena.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
