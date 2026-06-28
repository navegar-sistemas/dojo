import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-170",
    kind: "functional",
    description:
      "Um turno SEM animação (eventos vazios: no-op/pass, pivot, andar na parede, atacar o vazio) NÃO congela o jogo: o loop de turnos avança ao próximo tick normalmente. (O mecanismo — diferir all_done um frame quando não há tween — já está na 013 integrada; RF-170 fixa o invariante, guardado por teste unitário na 017; a prova de runtime de CENA (render-rule) foi entregue como follow-up integrado: test_017_noop_render_cena.gd na main.)",
    priority: "highest",
    rationale: "Bug #1 do code review (ALTA, era release-blocker). game_controller esperava animations_finished que era emitido síncrono antes do await.",
  },
  {
    key: "RF-171",
    kind: "functional",
    description:
      "Atacar ou atirar num CATIVO não o conta como inimigo derrotado e não pontua: não emite ENEMY_DEFEATED e não soma pontos (vira não-evento ou falha de resgate). _attack/_shoot passam a respeitar is_captive() como _rescue já faz.",
    priority: "high",
    rationale: "Bug #2 do code review: integridade de combate (PR-003) e pontuação (PR-006).",
  },
  {
    key: "RF-172",
    kind: "functional",
    description:
      "Um inimigo ranged posicionado EXATAMENTE na posição da escada calcula um facing VÁLIDO (não-zero) e dispara/causa dano ao warrior quando no alcance e na linha; o nível _level_6 (Archer na pos 7 == escada 7) deixa de ter um arqueiro inerte.",
    priority: "high",
    rationale: "Bug #3 do code review: ranged_behavior facing=signi(self-stairs)=0 quando inimigo==escada zera o dano; jogabilidade do beginner_tower quebrada.",
  },
  {
    key: "RNF-170",
    kind: "non_functional",
    description:
      "Cada correção é provada por um teste que EXERCITA o caso: #1 = o teste UNITÁRIO do sequencer já existente na 013 (referenciado) MAIS um guard UNITÁRIO co-localizado na 017 (test_017_noop_cena.gd); a prova de NÍVEL DE CENA (render-rule: instanciar game.tscn / dirigir game_controller, renderizar ≥1 frame, asserir o avanço) foi ENTREGUE como follow-up integrado (test_017_noop_render_cena.gd na main). #2 e #3 = 1 teste GUT cada que exercita o caso. A suíte permanece 100% verde, com 0 regressão das features integradas.",
    priority: "highest",
    rationale: "Critério de pronto do PO (cmqxnaz83): teste que exercita cada caso, prova de runtime para o #1, sem regressão.",
  },
];
