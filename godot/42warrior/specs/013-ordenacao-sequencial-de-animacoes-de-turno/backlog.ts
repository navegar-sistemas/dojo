import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-130",
    asA: "jogador",
    iWant: "que as animações de um turno toquem em ordem — o warrior chega ao destino e só então sofre/causa dano",
    soThat: "eu entenda a causalidade do turno (andou → chegou → levou dano) sem confusão visual",
    acceptanceCriteria: [
      "Dado um turno com [MOVED, DAMAGED], quando as animações tocam, então o flash de dano só inicia APÓS o tween de move concluir (warrior no destino) (RF-130).",
      "Dado um turno com [MOVED, ATTACKED], quando as animações tocam, então o ataque só inicia após o move concluir (RF-130).",
      "Dado a sequência de animações do turno, quando a última conclui, então all_done emite e a câmera (011) sincroniza com o fim da sequência (RF-132).",
    ],
    requirementKeys: ["RF-130", "RF-132"],
    priority: "highest",
    storyPoints: 8,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-131",
    asA: "jogador",
    iWant: "que um golpe e o dano que ele causa no mesmo instante apareçam juntos, não em dois passos separados",
    soThat: "o feedback de um ataque continue natural e imediato",
    acceptanceCriteria: [
      "Dado um ATTACKED (pulse do atacante + hurt do alvo no mesmo instante), quando ele anima, então ambos tocam juntos como um único beat concorrente, sem serializar um após o outro (RF-131).",
    ],
    requirementKeys: ["RF-131"],
    priority: "high",
    storyPoints: 3,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-132",
    asA: "agente-dev",
    iWant: "que a orquestração de animações seja uma fila ordenada consultável que respeite os controles de velocidade existentes",
    soThat: "a ordem possa ser provada por teste (não por timing) sem regredir a velocidade do turno",
    acceptanceCriteria: [
      "Dado a orquestração de animações, quando inspeciono a fila/sequência, então ela é consultável e um teste GUT confirma que o tween do evento N+1 só inicia após o N (par MOVED→dano) (RF-133, RNF-130).",
      "Dado os controles de velocidade/step da 004, quando a sequência roda, então ela os respeita sem redesenhá-los e a suíte permanece 100% verde (RNF-130).",
    ],
    requirementKeys: ["RF-133", "RNF-130"],
    priority: "high",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
];
