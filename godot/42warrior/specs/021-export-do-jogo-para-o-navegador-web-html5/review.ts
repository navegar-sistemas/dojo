import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

const CHECKS_T210: IReviewCheckOutcome[] = [
  {
    name: "project.godot: rendering/renderer/rendering_method.web=gl_compatibility (Forward+ preservado no desktop); o 2D renderiza no WebGL2 — integrado na main (merge cf26d61)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T211: IReviewCheckOutcome[] = [
  {
    name: "export_presets.cfg preset Web + export templates do Godot 4.7 INSTALADOS; build HTML5/WASM verificado (wasm+pck gerados) — integrado na main (cf26d61)",
    command: "godot --headless --export-release Web (verificação do tech-lead)",
    passed: true,
  },
];

const CHECKS_T212: IReviewCheckOutcome[] = [
  {
    name: "AudioManager: áudio inicia/retoma no 1º gesto do usuário (autoplay-block do browser), desktop inalterado (0-regressão) — integrado na main (cf26d61)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T213: IReviewCheckOutcome[] = [
  {
    name: "Persistência user:// (player_code/level_progress/progress stores) validada p/ IndexedDB no web, sobrevive a reload; desktop inalterado — integrado na main (cf26d61)",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-210",
    phase: null,
    status: "approved",
    checks: CHECKS_T210,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-211",
    phase: null,
    status: "approved",
    checks: CHECKS_T211,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-212",
    phase: null,
    status: "approved",
    checks: CHECKS_T212,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-213",
    phase: null,
    status: "approved",
    checks: CHECKS_T213,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
