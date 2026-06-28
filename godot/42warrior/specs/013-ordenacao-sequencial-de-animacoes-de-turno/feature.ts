import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "013-ordenacao-sequencial-de-animacoes-de-turno",
  name: "Ordenacao sequencial de animacoes de turno",
  problem:
    "Em src/presentation/entity_sprite_registry.gd, animate_events(events) dispara TODOS os tweens do turno em PARALELO: o loop chama _animate_event que já inicia cada tween na hora e só incrementa _pending; all_done.emit() dispara quando todos terminam, sem encadeamento por ordem de evento. Consequência (bug do Usuário): num turno com [MOVED, DAMAGED] (o warrior anda e leva dano no mesmo turno), o flash de dano (_tween_hurt) roda SIMULTÂNEO ao movimento (_tween_move) — visualmente o warrior toma dano antes de chegar ao local onde o tomou. Mesmo padrão para MOVED seguido de ATTACKED. A causalidade fica ilegível.",
  productRequirementKeys: ["PR-007"],
  goals: [
    "As animações de um turno tocam EM ORDEM DE EVENTO, cada uma aguardando a anterior concluir: um MOVED sempre termina antes de um DAMAGED/ATTACKED subsequente (o warrior chega ao destino e só então reage).",
    "Preservar como UM beat concorrente o par causa-efeito intrínseco do mesmo instante (ex.: ATTACKED = pulse do atacante + hurt do alvo juntos); o requisito é a ordem ENTRE eventos sequenciais, não quebrar pares simultâneos.",
    "all_done só emite após a ÚLTIMA animação da sequência; a câmera (feature 011) permanece sincronizada com o fim da sequência.",
    "Tornar a orquestração testável (fila/sequência ordenada) para que um teste GUT confirme que o tween do evento N+1 só inicia após o N — ao menos no par MOVED→dano.",
  ],
  outOfScope: [
    "Alterar o motor de turnos ou a ORDEM dos TurnEvents do domínio (a ordem já vem correta do domínio; o defeito é só na orquestração visual).",
    "Alterar a API ou o conteúdo das animações.",
    "Redesenhar os controles de velocidade (feature 004) — a sequência deve respeitar a velocidade/step já existentes.",
  ],
  productDecisions: [],
  phase: "implementing",
  createdAt: "2026-06-28",
};
