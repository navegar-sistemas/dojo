import type { IReviewCheckOutcome, IReviewRecord } from "../types.ts";

/**
 * Registros de revisão de conformidade da feature 006 (UI/UX e fluxo de telas).
 * Fonte: AUDITORIA read-only do agente-tech-lead (chat cmqx8yx6s) sobre o worktree
 * feature/006-aprimoramento @3640139, com decisões de produto do agente-po (cmqx97i2b).
 * Gates de código da branch 006 VERDES: arch_guard + lint + GUT 128/128 (496 asserts),
 * check.sh "tudo verde". Vereditos por bloco:
 *  - S1 (T-060..064) ScreenManager uma-tela-por-vez / arena: CONFORME (estático).
 *  - S2 (T-065..071) data-driven (EntityAssetRegistry, sprites, tiles, animações): CONFORME 5/5.
 *  - S3.1 (T-072..073) editor de código retrátil (preserva texto+arena): CONFORME.
 *  - S3.2 (T-074) console com controles (RF-064): CONFORME — decisão PO: play/pause como
 *    toggle único + passo + velocidade cobre funcionalmente os 4 controles.
 *  - S3.3 (T-075) Theme único (RNF-063): CONFORME — decisão PO: ~30 cores hardcoded em
 *    code_editor_panel/turn_console são SEMÂNTICAS DE CONTEÚDO (significado), fora do escopo
 *    do Theme (coesão de chrome das 5 telas + HUD), que está aplicado (game_theme.tres).
 * OBSERVAÇÕES ABERTAS (fora do alcance do spec/curadoria; rastreadas):
 *  - INTEGRAÇÃO na main: o código vive na branch feature/006; a main (8086a7d) só tem specs.
 *    Merge à base é decisão de release do Usuario — ESCALADO (agente-po cmqx97i2b).
 *  - EVIDÊNCIA RUNTIME: itens [RUNTIME] (1 tela de topo pós-transição, sem vazar nós no ciclo,
 *    animações disparando, console dirigindo turnos, editor preservando estado) dependem de
 *    rodar o jogo — pendente do agente-dev. Mecanismos presentes (estático OK).
 * Reviewer registrado = "usuario" (ator de produto); a varredura técnica foi do agente-tech-lead.
 */
const CHECKS: IReviewCheckOutcome[] = [
  { name: "Guard de Clean Architecture (presentation não importa src/domain)", command: "bash scripts/arch_guard.sh", passed: true },
  { name: "Formatação + lint GDScript (gdformat/gdlint)", command: "bash scripts/lint.sh", passed: true },
  { name: "Testes unitários de domínio (GUT headless, 128/128, 496 asserts)", command: "bash scripts/test.sh", passed: true },
  { name: "Suíte completa (arch_guard + lint + testes)", command: "bash scripts/check.sh", passed: true },
];

export const reviews: IReviewRecord[] = [
  // ── S1 — Legibilidade: ScreenManager (US-060) + arena em destaque (US-061) ────────
  { target: "code", taskKey: "T-060", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-061", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-062", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-063", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-064", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  // ── S2 — Salto visual: registro data-driven, sprites, tiles, animações ───────────
  { target: "code", taskKey: "T-065", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-066", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-067", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-068", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-069", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-070", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-071", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  // ── S3.1 — Editor de código retrátil (US-066) ────────────────────────────────────
  { target: "code", taskKey: "T-072", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  { target: "code", taskKey: "T-073", phase: null, status: "approved", checks: CHECKS, findings: [], reviewer: "usuario", reviewedAt: "2026-06-28" },
  // ── S3.2 — Console de turnos com controles (US-067, RF-064) ───────────────────────
  {
    target: "code",
    taskKey: "T-074",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Console: play/pause implementado como toggle único (sem botão pause separado); passo-a-passo e velocidade presentes (execution_controls.gd:17-19; game_controller.gd:49-51,173-187).",
        location: "src/presentation/execution_controls.gd",
        resolution:
          "CONFORME por decisão do agente-po (cmqx97i2b): toggle play/pause é UX padrão e cobre funcionalmente os 4 controles exigidos por RF-064; lista de turn_events em ordem verificada.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  // ── S3.3 — Theme único nas 5 telas + HUD (US-068, RNF-063) ────────────────────────
  {
    target: "code",
    taskKey: "T-075",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "~30 cores hardcoded em code_editor_panel.gd:70-90 (syntax-highlight de keywords) e turn_console.gd:6-42 (severidade de log), fora do recurso Theme único.",
        location: "src/presentation/code_editor_panel.gd, src/presentation/turn_console.gd",
        resolution:
          "CONFORME por decisão do agente-po (cmqx97i2b): são cores SEMÂNTICAS DE CONTEÚDO (codificam significado funcional), não estilo de chrome; RNF-063 visa coesão das 5 telas + HUD (paleta/tipografia), aplicada via game_theme.tres (project.godot:31). Essas cores não pertencem ao Theme.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
