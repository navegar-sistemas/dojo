import type { IClarification } from "../types.ts";

/**
 * Clarify da 007 registrada a partir das DECISÕES do Usuario delegadas ao agente-po
 * (Matheus: "tome essas decisões por mim" — chat cmqxbo4wx). confirmedBy: usuario.
 * Reconcilia/sobrescreve o clarifications.ts scaffoldado fora do canal de spec.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "UX e localização do painel de referência da API",
    questions: [
      {
        question:
          "O painel de referência da API aparece como aba/seção dentro do painel de editor já existente (feature 006, botão '</> Código') ou como painel separado com botão próprio no HUD?",
        answer:
          "Como ABA dentro do painel do editor retrátil da feature 006 (botão '</> Código') — NÃO um painel separado no HUD.",
      },
      {
        question:
          "O conteúdo (lista de ações/sentidos) muda por nível (mostrando só o que o nível disponibiliza) ou é fixo para toda a beginner tower?",
        answer:
          "POR NÍVEL — data-driven da fachada do warrior daquele nível, mostrando só o que o nível disponibiliza (revelação progressiva, estilo Ruby Warrior).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Relação com a feature 008 (glossário) e ordem",
    questions: [
      {
        question:
          "A feature 007 (referência de API) e a feature 008 (glossário de termos) devem ser entregues no mesmo painel com abas, ou são painéis/features completamente independentes?",
        answer: "No MESMO PAINEL com ABAS — aba 'API' (007) + aba 'Glossário' (008).",
      },
      {
        question:
          "Qual a ordem de prioridade: 007 primeiro e 008 em seguida, ou implementar ambas simultaneamente?",
        answer:
          "007 PRIMEIRO — estabelece o painel/aba; a 008 adiciona a aba de glossário depois.",
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
          "Resumo: a 007 entrega uma aba 'API' dentro do painel do editor retrátil da 006, listando as ações/sentidos do warrior POR NÍVEL (data-driven da fachada), no mesmo painel que depois receberá a aba 'Glossário' (008); a 007 vem primeiro. Confirma?",
        answer: "Sim, confirmado — decisão do Usuario delegada ao agente-po (cmqxbo4wx).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
