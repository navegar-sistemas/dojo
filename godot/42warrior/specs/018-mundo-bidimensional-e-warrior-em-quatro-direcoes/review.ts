import type { IReviewRecord, IReviewCheckOutcome } from "../types.ts";

/**
 * Registros de revisão desta feature: code review por task e revisão de qualidade de spec.
 * Escritos pelo agente revisor (references/review.md) e gateados por review-feature.ts —
 * uma task done do sprint ativo exige um registro target="code" com status="approved",
 * sem achado pendente, sem uso de padrão rejeitado e com as checagens do projeto verdes.
 */

const CHECKS_T181: IReviewCheckOutcome[] = [
  {
    name: "Direction 4-dir (NORTH/SOUTH/EAST/WEST + delta()/pivot() horário/opposite()) — domínio puro, 0-RNG; FORWARD/BACKWARD mantidos, extensão NÃO-breaking (callers de relative_sign intocados) → 0-regressão por construção; merge-tree limpo (exit=0)",
    command: "git merge-tree (verificação do tech-lead) + arch_guard",
    passed: true,
  },
  {
    name: "Testes GUT — 288/288 na main pós-merge (test_direction: 19 testes — 4 direções + delta + pivot + opposite + equals + relative_sign); teste POR DIREÇÃO ✓, 0-regressão 001-016 ✓",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T180: IReviewCheckOutcome[] = [
  {
    name: "LevelState 2D (from_2d() grade R×C com Vector2i + space_at_2d() bounds) com a API 1D 100% PRESERVADA — R=1 = corredor beginner testado (retrocompat por construção, o DoD de R=1 que o PO reservou); merge-tree limpo",
    command: "git merge-tree (verificação do tech-lead) + arch_guard",
    passed: true,
  },
  {
    name: "Testes GUT — 286/286 na main pós-merge (test_018_level_state_2d); domínio puro, 0-RNG; 0-regressão 001-016",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T182: IReviewCheckOutcome[] = [
  {
    name: "Sentidos 2D (feel_2d/look_2d/direction_of_2d por eixo dominante |Δrow|≥|Δcol|→N/S senão E/W + direction_of_stairs_2d + step_of_2d/position_toward_2d) expostos ao código do jogador (WarriorFacade); domínio puro (RefCounted), 0-RNG, CQS; API 1D INTACTA → 0-regressão por construção; merge-tree limpo",
    command: "git merge-tree (verificação do tech-lead) + arch_guard",
    passed: true,
  },
  {
    name: "Testes GUT — 338/338 na main pós-merge (test_018_space_sentidos_2d: 21 testes feel/look/direction/step/CQS + diretos em Senses); teste POR DIREÇÃO ✓, 0-regressão 001-016 ✓",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T183: IReviewCheckOutcome[] = [
  {
    name: "PROVENIÊNCIA: aceite formal do PO (agente-po, cmqy2yfzg, verificado read-only @9587d40) + integrado na main (merge 9017967). RETROCOMPAT por construção (ponto crítico do DoD): diffstat dos testes +151/-0 (ZERO deleções; os 403 existentes, incl. suíte beginner 1×N, INTOCADOS); warrior_facade.gd (a API que o código do jogador CHAMA) NÃO alterada — só catalog+glossary (metadados das direções) → jogador não muda uma linha. reviewer=usuario = aceite REAL do PO, não rótulo presumido (git-author não usado como prova).",
    command: "git merge-tree (tech-lead) + chat_query cmqy2yfzg (aceite PO)",
    passed: true,
  },
  {
    name: "WarriorApiCatalog.direction_entries() 7 entradas kind=direction (N/S/E/W cardinais + forward/backward relativas + pivot_dir) SEPARADO de entries_for_level (não polui catálogo por nível); GlossaryCatalog chave 'directions' estável entre níveis; semântica forward/backward (relative_sign +1/-1) e pivot horário N→E→S→W preservados; Testes GUT 420/420 na main pós-merge (test_018_api_direcoes: 17 novos), 0-regressão 001-021",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T184: IReviewCheckOutcome[] = [
  {
    name: "PROVENIÊNCIA: aceite formal do PO (agente-po, cmqy4ho3d, verificado read-only na branch) + integrado na main (merge ca137a6). reviewer=usuario = aceite REAL do PO (git-author NÃO usado como prova).",
    command: "git log ca137a6 + chat_query cmqy4ho3d (aceite PO)",
    passed: true,
  },
  {
    name: "RENDER-RULE COUNT-LEVEL (conteúdo, não node-presence): floor_layer.get_used_cells().size()>=27 numa grade 3×9 (tiles REALMENTE desenhados); câmera segue o warrior em Y em nível alto (test_camera_segue_warrior_em_y_em_nivel_alto) + NÃO move quando nível<viewport (retrocompat sem level_height); animação 4-dir: flip_h Leste≠Oeste + rotation Norte≠Sul, AnimatedSprite2D ATIVO pós-refresh (o sprite MUDA conforme a direção). Testes GUT 461/461 na main, 0-regressão 001-021.",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T185: IReviewCheckOutcome[] = [
  {
    name: "LevelLoader 2D R×C: level_loader detecta rows>1 → LevelState.from_2d() (rows/warrior_position_2d/stairs_position_2d corretos); 1D INTACTO (rows()=1, cols=width). RETROCOMPAT EXEMPLAR: as reference_solutions dos 9 níveis continuam VENCIDAS pelas soluções (não só 'carrega' — joga). Aceite PO cmqy4ho3d, integrado ca137a6.",
    command: "bash scripts/check.sh",
    passed: true,
  },
  {
    name: "Testes GUT 461/461 na main pós-merge (13 domain T-185 + 8 retrocompat 1D); level_definition campos rows/warrior_position_2d/build_units_2d; LevelState API 2D completa; 0-regressão.",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

const CHECKS_T186: IReviewCheckOutcome[] = [
  {
    name: "US-185 (Jurado, não-regressão/cobertura) MATERIALMENTE CUMPRIDO pela bateria embutida da entrega (PO cmqy4ho3d, integrado ca137a6): 4 direções (flip E/W + rotation N/S presentation + feel_2d N/S/E/W domain); paredes nas bordas R×C (space fora da grade = parede); sentidos 2D (test_018_space_sentidos_2d); R=1 beginner preservado (retrocompat 1D + reference_solutions verdes). check.sh 461/461, 0-regressão (os 420 anteriores INTACTOS).",
    command: "bash scripts/check.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-180",
    phase: null,
    status: "approved",
    checks: CHECKS_T180,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-181",
    phase: null,
    status: "approved",
    checks: CHECKS_T181,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-182",
    phase: null,
    status: "approved",
    checks: CHECKS_T182,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-183",
    phase: null,
    status: "approved",
    checks: CHECKS_T183,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-184",
    phase: null,
    status: "approved",
    checks: CHECKS_T184,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-185",
    phase: null,
    status: "approved",
    checks: CHECKS_T185,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-186",
    phase: null,
    status: "approved",
    checks: CHECKS_T186,
    findings: [],
    reviewer: "usuario",
    reviewedAt: "2026-06-28",
  },
];
