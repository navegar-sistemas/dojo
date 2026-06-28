import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-130",
    kind: "functional",
    description:
      "As animações de um turno tocam EM ORDEM DE EVENTO, cada uma aguardando a anterior concluir: um MOVED sempre termina antes de um DAMAGED/ATTACKED subsequente (o warrior chega ao destino e só então reage).",
    priority: "highest",
    rationale: "CLR-001: corrige o bug de animate_events disparar todos os tweens em paralelo.",
  },
  {
    key: "RF-131",
    kind: "functional",
    description:
      "Um par causa-efeito intrínseco do mesmo instante (ex.: ATTACKED = pulse do atacante + hurt do alvo) é preservado como UM beat concorrente, não quebrado em dois passos.",
    priority: "high",
    rationale: "CLR-002: a ordem é ENTRE eventos sequenciais, não dentro de um par simultâneo.",
  },
  {
    key: "RF-132",
    kind: "functional",
    description:
      "O sinal all_done só emite após a ÚLTIMA animação da sequência do turno; a câmera (feature 011) permanece sincronizada com o fim da sequência.",
    priority: "high",
    rationale: "CLR-003: sincronização do fim do turno com câmera e fluxo.",
  },
  {
    key: "RF-133",
    kind: "functional",
    description:
      "A orquestração das animações é exposta como uma fila/sequência ordenada consultável, de modo que um teste possa confirmar que o tween do evento N+1 só inicia após o N concluir.",
    priority: "high",
    rationale: "CLR-003: testabilidade da ordem em vez de timing puro.",
  },
  {
    key: "RNF-130",
    kind: "non_functional",
    description:
      "A sequência respeita a velocidade/step já existentes (controles da 004) sem redesenhá-los; há ao menos 1 teste GUT que confirma a ordem do par MOVED→dano (N+1 só após N) e a suíte permanece 100% verde.",
    priority: "medium",
    rationale: "Não regredir os controles de velocidade e provar a ordem por teste, não por timing.",
  },
];
