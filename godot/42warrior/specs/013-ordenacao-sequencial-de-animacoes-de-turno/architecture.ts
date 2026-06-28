import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-030",
    title: "Orquestrador sequencial (fila ordenada) de animações de turno, com await por evento",
    context:
      "Em entity_sprite_registry.gd, animate_events(events) inicia todos os tweens na hora e só conta _pending — paralelo, sem ordem (RF-130). all_done emite quando o último termina, mas sem encadeamento; e não há estrutura consultável para testar a ordem (RF-132/133).",
    decision:
      "Refatorar animate_events para uma fila/sequência ordenada (AnimationSequencer): cada evento (ou beat) é enfileirado na ordem recebida e só inicia após o anterior CONCLUIR (await do tween/beat anterior). all_done emite após a última animação da fila. A fila/sequência é exposta de forma consultável para que um teste confirme que o evento N+1 só inicia após o N. Respeita a velocidade/step da 004 (RNF-130).",
    consequences:
      "Causalidade legível (andou→chegou→reagiu); câmera (011) sincroniza com o fim real da sequência. Testável por estrutura, não por timing. Custo: reescrever a orquestração de animate_events de paralelo para encadeado e expor a fila.",
    status: "accepted",
    requirementKeys: ["RF-130", "RF-132", "RF-133", "RNF-130"],
    rejectedAlternatives: [
      {
        alternative: "Manter o paralelo e só atrasar o tween de dano por um delay fixo",
        reason: "Timing frágil (não garante ordem em velocidades diferentes) e não testável estruturalmente; não resolve o bug de forma robusta.",
      },
    ],
  },
  {
    key: "ADR-031",
    title: "Par causa-efeito do mesmo instante tocado como um beat concorrente",
    context:
      "Nem todo par de eventos deve ser serializado: um ATTACKED é pulse do atacante + hurt do alvo no MESMO instante (RF-131). Serializá-los pareceria errado.",
    decision:
      "Modelar a unidade da fila como um 'beat': um beat pode conter mais de uma animação concorrente (par causa-efeito intrínseco), tocadas juntas; a ordenação/await acontece ENTRE beats sequenciais, não dentro de um beat. MOVED e o dano subsequente são beats distintos (serializados); pulse+hurt de um ATTACKED são um único beat (concorrente).",
    consequences:
      "Preserva o feel dos pares simultâneos enquanto serializa a sequência do turno. Custo: definir o que agrupa um beat a partir dos TurnEvents (sem alterar a ordem do domínio).",
    status: "accepted",
    requirementKeys: ["RF-131"],
    rejectedAlternatives: [
      {
        alternative: "Serializar TODOS os eventos, inclusive pulse e hurt de um mesmo ataque",
        reason: "CLR-002 vetou: quebraria o par causa-efeito simultâneo, que não é o bug.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "AnimationSequencer",
    responsibility:
      "Orquestra as animações de um turno (presentation, em entity_sprite_registry.gd): enfileira os eventos como beats ordenados, toca cada beat só após o anterior concluir (await), agrupa pares causa-efeito simultâneos em um único beat concorrente, emite all_done ao fim da sequência e expõe a fila/sequência consultável para teste.",
    dependsOn: [],
    requirementKeys: ["RF-130", "RF-131", "RF-132", "RF-133", "RNF-130"],
  },
];
