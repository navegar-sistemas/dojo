import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-200",
    asA: "Jogador",
    iWant:
      "que um código meu com recursão infinita não trave/feche o jogo, virando no-op com erro reportado",
    soThat:
      "eu não perca a sessão por um bug do meu código e entenda o que aconteceu, igual ao loop while infinito",
    acceptanceCriteria: [
      "Dado um código do jogador com recursão infinita, quando o turno é executado, então o jogo NÃO crasha (sem Stack overflow/underflow): a execução vira no-op e um erro legível é reportado na ErrorView.",
      "Dado o depth-guard, quando a profundidade de chamadas do jogador excede o teto seguro, então o turno é interrompido de forma determinística — sem depender de abort nativo da engine.",
      "Dado que a robustez vale em todas as superfícies, quando a recursão infinita ocorre na tela de jogo, na seleção/replay (009) ou no sandbox (010), então o comportamento no-op+erro é idêntico em todas.",
    ],
    requirementKeys: ["RF-200", "RF-201"],
    priority: "highest",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
  {
    key: "US-201",
    asA: "Jurado da Jam",
    iWant:
      "que a robustez contra recursão e sintaxe inválida seja provada por teste real, sem máscara",
    soThat:
      "eu confie que a promessa de 'não crasha com código ruim' é verdadeira e não um verde falso",
    acceptanceCriteria: [
      "Dado o defeito de recursão, quando rodo a suíte, então existe ≥1 teste que REPRODUZ o crash antes do fix e verifica no-op real depois — com 0 uso de pending/skip para mascarar.",
      "Dado o gap histórico, quando rodo a suíte, então há ≥1 teste de SINTAXE-INVÁLIDA cobrindo o caminho que deixou o defeito passar.",
      "Dado o conjunto, quando rodo check.sh, então fica 100% verde sem pending/skip e com 0 regressão da 014 e das features 001–019.",
    ],
    requirementKeys: ["RNF-200"],
    priority: "highest",
    storyPoints: 2,
    status: "done",
    assignee: null,
  },
];
