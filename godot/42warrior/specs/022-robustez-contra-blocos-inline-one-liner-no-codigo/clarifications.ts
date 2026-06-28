import type { IClarification } from "../types.ts";

/**
 * Fix-feature derivada de um P0 reportado pelo Matheus (crash por bloco inline/one-liner) já
 * corrigido na main (4b3f920), com o PO (cmqy0fd2g) PEDINDO o rastro (US/T) e dando a escolha do
 * mecanismo ao spec. O entendimento confirmado vem do critério explícito do PO.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Buraco de robustez (inline/one-liner) e escopo do rastro",
    questions: [
      {
        question: "O que estava quebrado e o que esta fix-feature precisa cobrir/tracear?",
        answer:
          "A 020 fechou a recursão multi-linha, mas blocos INLINE/one-liner (corpo na mesma linha do `:`) ESCAPAVAM do loop/depth-guard → Stack overflow → crash; o T-200 estava done com esse buraco. O Matheus corrigiu na produção (4b3f920, _normalize_inline_blocks normaliza inline→multi-linha antes da instrumentação, +4 testes, 347/347). Esta feature dá RASTRO ao fix (cobertura PR-010→RF→US→T) para o código não ficar órfão.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Critério de aceite (DoD) e mecanismo (escolha do spec)",
    questions: [
      {
        question: "Qual o DoD e por que fix-feature (não task na 020)?",
        answer:
          "DoD = exatamente os +4 testes do Matheus (recursão one-liner + while inline) verdes nas superfícies aplicáveis + 0-regressão (347/347), sem máscara. MECANISMO: o PO (cmqy0fd2g) deu a escolha (a) fix-feature nova ou (b) task na 020; o spec escolheu (a) FIX-FEATURE 022 pelo precedente EXATO — a 020 nasceu assim para um buraco da 014, sem reabrir a 014 (done/closed). Mantém a 020 imutável; 022 traça o mesmo PR-010. O código já está na main + o PO aceita (não é bloqueio).",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
];
