import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-220",
    asA: "Jogador",
    iWant:
      "que um código meu escrito em uma linha só (inline/one-liner) com while/recursão infinita não trave o jogo",
    soThat:
      "eu não perca a sessão por um estilo de código que escapava do guard, igual ao código multi-linha",
    acceptanceCriteria: [
      "Dado um código inline/one-liner com while ou recursão infinita (ex.: `func play_turn(w): while true: pass`), quando o turno executa, então o jogo NÃO crasha (sem Stack overflow): vira no-op + erro reportado, idêntico ao multi-linha.",
      "Dado o pré-processamento, quando o runner normaliza o corpo inline para multi-linha antes de instrumentar, então os guards (loop/depth) passam a cobrir o caso por construção, de forma determinística.",
      "Dado a regressão, quando rodo a suíte, então há ≥4 testes (recursão one-liner + while inline) que reproduzem o crash sem o fix e verificam no-op com ele — sem pending — e check.sh fica verde (347/347), 0 regressão 001–021.",
    ],
    requirementKeys: ["RF-220", "RNF-220"],
    priority: "highest",
    storyPoints: 2,
    status: "done",
    assignee: null,
  },
];
