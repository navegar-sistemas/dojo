import type { IClarification } from "../types.ts";

/**
 * Clarify registrada a partir das decisões que o usuario ratificou na sessão de correção de rumo
 * (2026-06-27): o editor de código in-game é a prioridade número 2, logo após a UI gráfica.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Como o jogador fornece e roda o código",
    questions: [
      {
        question:
          "O jogador escreve a lógica do warrior em GDScript real (play_turn) dentro do jogo, e não por blocos — confirmado para o projeto. A feature 003 é a interface onde ele digita, roda e corrige esse código?",
        answer:
          "Sim. Hoje o código vem embutido (reference_solutions) e o jogador não tem onde digitar; a 003 entrega o editor in-game. Mantém GDScript real (decisão de CLR-001 da feature 001).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-002",
    topic: "Forma do editor e integração com o motor",
    questions: [
      {
        question:
          "O editor é um painel de texto com destaque de sintaxe (CodeEdit), botões Rodar/Resetar/Ver solução, persistência do código por nível, e usa o PlayerScriptRunner que já compila GDScript em runtime?",
        answer:
          "Sim — CodeEdit com syntax highlight e numeração; Rodar compila e executa via PlayerScriptRunner existente; Resetar volta ao esqueleto do nível; Ver solução mostra a referência; o código do jogador persiste por nível em user://.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
  {
    key: "CLR-003",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question:
          "Resumo: feature 003 entrega o editor de código in-game (CodeEdit + Rodar/Resetar/Ver solução + persistência por nível + erros legíveis), ligado ao PlayerScriptRunner, realizando PR-010. Prioridade 2. Correto?",
        answer: "Sim, entendimento confirmado. Seguir para discovery com esse escopo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-27",
  },
];
