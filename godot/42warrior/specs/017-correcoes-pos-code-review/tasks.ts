import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-170",
    storyKey: "US-170",
    summary:
      "Guard UNITÁRIO do all_done diferido em turno no-op (a prova de cena real foi ENTREGUE como follow-up integrado).",
    definitionOfDone:
      "Existe um teste GUT (test_017_noop_cena.gd) que assere o invariante do all_done diferido num turno sem tween (no-op), equivalente/co-localizado ao test_all_done_nao_e_sincrono_sem_animacao da 013 — é UNITÁRIO do AnimationSequencer e NÃO instancia game.tscn nem dirige game_controller. A prova de NÍVEL DE CENA real (dirige game_controller / instancia game.tscn num turno no-op, renderiza ≥1 frame e assere que o loop AVANÇA, honrando a render-rule) foi ENTREGUE como follow-up (test_017_noop_render_cena.gd, dev 42warrior, aceito pelo PO e integrado na main 677d1c4). Suíte GUT 100% verde, 0 regressão das features integradas.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-171",
    storyKey: "US-171",
    summary: "Bug #2: _attack/_shoot respeitam is_captive() (cativo não pontua) + GUT.",
    definitionOfDone:
      "ActionApplier._attack e _shoot passam a checar is_captive() do alvo (como _rescue): acertar um cativo NÃO emite ENEMY_DEFEATED e NÃO pontua. Teste GUT exercita os dois caminhos (atacar e atirar num cativo) e assere ausência de ENEMY_DEFEATED e de incremento de pontuação. Causa raiz no domínio, determinismo do turno preservado. Suíte GUT 100% verde, 0 regressão.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-172",
    storyKey: "US-172",
    summary: "Bug #3: facing válido para ranged na posição da escada (dispara) + GUT no _level_6.",
    definitionOfDone:
      "RangedBehavior calcula um facing não-zero quando o inimigo coincide com a posição da escada, garantindo disparo/dano no alcance e na linha. Teste GUT no _level_6 do beginner_tower (Archer@7 == escada 7) assere que o arqueiro deixa de ser inerte e exerce o disparo. Causa raiz no domínio, determinismo preservado. Suíte GUT 100% verde, 0 regressão.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
];
