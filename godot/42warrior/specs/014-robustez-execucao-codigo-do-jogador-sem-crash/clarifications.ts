import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 014 (robustez de execução do código do jogador).
 * Fonte: comportamento e escopo do pedido do Usuário relayed pelo agente-po (cmqxhmug4) e
 * orientação de condução do PO (cmqxje4ik): fixar COMPORTAMENTO/ESCOPO observável, NÃO um
 * mecanismo (GDScript não tem try/catch — o dev investiga como capturar runtime).
 * Registrados como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Não-crash para erro de sintaxe E de runtime",
    questions: [
      {
        question: "O que deve acontecer quando o código do jogador tem erro?",
        answer:
          "Nenhum código do jogador — com erro de SINTAXE ou de RUNTIME — pode crashar/travar o jogo. O jogo continua responsivo: o jogador pode editar e rodar de novo. (Compilação já é guardada; a lacuna é o runtime em play_turn.)",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Reporte legível do erro",
    questions: [
      {
        question: "Como o erro é mostrado ao jogador?",
        answer:
          "De forma legível na ErrorView já existente, tanto para falha de compilação quanto para falha de runtime durante play_turn. Idealmente com causa/linha quando a engine fornecer (a mensagem genérica atual não basta).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Abrangência dos caminhos que rodam código do jogador",
    questions: [
      {
        question: "Em quais telas/fluxos isso vale?",
        answer:
          "Em TODOS os caminhos que rodam código do jogador: a tela de jogo (game_controller), a seleção/replay (feature 009) e o sandbox (feature 010).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Mecanismo aberto + critério de aceite comportamental",
    questions: [
      {
        question: "O spec prescreve COMO capturar o erro de runtime?",
        answer:
          "NÃO. GDScript não tem try/catch/exceções; o mecanismo (capturar texto do parse error, validar interface/sandbox antes de chamar, limitar a superfície chamável ao facade, guarda de iteração contra loop infinito, estratégias seguras de call) é investigação do dev — o spec não o prescreve. O critério é COMPORTAMENTAL e verificável por GUT: alimentar o runner com (a) sintaxe inválida, (b) play_turn com erro de runtime (método inexistente/null/tipo), (c) play_turn com loop/recursão — e em TODOS o runner NÃO crasha (has_error()/no-op) e reporta mensagem legível. O dev REPRODUZ o crash relatado antes de corrigir e prova a correção.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-005",
    topic: "Resumo do entendimento da feature 014 (ratificação)",
    questions: [
      {
        question: "O entendimento geral está correto?",
        answer:
          "Sim. Endurecer a execução do código do jogador para que nenhum erro (sintaxe ou runtime, incl. loop/recursão) trave o jogo, reportando o erro legível na ErrorView (com causa/linha quando possível), em game_controller + 009 + 010. Refina PR-010 e cobre a promessa 'sem travar' da 003. NÃO muda a API/o motor de turnos, NÃO transforma GDScript em linguagem com exceções, NÃO valida semanticamente a lógica do jogador, NÃO reescreve o editor (003); mecanismo é do dev.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
