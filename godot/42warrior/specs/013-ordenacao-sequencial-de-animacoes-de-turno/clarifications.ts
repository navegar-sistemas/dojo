import type { IClarification } from "../types.ts";

/**
 * Esclarecimentos da fase clarify da feature 013 (ordenação sequencial de animações de turno).
 * Fonte: comportamento especificado pelo Usuário no pedido relayed pelo agente-po (chat
 * cmqxh8ptq) e shell aprovado pelo PO (cmqxhhb40). Registrados como confirmedBy "usuario".
 */
export const clarifications: IClarification[] = [
  {
    key: "CLR-001",
    topic: "Ordem das animações dentro de um turno",
    questions: [
      {
        question: "As animações de um turno devem tocar em paralelo ou em ordem de evento?",
        answer:
          "EM ORDEM DE EVENTO, cada uma aguardando a anterior concluir: um MOVED sempre termina antes de um DAMAGED/ATTACKED subsequente (o warrior chega ao destino e SÓ ENTÃO reage). Hoje animate_events dispara todos os tweens em paralelo — esse é o bug.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-002",
    topic: "Pares causa-efeito do mesmo instante",
    questions: [
      {
        question: "Um par causa-efeito intrínseco do mesmo instante deve ser quebrado em dois passos?",
        answer:
          "NÃO. Um par causa-efeito do MESMO instante (ex.: ATTACKED = pulse do atacante + hurt do alvo juntos) pode permanecer como UM beat concorrente — isso não é o bug. O requisito é a ORDEM ENTRE eventos sequenciais do turno (mover antes de sofrer/causar dano no destino), não quebrar pares simultâneos.",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-003",
    topic: "Sincronização do fim da sequência e testabilidade",
    questions: [
      {
        question: "Quando all_done emite e como provar a ordem em teste?",
        answer:
          "all_done só emite após a ÚLTIMA animação da sequência; a câmera (feature 011) continua sincronizada com o fim da sequência. A orquestração deve ser testável (fila/sequência ordenada) de modo que um teste GUT confirme que o tween do evento N+1 só inicia após o N — ao menos no par MOVED→dano — em vez de depender de timing puro. A sequência respeita a velocidade/step já existentes (004).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
  {
    key: "CLR-004",
    topic: "Resumo do entendimento da feature 013 (ratificação)",
    questions: [
      {
        question: "O entendimento geral está correto?",
        answer:
          "Sim. Em entity_sprite_registry.gd, animate_events passa a tocar as animações do turno EM ORDEM DE EVENTO com encadeamento (cada evento aguarda o anterior), preservando pares simultâneos como um beat; all_done emite no fim da sequência (câmera 011 sincronizada); orquestração exposta como fila ordenada testável. NÃO altera o motor de turnos nem a ORDEM dos TurnEvents do domínio (já corretos), nem a API, nem o conteúdo das animações, nem os controles de velocidade (004). PR-007 (refina a 006 RF-067) + inspeção de turno (PR-011/004).",
      },
    ],
    status: "confirmed",
    confirmedBy: "usuario",
    confirmedAt: "2026-06-28",
  },
];
