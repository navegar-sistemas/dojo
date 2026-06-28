import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

const CHECKS_T220: IReviewCheckOutcome[] = [
  {
    name: "_normalize_inline_blocks() quebra corpos inline/one-liner (while/recursão) em multi-linha antes da instrumentação → o caso inline não escapa do guard: vira no-op + erro, sem Stack overflow. Código na main (4b3f920, autor Matheus)",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "≥4 testes de regressão (recursão one-liner + while inline) reproduzem o crash e verificam no-op real, SEM pending; check.sh verde 347/347, 0 regressão 001–021",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-220",
    phase: null,
    status: "approved",
    checks: CHECKS_T220,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
