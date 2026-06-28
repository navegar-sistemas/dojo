import type { IReviewCheckOutcome, IReviewRecord } from "../types.ts";

/**
 * Registros de revisão de conformidade da feature 008 (Glossário de termos in-game).
 * Fonte: evidência e aceite do agente-po (chat cmqxgr47s) — gate implement VERDE por task,
 * GUT test_glossary_catalog 9/9, aceite do PO (aceite-008). Tasks T-084..087 = done.
 * Reviewer registrado = "usuario" (ator de produto, aceite via agente-po); a verificação
 * técnica (gate/GUT) é do fluxo de implementação. Sem findings abertos.
 */
const CHECKS: IReviewCheckOutcome[] = [
  { name: "Guard de Clean Architecture (presentation não importa src/domain)", command: "bash scripts/arch_guard.sh", passed: true },
  { name: "Formatação + lint GDScript (gdformat/gdlint)", command: "bash scripts/lint.sh", passed: true },
  { name: "Testes GUT — test_glossary_catalog 9/9", command: "bash scripts/test.sh", passed: true },
  { name: "Suíte completa (arch_guard + lint + testes)", command: "bash scripts/check.sh", passed: true },
];

export const reviews: IReviewRecord[] = [
  { target: "code", taskKey: "T-084", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-085", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-086", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-087", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
];
