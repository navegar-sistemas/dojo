import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "004-debug-e-inspecao-de-turno",
  name: "Debug e inspecao de turno",
  problem: `O jogador nao consegue ver o que sua logica fez. So existe um HUD com numero do turno e HP, e o desfecho final (vitoria/derrota). Sem inspecao passo-a-passo — o que o warrior sentiu, qual acao tomou, quanto dano causou/levou — depurar a propria logica de turno e as cegas. Para um jogo de programacao, a inspecao da execucao e parte do jogo. Prioridade numero 3 da correcao de rumo.`,
  productRequirementKeys: ["PR-011"],
  goals: [
    "Console de turnos: lista em ordem o que o warrior sentiu e a acao tomada com seus efeitos (andou; atacou alvo causando N de dano; descansou recuperando N; levou dano; resgatou cativo; turno sem acao/erro), a partir dos turn_events que o dominio ja emite.",
    "Painel de estado corrente: HP, posicao e direcao do warrior, e estado relevante do nivel.",
    "Controles de execucao: play, pause, passo-a-passo (um turno por vez) e ajuste de velocidade.",
    "Mensagens de erro do codigo do jogador associadas ao turno em que ocorreram.",
  ],
  outOfScope: [
    "Breakpoints/debugger de linha no codigo do jogador (escopo de IDE); aqui a inspecao e do turno do dominio.",
    "O editor de codigo (feature 003), a renderizacao grafica (002) e o audio (005).",
    "Profiling de performance da engine.",
  ],
  productDecisions: [
    "O debug consome os turn_events que o dominio ja emite (turn_event.gd) — nenhuma regra nova entra no dominio.",
    "Controles de execucao (play/pause/step/velocidade) vivem na camada de apresentacao, sobre o loop de turno da Application.",
  ],
  phase: "done",
  createdAt: "2026-06-27",
};
