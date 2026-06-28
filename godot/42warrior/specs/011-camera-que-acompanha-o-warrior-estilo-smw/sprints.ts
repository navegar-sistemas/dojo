import type { ISprint } from "../types.ts";

export const sprints: ISprint[] = [
  {
    id: 1,
    name: "Câmera estilo SMW",
    goal: "Entregar o CameraFollowController: acompanhamento contínuo do warrior por frame com dead-zone, lookahead com histerese e clamp de bordas; zoom 1:1 constante e modo estático-clamped para nível que cabe no viewport. Realiza RF-110..115 / RNF-110 (PR-007), refinando a câmera da 006.",
    state: "active",
    startDate: "",
    endDate: "",
    storyKeys: ["US-110", "US-111", "US-112"],
  },
];
