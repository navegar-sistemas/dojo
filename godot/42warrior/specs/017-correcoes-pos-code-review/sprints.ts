import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Correções dos 3 bugs do code review",
    goal:
      "Fechar os 3 defeitos do code review com teste que exercita cada caso: #1 prova de cena do no-op (fix já na 013), #2 cativo não pontua, #3 ranged dispara na escada — 0 regressão.",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-170", "US-171", "US-172"],
  },
];
