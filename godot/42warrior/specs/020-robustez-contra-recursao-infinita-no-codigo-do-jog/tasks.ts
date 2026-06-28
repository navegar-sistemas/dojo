import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-200",
    storyKey: "US-200",
    summary:
      "Implementar o DEPTH-GUARD de recursão no player_script_runner: instrumentar a entrada/saída de cada chamada do código do jogador com um contador de profundidade + teto seguro; ao exceder, interromper o turno (no-op) e reportar erro legível (ErrorView). Remover/corrigir a premissa falsa do abort nativo. Vale nas 3 superfícies (game_controller, seleção/replay 009, sandbox 010).",
    definitionOfDone:
      "Código do jogador com recursão infinita NÃO crasha (sem Stack overflow/underflow): vira no-op + erro reportado, de forma determinística (sem depender de abort nativo), idêntico nas 3 superfícies; reusa o canal de erro da 014 (RF-143).",
    status: "todo",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-201",
    storyKey: "US-201",
    summary:
      "Provas de teste GUT: (1) teste que REPRODUZ o crash de recursão infinita antes do fix e verifica no-op real depois (sem pending/skip); (2) teste de SINTAXE-INVÁLIDA preenchendo o gap histórico. Rodar check.sh.",
    definitionOfDone:
      "≥1 teste de recursão infinita reproduz o crash e depois verifica no-op (has_error/reporte) sem máscara; ≥1 teste de sintaxe-inválida; check.sh 100% verde, sem pending/skip, com 0 regressão da 014 (RF-140..144) e das features 001–019.",
    status: "todo",
    dependsOn: ["T-200"],
    parallel: false,
    assignee: null,
  },
];
