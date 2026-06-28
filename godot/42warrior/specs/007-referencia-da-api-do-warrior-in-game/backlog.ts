import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-073",
    asA: "jogador",
    iWant: "uma aba 'API' no painel do editor que liste as ações e sentidos disponíveis no nível atual, com assinatura e descrição curta",
    soThat: "eu descubra o que posso chamar (walk!, feel, attack!, etc.) sem sair do jogo",
    acceptanceCriteria: [
      "Dado que estou na tela de jogo, quando abro a aba 'API' no painel do editor retrátil (006), então vejo cada ação/sentido disponível com assinatura + descrição curta (RF-070).",
      "Dado dois níveis com fachadas diferentes, quando comparo a aba 'API' em cada um, então as listas diferem e correspondem ao que cada nível disponibiliza (RF-071, por-nível).",
    ],
    requirementKeys: ["RF-070", "RF-071"],
    priority: "highest",
    storyPoints: 5,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-074",
    asA: "jogador",
    iWant: "a referência de API no mesmo painel do editor, em abas, sem perder meu código nem a arena ao alterná-las",
    soThat: "eu consulte a API sem trocar de tela nem interromper minha sessão de código",
    acceptanceCriteria: [
      "Dado o painel do editor, quando alterno entre a aba 'Editor' e a aba 'API', então não troco de tela, a arena não é recriada e o texto digitado permanece intacto (RF-073).",
      "Dado a estrutura de abas, quando a feature 008 for adicionada, então o mesmo painel recebe a aba 'Glossário' sem refazer a estrutura (RF-072, extensível).",
    ],
    requirementKeys: ["RF-072", "RF-073"],
    priority: "high",
    storyPoints: 3,
    status: "todo",
    assignee: null,
  },
  {
    key: "US-075",
    asA: "mantenedor do jogo",
    iWant: "que o conteúdo da aba 'API' venha da fachada do warrior (camada Application), sem lista hardcoded nem importar src/domain",
    soThat: "estender a API signifique mudar a fachada e a aba reflita sozinha, com o domínio independente da engine",
    acceptanceCriteria: [
      "Dado o código de cena da aba 'API', quando se busca lista de API hardcoded, então o resultado é 0 ocorrências — o conteúdo vem do WarriorApiCatalog (RNF-070).",
      "Dado os scripts da aba de referência, quando inspecionados, então há 0 load/preload/new de classes de src/domain; o acesso é via a camada Application (RNF-071).",
    ],
    requirementKeys: ["RNF-070", "RNF-071"],
    priority: "high",
    storyPoints: 3,
    status: "todo",
    assignee: null,
  },
];
