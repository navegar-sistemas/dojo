import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-220",
    title: "Normalizar inline→multi-linha ANTES de instrumentar (em vez de instrumentar inline)",
    context:
      "Os guards (loop-guard 014 + depth-guard 020) instrumentam corpos MULTI-LINHA. Código inline/one-liner (corpo na mesma linha do `:`) não casava o padrão de instrumentação → escapava → crash. Instrumentar diretamente cada forma inline seria frágil (muitas variações de sintaxe).",
    decision:
      "Pré-processar o código do jogador com `_normalize_inline_blocks()`: quebrar corpos inline em multi-linha ANTES da instrumentação dos guards. Assim os guards existentes (sem mudança) passam a cobrir o caso inline por construção. Determinístico; preserva a semântica do código do jogador.",
    consequences:
      "Inline/one-liner recebe o mesmo no-op+erro do multi-linha, sem crash; reusa os guards sem reescrevê-los. Custo: a heurística de normalização (decisão de implementação, já feita no 4b3f920) + os testes de regressão.",
    status: "accepted",
    requirementKeys: ["RF-220", "RNF-220"],
    rejectedAlternatives: [
      {
        alternative: "Instrumentar diretamente cada forma de corpo inline",
        reason: "Frágil — muitas variações de sintaxe inline; normalizar para multi-linha reusa os guards já provados.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "InlineBlockNormalizer",
    responsibility:
      "No player_script_runner: `_normalize_inline_blocks()` converte corpos inline/one-liner (while/recursão/statements na linha do `:`) em multi-linha antes da instrumentação dos guards, fechando o buraco do T-200. Coberto por ≥4 testes de regressão (recursão one-liner + while inline), sem máscara.",
    dependsOn: [],
    requirementKeys: ["RF-220", "RNF-220"],
  },
];
