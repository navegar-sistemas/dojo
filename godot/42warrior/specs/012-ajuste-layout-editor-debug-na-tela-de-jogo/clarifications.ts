import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 012 (layout editor/debug na tela de jogo).
 * Fonte: 3 decisões de comportamento fixadas pelo Usuário e relayed pelo agente-po (chat
 * cmqxh6jh3, "012-layout — PODE PROSSEGUIR"). Registradas como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Painel principal: editor vs debug",
    questions: [
      {
        question: "Qual painel ocupa o espaço principal da tela de jogo — o editor de código ou o debug?",
        answer:
          "O EDITOR DE CÓDIGO ocupa o painel principal (onde hoje aparece o DebugPanel). O editor é a ação primária do jogador; o debug é auxiliar sob demanda.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Visibilidade e toggle do debug",
    questions: [
      {
        question: "O DebugPanel deve ficar sempre visível ou ser retrátil?",
        answer:
          "O DEBUG inicia OCULTO por padrão e é aberto/fechado ao clicar num botão de Debug (toggle), espelhando o padrão retrátil do editor já existente (_on_toggle_editor).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Local do botão de Debug",
    questions: [
      {
        question: "Onde fica o botão que abre/fecha o debug?",
        answer:
          "AO LADO/AO FINAL da barra de botões do próprio editor (HBox Buttons: RunBtn, ResetBtn, RefBtn → + DebugBtn), NÃO como botão solto no HUD (ToggleEditorBtn). Unifica os controles na barra do editor.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento da feature 012 (ratificação)",
    questions: [
      {
        question: "O entendimento geral do ajuste de layout está correto?",
        answer:
          "Sim. Reposicionamento: editor no painel principal; DebugPanel (estado/console/controles da 004) inicia oculto e alterna por um DebugBtn no fim da barra do editor. Abrir/fechar o debug NÃO troca de tela, NÃO recria a arena e NÃO perde o código digitado. Refina a decisão de layout da 006 (CLR-003 punha o console na faixa inferior) conforme nova orientação do Usuário. Reusa o padrão de toggle e os componentes da 004/006; não altera o conteúdo do debug nem as abas API/Glossário (007/008). PR-007 + PR-010 + PR-011.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
