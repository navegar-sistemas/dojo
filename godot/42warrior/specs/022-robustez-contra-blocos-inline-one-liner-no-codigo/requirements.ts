import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-220",
    kind: "functional",
    description:
      "NORMALIZAÇÃO DE BLOCOS INLINE: o player_script_runner NORMALIZA corpos inline/one-liner (statements escritos na mesma linha do `:`, ex.: `func play_turn(w): while true: pass`) para a forma MULTI-LINHA ANTES de instrumentar os guards (loop-guard da 014 + depth-guard da 020). Assim, código inline com while/recursão infinita NÃO escapa do guard — recebe o MESMO tratamento do multi-linha: a execução vira no-op + erro reportado, SEM crash/Stack overflow. Fecha o buraco com que o T-200 estava done.",
    priority: "highest",
    rationale: "P0 do Matheus (cmqy0fd2g): inline/one-liner escapava do guard → crash; o fix 4b3f920 normaliza inline→multi-linha. Estende RF-143/RF-200 ao caso inline.",
  },
  {
    key: "RNF-220",
    kind: "non_functional",
    description:
      "PROVADO POR TESTE, SEM MÁSCARA: há ≥4 testes de regressão (recursão one-liner + while inline, nas superfícies aplicáveis) que REPRODUZEM o crash sem a normalização e verificam no-op real com ela — 0 uso de pending/skip. check.sh permanece 100% verde (347/347 no fix), com 0 regressão das features 001–021.",
    priority: "highest",
    rationale: "Critério do PO (cmqy0fd2g): o DoD é exatamente os +4 testes do fix do Matheus, verdes e sem máscara, com 0-regressão.",
  },
];
