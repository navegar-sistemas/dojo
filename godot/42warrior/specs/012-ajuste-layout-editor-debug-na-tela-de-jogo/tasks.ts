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
    summary: "Estruturar o debug de inspeção (WarriorStatePanel + TurnConsole) como unidade ocultável SEPARADA do editor (não aninhar o editor dentro dela), com os ExecutionControls SEMPRE visíveis fora dela, e adicionar um DebugBtn ao fim da HBox Buttons do editor (Run/Reset/Ref → + DebugBtn) que alterna essa unidade",
    definitionOfDone:
      "Ao entrar no nível: WarriorStatePanel + TurnConsole iniciam com visible=false; o editor e os ExecutionControls iniciam VISÍVEIS. Há um DebugBtn ao final da barra do editor; clicar abre WarriorStatePanel+TurnConsole como UNIDADE e clicar de novo fecha, SEM ocultar o editor nem os controles. Teste GUT/smoke-test de cena confirma os estados iniciais (state+console ocultos; editor+controles visíveis) e o toggle pela DebugBtn (RF-121, RF-122).",
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
