import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Fundações P0 (paralelizáveis entre 2 devs)",
    goal:
      "As 4 fundações reutilizáveis, INDEPENDENTES entre si (sem dependsOn cruzado) para alocação por dev em worktrees disjuntas: US-160 (AnimatedSprite2D dos personagens), US-161 (TileMap 32px nativo da arena + feet-anchor), US-162 (botão 4-estados), US-172 (F4: Theme global + design system, resolve RNF-063). DoD por task = prova de render de cena (RNF-160).",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-160", "US-161", "US-162", "US-172"],
  },
  {
    id: 2,
    name: "Telas P0 (fluxo principal: jogo, menu, seleção)",
    goal:
      "As telas onde o jogador passa o tempo, fiéis aos mockups, reusando as fundações: US-163 (tela de JOGO/arena), US-164 (menu inicial), US-165 (seleção de níveis). Valor visível cedo. DoD por tela = prova de render de cena.",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-163", "US-164", "US-165"],
  },
  {
    id: 3,
    name: "Telas P1 (secundárias)",
    goal:
      "As telas secundárias, fiéis aos mockups: US-166 (resultado), US-167 (transição), US-168 (sandbox/tutorial), US-169 (glossário), US-170 (referência da API), US-171 (conclusão/créditos). Paralelizáveis por tela. DoD por tela = prova de render de cena.",
    state: "future",
    startDate: "",
    endDate: "",
    storyKeys: ["US-166", "US-167", "US-168", "US-169", "US-170", "US-171"],
  },
];
