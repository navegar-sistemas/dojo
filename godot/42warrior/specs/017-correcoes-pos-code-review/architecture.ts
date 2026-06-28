import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-041",
    title: "Bug #1 (deadlock no-op): fix permanece na 013; a 017 só adiciona a prova de CENA",
    context:
      "O deadlock do turno sem animação (game_controller aguarda animations_finished, mas all_done era emitido SÍNCRONO antes do await em turnos no-op/pivot/parede/atacar-vazio) já foi corrigido na 013 (AnimationSequencer.play() difere all_done um frame quando nenhum tween foi aguardado, commit 6ccc57c), integrada na main. Há teste UNITÁRIO do mecanismo na 013 (test_all_done_nao_e_sincrono_sem_animacao). O PO exige, além do unitário, a prova de RUNTIME no nível de cena.",
    decision:
      "NÃO duplicar o fix nem o teste unitário. A 017 referencia o fix/teste da 013 para rastreabilidade e adiciona EXCLUSIVAMENTE um teste de NÍVEL DE CENA que instancia game_controller, joga um turno no-op (pivot/andar-na-parede) e assere que o loop de turnos AVANÇA ao próximo tick (não congela). Nenhuma lógica de produção nova entra pelo #1.",
    consequences:
      "Cobertura completa do #1 (mecanismo no sequencer + comportamento integrado na cena) sem retrabalho nem risco de regressão por re-edição. Custo: um teste de cena headless que dirige o game_controller. Acoplado ao fluxo all_done/animations_finished da 013.",
    status: "accepted",
    requirementKeys: ["RF-170", "RNF-170"],
    rejectedAlternatives: [
      {
        alternative: "Reabrir a 013 / reaplicar o fix dentro da 017",
        reason: "O fix já está vivo e testado na main; reaplicar duplicaria fonte e arriscaria regressão. O que falta é só a prova de cena.",
      },
    ],
  },
  {
    key: "ADR-042",
    title: "Bug #2 (cativo não pontua): _attack/_shoot respeitam is_captive() como _rescue, no domínio",
    context:
      "ActionApplier._attack e _shoot emitem ENEMY_DEFEATED (amount=max_health) e pontuam ao acertar QUALQUER entidade, sem checar is_captive() — ao contrário de _rescue, que já trata cativo. Atacar/atirar num cativo o conta como inimigo derrotado e soma pontos, ferindo integridade de combate (PR-003) e pontuação (PR-006).",
    decision:
      "Corrigir na causa raiz no domínio: _attack e _shoot passam a checar is_captive() do alvo antes de resolver dano/derrota. Acertar um cativo NÃO emite ENEMY_DEFEATED e NÃO pontua — vira não-evento ou falha de resgate, coerente com a semântica já estabelecida em _rescue. Determinismo do turno preservado (decisão pura no applier).",
    consequences:
      "Combate e pontuação íntegros: cativo nunca é contabilizado como inimigo. Custo: o ramo is_captive() em dois métodos + teste GUT que exercita o caso. Sem mudança de apresentação.",
    status: "accepted",
    requirementKeys: ["RF-171"],
    rejectedAlternatives: [
      {
        alternative: "Filtrar o evento ENEMY_DEFEATED de cativo só na apresentação/pontuação",
        reason: "Mascararia o defeito na borda; a fonte da verdade é o domínio (applier), onde _rescue já distingue cativo. Filtrar na UI deixaria o evento errado no histórico de turno.",
      },
    ],
  },
  {
    key: "ADR-043",
    title: "Bug #3 (ranged na escada não dispara): facing VÁLIDO (não-zero) quando inimigo == escada",
    context:
      "RangedBehavior calcula a direção de disparo como signi(stairs_pos - self_pos). Quando o inimigo ranged está EXATAMENTE na posição da escada, a diferença é 0 → facing 0 → não dispara nem causa dano. O nível _level_6 do beginner_tower posiciona um Archer na pos 7, que é a própria escada (7) — arqueiro inerte, nível quebrado.",
    decision:
      "Corrigir na causa raiz no domínio: RangedBehavior calcula um facing VÁLIDO (não-zero) também quando o inimigo coincide com a escada — derivando a direção da posição do warrior/da linha de tiro em vez de zerar em signi(0). Com facing válido, o ranged dispara e causa dano quando o warrior está no alcance e na linha. Determinismo preservado.",
    consequences:
      "O _level_6 deixa de ter arqueiro inerte; ranged na posição da escada passa a ameaçar como esperado. Custo: ajuste do cálculo de facing + teste GUT no _level_6 que assere o disparo. Sem impacto em apresentação.",
    status: "accepted",
    requirementKeys: ["RF-172"],
    rejectedAlternatives: [
      {
        alternative: "Mover o Archer da escada no _level_6 (esconder o sintoma no level design)",
        reason: "Trataria o sintoma num nível e deixaria o bug de facing vivo para qualquer ranged que caia na escada. A causa raiz é o cálculo de direção no behavior.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "NoOpSceneProof",
    responsibility:
      "Verificação (apresentação/integração): teste de nível de cena que instancia game_controller, executa um turno no-op (pivot/andar-na-parede) e assere que o loop de turnos avança ao próximo tick. Referencia o fix e o teste unitário do all_done diferido já vivos na 013; NÃO reimplementa lógica de produção.",
    dependsOn: [],
    requirementKeys: ["RF-170", "RNF-170"],
  },
  {
    name: "ActionApplierCaptiveGuard",
    responsibility:
      "Domínio: ActionApplier._attack/_shoot passam a checar is_captive() do alvo (como _rescue), de modo que acertar um cativo não emite ENEMY_DEFEATED nem pontua. Decisão pura, determinismo do turno preservado.",
    dependsOn: [],
    requirementKeys: ["RF-171"],
  },
  {
    name: "RangedStairsFacing",
    responsibility:
      "Domínio: RangedBehavior calcula um facing não-zero quando o inimigo coincide com a posição da escada, garantindo disparo/dano no alcance e na linha. Corrige o arqueiro inerte do _level_6 (Archer@7 == escada 7).",
    dependsOn: [],
    requirementKeys: ["RF-172"],
  },
];
