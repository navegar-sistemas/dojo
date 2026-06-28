import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "TileMap + sprites estáticos CC0",
    goal: "Substituir o render procedural (game_view.gd _draw) pelo TileMap2D de masmorra com sprites estáticos das entidades (warrior, inimigos, escada, captive) usando assets CC0. O corredor deve ser visível e fiel à referência ao rodar o jogo.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-017", "US-018", "US-022"],
  },
  {
    id: 2,
    name: "Animações de turno + HUD + câmera",
    goal: "Animar cada TurnEvent com AnimationPlayer/Tween (walk, attack, hurt, die, etc.), exibir o HUD fixo (CanvasLayer) com HP/turno/score/descrição e ajustar a Camera2D com smoothing e zoom automático.",
    state: "closed",
    startDate: "",
    endDate: "",
    storyKeys: ["US-019", "US-020", "US-021"],
  },
];
