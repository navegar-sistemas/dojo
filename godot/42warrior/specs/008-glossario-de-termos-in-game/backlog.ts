import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-076",
    asA: "jogador",
    iWant: "um glossário que defina as entidades do nível atual e os termos de pontuação com seus valores numéricos",
    soThat: "eu entenda o que as coisas significam e como o score funciona sem sair do jogo",
    acceptanceCriteria: [
      "Dado um nível, quando abro a aba 'Glossário', então vejo cada entidade presente no nível com nome + descrição curta (RF-080).",
      "Dado o mesmo glossário, quando olho os termos de pontuação, então cada um (time/rescue/ace bonus) tem nome + definição + valor numérico do nível quando aplicável (RF-081).",
      "Dado dois níveis com entidades diferentes, quando comparo o glossário, então os conjuntos diferem conforme o LevelState de cada um (RF-082).",
    ],
    requirementKeys: ["RF-080", "RF-081", "RF-082"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
  {
    key: "US-077",
    asA: "jogador",
    iWant: "o glossário como uma aba ao lado da aba 'API', no mesmo painel do editor",
    soThat: "eu consulte os termos sem trocar de tela nem perder meu código ou a arena",
    acceptanceCriteria: [
      "Dado o painel do editor com abas (007), quando a 008 é entregue, então há a aba 'Glossário' ao lado da aba 'API', sem nova estrutura, e alternar para ela preserva arena e texto (RF-083).",
    ],
    requirementKeys: ["RF-083"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
  {
    key: "US-078",
    asA: "mantenedor do jogo",
    iWant: "o conteúdo do glossário resolvido do LevelState e das regras de pontuação, sem hardcode e sem importar src/domain",
    soThat: "o glossário acompanhe o nível automaticamente e o domínio permaneça independente da engine",
    acceptanceCriteria: [
      "Dado os scripts de cena da aba 'Glossário', quando se busca lista de entidades/score hardcoded, então o resultado é 0 ocorrências — o conteúdo vem do GlossaryCatalog (RNF-072).",
      "Dado os scripts da aba, quando inspecionados, então há 0 load/preload/new de classes de src/domain; o acesso é via a camada Application (RNF-072).",
    ],
    requirementKeys: ["RNF-072"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
];
