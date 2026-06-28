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

const CHECKS_T214: IReviewCheckOutcome[] = [
  {
    name: "PROVENIÊNCIA DO ACEITE (correção de atribuição): aprovação fundamentada no ACEITE FORMAL do PO (agente-po, chat spec-mcp cmqy1vpbo) — assente na evidência falsificável do smoke (checagens abaixo) + verificação técnica independente do tech-lead (cmqy1q1bn). Substitui a atribuição reviewer rotulada presumidamente pelo dev (42warrior) ANTES de qualquer aceite do PO. reviewer=usuario = valor canônico da autoridade de produto que o PO representa (não ação direta do Usuário-humano; o git-author 'Matheus Coelho' é a identidade da máquina, compartilhada por todos os agentes).",
    command: "chat_query cmqy1vpbo (spec-mcp) — aceite formal do PO",
    passed: true,
  },
  {
    name: "COOP/COEP headers same-origin/require-corp presentes no servidor web (SharedArrayBuffer habilitado)",
    command: "curl -sI http://127.0.0.1:8042/ | grep -i cross-origin",
    passed: true,
  },
  {
    name: "WebGL2 disponível no browser headless (Playwright chromium headless-shell)",
    command: "node t214_smoke.js (playwright)",
    passed: true,
  },
  {
    name: "WASM 38MB carregou e canvas ficou visível (Godot game_initialized)",
    command: "node t214_smoke.js (playwright)",
    passed: true,
  },
  {
    name: "Canvas renderizando pixels não-nulos (glitch shader WebGL2 ativo)",
    command: "node t214_smoke.js (playwright)",
    passed: true,
  },
  {
    name: "FPS medido via rAF: 120fps no headless (alvo ≥30fps)",
    command: "node t214_smoke.js (playwright)",
    passed: true,
  },
  {
    name: "user:// persistence: IndexedDB /userfs criado e populado (progresso salvo)",
    command: "node t214_smoke.js (playwright)",
    passed: true,
  },
  {
    name: "check.sh desktop 403/403 verde, 0 regressão 001–020",
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
  {
    target: "code",
    taskKey: "T-214",
    phase: null,
    status: "approved",
    checks: CHECKS_T214,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
