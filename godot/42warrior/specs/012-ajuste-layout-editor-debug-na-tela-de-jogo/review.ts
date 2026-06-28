import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

const CHECKS: IReviewCheckOutcome[] = [
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
    name: "Testes unitários de domínio (GUT, headless) — 165/165",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-120",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-121",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "DoD T-121 pede 'teste GUT cobre o toggle de visibilidade pelo DebugBtn'. Nenhum teste GUT foi adicionado para esse comportamento. O toggle é 100% presentation-layer (emissão de sinal + visibilidade de nó), fora do escopo de CONV-006 (testes de domínio). Verificado por inspeção: sinal debug_toggled emitido pelo DebugBtn; _on_toggle_debug togela _debug_panel.visible (WarriorStatePanel+TurnConsole juntos, ADR-028 cumprido).",
        location: "src/presentation/code_editor_panel.gd:_on_debug_toggle",
        resolution:
          "Não-bloqueante para a jam: coverage por inspeção é suficiente. Um teste GUT de apresentação pode ser adicionado em iteração futura se o padrão de testes for expandido além do domínio.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-122",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
