import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 011 (câmera estilo SMW).
 * Fonte: decisões do Usuário relayed pelo agente-po (chat cmqxh6jh3), como refinamento contido
 * e fiel à referência SMW que o próprio Usuário escolheu; o Usuário tem veto (informado pelo PO).
 * Registradas como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Zoom / escala de tile entre níveis de tamanhos diferentes",
    questions: [
      {
        question:
          "A câmera deve dar zoom para enquadrar cada nível (scale-to-fit) ou manter escala de tile constante?",
        answer:
          "Zoom CONSTANTE 1:1 sempre — NUNCA scale-to-fit. Como no Super Mario World (escala de tile constante). Remove o zoom-pra-caber atual, que era parte da inconsistência reclamada.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Comportamento da câmera em nível que cabe inteiro no viewport",
    questions: [
      {
        question:
          "Para um nível que cabe inteiro na tela (sem o que rolar), qual o comportamento da câmera?",
        answer:
          "Câmera ESTÁTICA, centrada no corredor, CLAMPED aos limites do nível — mostra o corredor curto inteiro no mesmo tamanho de tile dos níveis grandes (sem margem de scroll, pois não há o que rolar). O acompanhamento contínuo + dead-zone + lookahead com histerese engajam SOMENTE quando o nível é MAIS LARGO que o viewport.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Resumo do entendimento da feature 011 (ratificação)",
    questions: [
      {
        question: "O entendimento geral da câmera estilo SMW está correto?",
        answer:
          "Sim. A câmera acompanha o warrior continuamente DURANTE o movimento (sem snap pós-animação), com dead-zone central, lookahead com histerese na direção do movimento e clamp nas bordas do nível; zoom 1:1 constante; nível-que-cabe-na-tela = estático/centrado/clamped (follow/dead-zone/lookahead só quando o nível excede o viewport). Refina o comportamento de câmera entregue na 006 (PR-007). Não altera motor de turnos, API, layout de painéis (012) nem níveis.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
