import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-120",
    asA: "jogador",
    iWant: "que o editor de código ocupe o painel principal da tela de jogo",
    soThat: "a ação primária (escrever a lógica do warrior) fique em foco, não o debug",
    acceptanceCriteria: [
      "Dado que entro num nível, quando a tela de jogo aparece, então o editor de código ocupa o painel principal (onde antes ficava o DebugPanel) (RF-120).",
    ],
    requirementKeys: ["RF-120"],
    priority: "highest",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
  {
    key: "US-121",
    asA: "jogador",
    iWant: "que o debug fique oculto por padrão e eu o abra/feche por um botão na barra do editor",
    soThat: "eu use o debug sob demanda sem que ele tome o espaço do editor",
    acceptanceCriteria: [
      "Dado que entro num nível, quando a tela de jogo aparece, então o debug de inspeção (WarriorStatePanel + TurnConsole) inicia OCULTO, enquanto o editor e os ExecutionControls (play/pause/passo/velocidade) ficam VISÍVEIS (RF-121).",
      "Dado o debug oculto, quando clico no DebugBtn ao final da barra de botões do editor (junto de Run/Reset/Ref), então WarriorStatePanel + TurnConsole abrem COMO UNIDADE; quando clico de novo, então fecham juntos — sem ocultar o editor nem os ExecutionControls (RF-121, RF-122).",
    ],
    requirementKeys: ["RF-121", "RF-122"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
  {
    key: "US-122",
    asA: "jogador",
    iWant: "que abrir ou fechar o debug não me faça perder o código nem reinicie a cena",
    soThat: "eu alterne o debug livremente durante a resolução do nível",
    acceptanceCriteria: [
      "Dado código digitado no editor e um nível em andamento, quando alterno o debug (abrir/fechar), então não há troca de tela, a arena não é recriada e o texto do editor é preservado (RF-123).",
      "Dado a alternância do debug, quando ela ocorre, então há 0 recriação da cena da arena e 0 perda de texto, reusando o padrão de toggle existente, e a suíte GUT permanece verde (RNF-120).",
    ],
    requirementKeys: ["RF-123", "RNF-120"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
];
