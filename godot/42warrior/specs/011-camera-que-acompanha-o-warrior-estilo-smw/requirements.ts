import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-110",
    kind: "functional",
    description:
      "A câmera acompanha o warrior continuamente DURANTE o movimento, trilhando a posição do sprite a cada frame enquanto ele desliza entre tiles, com interpolação suave — sem snap pós-animação (não esperar _on_animations_done para reposicionar).",
    priority: "highest",
    rationale: "Elimina o solavanco/atraso relatado (câmera parada que corre atrás no fim do passo). CLR-003.",
  },
  {
    key: "RF-111",
    kind: "functional",
    description:
      "Há uma dead-zone (camera window) central: enquanto o warrior se move dentro dessa faixa, a câmera NÃO rola; ela só passa a rolar quando o warrior se aproxima da borda da janela.",
    priority: "high",
    rationale: "Estabilidade visual estilo SMW; evita micro-movimentos da câmera a cada passo.",
  },
  {
    key: "RF-112",
    kind: "functional",
    description:
      "Há lookahead (forward focus) na direção em que o warrior anda/encara, deslocando a câmera à frente para mostrar mais do caminho; ao inverter de direção, a âncora atual é mantida até cruzar um limiar (histerese) antes de trocar de lado.",
    priority: "high",
    rationale: "Mostra o que vem à frente sem tremor em idas-e-vindas. CLR-003.",
  },
  {
    key: "RF-113",
    kind: "functional",
    description:
      "A câmera faz clamp nas bordas do nível (Camera2D limits): nunca rola além das extremidades do corredor, em nenhum eixo.",
    priority: "high",
    rationale: "Impede mostrar vazio fora do nível.",
  },
  {
    key: "RF-114",
    kind: "functional",
    description:
      "O zoom é constante 1:1 em todos os níveis — nunca scale-to-fit: a escala de tile é a mesma independentemente do tamanho do nível.",
    priority: "highest",
    rationale: "CLR-001: SMW nunca dá zoom; remove o zoom-pra-caber atual (parte da inconsistência reclamada).",
  },
  {
    key: "RF-115",
    kind: "functional",
    description:
      "Para um nível que cabe inteiro no viewport, a câmera fica ESTÁTICA, centrada no corredor e clamped aos limites do nível; o acompanhamento contínuo + dead-zone + lookahead engajam SOMENTE quando o nível é mais largo que o viewport.",
    priority: "high",
    rationale: "CLR-002: sem o que rolar, não há scroll; comportamento sensato e consistente.",
  },
  {
    key: "RNF-110",
    kind: "non_functional",
    description:
      "Os parâmetros de câmera (largura da dead-zone, distância de lookahead, velocidade de suavização) têm defaults sensatos e são ajustáveis; o acompanhamento por frame mantém a taxa de quadros do jogo (alvo 60 FPS) sem queda perceptível.",
    priority: "medium",
    rationale: "Ajustabilidade para tuning de game feel; trilhar por frame não pode degradar performance.",
  },
];
