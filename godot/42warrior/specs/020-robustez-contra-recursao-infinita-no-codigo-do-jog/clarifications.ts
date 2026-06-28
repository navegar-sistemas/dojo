import type { IClarification } from "../types.ts";

/**
 * Fix-feature derivada de um DEFEITO P0 reportado pelo Matheus e RATIFICADO pelo agente-po
 * (cmqxwb2yr), com o tech-lead reproduzindo o crash (cmqxw649g). O entendimento confirmado vem
 * do critério de aceite explícito do PO — autoridade de produto neste canal.
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Natureza do defeito e escopo da correção",
    questions: [
      {
        question:
          "O que exatamente está quebrado e o que a fix-feature precisa cobrir?",
        answer:
          "A 014 promete robustez contra código ruim do jogador, mas RECURSÃO INFINITA crasha o motor (Stack overflow/underflow). Causa: o loop-guard só cobre `while`; a premissa em player_script_runner.gd de que 'recursão aborta nativamente' é FALSA. A fix-feature deve estender a robustez à recursão via BOUND DE PROFUNDIDADE (depth-guard na entrada de cada chamada do código do jogador), fazendo recursão infinita virar no-op + erro reportado (igual ao while-infinito), sem crash.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Critério de aceite (produto) — ratificado pelo PO",
    questions: [
      {
        question: "Qual o critério de aceite comportamental?",
        answer:
          "(1) Código do jogador com RECURSÃO INFINITA → o processo SOBREVIVE, vira no-op + erro reportado ao jogador (NUNCA crash/Stack-underflow), igual ao tratamento do while-infinito da 014. (2) ADICIONAR teste de SINTAXE-INVÁLIDA (preenche o gap histórico que deixou o defeito passar verde). (3) o crash é reproduzido por teste ANTES da correção (no-op real, não mascarado por pending/skip). check.sh 100% verde, SEM pending/skip. A mecânica (depth-guard, teto seguro) é do dev; o spec não prescreve o valor do teto.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Mecanismo de spec e rastreabilidade",
    questions: [
      {
        question: "Por que uma fix-feature nova e não uma task na 014?",
        answer:
          "A 014 está phase=done com o sprint fechado e todas as tasks/US done — reabri-la para adicionar trabalho quebra a semântica de 'done' e o sprint fechado. O PO deu a escolha do mecanismo ao spec; escolho FIX-FEATURE curta (precedente 017-correcoes-pos-code-review), tracando o mesmo PR-010 da 014. Assim o fix ganha rastro (RF nomeando recursão-depth) sem corromper a 014. A premissa falsa fica documentada aqui e o RF-142 genérico da 014 é complementado, não reescrito.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Prioridade e sequenciamento",
    questions: [
      {
        question: "Qual a prioridade e a relação com o web export?",
        answer:
          "PRIORIDADE MÁXIMA (P0): supera as telas P1 da 016 e o web export. É PRÉ-REQUISITO do web export (cmqxwb2zw): o smoke web do código do jogador no WASM só vale após este fix, pois um crash no desktop crasha no web igual. Implementação da 020 vem na frente; o web export corre em paralelo só na spec/preparo.",
      },
    ],
    status: "confirmed",
    confirmedBy: "agente-po",
    confirmedAt: "2026-06-28",
  },
];
