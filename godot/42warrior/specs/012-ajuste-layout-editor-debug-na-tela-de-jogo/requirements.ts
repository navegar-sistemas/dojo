import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-120",
    kind: "functional",
    description:
      "Ao entrar no nível, o editor de código (CodeEditorPanel) ocupa o painel principal da tela de jogo — a posição onde hoje aparece o DebugPanel.",
    priority: "highest",
    rationale: "CLR-001: o editor é a ação primária do jogador; corrige a hierarquia visual.",
  },
  {
    key: "RF-121",
    kind: "functional",
    description:
      "O DebugPanel (estado/console/controles da 004) inicia OCULTO por padrão e é aberto/fechado por um botão de Debug (toggle), espelhando o padrão retrátil do editor.",
    priority: "highest",
    rationale: "CLR-002: debug é auxiliar sob demanda.",
  },
  {
    key: "RF-122",
    kind: "functional",
    description:
      "O botão de abrir/fechar o debug (DebugBtn) fica ao final da barra de botões do editor (HBox Buttons, junto de Run/Reset/Ref), e NÃO como botão solto no HUD (o ToggleEditorBtn do HUD deixa de ser o controle do debug).",
    priority: "high",
    rationale: "CLR-003: unifica os controles na barra do editor.",
  },
  {
    key: "RF-123",
    kind: "functional",
    description:
      "Abrir ou fechar o debug não troca de tela (continua a mesma tela do ScreenManager), não recria a arena e não perde o código já digitado no editor.",
    priority: "high",
    rationale: "CLR-004: alternância não-destrutiva, coerente com o editor retrátil da 006.",
  },
  {
    key: "RNF-120",
    kind: "non_functional",
    description:
      "A alternância do debug preserva 100% do estado relevante — 0 recriação da cena da arena e 0 perda do texto do editor — reusando o padrão de toggle e os componentes já existentes (004/006); a suíte GUT permanece verde (0 falhas).",
    priority: "medium",
    rationale: "Garante que o reposicionamento é não-destrutivo e sem regressão.",
  },
];
