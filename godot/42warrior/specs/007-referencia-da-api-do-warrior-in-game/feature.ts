import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "007-referencia-da-api-do-warrior-in-game",
  name: "Referência da API do warrior in-game",
  problem:
    "No 42warrior o jogador escreve a lógica de turno do warrior (play_turn), mas o catálogo de ações e sentidos disponíveis em cada nível (walk!, attack!, feel, look, health, rest!, rescue!, pivot!, shoot! etc.) vive só em reference_solutions/código. O jogador, sobretudo iniciante, não tem como descobrir a API disponível sem sair do jogo — isso trava o pilar de PROGRAMAÇÃO logo após o editor in-game (PR-010) dar onde digitar mas não o quê chamar; o Ruby Warrior original entrega esse catálogo por nível.",
  productRequirementKeys: ["PR-002", "PR-010"],
  goals: [
    "Expor, na tela de jogo, um painel/aba de referência da API disponível NAQUELE nível, com assinatura + descrição curta de cada ação e sentido.",
    "Gerar o conteúdo de forma data-driven a partir da fachada do warrior / estado do nível, sem hardcode espalhado, coerente com o que o nível realmente expõe.",
    "Abrir/fechar a referência sem trocar de tela, sem recriar a arena e sem perder o código digitado (não-bloqueante), integrável ao editor retrátil da feature 006.",
  ],
  outOfScope: [
    "Tutorial interativo / onboarding guiado (candidata separada, decisão do usuário).",
    "Alterar a API, o motor de turnos ou adicionar níveis.",
    "Substituir o botão 'ver solução de referência' (PR-010) — é catálogo de API, não solução pronta.",
  ],
  productDecisions: [],
  phase: "backlog",
  createdAt: "2026-06-28",
};
