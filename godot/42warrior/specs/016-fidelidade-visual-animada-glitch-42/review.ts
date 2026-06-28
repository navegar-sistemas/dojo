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

const CHECKS_T161_T162: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture + lint GDScript",
    command: "bash scripts/arch_guard.sh && bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 226/226 na main pós-merge (inclui render-proof do TileMapArena e os 4 estados do FourStateButton)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T172: IReviewCheckOutcome[] = [
  {
    name: "Guard de Clean Architecture + lint GDScript (0 warnings)",
    command: "bash scripts/arch_guard.sh && bash scripts/lint.sh",
    passed: true,
  },
  {
    name: "Testes GUT headless — 224/224 (assert HARD heading_font()/body_font()!=null, sem pending; .import das 4 fontes committados @73cfefd)",
    command: "bash scripts/check.sh",
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
  {
    target: "code",
    taskKey: "T-161",
    phase: null,
    status: "approved",
    checks: CHECKS_T161_T162,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-162",
    phase: null,
    status: "approved",
    checks: CHECKS_T161_T162,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-172",
    phase: null,
    status: "approved",
    checks: CHECKS_T172,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
