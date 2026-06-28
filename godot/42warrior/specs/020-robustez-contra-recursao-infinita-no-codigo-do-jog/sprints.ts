import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Depth-guard de recursão + provas de teste",
    goal: "Recursão infinita no código do jogador vira no-op + erro (sem crash) via depth-guard explícito, em todas as superfícies, provado por teste que reproduz o crash + teste de sintaxe-inválida — sem pending/skip, 0 regressão.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-200", "US-201"],
  },
];
