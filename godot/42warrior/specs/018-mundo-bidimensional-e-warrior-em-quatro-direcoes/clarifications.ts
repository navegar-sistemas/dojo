import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 018 (mundo 2D + warrior em 4 direções).
 * Fonte: pedido direto do Matheus via /spec + respostas dele no AskUserQuestion (2026-06-28).
 * Registrados como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Conflito com o princípio 'Fidelidade ao Ruby Warrior beginner'",
    questions: [
      {
        question:
          "Evoluir para 2D conflita com o princípio de fidelidade ao beginner. Reconciliar como evolução acima do beginner, ou reinterpretar/alterar o princípio?",
        answer:
          "REINTERPRETAR/ALTERAR o princípio. Decisão do Usuário: o princípio foi ampliado (via project-mutate, proveniência usuario) de 'Fidelidade ao Ruby Warrior beginner' para 'Fidelidade ao Ruby Warrior' — o beginner (1×N) permanece fiel, e a evolução para mundo 2D (linha×coluna + 4 direções) espelha deliberadamente as torres Intermediate/Advanced do Ruby Warrior original (que já são 2D). 2D é evolução, não ruptura.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Rastreabilidade de produto (PR)",
    questions: [
      {
        question: "Criar novo PR para o 2D ou só refinar PRs existentes?",
        answer:
          "NOVO PR + refinar existentes. Criado PR-013 'Mundo bidimensional — torres Intermediate/Advanced (grade RxC + 4 direções)' (via project-mutate, proveniência usuario). A feature 018 rastreia PR-013 (capacidade nova) + refina PR-001 (motor de turnos/estado de nível) e PR-002 (API do warrior — sentidos/ações).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Modelo do mundo e retrocompatibilidade do beginner",
    questions: [
      {
        question: "Como manter o beginner 1×N funcionando junto do 2D — unificar (R=1) ou caminho dual?",
        answer:
          "O Usuário delegou a decisão técnica ('faça o que for mais rápido de implementar'). Decisão do agente-spec: UNIFICAR — um só modelo 2D (linha×coluna); os níveis beginner viram mapas de 1 linha (R=1), e o caminho 1D vira subcaso do 2D, sem código duplicado. Retrocompatibilidade do beginner por construção (1×N = R×C com R=1). Evita a dívida de manter dois modelos de mundo/sentidos.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Escopo da feature 018 e fatiamento",
    questions: [
      {
        question: "Esta feature cobre a vertical completa (Domínio+API+Apresentação+Níveis) ou só o núcleo?",
        answer:
          "VERTICAL COMPLETA, fatiada em sprints priorizados: P0 = Domínio 2D (LevelState/posição 2D, grade R×C, Direction com 4 direções, Space, sentidos feel/look/direction_of/direction_of_stairs, cálculo de passo step_of/position_toward) com cobertura de teste; P1 = API do jogador (warrior_facade/warrior_api_catalog/glossário, pivot nas 4 direções) + retrocompat beginner; P2 = Apresentação (TileMap 2D linha×coluna, câmera nos 2 eixos, animações de virar/andar nas 4 direções, reference_solutions) + Níveis (level_loader aceitando layout 2D).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-005",
    topic: "Resumo do entendimento (ratificação) + invariantes",
    questions: [
      {
        question: "O entendimento geral e as invariantes estão corretos?",
        answer:
          "Sim. A 018 evolui o mundo de 1×N para 2D (R×C) com warrior em 4 direções absolutas, espelhando Intermediate/Advanced; modelo unificado (1×N = R=1, retrocompat por construção); rastreia PR-013/PR-001/PR-002; vertical completa em 3 sprints (Domínio → API/retrocompat → Apresentação/Níveis). INVARIANTES OBRIGATÓRIAS: turno determinístico (0 RNG), domínio independente de engine (0 imports de engine em src/domain), suíte de domínio 100% verde SEM regressão das features 001–016, cobertura de teste para a movimentação 2D; gates verdes (bash scripts/check.sh + validate-feature) antes de declarar qualquer task done.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
