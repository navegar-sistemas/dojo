import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "009-selecao-e-replay-de-niveis",
  name: "Seleção e replay de níveis",
  problem:
    "O jogador avança pela beginner tower nível a nível, mas NÃO pode revisitar/re-jogar um nível já vencido para otimizar sua solução e pontuação. No Ruby Warrior, re-jogar níveis faz parte do loop (melhorar o código, buscar ace/time/rescue bonus). Hoje, sem seleção de nível, a pontuação (PR-006) e a progressão (PR-008) ficam sem o loop de OTIMIZAÇÃO — o jogador conclui e segue, sem caminho de volta para melhorar o score.",
  productRequirementKeys: ["PR-008", "PR-006"],
  goals: [
    "Oferecer uma tela/menu de seleção listando os níveis já desbloqueados/vencidos da torre.",
    "Permitir re-entrar num nível concluído PRESERVANDO o código salvo daquele nível (user://), sem sobrescrever o progresso.",
    "Exibir a melhor pontuação por nível (incl. ace/time/rescue bonus) na seleção, para guiar a otimização.",
    "Integrar a seleção/re-entrada ao fluxo de navegação existente (ScreenManager da feature 006), uma-tela-por-vez.",
  ],
  outOfScope: [
    "Criar novos níveis (PR-004) — só permite re-jogar os existentes.",
    "Alterar regras de pontuação ou mecânica de combate (PR-006/PR-003).",
    "Leaderboard online ou modo speedrun.",
  ],
  productDecisions: [],
  phase: "clarifying",
  createdAt: "2026-06-28",
};
