import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-026",
    title: "Controller dedicado de câmera trilhando o warrior por frame (follow + dead-zone + lookahead com histerese)",
    context:
      "Hoje (dungeon_view.gd) a câmera só reposiciona em _on_animations_done (snap pós-animação), sem dead-zone nem lookahead — gerando solavanco. O acompanhamento estilo SMW exige seguir o sprite a cada frame durante o deslize entre tiles (RF-110), com dead-zone (RF-111), lookahead com histerese (RF-112) e clamp de bordas (RF-113).",
    decision:
      "Introduzir um CameraFollowController (camada presentation) que, a cada frame (_process/_physics_process), lê a posição corrente do sprite do warrior e atualiza a Camera2D aplicando: faixa de dead-zone central (só rola ao tocar a borda), deslocamento de lookahead na direção do movimento com histerese ao inverter, e clamp aos limites do nível. Remove o reposicionamento por snap no fim da animação; o alvo da câmera passa a ser o sprite em movimento, com suavização (smoothing) configurável.",
    consequences:
      "Câmera fluida sem parar-e-pular; game feel coerente com SMW. all_done deixa de ser o gatilho de reposição (a câmera já está sincronizada com o sprite). Custo: lógica de câmera por frame e parâmetros de tuning (RNF-110). Testabilidade: o controller deve expor estado consultável (alvo/offset corrente) para teste.",
    status: "accepted",
    requirementKeys: ["RF-110", "RF-111", "RF-112", "RF-113", "RNF-110"],
    rejectedAlternatives: [
      {
        alternative: "Manter o snap pós-animação, só reduzindo o tempo de smoothing",
        reason: "Não resolve o atraso estrutural (câmera parada durante o passo) nem entrega dead-zone/lookahead; é o comportamento reclamado.",
      },
    ],
  },
  {
    key: "ADR-027",
    title: "Zoom 1:1 constante + modo estático-clamped para nível que cabe no viewport",
    context:
      "_fit_camera dá zoom para enquadrar níveis pequenos (scale-to-fit) e cola no warrior nos grandes — inconsistente (CLR-001/CLR-002). SMW usa escala de tile constante (RF-114); e um nível que cabe inteiro na tela não tem o que rolar (RF-115).",
    decision:
      "Fixar zoom 1:1 constante em todos os níveis (sem scale-to-fit). O CameraFollowController detecta se o nível é mais largo que o viewport: se NÃO, entra em modo ESTÁTICO — câmera centrada no corredor e clamped aos limites, sem follow/dead-zone/lookahead; se SIM, ativa o acompanhamento dinâmico do ADR-026.",
    consequences:
      "Escala de tile uniforme entre níveis; níveis curtos exibidos inteiros sem snap; dinâmica de câmera só onde há rolagem. Custo: cálculo de bounds do nível vs viewport para escolher o modo.",
    status: "accepted",
    requirementKeys: ["RF-114", "RF-115"],
    rejectedAlternatives: [
      {
        alternative: "Zoom adaptativo por nível (scale-to-fit) mantido para níveis pequenos",
        reason: "CLR-001 vetou: viola a escala constante do SMW e era parte da inconsistência reclamada.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "CameraFollowController",
    responsibility:
      "Dirige a Camera2D da tela de jogo: trilha o sprite do warrior por frame com dead-zone, lookahead com histerese e clamp de bordas (modo dinâmico quando o nível excede o viewport); aplica zoom 1:1 constante e modo estático-centrado-clamped quando o nível cabe na tela. Expõe estado consultável (alvo/offset) para teste.",
    dependsOn: [],
    requirementKeys: ["RF-110", "RF-111", "RF-112", "RF-113", "RF-114", "RF-115", "RNF-110"],
  },
];
