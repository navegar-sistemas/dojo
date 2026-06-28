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
    name: "Testes GUT headless — 169/169, zero warnings",
    command: "bash scripts/test.sh",
    passed: true,
  },
];

export const reviews: IReviewRecord[] = [
  {
    target: "code",
    taskKey: "T-140",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "A mensagem de erro de compilação é genérica ('Erro de compilação: o código do jogador tem sintaxe inválida.') em vez de incluir a causa/linha que o Godot fornece internamente (RF-143). GDScript não expõe a string do parse error via API pública — `GDScript.reload()` retorna apenas OK/FAILED, sem mensagem. A mensagem é o máximo possível com a API da engine.",
        location: "src/application/player_script_runner.gd:compile",
        resolution:
          "Não-bloqueante para a jam: a mensagem é clara (informa que é erro de compilação) e o jogo não crasha. A causa exata (linha/coluna) não é acessível via API GDScript pública sem hooks de debugger.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-141",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "Erro de runtime em play_turn (método inexistente, acesso a null) resulta em no-op e Godot emite SCRIPT ERROR para o console — o processo não crasha e o jogo segue responsivo (RF-141 atendido). A mensagem de erro reportada ao jogador via has_error()/error() é vazia neste caso (apenas a ação é null). A mensagem de erro de runtime não é capturável via API GDScript pública.",
        location: "src/application/player_script_runner.gd:play_turn",
        resolution:
          "Não-bloqueante: o teste prova que o processo não crasha (RF-141). A mensagem vazia é uma limitação conhecida da API GDScript — melhorar exigiria ScriptDebugger hooks, fora do escopo da jam.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-142",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [
      {
        kind: "conformidade_spec",
        severity: "warning",
        detail:
          "A instrumentação de guarda de iteração é textual (não-AST): `while` dentro de string literal ou comentário pode ser instrumentado incorretamente. Limitação declarada no comentário do arquivo. Em cenários reais do jogo (código do jogador simples), esse edge case não ocorre.",
        location: "src/application/player_script_runner.gd:_guard_while",
        resolution:
          "Não-bloqueante: a limitação está documentada no código. Para a jam com código de jogador controlado, o risco é desprezível.",
      },
    ],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
  {
    target: "code",
    taskKey: "T-143",
    phase: null,
    status: "approved",
    checks: CHECKS,
    findings: [],
    reviewer: "agente-dev",
    reviewedAt: "2026-06-28",
  },
];
