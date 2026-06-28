import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-110 — acompanhamento contínuo + dead-zone + lookahead ──────────────────────
  {
    key: "T-110",
    storyKey: "US-110",
    summary: "Criar o CameraFollowController (presentation) que trilha o sprite do warrior a cada frame com suavização, substituindo o reposicionamento por snap em _on_animations_done (dungeon_view.gd)",
    definitionOfDone:
      "Numa caminhada de vários tiles a câmera segue o sprite a cada frame (alvo = posição corrente do sprite, não só no fim da animação); o controller expõe o alvo/posição corrente para teste; teste GUT confirma que o alvo acompanha o sprite durante o movimento (RF-110).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-111",
    storyKey: "US-110",
    summary: "Implementar dead-zone (camera window) central e lookahead com histerese na direção do movimento",
    definitionOfDone:
      "Dentro da faixa central a câmera não rola; ao aproximar-se da borda da janela passa a rolar; há deslocamento de lookahead na direção do movimento; ao inverter a direção a âncora é mantida até cruzar um limiar antes de trocar de lado; teste GUT cobre a dead-zone e a histerese de inversão (RF-111, RF-112).",
    status: "done",
    dependsOn: ["T-110"],
    parallel: false,
    assignee: null,
  },
  // ── US-111 — clamp de bordas + zoom 1:1 constante ────────────────────────────────
  {
    key: "T-112",
    storyKey: "US-111",
    summary: "Aplicar clamp aos limites do nível (Camera2D limits) e fixar zoom 1:1 constante, removendo o scale-to-fit de _fit_camera",
    definitionOfDone:
      "A câmera nunca ultrapassa as bordas do nível em nenhum eixo (clamp); o zoom é 1:1 em todos os níveis (mesma escala de tile), sem scale-to-fit; teste GUT confirma o clamp nas extremidades e a escala constante (RF-113, RF-114).",
    status: "done",
    dependsOn: ["T-110"],
    parallel: true,
    assignee: null,
  },
  // ── US-112 — modo estático para nível-cabe-na-tela + parâmetros/perf ──────────────
  {
    key: "T-113",
    storyKey: "US-112",
    summary: "Implementar o modo estático-centrado-clamped para nível que cabe no viewport e expor os parâmetros de câmera (dead-zone, lookahead, suavização) com defaults sensatos",
    definitionOfDone:
      "Nível que cabe no viewport => câmera estática, centrada e clamped, sem ativar follow/dead-zone/lookahead; nível mais largo => modo dinâmico (T-110/T-111); parâmetros expostos com defaults ajustáveis; suíte GUT verde e acompanhamento por frame mantém o alvo de 60 FPS sem queda perceptível (RF-115, RNF-110).",
    status: "done",
    dependsOn: ["T-110", "T-112"],
    parallel: false,
    assignee: null,
  },
];
