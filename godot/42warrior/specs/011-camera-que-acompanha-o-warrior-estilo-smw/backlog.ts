import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-110",
    asA: "jogador",
    iWant: "que a câmera acompanhe o warrior suavemente durante o movimento, com uma faixa central estável e mostrando o caminho à frente",
    soThat: "eu acompanhe a ação sem solavancos e veja para onde o warrior está indo",
    acceptanceCriteria: [
      "Dado um warrior andando vários tiles, quando ele desliza entre tiles, então a câmera trilha o sprite a cada frame com suavização, sem parar-e-pular no fim da animação (RF-110).",
      "Dado o warrior se movendo dentro da faixa central, quando ele não se aproxima da borda da janela, então a câmera não rola (dead-zone); quando se aproxima da borda, então a câmera passa a rolar (RF-111).",
      "Dado o warrior andando numa direção, quando ele avança, então a câmera desloca-se à frente (lookahead) nessa direção; quando o warrior inverte a direção, então a âncora é mantida até cruzar um limiar antes de trocar de lado (RF-112).",
    ],
    requirementKeys: ["RF-110", "RF-111", "RF-112"],
    priority: "highest",
    storyPoints: 8,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-111",
    asA: "jogador",
    iWant: "que a câmera nunca mostre além das bordas do nível e mantenha a mesma escala de tile em todos os níveis",
    soThat: "a apresentação seja consistente e eu nunca veja vazio fora do corredor",
    acceptanceCriteria: [
      "Dado um nível em qualquer ponto, quando a câmera rola até uma extremidade do corredor, então ela faz clamp e não ultrapassa os limites do nível em nenhum eixo (RF-113).",
      "Dado níveis de tamanhos diferentes, quando observo qualquer um, então o zoom é constante 1:1 (mesma escala de tile), sem scale-to-fit (RF-114).",
    ],
    requirementKeys: ["RF-113", "RF-114"],
    priority: "high",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-112",
    asA: "jogador",
    iWant: "que níveis curtos que cabem na tela sejam exibidos inteiros e estáveis, com a câmera ajustável e fluida",
    soThat: "níveis pequenos não fiquem com zoom-e-snap esquisito e o game feel seja afinável",
    acceptanceCriteria: [
      "Dado um nível que cabe inteiro no viewport, quando ele é exibido, então a câmera fica estática, centrada no corredor e clamped, sem ativar follow/dead-zone/lookahead (RF-115).",
      "Dado os parâmetros de câmera (dead-zone, lookahead, suavização), quando o jogo roda, então eles têm defaults sensatos ajustáveis e o acompanhamento por frame mantém o alvo de 60 FPS sem queda perceptível (RNF-110).",
    ],
    requirementKeys: ["RF-115", "RNF-110"],
    priority: "medium",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
];
