import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "P0 — Domínio 2D (mundo, direções, sentidos)",
    goal: "Núcleo do domínio operando em 2D: LevelState unificado (R×C, 1×N=R=1), 4 direções absolutas com pivot, e sentidos/passo 2D — determinístico e engine-independente.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-180", "US-181", "US-182"],
  },
  {
    id: 2,
    name: "P1 — API do jogador nas 4 direções (retrocompat)",
    goal: "Fachada/catálogo/glossário expõem as 4 direções e o pivot 4-direções, preservando os scripts e níveis beginner (1×N como R=1) sem alteração do código do jogador.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-183"],
  },
  {
    id: 3,
    name: "P2 — Apresentação 2D, níveis e não-regressão",
    goal: "TileMap linhas×colunas, câmera 2 eixos, animações nas 4 direções e level_loader 2D; fecha a vertical com 0 regressão das 001–016 e cobertura de teste real do 2D.",
    state: "future",
    startDate: "",
    endDate: "",
    storyKeys: ["US-184", "US-185"],
  },
];
