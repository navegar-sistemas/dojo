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
    name: "Testes GUT headless — 171/171, zero warnings",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-130",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-131",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "O play() do AnimationSequencer aguarda os tweens de cada beat sequencialmente com `for tween in tweens: await tween.finished`, não em paralelo verdadeiro. Para beats com 2 factories (pulse+hurt), a segunda animação começa imediatamente após a primeira terminar dentro do mesmo beat, não simultaneamente. Em durações iguais (ANIM_ATTACK = ANIM_HURT = 0.20s) e dado que ambas são iniciadas antes do loop de await (factories chamadas antes do for de await), a concorrência é preservada: ambos os tweens são criados e iniciam no mesmo frame; o await sequencial apenas espera a mais longa. Correto para o uso turn-based do jogo.",
        location:
          "src/presentation/animation_sequencer.gd:play — loop `for tween in tweens: await tween.finished`",
        resolution:
          "Não-bloqueante: as factories são chamadas antes do loop de await, portanto todos os tweens de um beat iniciam no mesmo frame (concorrência garantida). O await sequencial aguarda o mais longo. Aceito para o loop turn-based.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-132",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
];
