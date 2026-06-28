import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Normalização de blocos inline + provas de regressão",
    goal: "Código inline/one-liner com while/recursão infinita vira no-op + erro (sem crash) via normalização inline→multi-linha antes da instrumentação dos guards, provado por ≥4 testes de regressão sem máscara, 0-regressão. Código já na main (4b3f920).",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-220"],
  },
];
