import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-120 — editor no painel principal ──────────────────────────────────────────
  {
    key: "T-120",
    storyKey: "US-120",
    summary: "Reposicionar o CodeEditorPanel para o slot principal da tela de jogo em scenes/game.tscn + game_controller.gd (onde hoje fica o DebugPanel)",
    definitionOfDone:
      "Ao entrar num nível, o editor de código ocupa o painel principal; verificação por inspeção da cena/controller e teste de fumaça confirma o editor no slot principal (RF-120).",
    status: "todo",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-121 — debug oculto + DebugBtn na barra do editor ──────────────────────────
  {
    key: "T-121",
    storyKey: "US-121",
    summary: "Fazer o DebugPanel iniciar oculto e adicionar um DebugBtn ao fim da HBox Buttons do editor (Run/Reset/Ref → + DebugBtn) que alterna a visibilidade do DebugPanel",
    definitionOfDone:
      "DebugPanel inicia com visible=false; existe um DebugBtn ao final da barra de botões do editor; clicar nele abre o DebugPanel e clicar de novo fecha; teste GUT cobre o toggle de visibilidade pelo DebugBtn (RF-121, RF-122).",
    status: "todo",
    dependsOn: ["T-120"],
    parallel: false,
    assignee: null,
  },
  // ── US-122 — alternância não-destrutiva + remover controle solto do HUD ──────────
  {
    key: "T-122",
    storyKey: "US-122",
    summary: "Garantir alternância não-destrutiva (reusar o padrão _on_toggle_editor — só visibilidade) e remover/realinhar o ToggleEditorBtn solto do HUD como controle do debug",
    definitionOfDone:
      "Alternar o debug não troca de tela, não recria a arena e preserva o texto do editor (0 recriação de cena, 0 perda de texto); o controle do debug não vive mais solto no HUD; teste GUT confirma que o código digitado e a arena permanecem após abrir/fechar o debug, e a suíte permanece verde (RF-123, RNF-120).",
    status: "todo",
    dependsOn: ["T-120", "T-121"],
    parallel: false,
    assignee: null,
  },
];
