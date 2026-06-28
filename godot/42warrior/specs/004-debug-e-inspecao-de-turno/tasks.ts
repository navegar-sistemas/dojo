import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-040",
    storyKey: "US-040",
    summary:
      "Implementar o TurnEventFormatter e o TurnConsole: traduzir cada TurnEvent numa entrada textual (ação + efeito) e listá-las em ordem, destacando o turno corrente.",
    definitionOfDone:
      "Rodar um nível popula o console com uma entrada por turno descrevendo ação e efeito (andou/atacou N/descansou +N/dano/resgate/sem ação); a entrada do turno exibido fica destacada.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-041",
    storyKey: "US-041",
    summary:
      "Implementar o WarriorStatePanel: exibir HP atual/máximo, posição e direção do warrior e o turno/inimigos restantes, atualizado a cada turno exibido.",
    definitionOfDone:
      "Durante a execução, o painel mostra HP/posição/direção do warrior e turno/inimigos coerentes com o LevelState de cada turno exibido.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-042",
    storyKey: "US-042",
    summary:
      "Implementar o ExecutionControls: play, pause, passo-a-passo (1 turno) e ajuste de velocidade, governando o ritmo de apresentação sobre o LevelRunner sem alterar o resultado.",
    definitionOfDone:
      "play/pause e passo-a-passo funcionam; mudar a velocidade altera o intervalo. Teste compara o LevelState final entre execução contínua, pausada e passo-a-passo: 0 diferenças (RNF-041).",
    status: "done",
    dependsOn: ["T-040", "T-041"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-043",
    storyKey: "US-043",
    summary:
      "Associar erros do código do jogador e o contexto sentido (quando disponível) à entrada do turno no console, mantendo a inspeção como leitura pura dos TurnEvents.",
    definitionOfDone:
      "Um erro num turno aparece na entrada daquele turno sem travar a navegação; grep confirma que a camada de debug não escreve no domínio (RNF-040).",
    status: "done",
    dependsOn: ["T-040"],
    parallel: false,
    assignee: "usuario",
  },
];
