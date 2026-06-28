import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-220",
    storyKey: "US-220",
    summary:
      "InlineBlockNormalizer no player_script_runner: `_normalize_inline_blocks()` quebra corpos inline/one-liner (while/recursão/statements na linha do `:`) em multi-linha ANTES da instrumentação dos guards (loop/depth), fechando o buraco do T-200. + ≥4 testes de regressão (recursão one-liner + while inline). [Código já na main: 4b3f920, autor Matheus.]",
    definitionOfDone:
      "Código inline/one-liner com while/recursão infinita NÃO crasha (vira no-op + erro, idêntico ao multi-linha); ≥4 testes de regressão reproduzem o crash sem o fix e verificam no-op com ele, sem pending; check.sh 100% verde (347/347), 0 regressão das features 001–021.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
];
