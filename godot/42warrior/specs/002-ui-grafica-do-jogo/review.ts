import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão da feature 002 (UI gráfica, PR-007). Revisão independente
 * do tech-lead sobre o worktree feature/002. Checagens do projeto verdes
 * (arch_guard / gdformat+gdlint / GUT 102/102). Saída real conferida no worktree.
 */
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
    name: "Testes unitários de domínio (GUT, headless)",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-023",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-024",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-025",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "DoD de T-025 ('substituir game_view.gd/_draw pelo DungeonView; remover render procedural por completo'): na 1ª revisão independente o game_view.gd (267 linhas, func _draw) ainda estava RASTREADO no commit c4d5228, como código morto (não referenciado por nenhuma .tscn). Reportado como bloqueio (chat cmqwyexbb).",
        location: "src/presentation/game_view.gd",
        resolution:
          "RESOLVIDO em a7ab7e2 ('fix(002): remove game_view.gd e _tween_victory'): o dev removeu o arquivo + .uid. Confirmado pelo revisor: grep 'func _draw' src/ = zero; game.tscn usa DungeonView (TileMap real + sprites CC0); check.sh 102/102 verde. PR-007 (proíbe render procedural) cumprido.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-026",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-027",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-028",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-029",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-030",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "_tween_victory (entity_sprite_registry.gd) estava definido mas nunca chamado (WON usa _tween_scale_pulse) — código morto.",
        location: "src/presentation/entity_sprite_registry.gd",
        resolution: "RESOLVIDO em a7ab7e2 (removido junto com o game_view.gd).",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-031",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-032",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-033",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
];
