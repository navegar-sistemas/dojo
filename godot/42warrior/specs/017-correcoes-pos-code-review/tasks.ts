import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-170",
    storyKey: "US-170",
    summary:
      "Teste de NÍVEL DE CENA do turno no-op (o fix do all_done diferido já está na 013; aqui só a prova de runtime).",
    definitionOfDone:
      "Existe um teste headless que instancia game_controller, submete um turno no-op (pivot ou andar contra a parede, sem tween) e assere que o loop de turnos AVANÇA ao próximo tick (não congela aguardando animations_finished). O teste referencia, em comentário, o unitário da 013 (test_all_done_nao_e_sincrono_sem_animacao) para rastreabilidade e NÃO reimplementa o fix. Suíte GUT 100% verde, 0 regressão das features integradas.",
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
