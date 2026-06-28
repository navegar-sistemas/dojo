import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

const CHECKS_T200: IReviewCheckOutcome[] = [
  {
    name: "Depth-guard CALL_DEPTH_LIMIT=64 (__enter_func) no player_script_runner: recursão infinita (direta/helper) vira no-op + erro reportado — reproduzi 'SURVIVED' sem Stack overflow/underflow/Engine Bug; corrige a premissa falsa da 014 (não depende de abort nativo)",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Código integrado na main (merge 3662408); check.sh verde pós-merge",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T201: IReviewCheckOutcome[] = [
  {
    name: "Provas sem máscara: 3 testes de recursão (direta/helper/legítimo) reproduzem o crash e verificam no-op real + teste de SINTAXE-INVÁLIDA (compile('func play_turn(w) walk(') == null E has_error()) — gap histórico fechado; 0 pending/skip",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Testes GUT — 278/278 verde; 0-regressão da 014 (RF-140..144) e das features 001–019",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-200",
    phase: null,
    status: "approved",
    checks: CHECKS_T200,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-201",
    phase: null,
    status: "approved",
    checks: CHECKS_T201,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
