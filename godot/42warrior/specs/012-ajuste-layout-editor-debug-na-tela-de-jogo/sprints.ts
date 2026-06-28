import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Layout editor/debug",
    goal: "Reposicionar a tela de jogo: editor no painel principal, DebugPanel oculto por padrão e retrátil por um DebugBtn no fim da barra de botões do editor, com alternância não-destrutiva (sem trocar tela, recriar arena ou perder código). Realiza RF-120..123 / RNF-120 (PR-007/PR-010/PR-011).",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-120", "US-121", "US-122"],
  },
];
