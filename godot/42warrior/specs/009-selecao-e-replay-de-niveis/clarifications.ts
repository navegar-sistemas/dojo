import type { IClarification } from "../types.ts";

/**
 * Clarify da 009 registrada a partir das DECISÕES do Usuario delegadas ao agente-po
 * (chat cmqxbo4wx). confirmedBy: usuario. Reconcilia/sobrescreve o clarifications.ts
 * scaffoldado fora do canal de spec.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "UX e fluxo de navegação para seleção de nível",
    questions: [
      {
        question:
          "A tela de seleção de nível é uma tela nova no ScreenManager (feature 006) acessada a partir do menu principal, ou é uma seção/modal dentro de uma tela já existente (ex.: tela de resultado)?",
        answer:
          "TELA NOVA no ScreenManager (006), acessada pelo menu principal — é navegação de 1ª classe, não modal nem seção de outra tela.",
      },
      {
        question:
          "De onde o jogador pode acessar a seleção durante uma run — só pelo menu principal (ao sair/concluir), pelo menu de pause dentro do nível, ou por ambos?",
        answer:
          "Só pelo MENU PRINCIPAL por ora (sem pause-replay dentro do nível; pause pode ser refinamento futuro — mantém o escopo contido).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Estado salvo e código por nível ao re-entrar",
    questions: [
      {
        question:
          "Ao re-entrar num nível já vencido, o editor carrega o código salvo daquele nível específico (arquivo separado por nível, ex.: user://code_level_3.gd) ou o código atual do editor (o mesmo arquivo compartilhado que o jogador usa no fluxo normal)?",
        answer:
          "POR NÍVEL — arquivo separado (ex.: user://code_level_N.gd); re-jogar para otimizar exige preservar a solução daquele nível específico.",
      },
      {
        question:
          "Ao re-jogar um nível já vencido com pontuação pior, o score máximo é preservado (atualiza só se melhorar) ou é sempre sobrescrito pelo resultado mais recente?",
        answer:
          "MÁXIMO PRESERVADO — atualiza só se melhorar (o ponto do replay é OTIMIZAR; sobrescrever puniria a exploração).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Dados exibidos por nível na tela de seleção",
    questions: [
      {
        question:
          "Quais informações são exibidas por nível na tela de seleção: apenas nome + status (bloqueado/desbloqueado/vencido), ou também o breakdown de pontuação (time bonus, rescue bonus, ace/clear bonus) da melhor run?",
        answer:
          "Nome + status (bloqueado/desbloqueado/vencido) + MELHOR PONTUAÇÃO com breakdown (time/rescue/ace) — o breakdown é o que motiva o replay.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento (ratificação)",
    questions: [
      {
        question:
          "Resumo: a 009 é uma TELA NOVA de seleção (ScreenManager da 006) acessada pelo menu principal; ao re-entrar num nível vencido carrega o código salvo POR NÍVEL (user://code_level_N.gd), preserva o score MÁXIMO (só melhora) e lista por nível nome + status + melhor pontuação com breakdown. Confirma?",
        answer: "Sim, confirmado — decisão do Usuario delegada ao agente-po (cmqxbo4wx).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
