import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Legibilidade — fim da sobreposição",
    goal: "Destravar a legibilidade da tela de jogo: ScreenManager uma-tela-por-vez (mata o bug de sobreposição) e layout 'arena em destaque'. Prioridade 1 do PO.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-060", "US-061"],
  },
  {
    id: 2,
    name: "Salto visual",
    goal: "Identidade visual coesa: registro data-driven de assets, sprites das 7 entidades e tiles do corredor com arte da internet, e animações por TurnEvent. Prioridade 2 do PO.",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-062", "US-063", "US-064", "US-065"],
  },
  {
    id: 3,
    name: "Imersão e polish",
    goal: "Imersão na batalha: editor de código retrátil, console de turnos com controles e Theme único coeso nas 5 telas + HUD. Prioridade 3 do PO.",
    state: "future",
    startDate: "",
    endDate: "",
    storyKeys: ["US-066", "US-067", "US-068"],
  },
];
