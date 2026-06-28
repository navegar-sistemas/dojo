import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-028",
    title: "Editor no painel principal e DebugPanel retrátil por toggle (reuso do padrão da 006)",
    context:
      "Em scenes/game.tscn + game_controller.gd, o DebugPanel (DebugLayer/DebugPanel da 004) está sempre visível ocupando o lugar do editor, e o editor é alternado por um ToggleEditorBtn solto no HUD. A nova orientação (CLR-001/002/004) é: editor no painel principal (RF-120), debug oculto por padrão e retrátil (RF-121), sem destruir estado ao alternar (RF-123/RNF-120).",
    decision:
      "Reorganizar o layout da tela de jogo: o CodeEditorPanel passa a ocupar o slot principal; o DebugPanel inicia oculto (visible=false) e é alternado por toggle, reutilizando o mesmo mecanismo do editor retrátil da 006 (_on_toggle_editor) — só visibilidade, sem recriar nós nem trocar de tela. O texto do editor e a arena permanecem intactos ao alternar.",
    consequences:
      "Hierarquia visual corrigida (ação primária em foco; auxiliar sob demanda); alternância não-destrutiva por reuso do padrão existente. Não altera o conteúdo do debug (004) nem as abas API/Glossário (007/008). Custo: rearranjo da cena e fiação do toggle de visibilidade.",
    status: "accepted",
    requirementKeys: ["RF-120", "RF-121", "RF-123", "RNF-120"],
    rejectedAlternatives: [
      {
        alternative: "Manter o DebugPanel sempre visível e só mover o editor para cima dele",
        reason: "Não corrige a hierarquia (debug continua tomando palco) nem atende RF-121 (debug oculto sob demanda).",
      },
    ],
  },
  {
    key: "ADR-029",
    title: "DebugBtn na barra de botões do editor (não no HUD)",
    context:
      "O controle de alternância vivia solto no HUD (ToggleEditorBtn), separado da barra do editor. CLR-003 pede unificar os controles: o botão de debug deve ficar junto de Run/Reset/Ref.",
    decision:
      "Adicionar um DebugBtn ao final da HBox Buttons do CodeEditorPanel (RunBtn, ResetBtn, RefBtn → + DebugBtn); ele alterna a visibilidade do DebugPanel. O ToggleEditorBtn do HUD deixa de ser o controle do debug.",
    consequences:
      "Controles unificados na barra do editor, coerentes e descobríveis. Custo: adicionar o botão e remover/realinhar o controle antigo do HUD.",
    status: "accepted",
    requirementKeys: ["RF-122"],
    rejectedAlternatives: [
      {
        alternative: "Novo botão flutuante separado no HUD",
        reason: "CLR-003 vetou: repete o problema do controle solto e desunificado.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "GameScreenLayout",
    responsibility:
      "Arranjo da tela de jogo (presentation): coloca o CodeEditorPanel no painel principal, mantém o DebugPanel (004) oculto por padrão e retrátil por visibilidade, e hospeda o DebugBtn ao fim da barra de botões do editor para alternar o debug sem trocar de tela, recriar a arena ou perder o código.",
    dependsOn: [],
    requirementKeys: ["RF-120", "RF-121", "RF-122", "RF-123", "RNF-120"],
  },
];
