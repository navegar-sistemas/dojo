import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-092 — LevelProgressStore: código por nível + score máximo (RF-093, RNF-090) ─
  {
    key: "T-090",
    storyKey: "US-092",
    summary: "Implementar o LevelProgressStore (user://): por nível, guarda código (user://code_level_N.gd), status e melhor pontuação+breakdown; atualiza o score máximo só se a nova run melhorar",
    definitionOfDone:
      "Re-jogar com pontuação pior preserva o máximo e re-jogar melhor atualiza; toda escrita é em user:// e busca por escrita em res:// de código/score retorna 0 ocorrências (RF-093, RNF-090).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-090 — Tela de seleção (RF-090, RF-091, RF-094) ────────────────────────────
  {
    key: "T-091",
    storyKey: "US-090",
    summary: "Implementar a LevelSelectScreen como nova tela no ScreenManager (006), acessada pelo menu principal, listando níveis com status + melhor pontuação/breakdown do LevelProgressStore",
    definitionOfDone:
      "Pelo menu principal abre-se a tela de seleção (1 tela de topo via ScreenManager) listando os níveis com status e, por nível vencido, a melhor pontuação com breakdown; acesso pelo pause à seleção == 0 (RF-090, RF-091, RF-094).",
    status: "done",
    dependsOn: ["T-090"],
    parallel: false,
    assignee: null,
  },
  // ── US-091 — Re-entry com código por nível (RF-092) ──────────────────────────────
  {
    key: "T-092",
    storyKey: "US-091",
    summary: "Implementar o re-entry: selecionar um nível vencido na LevelSelectScreen carrega o código daquele nível (user://code_level_N.gd) no editor",
    definitionOfDone:
      "Re-entrar num nível N pela seleção carrega o código de user://code_level_N.gd no editor, não o código compartilhado do fluxo normal (RF-092).",
    status: "done",
    dependsOn: ["T-090", "T-091"],
    parallel: false,
    assignee: null,
  },
];
