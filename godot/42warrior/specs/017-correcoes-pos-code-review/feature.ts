import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "017-correcoes-pos-code-review",
  name: "Correcoes pos code review",
  problem:
    "Um code review (ordem direta do Matheus) das tasks concluídas que não tinham auditoria de código achou 3 BUGS REAIS, e o PO pediu governá-los como itens VERIFICÁVEIS (task+DoD com teste que exercita o caso), não correção ad-hoc. #1 (ALTA, release-blocker): turno SEM animação congela o jogo — game_controller espera animations_finished mas all_done era emitido SÍNCRONO no turno sem tween (no-op/pivot/parede/atacar-vazio) antes do await. #2 (MÉDIA): atacar/atirar num cativo emite ENEMY_DEFEATED e PONTUA (action_applier _attack/_shoot não checam is_captive, ao contrário de _rescue) — fere integridade de combate/pontuação. #3 (MÉDIA): inimigo ranged exatamente na posição da escada nunca atira (ranged_behavior facing=signi(0)=0); o _level_6 tem Archer na pos 7 == escada 7 — arqueiro inerte, nível quebrado.",
  productRequirementKeys: ["PR-007", "PR-003", "PR-006"],
  goals: [
    "#1 (deadlock no-op): o jogo NÃO congela num turno sem animação — avança ao próximo tick. O fix (difere all_done um frame quando não há tween) e seu teste UNITÁRIO já existem na 013 integrada (6ccc57c); a 017 REFERENCIA esse teste e ADICIONA a DoD que falta: um teste de NÍVEL DE CENA que joga um turno no-op (pivot/parede) via game_controller e assere o avanço (exigência de runtime do PO).",
    "#2 (cativo não pontua): atacar/atirar num cativo NÃO emite ENEMY_DEFEATED nem soma pontos (vira não-evento ou falha de resgate); _attack/_shoot passam a checar is_captive como _rescue. DoD = teste GUT que exercita o caso.",
    "#3 (ranged na escada dispara): inimigo ranged na posição da escada calcula um facing VÁLIDO (não-zero) e causa dano. DoD = teste GUT no _level_6 (Archer@7 == escada 7) que assere o disparo.",
  ],
  outOfScope: [
    "Re-implementar o que já está feito: o fix+teste-unitário do #1 já vivem na 013 (não duplicar; só referenciar + adicionar o teste de cena).",
    "Refactor amplo ou mudança de design: corrige SÓ os 3 defeitos apontados, na causa raiz, com teste.",
    "A divergência de percepção pós-ação do inimigo (turn_resolver) — tratada como decisão de design, fora deste escopo (só confirmar intenção, não alterar).",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
