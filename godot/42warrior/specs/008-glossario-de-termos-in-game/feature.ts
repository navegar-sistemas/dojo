import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "008-glossario-de-termos-in-game",
  name: "Glossário de termos in-game",
  problem:
    "O jogador, sobretudo iniciante, encontra no jogo termos e entidades sem definição acessível — inimigos (sludge, thick sludge, archer, wizard), cativo e escada — e termos de pontuação/feedback (time bonus, rescue bonus, ace/clear bonus). Hoje o significado vive em código/níveis; o jogador precisa inferir ou sair do jogo, o que prejudica o onboarding do conteúdo da beginner tower. Complementa a feature 007 (referência de API): 007 = o que o jogador PODE CHAMAR (comandos); 008 = o que as COISAS no nível SIGNIFICAM (entidades + pontuação).",
  productRequirementKeys: ["PR-003", "PR-006"],
  goals: [
    "Expor, na tela de jogo, um glossário (painel/tooltip) que define as entidades presentes no nível atual (nome + descrição curta de cada inimigo, cativo e escada).",
    "Definir, no mesmo glossário, os termos de pontuação/feedback relevantes ao nível (time bonus, rescue bonus, ace/clear bonus) com descrição curta.",
    "Gerar o conteúdo de forma data-driven a partir do estado do nível (entidades do LevelState) e das regras de pontuação, sem hardcode espalhado.",
    "Abrir/fechar o glossário sem trocar de tela, sem recriar a arena e sem perder o código digitado (não-bloqueante).",
  ],
  outOfScope: [
    "Tutorial interativo / onboarding guiado (candidata separada, decisão do usuário).",
    "Alterar entidades, mecânica de combate ou regras de pontuação.",
    "Duplicar a referência de API (feature 007) — glossário é semântica de termos/entidades, não catálogo de comandos.",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
