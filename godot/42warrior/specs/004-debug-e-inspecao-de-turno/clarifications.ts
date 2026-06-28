import type { IClarification } from "../types.ts";

/**
 * Clarify registrada a partir das decisões que o usuario ratificou na sessão de correção de rumo
 * (2026-06-27): debug e inspeção de turno é a prioridade número 3, após UI e editor.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "O que o jogador precisa inspecionar",
    questions: [
      {
        question:
          "Hoje só há HUD de turno/HP e o desfecho final. A feature 004 dá ao jogador a inspeção do que sua lógica fez: o que o warrior sentiu, a ação tomada e os efeitos, por turno?",
        answer:
          "Sim — console de turnos listando, em ordem, sentido + ação + efeitos (andou, atacou causando N, descansou +N, levou dano, resgatou, sem ação/erro), além de um painel de estado do warrior (HP/posição/direção).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-002",
    topic: "Controles de execução e origem dos dados",
    questions: [
      {
        question:
          "A inspeção inclui controles de play/pause/passo-a-passo/velocidade e consome os turn_events que o domínio já emite (sem nova regra no domínio)?",
        answer:
          "Sim — controles play/pause/step/velocidade sobre o loop de turno; os dados vêm dos TurnEvents existentes (turn_event.gd); erros do código do jogador aparecem associados ao turno em que ocorreram.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-003",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question:
          "Resumo: feature 004 entrega debug/inspeção de turno (console passo-a-passo + estado do warrior + play/pause/step/velocidade + erros por turno), consumindo os TurnEvents, realizando PR-011. Prioridade 3. Correto?",
        answer: "Sim, entendimento confirmado. Seguir para discovery com esse escopo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
];
