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
    name: "Testes GUT headless — 181/181, zero warnings",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-154",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-151",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "GlitchRule.evaluate() recebe floor_index e turn_number mas não os usa no cálculo atual (RF-155 P1 futuro). Parâmetros prefixados com _ para suprimir warning do gdlint e manter a assinatura pública determinística documentada no ADR-034.",
        location: "src/domain/glitch_rule.gd:evaluate",
        resolution:
          "Não-bloqueante: a assinatura pública está correta para extensão futura (RF-155). O comportamento determinístico é garantido pelos testes.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-150",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-152",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "GlitchPostProcess usa CanvasLayer + ColorRect com hint_screen_texture para capturar o frame anterior. Em Godot 4 headless (sem GPU), o shader não renderiza — o efeito visual exige display. Testável apenas em runtime com GPU; os testes GUT cobrem a regra (GlitchRule) que determina a intensidade.",
        location: "src/presentation/glitch_post_process.gd",
        resolution:
          "Não-bloqueante para a jam: o efeito visual é verificado por inspeção em runtime. A regra que define a intensidade é coberta por teste de domínio (GlitchRule).",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-153",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
];
