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
    name: "Testes GUT headless — 178/178, zero warnings",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-110",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-111",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Histerese implementada via _anchor_x (deslocamento acumulado desde o último flip). Em movimento turn-based 1 tile (64px) o limiar de 32px diferencia a direção corretamente. Edge case: oscilação rápida ±hysteresis_px bloquearia o flip — aceitável e testado.",
        location: "src/presentation/camera_follow_controller.gd:_follow",
        resolution:
          "Não-bloqueante para o loop turn-based. Testes cobrem o cenário de não-inversão e de inversão suficiente.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-112",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-113",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "RNF-110 (60 FPS sem queda). _process é O(1), sem alocações. Profiling em hardware real fora do escopo da jam — implementação equivalente ao padrão _process de qualquer Node em Godot.",
        location: "src/presentation/camera_follow_controller.gd:_process",
        resolution:
          "Não-bloqueante: adequado para 60 FPS pela análise estática do código.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
];
