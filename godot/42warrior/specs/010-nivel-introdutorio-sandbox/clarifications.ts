import type { IClarification } from "../types.ts";

/**
 * Clarify da 010 registrada a partir das DECISÕES do Usuario delegadas ao agente-po
 * (chat cmqxcjw36). confirmedBy: usuario. Reconcilia/sobrescreve o clarifications.ts
 * scaffoldado fora do canal de spec. Prioridade: 010 implementa por último (após 007→008→009).
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Conteúdo e objetivo do nível sandbox",
    questions: [
      {
        question:
          "O nível sandbox tem exatamente: corredor reto com escada no final E 1 inimigo fraco opcional, ou o layout/conteúdo ainda está em aberto (ex.: só escada sem inimigo, ou inimigo obrigatório)?",
        answer:
          "Conteúdo DEFINIDO: corredor CURTO + escada + 1 inimigo fraco OPCIONAL (sludge) para demonstrar attack!. Objetivo trivial: andar até a escada (e, havendo o sludge, um ataque). Reusa entidades existentes.",
      },
      {
        question:
          "O texto de orientação exibido na tela é fixo e genérico (ex.: 'use walk!, feel e attack! para passar o nível') ou adapta com base nos objetos presentes no nível (ex.: menciona o inimigo só se houver um)?",
        answer:
          "FIXO/genérico e curto (1-2 linhas). NÃO adaptativo — mantém o escopo contido.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Fluxo de acesso e progressão",
    questions: [
      {
        question:
          "O sandbox é acessado automaticamente na primeira vez que o jogador inicia o jogo (antes de entrar no nível 1), ou está disponível como opção no menu/seleção de níveis para acessar a qualquer momento?",
        answer:
          "SEMPRE DISPONÍVEL no menu/seleção (não força automaticamente na 1ª run; respeita quem já sabe; integra à seleção da feature 009).",
      },
      {
        question:
          "Ao concluir o sandbox, o jogador vai direto para o nível 1 (sem tela de resultado/pontuação), ou há uma tela de transição/resultado mesmo sem pontuação valer para a torre?",
        answer:
          "Vai DIRETO ao nível 1 — SEM tela de transição/resultado extra; o sandbox NÃO pontua na torre.",
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
          "Resumo: nível introdutório sandbox = corredor curto + escada + 1 sludge opcional (demo de attack!); texto de orientação fixo e curto; sempre disponível no menu/seleção; ao concluir vai direto ao nível 1, sem pontuar na torre. Confirma?",
        answer: "Sim, confirmado — decisão do Usuario delegada ao agente-po (cmqxcjw36).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
