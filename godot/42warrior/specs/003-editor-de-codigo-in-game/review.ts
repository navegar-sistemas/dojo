import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão da feature 003 (editor de código in-game, PR-010).
 * Revisão independente do tech-lead sobre o worktree feature/003. RNF-030
 * (isolamento: editor não referencia LevelState/Unit) e RNF-031 (save exclusivo
 * em user://) verificados por grep; arch_guard verde, Domain intocado (diff vs
 * main vazio); GUT 102/102. Tratamento de erro de compilação não trava o jogo.
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
    taskKey: "T-030",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
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
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "PlayerCodeStore.save() ignora silenciosamente falha de FileAccess.open — perda do código do jogador (user://) seria silenciosa.",
        location: "src/application/player_code_store.gd:6-8",
        resolution:
          "Não-bloqueante (baixo impacto; user:// raramente falha). Recomendado logar/retornar a falha. RNF-031 cumprido: save exclusivo em user:// (grep confirmou zero res://).",
      },
    ],
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
  {
    target: "code",
    taskKey: "T-034",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Robustez do runner: não há proteção contra loop infinito DENTRO de um turno (while true no play_turn do jogador congelaria a thread); MAX_TURNS=200 limita o número de turnos, não a duração de um turno.",
        location: "src/application/player_script_runner.gd:46",
        resolution:
          "Não-bloqueante: limitação inerente do modelo (igual ao Ruby Warrior original); aceitável p/ a jam. O tratamento de erro de COMPILAÇÃO está correto (ErrorView + return, não trava o jogo); RNF-030 (isolamento) OK.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-035",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "CodeEditorPanel usa igualdade de texto (_editor.text == _ref_source) como flag de toggle do 'Ver solução'; se o jogador digitar exatamente a solução-referência, o toggle se confunde.",
        location: "src/presentation/code_editor_panel.gd:59-64",
        resolution:
          "Edge case cosmético, não-bloqueante. RNF-030 confirmado: o editor só emite signal run_pressed(source), sem referenciar LevelState/Unit (verificado por grep).",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
];
