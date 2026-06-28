import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Build web jogável + smoke do runtime",
    goal: "O jogo abre e roda no navegador (renderer Compatibility + preset Web), com áudio no 1º gesto e persistência user://-IndexedDB, e o PILAR provado por smoke web (o warrior executa o código do jogador no WASM) com 0 regressão desktop e shader/perf no WebGL2.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-210", "US-211", "US-212"],
  },
];
