import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão da feature 005 (áudio + fluxo de jogo, PR-008/PR-009).
 * Revisão independente do tech-lead sobre o worktree feature/005 (HEAD 8e11343).
 * PR-008 (fluxo: menu→transição→jogo→resultado→créditos via TowerFlow autoload) e
 * PR-009 (áudio: AudioManager SFX+música em loop+volume, gracioso) cobertos.
 * ProgressStore persiste em user:// (zero res:// de escrita); arch_guard verde;
 * Domain intocado (diff vs main vazio); GUT 128/128. Varredura delegada a
 * subagente read-only e consolidada pelo revisor.
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
    taskKey: "T-050",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "ProgressStore (Application) depende de APIs de engine (ConfigFile/FileAccess/DirAccess) para persistir em user://progress.cfg. Em Clean Architecture estrita, I/O de persistência seria camada Infra, não Application.",
        location: "src/application/progress_store.gd",
        resolution:
          "Não-bloqueante: consistente com o padrão do projeto (stores de persistência em Application — ex.: PlayerCodeStore da 003, já aprovado) e arch_guard verde (barra 'extends Node'/dependência de Domain, não FileAccess). Persistência em user:// confirmada (zero res:// de escrita).",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-051",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-052",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-053",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-054",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "AudioManager.on_events toca só o PRIMEIRO evento do turno (break); sons relevantes (ex.: ENEMY_DEFEATED/WON após um MOVED no mesmo turno) podem ser suprimidos.",
        location: "src/presentation/audio_manager.gd:42-44",
        resolution:
          "Não-bloqueante: documentado como anti-overlap intencional. Recomendado priorizar o evento mais relevante do turno (não o primeiro) p/ não perder feedback sonoro. Mapeamento dos 9 TurnEvent.Kind→SFX e graceful (silêncio se asset ausente) verificados.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
  {
    target: "code",
    taskKey: "T-055",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "desvio_convencao",
        severity: "warning",
        detail:
          "linear_to_db(0.0) retorna -inf ao zerar o volume; muta corretamente, mas -inf em volume_db é frágil.",
        location: "src/presentation/audio_manager.gd:34,58",
        resolution:
          "Não-bloqueante: funcional (muta). Recomendado clampf mínimo (ex.: -80 dB) em vez de -inf. Música em loop e controle de volume (com clamp) verificados.",
      },
    ],
    reviewer: "usuario",
    reviewedAt: "2026-06-27",
  },
];
