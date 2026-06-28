import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-090",
    asA: "jogador",
    iWant: "uma tela de seleção de níveis pelo menu principal, mostrando o status e a minha melhor pontuação com breakdown de cada nível",
    soThat: "eu escolha um nível vencido para re-jogar e veja onde posso melhorar o score",
    acceptanceCriteria: [
      "Dado o menu principal, quando abro a seleção de níveis, então vejo os níveis com status (bloqueado/desbloqueado/vencido) numa tela do ScreenManager (RF-090, RF-094).",
      "Dado um nível vencido na seleção, quando o observo, então vejo a melhor pontuação com breakdown time/rescue/ace (RF-091).",
    ],
    requirementKeys: ["RF-090", "RF-091", "RF-094"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
  {
    key: "US-091",
    asA: "jogador",
    iWant: "re-entrar num nível já vencido carregando o código que salvei naquele nível",
    soThat: "eu continue otimizando a solução específica daquele nível sem perdê-la",
    acceptanceCriteria: [
      "Dado um nível vencido, quando re-entro nele pela seleção, então o editor carrega o código salvo daquele nível (user://code_level_N.gd), não o código compartilhado (RF-092).",
    ],
    requirementKeys: ["RF-092"],
    priority: "highest",
    storyPoints: 5,
    status: "done",
    assignee: null,
  },
  {
    key: "US-092",
    asA: "jogador",
    iWant: "que minha melhor pontuação por nível seja preservada (só melhora) e persistida localmente",
    soThat: "eu possa explorar runs piores sem perder meu recorde, entre sessões",
    acceptanceCriteria: [
      "Dado um nível com score máximo registrado, quando re-jogo com pontuação pior, então o máximo é preservado; quando re-jogo melhor, então o máximo atualiza (RF-093).",
      "Dado o código e o score por nível, quando são salvos, então a escrita é em user:// e há 0 escrita em res:// (RNF-090).",
    ],
    requirementKeys: ["RF-093", "RNF-090"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
];
