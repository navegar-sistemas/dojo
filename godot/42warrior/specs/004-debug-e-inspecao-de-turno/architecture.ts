import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-001",
    title: "Debug consome TurnEvents (read-only), sem tocar o domínio",
    context:
      "O jogador precisa inspecionar o que sua lógica fez por turno, mas a inspeção não pode alterar a regra nem o resultado determinístico (RNF-040; ADR-002 do projeto).",
    decision:
      "A camada de debug assina os TurnEvents emitidos pelo domínio e o estado exposto pela Application, apenas para leitura; nada do debug retroalimenta o TurnResolver.",
    consequences:
      "Inspeção fiel e sem efeito colateral; o motor permanece determinístico. Custo: garantir que os TurnEvents carreguem informação suficiente para descrever cada turno.",
    status: "accepted",
    requirementKeys: ["RF-040", "RF-041", "RNF-040"],
  },
  {
    key: "ADR-002",
    title: "Controles de ritmo na apresentação, sobre o loop de turno, sem mudar resultado",
    context:
      "Depurar exige play/pause/passo-a-passo/velocidade (RF-042), mas pausar ou avançar não pode alterar o resultado da simulação (RNF-041).",
    decision:
      "Um ExecutionControls governa QUANDO o loop de turno avança/é exibido (timer controlável, passo manual), separado da resolução do turno em si, que continua pura.",
    consequences:
      "O jogador controla o tempo de apresentação sem afetar o resultado; passo-a-passo isola transições. Custo: desacoplar o tick de apresentação do cálculo do turno.",
    status: "accepted",
    requirementKeys: ["RF-042", "RF-044", "RNF-041"],
  },
  {
    key: "ADR-003",
    title: "Formatação evento→texto isolada num formatter",
    context:
      "As entradas do console (RF-040, RF-043, RF-045) traduzem TurnEvents em linguagem legível; essa tradução não deve se espalhar pela UI.",
    decision:
      "Um TurnEventFormatter converte cada TurnEvent (incl. erros e sentidos quando disponíveis) numa entrada textual; o TurnConsole apenas exibe.",
    consequences:
      "Tradução centralizada e testável; mudar a redação não mexe na UI. Custo: manter o formatter em dia com novos tipos de evento.",
    status: "accepted",
    requirementKeys: ["RF-040", "RF-043", "RF-045"],
  },
];

export const components: IComponent[] = [
  {
    name: "TurnConsole",
    responsibility:
      "Lista cronológica de entradas por turno (sentido/ação/efeitos/erro), destacando o turno corrente; apenas exibe o que o formatter produz.",
    dependsOn: ["TurnEventFormatter", "ExecutionControls"],
    requirementKeys: ["RF-040", "RF-043", "RF-044", "RF-045"],
  },
  {
    name: "WarriorStatePanel",
    responsibility:
      "Mostra o estado corrente do warrior (HP, posição, direção) e do nível (turno, inimigos restantes), atualizado a cada turno exibido.",
    dependsOn: ["ExecutionControls"],
    requirementKeys: ["RF-041"],
  },
  {
    name: "ExecutionControls",
    responsibility:
      "Governa o ritmo de apresentação do loop de turno (LevelRunner, feature 001): play, pause, passo-a-passo e velocidade; emite qual turno está sendo exibido.",
    dependsOn: [],
    requirementKeys: ["RF-042", "RF-044", "RNF-041"],
  },
  {
    name: "TurnEventFormatter",
    responsibility:
      "Converte cada TurnEvent do domínio (incl. erro do código do jogador e sentidos, quando disponíveis) numa entrada textual legível para o console.",
    dependsOn: [],
    requirementKeys: ["RF-040", "RF-043", "RF-045"],
  },
];
