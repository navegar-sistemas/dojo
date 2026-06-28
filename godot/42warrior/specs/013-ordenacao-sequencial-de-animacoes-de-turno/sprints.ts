import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Ordenação sequencial de animações",
    goal: "Refatorar animate_events (entity_sprite_registry.gd) para um AnimationSequencer: fila ordenada de beats que toca cada um só após o anterior concluir, preservando pares causa-efeito simultâneos como um beat, emitindo all_done no fim e expondo a fila para teste. Realiza RF-130..133 / RNF-130 (PR-007, refina 006 RF-067; PR-011/004).",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-130", "US-131", "US-132"],
  },
];
