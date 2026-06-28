import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 015 (Tema Glitch — Game Jam).
 * Fonte: decisões já tomadas pelo Matheus (usuário) no pedido DIRETO de criação desta feature
 * (autoridade: decisão direta do Matheus — requisito obrigatório da game jam, não refinamento).
 * Registradas como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Direção do tema (glitch + Ruby Warrior + identidade 42)",
    questions: [
      {
        question: "Como o tema 'glitch' deve casar com o jogo e a escola?",
        answer:
          "O tema casa Ruby Warrior + glitch + identidade 42 (terminal/Unix/hacker; paleta P&B com neon de acento; o '42'). Conceito guarda-chuva: 'Kernel corrompido da 42' — a torre é um mainframe da 42 infectado; o warrior é um processo de debug que sobe limpando a corrupção.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Glitch na mecânica, não só visual (obrigatório)",
    questions: [
      {
        question: "O glitch precisa afetar a jogabilidade ou pode ser só decorativo?",
        answer:
          "OBRIGATÓRIO aparecer na MECÂNICA, não só no visual: o P0 inclui 'erro do código do jogador → glitch determinístico no mundo' (warrior/tela/tile corrompem quando o script falha), ligando o tema ao núcleo de programar. Tema na jogabilidade pontua mais que decorativo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Determinismo do turno é sagrado",
    questions: [
      {
        question: "Glitches que afetam regra podem usar aleatoriedade?",
        answer:
          "NÃO. Determinismo é sagrado: qualquer glitch que afete REGRA é scriptado/seedado, nunca RNG injusto, e testável. Efeitos puramente visuais/áudio vivem só na apresentação; mecânicas de glitch que tocam regra entram em Domain/Application de forma determinística e coberta por teste de domínio, consumindo os turn_events existentes (sem duplicar regra na cena).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Calibração de esforço para a jam (P0 > P1/P2)",
    questions: [
      {
        question: "Como priorizar o escopo dado o tempo de jam?",
        answer:
          "Entregar o P0 COMPLETO (conceito Kernel-42 + ≥1 mecânica de glitch jogável + estética glitch escalando + corrupção da UI + mensagens de erro Unix/42) vale mais que P1/P2 incompletos. P1 (mecânica glitch por andar, sprite corrompe em dano/morte, transições datamosh, áudio bit-crush) entra se couber; P2 (glitch-through-walls, falso crash, variação narrativa 'o warrior é o glitch') fica como backlog.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-005",
    topic: "Estrutura da feature e ancoragem de PR",
    questions: [
      {
        question: "Feature guarda-chuva ou dividir? Quais PRs?",
        answer:
          "Feature guarda-chuva 'Tema Glitch (Game Jam)' com RFs por CAMADA (conceito, mecânica, estética, áudio, identidade 42) e o 1º sprint só com o P0; dividir em duas features (mecânica × apresentação) só se os gates de coesão/rastreabilidade pedirem. PR: registrado PR-012 'Tema da game jam — Glitch (identidade 42)' (cross-cutting, autorizado pelo Matheus) + ancoragem em PR-007 (apresentação/estética) e PR-001 (motor/turnos para as mecânicas de glitch). Criada na main com --no-worktree.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-006",
    topic: "Invariantes não-negociáveis e fora de escopo (ratificação)",
    questions: [
      {
        question: "Quais invariantes e limites a spec deve impor?",
        answer:
          "Invariantes: (1) determinismo do turno preservado (glitch que afeta regra é scriptado/seedado, testável); (2) domínio independente da engine (visual/áudio só na apresentação; regra de glitch em Domain/Application determinística + teste de domínio); (3) consumir turn_events existentes, sem duplicar regra na cena; (4) assets/efeitos data-driven via EntityAssetRegistry com pontos de troca; (5) respeitar CONV-001..007; nada de 001–006 regride (tema ADITIVO). Fora de escopo: reescrever mecânica core ou os 9 níveis canônicos; multiplayer/online; arte final definitiva (placeholder/gerado basta). Critério de aceite: tema perceptível em conceito + ≥1 mecânica jogável + estética + identidade 42; validate-feature verde, cadeia PR→RF→US→T íntegra, testes de domínio verdes, jogo atual sem regressão.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
