import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-140",
    asA: "jogador",
    iWant: "que meu código com erro (de sintaxe ou que quebra ao rodar) não trave o jogo e me mostre o erro de forma legível",
    soThat: "eu corrija e tente de novo sem reiniciar o jogo — o público iniciante erra o tempo todo",
    acceptanceCriteria: [
      "Dado código do jogador com erro de SINTAXE, quando eu rodo, então o jogo não crasha, o runner fica em erro e a ErrorView mostra a falha de forma legível (RF-140, RF-143).",
      "Dado código que compila mas falha em RUNTIME no play_turn (método inexistente/null/tipo/assert), quando o turno roda, então o jogo não crasha, o turno vira no-op/erro e a ErrorView mostra a causa/linha quando disponível (RF-141, RF-143).",
    ],
    requirementKeys: ["RF-140", "RF-141", "RF-143"],
    priority: "highest",
    storyPoints: 8,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-141",
    asA: "jogador",
    iWant: "que um código meu com loop ou recursão sem fim não congele o jogo",
    soThat: "um engano comum de iniciante não me obrigue a matar o processo",
    acceptanceCriteria: [
      "Dado código do jogador com loop/recursão que não termina, quando o turno roda, então a execução é interrompida com segurança, reportada como erro, e o jogo segue responsivo (RF-142).",
    ],
    requirementKeys: ["RF-142"],
    priority: "high",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-142",
    asA: "jogador",
    iWant: "que essa proteção valha em todas as telas onde meu código roda, com a correção comprovada por testes",
    soThat: "eu nunca caia num crash, seja no jogo normal, no replay ou no sandbox",
    acceptanceCriteria: [
      "Dado os caminhos que rodam código do jogador (game_controller, replay 009, sandbox 010), quando qualquer um executa código com erro, então todos têm a mesma robustez (não-crash + reporte) (RF-144).",
      "Dado os 3 caminhos de erro (sintaxe, runtime, loop/recursão), quando os testes GUT os exercitam, então em todos o runner não crasha (has_error/no-op) e reporta, o crash relatado é reproduzido antes da correção e a suíte permanece 100% verde (RNF-140).",
    ],
    requirementKeys: ["RF-144", "RNF-140"],
    priority: "high",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
];
