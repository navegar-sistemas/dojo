import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-050",
    storyKey: "US-050",
    summary:
      "Implementar o menu inicial e o ProgressStore: iniciar (nível 1) ou continuar (nível salvo), lendo/gravando o progresso em user://.",
    definitionOfDone:
      "O menu mostra iniciar e continuar; continuar leva ao nível salvo; sem save, iniciar começa no nível 1 sem erro (RNF-051).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-051",
    storyKey: "US-051",
    summary:
      "Implementar a tela de transição de nível: exibir nome/descrição do nível e as habilidades novas introduzidas antes de iniciá-lo.",
    definitionOfDone:
      "Ao começar um nível, a transição mostra descrição e habilidades novas coerentes com a definição do nível (feature 001).",
    status: "done",
    dependsOn: ["T-050"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-052",
    storyKey: "US-052",
    summary:
      "Implementar o TowerFlowController: avanço ao vencer, reinício do nível e tela de resultado com pontuação/ace (consumindo o ScoringService da feature 001).",
    definitionOfDone:
      "Vencer mostra o resultado com score e ace e avança ao próximo; reiniciar recomeça o nível do estado inicial.",
    status: "done",
    dependsOn: ["T-050"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-053",
    storyKey: "US-053",
    summary:
      "Implementar a tela de conclusão da torre + créditos, exibida ao vencer o último nível.",
    definitionOfDone:
      "Vencer o último nível mostra a tela de conclusão e os créditos.",
    status: "done",
    dependsOn: ["T-052"],
    parallel: false,
    assignee: "usuario",
  },
  {
    key: "T-054",
    storyKey: "US-054",
    summary:
      "Implementar o AudioManager para SFX: assinar TurnEvents e tocar o efeito sonoro de cada evento (andar/atacar/dano/descanso/resgate/tiro/vitória/derrota) de forma assíncrona.",
    definitionOfDone:
      "Cada evento de turno toca o SFX correspondente; medição mostra 0 ms de atraso adicionado ao ciclo de turno (RNF-052).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: "usuario",
  },
  {
    key: "T-055",
    storyKey: "US-055",
    summary:
      "Adicionar trilha de fundo em loop e controle de volume (música/SFX) ao AudioManager, com assets de áudio CC0 referenciados de forma trocável.",
    definitionOfDone:
      "Há trilha em loop e controle de volume música/SFX; os assets são CC0 num diretório trocável; grep confirma 0 referência a áudio em src/domain (RNF-050).",
    status: "done",
    dependsOn: ["T-054"],
    parallel: false,
    assignee: "usuario",
  },
];
