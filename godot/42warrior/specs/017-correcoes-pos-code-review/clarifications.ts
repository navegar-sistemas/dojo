import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 017 (correções pós code-review).
 * Fonte: code review pedido pelo Matheus (achados em chat cmqxmueqi), validados pelo PO
 * (cmqxmzi89) + decisão de governança do PO (cmqxnaz83: lar = 017; ancoragem; DoD = teste
 * que exercita cada caso). Registradas como confirmedBy "usuario" (delegação ao PO).
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Lar e ancoragem da governança dos 3 bugs",
    questions: [
      {
        question: "Onde governar os 3 bugs e ancorados a quais PRs?",
        answer:
          "Feature 017 governa os 3 (decisão do PO cmqxnaz83, pure-script, sem reabrir 013/001). Ancoragem: #1 (deadlock no-op) → PR-007 (apresentação/fluxo all_done); #2 (cativo pontua) → PR-003 (combate) + PR-006 (pontuação); #3 (ranged na escada) → PR-003 (entidades/comportamento).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Bug #1 (deadlock no-op) — fix já feito; falta o teste de cena",
    questions: [
      {
        question: "O #1 é re-implementação pelo dev?",
        answer:
          "NÃO. O fix (AnimationSequencer.play() difere all_done um frame quando nenhum tween foi aguardado) e seu teste UNITÁRIO (test_all_done_nao_e_sincrono_sem_animacao) JÁ existem na 013 integrada (6ccc57c, na main ede7ec7). A 017 REFERENCIA esse teste (rastreabilidade) e NÃO duplica. O que FALTA p/ fechar o #1 (exigência de runtime do PO): um teste de NÍVEL DE CENA que joga um turno no-op (pivot/andar-na-parede) via game_controller e assere que o jogo AVANÇA ao próximo tick — o unitário prova o mecanismo no sequencer; o de cena prova o comportamento integrado.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Bugs #2 e #3 — trabalho fresco do dev (domínio/core)",
    questions: [
      {
        question: "O que o dev precisa corrigir em #2 e #3 e como provar?",
        answer:
          "#2: action_applier _attack/_shoot passam a checar is_captive() (como _rescue) — atacar/atirar num cativo NÃO emite ENEMY_DEFEATED nem pontua (não-evento ou falha de resgate); teste GUT que exercita o caso. #3: ranged_behavior calcula um facing VÁLIDO (não-zero) para inimigo na posição da escada e causa dano; teste GUT no _level_6 (Archer@7 == escada 7) que assere o disparo. Ambos na causa raiz (domínio), com teste.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento da feature 017 (ratificação)",
    questions: [
      {
        question: "O entendimento e o critério de pronto estão corretos?",
        answer:
          "Sim. 017 governa os 3 bugs do code review como RF/US/T com DoD = teste que EXERCITA cada caso. Critério de pronto do PO: cadeia PR→RF→US→T íntegra (validate-feature 017 verde); 3 testes que exercitam (sequencer-unitário-já-feito na 013 + teste de cena no-op + #2 cativo + #3 ranged@escada); 0 regressão. O dev faz #2/#3 (core) e o teste de cena do #1; o fix do #1 já está na 013. Não duplica o já-feito, não faz refactor amplo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
