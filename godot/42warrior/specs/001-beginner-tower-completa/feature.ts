import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "001-beginner-tower-completa",
  name: "Beginner Tower completa",
  problem: `Para a game jam da 42SP, é preciso entregar um jogo completo e jogável: o remake do Ruby Warrior beginner tower (9 níveis) em Godot/GDScript, com identidade visual 42. O desafio é recriar fielmente as mecânicas do original (turnos, sentidos, ações, combate, saúde, resgate, pontuação) sob uma arquitetura limpa — Domain independente da engine, responsabilidade única por arquivo e método — e permitir que o jogador escreva código (play_turn) que controla o warrior, executado em runtime. Sem essa feature não há produto para a jam.`,
  productRequirementKeys: [
    "PR-001",
    "PR-002",
    "PR-003",
    "PR-004",
    "PR-005",
    "PR-006",
    "PR-007",
    "PR-008",
    "PR-009",
  ],
  goals: [
    "Recriar os 9 níveis da beginner tower com paridade funcional ao Ruby Warrior original.",
    "Implementar o motor de turnos determinístico no Domain (GDScript puro, sem dependência da engine).",
    "Expor a API do warrior (sentidos sem efeito colateral + ações que consomem o turno) via fachada.",
    "Permitir que o jogador escreva GDScript (play_turn(warrior)) executado em runtime, com soluções-referência embarcadas por nível.",
    "Apresentação 2D top-down em grade com assets placeholder com pontos de troca para a arte final da 42.",
    "Pontuação com time bonus e ace score; telas de transição/torre; áudio (SFX+música) completo; menu inicial e créditos.",
    "Aderir a Clean Architecture, DDD e Clean Code: responsabilidade única por arquivo e método, testes de domínio verdes.",
  ],
  outOfScope: [
    "Torres além da beginner (intermediate/advanced) — apenas a beginner tower nesta entrega.",
    "Arte final/definitiva da 42 — usar placeholders com pontos de troca; integração da arte final é posterior.",
    "Editor visual de programação por blocos — descartado pelo usuário (jogador escreve código real).",
    "Multiplayer, ranking online ou persistência em servidor.",
    "Direções :left/:right do jogo completo — a beginner tower usa apenas :forward/:backward.",
  ],
  productDecisions: [
    "Jogador escreve código real (GDScript play_turn(warrior)) em vez de blocos — decisão do usuário ('blocos dão muito trabalho').",
    "Execução do código do jogador via compilação de GDScript em runtime (source_code + reload()), contra uma fachada que só expõe a API pública do warrior.",
    "Apresentação 2D top-down em grade.",
    "Assets placeholder agora, com pontos de troca para a arte temática da 42.",
    "Escopo extra aprovado: pontuação+ace, telas de torre, áudio completo (SFX+música), menu+créditos.",
    "Fonte canônica dos 9 níveis ratificada por usuario (2026-06-27): o gem original ryanb/ruby-warrior (towers/beginner/level_001..009.rb). beginner_tower.gd usa os literais do código-fonte (width/unidades/escada/time_bonus/ace_score), ancorados por test_beginner_tower_canonical.gd. Correção aplicada: L5 (size 7, stairs 6) e L6 (size 8, stairs 7), antes reconstruídos de walkthrough.",
  ],
  phase: "done",
  createdAt: "2026-06-27",
};
