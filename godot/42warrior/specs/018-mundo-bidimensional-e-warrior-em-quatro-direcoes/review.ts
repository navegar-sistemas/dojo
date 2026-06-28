import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

const CHECKS_T181: IReviewCheckOutcome[] = [
  {
    name: "Direction 4-dir (NORTH/SOUTH/EAST/WEST + delta()/pivot() horário/opposite()) — domínio puro, 0-RNG; FORWARD/BACKWARD mantidos, extensão NÃO-breaking (callers de relative_sign intocados) → 0-regressão por construção; merge-tree limpo (exit=0)",
    command: "git merge-tree (verificação do tech-lead) + arch_guard",
    passed: true,
  },
  {
    name: "Testes GUT — 288/288 na main pós-merge (test_direction: 19 testes — 4 direções + delta + pivot + opposite + equals + relative_sign); teste POR DIREÇÃO ✓, 0-regressão 001-016 ✓",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T180: IReviewCheckOutcome[] = [
  {
    name: "LevelState 2D (from_2d() grade R×C com Vector2i + space_at_2d() bounds) com a API 1D 100% PRESERVADA — R=1 = corredor beginner testado (retrocompat por construção, o DoD de R=1 que o PO reservou); merge-tree limpo",
    command: "git merge-tree (verificação do tech-lead) + arch_guard",
    passed: true,
  },
  {
    name: "Testes GUT — 286/286 na main pós-merge (test_018_level_state_2d); domínio puro, 0-RNG; 0-regressão 001-016",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-180",
    phase: null,
    status: "approved",
    checks: CHECKS_T180,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-181",
    phase: null,
    status: "approved",
    checks: CHECKS_T181,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
