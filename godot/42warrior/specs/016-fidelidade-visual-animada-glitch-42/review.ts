import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

const CHECKS_T160: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture (Domain/Application puros)",
    command: "bash scripts/arch_guard.sh",
    passed: true,
  },
  {
    name: "Formatação + lint GDScript (gdformat/gdlint sobre src e test)",
    command: "bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 212/212 (inclui a prova de render do T-160)",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-160",
    phase: null,
    status: "approved",
    checks: CHECKS_T160,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
