import type { IReviewCheckOutcome, IReviewRecord } from "../types.ts";

/**
 * Registros de revisão de conformidade da feature 010 (Nível introdutório / sandbox).
 * Fonte: evidência e aceite do agente-po (chat cmqxgr47s) — gate implement VERDE por task,
 * GUT test_sandbox_level + suíte 135/135, aceite do PO (aceite-010). Tasks T-076..079 = done.
 * Reviewer registrado = "usuario" (ator de produto, aceite via agente-po); a verificação
 * técnica (gate/GUT) é do fluxo de implementação. Sem findings abertos.
 */
const CHECKS: IReviewCheckOutcome[] = [
  { name: "Guard de Clean Architecture (presentation não importa src/domain)", command: "bash scripts/arch_guard.sh", passed: true },
  { name: "Formatação + lint GDScript (gdformat/gdlint)", command: "bash scripts/lint.sh", passed: true },
  { name: "Testes GUT — test_sandbox_level", command: "bash scripts/test.sh", passed: true },
  { name: "Suíte completa (arch_guard + lint + testes, 135/135)", command: "bash scripts/check.sh", passed: true },
];

export const reviews: IReviewRecord[] = [
  { target: "code", taskKey: "T-076", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-077", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-078", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-079", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
];
