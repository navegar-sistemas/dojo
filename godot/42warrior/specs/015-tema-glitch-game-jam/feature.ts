import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "015-tema-glitch-game-jam",
  name: "Tema Glitch Game Jam",
  problem:
    "O tema OBRIGATÓRIO da game jam é 'glitch', mas nada do tema está implementado: hoje o jogo (mecânica sólida do remake do Ruby Warrior) não comunica o tema em nenhuma camada — conceito, mecânica, estética, áudio ou identidade da 42. Sem o tema, o jogo perde o critério CENTRAL de pontuação da jam, por mais sólida que seja a mecânica. O tema precisa aparecer na JOGABILIDADE (não só decorativo) e casar com a identidade da 42 (terminal/Unix/hacker, P&B com neon de acento, o '42').",
  productRequirementKeys: ["PR-012", "PR-007", "PR-001"],
  goals: [
    "CONCEITO — 'Kernel corrompido da 42': a torre é um mainframe da 42 infectado; o warrior é um processo de debug que sobe limpando a corrupção. Fio narrativo nas telas/transições/textos.",
    "MECÂNICA (obrigatória) — erro do código do jogador vira glitch DETERMINÍSTICO no mundo: quando o script do jogador lança exceção/erro, o jogo glitcha de verdade (warrior/tela/tile corrompem) além do log no console, ligando o tema ao núcleo (programar). Determinístico/seedado, nunca RNG injusto.",
    "ESTÉTICA — pós-processo glitch escalando com eventos (RGB split/aberração cromática/scanlines, intensificando em dano/morte/erro) + corrupção progressiva da UI conforme sobe na torre (scanlines, texto embaralhado, RGB split).",
    "IDENTIDADE 42 — mensagens de erro na língua Unix/42 (segfault (core dumped), command not found, exit 0, etc.).",
    "REFORÇO (P1, se couber no tempo) — mecânica de glitch determinística por andar (entidades cintilantes em turnos alternados OU ação corrompida scriptada que o jogador contorna no código); sprite que corrompe em dano/morte via turn_events; transições datamosh; áudio que corrompe com o estado (bit-crush quando HP baixo/erro).",
    "Priorização de jam: entregar o P0 COMPLETO (conceito + mecânica jogável + estética + identidade 42) vale mais que P1/P2 incompletos; P2 (glitch-through-walls, falso crash, variação narrativa 'o warrior é o glitch') fica como backlog.",
  ],
  outOfScope: [
    "Reescrever a mecânica core ou os 9 níveis canônicos (o tema é ADITIVO; nada das features 001–006 pode regredir).",
    "Multiplayer/online.",
    "Arte final definitiva (placeholder/gerado + pontos de troca via EntityAssetRegistry bastam).",
    "Qualquer glitch que afete REGRA por RNG injusto: glitches mecânicos são fixos/seedados e testáveis (determinismo do turno é sagrado).",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
