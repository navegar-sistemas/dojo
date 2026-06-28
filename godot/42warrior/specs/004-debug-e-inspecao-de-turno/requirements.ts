import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Debug e inspeção de turno (PR-011) ────────────────────────────────────────
  {
    key: "RF-040",
    kind: "functional",
    description:
      "Um console de turnos exibe, em ordem cronológica, uma entrada por turno descrevendo a ação do warrior e seus efeitos a partir dos TurnEvents: andou para uma direção; atacou um alvo causando N de dano; descansou recuperando N; levou N de dano; resgatou um cativo; turno sem ação ou com erro.",
    priority: "highest",
    rationale: "CLR-001: dá ao jogador a visão do que sua lógica fez a cada turno; hoje só há o desfecho final.",
  },
  {
    key: "RF-041",
    kind: "functional",
    description:
      "Um painel de estado mostra o estado corrente do warrior (HP atual/máximo, posição na grade, direção que está virado) e dados do nível (número do turno, inimigos restantes), atualizado a cada turno exibido.",
    priority: "highest",
    rationale: "CLR-001: o jogador precisa do estado para entender por que sua lógica decidiu cada ação.",
  },
  {
    key: "RF-042",
    kind: "functional",
    description:
      "Controles de execução permitem play (avanço automático), pause, passo-a-passo (avança exatamente um turno) e ajuste da velocidade do avanço automático.",
    priority: "highest",
    rationale: "CLR-002: depurar exige controlar o ritmo e isolar um turno por vez.",
  },
  {
    key: "RF-043",
    kind: "functional",
    description:
      "Quando o código do jogador falha em um turno (exceção ou ação inválida), a entrada do console daquele turno mostra a mensagem de erro associada, sem interromper a navegação pelos demais turnos.",
    priority: "high",
    rationale: "CLR-002: o erro fica ancorado no turno em que ocorreu, facilitando o diagnóstico.",
  },
  {
    key: "RF-044",
    kind: "functional",
    description:
      "Em modo passo-a-passo, o console e o painel de estado refletem exatamente o turno sendo exibido, permitindo ao jogador ver cada transição isolada do começo ao fim do nível.",
    priority: "high",
    rationale: "Inspeção turno a turno é o coração do debug de uma lógica de turno.",
  },
  {
    key: "RF-045",
    kind: "functional",
    description:
      "Quando os TurnEvents carregam o que o warrior sentiu naquele turno, o console pode exibir esse contexto junto à ação, ajudando o jogador a correlacionar sentido e decisão.",
    priority: "low",
    rationale: "Enriquecimento opcional do debug; depende dos eventos disponíveis sem alterar o domínio.",
  },
  // ── Não-funcionais ────────────────────────────────────────────────────────────
  {
    key: "RNF-040",
    kind: "non_functional",
    description:
      "A inspeção consome exclusivamente TurnEvents e estado expostos pela Application; não adiciona regra ao domínio nem altera o resultado determinístico do turno (ADR-002). Zero lógica de jogo na camada de debug.",
    priority: "highest",
    rationale: "Determinismo e Clean Architecture: o debug observa, nunca interfere.",
  },
  {
    key: "RNF-041",
    kind: "non_functional",
    description:
      "Os controles de execução governam apenas o ritmo de APRESENTAÇÃO: o LevelState final é idêntico entre execução contínua, pausada e passo-a-passo — 0 diferenças no estado final, verificável por teste comparando as três execuções.",
    priority: "high",
    rationale: "Separa o tempo de apresentação do resultado determinístico do motor.",
  },
];
