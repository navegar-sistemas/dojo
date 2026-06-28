import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-200",
    title: "Depth-guard explícito no runner (não confiar em abort nativo de recursão)",
    context:
      "O player_script_runner hoje confia que 'recursão aborta nativamente' — premissa FALSA: recursão infinita estoura a pilha do motor e crasha (Stack overflow/underflow). O loop-guard da 014 instrumenta apenas `while`, não as chamadas de função, então recursão escapa do guard.",
    decision:
      "Instrumentar a execução do código do jogador com um DEPTH-GUARD explícito: um contador de profundidade da pilha de chamadas DO JOGADOR, incrementado na entrada de cada chamada e decrementado na saída; ao exceder um teto seguro, abortar o turno como no-op + erro reportado (mesmo caminho do loop-guard do while). O guard é determinístico e não depende de exceção/abort da engine. Reusa o canal de erro (ErrorView, RF-143) e vale em todas as superfícies (RF-144).",
    consequences:
      "Recursão infinita vira no-op+erro em vez de crash, com paridade ao while-guard. Custo: estender a instrumentação do runner (_instrument) e cobrir o caso por teste que reproduz o crash. O teto exato é decisão de implementação (não prescrito no spec).",
    status: "accepted",
    requirementKeys: ["RF-200", "RF-201", "RNF-200"],
    rejectedAlternatives: [
      {
        alternative: "Confiar no abort nativo da engine / try-catch da exceção de stack",
        reason: "É a premissa que falhou — a engine crasha antes de qualquer captura; não há exceção recuperável de stack-overflow em GDScript.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "RecursionDepthGuard",
    responsibility:
      "Extensão da instrumentação do player_script_runner: depth-guard na entrada/saída de cada chamada do código do jogador, com teto seguro; ao exceder, interrompe o turno (no-op) e reporta erro legível (ErrorView), em todas as superfícies que executam código do jogador. Coberto por teste que reproduz o crash + teste de sintaxe-inválida, sem pending/skip.",
    dependsOn: [],
    requirementKeys: ["RF-200", "RF-201", "RNF-200"],
  },
];
