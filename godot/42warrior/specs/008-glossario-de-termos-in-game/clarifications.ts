import type { IClarification } from "../types.ts";

/**
 * Clarify da 008 registrada a partir das DECISÕES do Usuario delegadas ao agente-po
 * (chat cmqxbo4wx). confirmedBy: usuario. Reconcilia/sobrescreve o clarifications.ts
 * scaffoldado fora do canal de spec.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "UX e localização do glossário",
    questions: [
      {
        question:
          "O glossário aparece como aba dentro do painel de referência da feature 007, como painel separado, ou como tooltip sobre as entidades na arena?",
        answer:
          "Como ABA no painel da feature 007 (mesmo painel da aba 'API') — NÃO tooltip; o tooltip não cobre os termos de pontuação.",
      },
      {
        question:
          "Conteúdo de pontuação: mostra só os nomes dos bônus com definição curta ('time bonus: pts pelos turnos sobrando'), ou inclui também os valores numéricos do nível atual?",
        answer:
          "Nome + definição curta + VALORES NUMÉRICOS do nível atual quando aplicável (data-driven; ajuda o jogador a otimizar o score, liga com a feature 009).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Escopo de entidades exibidas",
    questions: [
      {
        question:
          "O glossário mostra só as entidades presentes no nível atual (data-driven de LevelState) ou sempre mostra o catálogo completo da tower (todas as entidades possíveis)?",
        answer:
          "SÓ as entidades presentes no nível atual (data-driven do LevelState), coerente com o 'por nível' da feature 007.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question:
          "Resumo: a 008 é uma aba 'Glossário' no MESMO painel da 007, que define as entidades presentes NO NÍVEL ATUAL (data-driven do LevelState) e os termos de pontuação com nome + definição curta + valores numéricos do nível quando aplicável. Confirma?",
        answer: "Sim, confirmado — decisão do Usuario delegada ao agente-po (cmqxbo4wx).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
