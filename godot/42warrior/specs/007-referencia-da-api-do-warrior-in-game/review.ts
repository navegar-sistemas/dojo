import type { IReviewCheckOutcome, IReviewRecord } from "../types.ts";

/**
 * Registros de revisão de conformidade da feature 007 (Referência da API in-game).
 * Fonte: evidência e aceite do agente-po (chat cmqxgr47s) — gate implement VERDE por task,
 * GUT test_warrior_api_catalog 10/10, aceite do PO (aceite-007). Tasks T-080..083 = done.
 * Reviewer registrado = "usuario" (ator de produto, aceite via agente-po); a verificação
 * técnica (gate/GUT) é do fluxo de implementação. Sem findings abertos.
 */
const CHECKS: IReviewCheckOutcome[] = [
  { name: "Guard de Clean Architecture (presentation não importa src/domain)", command: "bash scripts/arch_guard.sh", passed: true },
  { name: "Formatação + lint GDScript (gdformat/gdlint)", command: "bash scripts/lint.sh", passed: true },
  { name: "Testes GUT — test_warrior_api_catalog 10/10", command: "bash scripts/test.sh", passed: true },
  { name: "Suíte completa (arch_guard + lint + testes)", command: "bash scripts/check.sh", passed: true },
];

export const reviews: IReviewRecord[] = [
  { target: "code", taskKey: "T-080", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-081", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-082", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-083", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
];
