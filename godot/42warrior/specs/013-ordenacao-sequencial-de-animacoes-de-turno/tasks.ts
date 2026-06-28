import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-130 — sequência ordenada + all_done no fim ────────────────────────────────
  {
    key: "T-130",
    storyKey: "US-130",
    summary: "Refatorar animate_events (entity_sprite_registry.gd) para o AnimationSequencer: enfileirar os eventos do turno como beats ordenados e tocar cada beat só após o anterior concluir (await), emitindo all_done após o último",
    definitionOfDone:
      "Num turno com [MOVED, DAMAGED] o flash de dano só inicia após o tween de move concluir; idem [MOVED, ATTACKED]; all_done emite no fim da sequência; teste GUT cobre a ordem MOVED→dano e o disparo de all_done no fim (RF-130, RF-132).",
    status: "todo",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-131 — par causa-efeito simultâneo como um beat ────────────────────────────
  {
    key: "T-131",
    storyKey: "US-131",
    summary: "Modelar a unidade da fila como beat e agrupar o par causa-efeito intrínseco (ATTACKED = pulse do atacante + hurt do alvo) num único beat concorrente",
    definitionOfDone:
      "Um ATTACKED toca pulse e hurt juntos como um único beat (concorrentes), sem serializá-los; a serialização ocorre só ENTRE beats sequenciais; teste GUT confirma que o par simultâneo não é dividido (RF-131).",
    status: "todo",
    dependsOn: ["T-130"],
    parallel: false,
    assignee: null,
  },
  // ── US-132 — fila consultável/testável + respeita velocidade ─────────────────────
  {
    key: "T-132",
    storyKey: "US-132",
    summary: "Expor a fila/sequência de animação de forma consultável e garantir que a sequência respeita os controles de velocidade/step da 004 sem redesenhá-los",
    definitionOfDone:
      "A fila/sequência é consultável; um teste GUT confirma que o tween do evento N+1 só inicia após o N (par MOVED→dano) sem depender de timing puro; a velocidade/step da 004 é respeitada; a suíte GUT permanece 100% verde (RF-133, RNF-130).",
    status: "todo",
    dependsOn: ["T-130"],
    parallel: true,
    assignee: null,
  },
];
