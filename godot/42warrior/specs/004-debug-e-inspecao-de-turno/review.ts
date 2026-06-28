import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão da feature 004 (debug e inspeção de turno, PR-011).
 * Revisão independente do tech-lead sobre o worktree feature/004. RNF-041
 * (determinismo) confirmado: GameController._compute_turns usa o MESMO loop do
 * LevelRunner.run (mesmo TurnResolver/resolve); o passo-a-passo só lê/exibe o
 * pré-computado, não re-resolve (TurnResolver puro + LevelState imutável).
 * arch_guard verde (TurnEventFormatter puro em Application); Domain intocado;
 * GUT 119/119. Varredura de conformidade delegada a subagente read-only.
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
    taskKey: "T-040",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "GameController usa Array não-tipado para _turn_history/_turn_errors/_level_events (CONV-004 pede tipagem explícita).",
        location: "src/presentation/game_controller.gd:17-19",
        resolution:
          "Não-bloqueante: typed arrays de classes custom em GDScript têm atrito conhecido; aceitável. Recomendado tipar (Array[TurnResult]) onde viável.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-041",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "test_execution_determinism reimplementa o loop de turnos em vez de exercitar GameController._compute_turns; uma divergência futura no controller não seria pega (hoje idênticos).",
        location: "test/application/test_execution_determinism.gd:8-30",
        resolution:
          "Não-bloqueante: RNF-041 verificado hoje (mesmo loop, confirmado na revisão). Recomendado o teste chamar _compute_turns diretamente p/ proteger contra regressão.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-042",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "test_execution_determinism compara só outcome+turns (não HP/posições/eventos) e cobre níveis 1/3/5 (não os 9).",
        location: "test/application/test_execution_determinism.gd:46-47",
        resolution:
          "Não-bloqueante: outcome+turns são o invariante crítico de RNF-041 (o passo-a-passo não muda o desfecho). Recomendado ampliar p/ os 9 níveis e comparar o estado final.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-043",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "PR-011 menciona logar 'o que o warrior SENTIU'; o log cobre ações+efeitos (todos os exemplos concretos do PR) mas não os sentidos (feel/look não geram TurnEvent).",
        location: "src/application/turn_event_formatter.gd",
        resolution:
          "Cumpre o DoD de T-043 ('contexto sentido QUANDO DISPONÍVEL' / 'leitura pura dos TurnEvents'): sentidos não estão nos TurnEvents, então a leitura pura não os mostra — coerente. Logar sentidos (gerar eventos SENSED) é melhoria futura de PR-011, fora do escopo das tasks atuais.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
];
