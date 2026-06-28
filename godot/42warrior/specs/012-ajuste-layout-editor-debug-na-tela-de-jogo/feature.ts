import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "012-ajuste-layout-editor-debug-na-tela-de-jogo",
  name: "Ajuste layout editor debug na tela de jogo",
  problem:
    "Na tela de jogo (scenes/game.tscn + src/presentation/game_controller.gd), o DebugPanel (DebugLayer/DebugPanel: WarriorStatePanel + TurnConsole + ExecutionControls, da feature 004) está SEMPRE visível, sem toggle, e ocupa a posição onde deveria estar o editor de código. O editor (EditorLayer/CodeEditorPanel) é alternado por um ToggleEditorBtn que vive solto no HUD (HudView/ToggleEditorBtn), separado da barra de botões do próprio editor. A hierarquia visual fica invertida: o debug (auxiliar) toma o palco e o editor (ação primária do jogador) fica secundário, com controle desunificado.",
  productRequirementKeys: ["PR-007", "PR-010", "PR-011"],
  goals: [
    "O editor de código ocupa o painel principal — o lugar onde hoje aparece o debug.",
    "O debug passa a iniciar OCULTO e é aberto/fechado por um botão de Debug (toggle), espelhando o padrão retrátil do editor.",
    "O botão de abrir/fechar o debug fica ao lado/ao final da barra de botões do editor (HBox Buttons: RunBtn, ResetBtn, RefBtn → + DebugBtn), não como botão solto no HUD.",
    "Abrir/fechar o debug não troca de tela, não recria a arena e não perde o código digitado.",
  ],
  outOfScope: [
    "Alterar o conteúdo do debug (estado/console/controles já entregues pela 004).",
    "Alterar a API ou o motor de turnos.",
    "Alterar as abas API/Glossário do editor (features 007/008).",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
