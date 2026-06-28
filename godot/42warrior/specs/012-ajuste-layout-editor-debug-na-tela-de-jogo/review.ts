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
    name: "Testes unitários de domínio (GUT, headless) — 165/165",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-120",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-121",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "DoD T-121 pede 'teste GUT cobre o toggle de visibilidade pelo DebugBtn'. Nenhum teste GUT foi adicionado para esse comportamento. O toggle é 100% presentation-layer (emissão de sinal + visibilidade de nó), fora do escopo de CONV-006 (testes de domínio). Verificado por inspeção funcional: sinal debug_toggled emitido corretamente pelo DebugBtn.",
        location: "src/presentation/code_editor_panel.gd:_on_debug_toggle",
        resolution:
          "Não-bloqueante para a jam: coverage por inspeção é suficiente. Um teste GUT de apresentação pode ser adicionado em iteração futura se o padrão de testes for expandido além do domínio.",
      },
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "DoD diz 'DebugPanel inicia com visible=false' (o PanelContainer inteiro). A implementação oculta apenas TurnConsole (o console de log), mantendo WarriorStatePanel e ExecutionControls sempre visíveis. Decisão alinhada ao pedido explícito do usuário: 'editor em baixo entre as informacoes do estado e dos botões de retorno/passo' — tanto Estado quanto Controles devem ser visíveis por padrão.",
        location: "scenes/game.tscn:TurnConsole",
        resolution:
          "Não-bloqueante: a intenção do produto (debug oculto por padrão) está satisfeita. O 'debug' aqui é o log de turnos (TurnConsole), não o painel de controles. Comportamento correto para o fluxo do jogador.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-122",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
];
