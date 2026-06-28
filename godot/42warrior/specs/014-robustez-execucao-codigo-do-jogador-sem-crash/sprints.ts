import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Execução robusta do código do jogador",
    goal: "Endurecer a execução do código do jogador no PlayerScriptRunner (fronteira única): sem crash para erro de sintaxe, runtime e loop/recursão; reporte legível na ErrorView; cobertura dos 3 caminhos (game_controller, 009, 010), provada por GUT. Realiza RF-140..144 / RNF-140 (PR-010).",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-140", "US-141", "US-142"],
  },
];
