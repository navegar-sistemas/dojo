import type { IClarification } from "../types.ts";

/**
 * Clarify registrada a partir das decisões que o usuario ratificou (CLR-003 da feature 001 e a
 * sessão de correção de rumo de 2026-06-27): áudio completo, fluxo de torre e menu são o "resto"
 * a fechar depois das prioridades 1-3 (UI, editor, debug).
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Escopo de áudio nesta entrega",
    questions: [
      {
        question:
          "Áudio entra completo (SFX + trilha) integrado de verdade nesta entrega, com assets CC0 trocáveis pela arte sonora da 42 — confirmado?",
        answer:
          "Sim — SFX por evento de turno (andar/atacar/dano/descanso/resgate/tiro/vitória/derrota) e trilha de fundo com controle de volume básico, usando assets de áudio CC0. Ratifica CLR-003 da feature 001.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-002",
    topic: "Fluxo de torre e progressão",
    questions: [
      {
        question:
          "O fluxo cobre menu inicial, telas de transição entre níveis (descrição + habilidades novas), avanço/reinício, tela de resultado/pontuação, créditos e progresso salvo localmente?",
        answer:
          "Sim — menu inicial; transições com descrição e habilidades novas; avançar na vitória e reiniciar nível; resultado/score; créditos ao concluir a torre; progresso persistido em user:// entre sessões.",
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
          "Resumo: feature 005 entrega áudio (SFX+trilha CC0), fluxo de torre (menu, transições, resultado, créditos) e progresso salvo, realizando PR-008 e PR-009. É o 'resto' após as prioridades 1-3. Correto?",
        answer: "Sim, entendimento confirmado. Seguir para discovery com esse escopo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
];
