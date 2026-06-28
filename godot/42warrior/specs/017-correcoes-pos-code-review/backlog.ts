import type { IUserStory } from "../types.ts";

export const stories: IUserStory[] = [
  {
    key: "US-170",
    asA: "Jogador",
    iWant:
      "que um turno sem animação (pivot, andar na parede, no-op) não congele o jogo",
    soThat: "eu consiga continuar jogando após qualquer ação, inclusive as que não movem nada",
    acceptanceCriteria: [
      "Dado um jogo em execução via game_controller, quando eu submeto um turno no-op (pivot ou andar contra a parede) que não produz tween, então o loop de turnos avança ao próximo tick e o jogo não fica travado aguardando animations_finished.",
      "Dado o mecanismo do all_done diferido já corrigido e testado na 013 (test_all_done_nao_e_sincrono_sem_animacao), quando a 017 é entregue, então existe um GUARD UNITÁRIO do invariante co-localizado na 017 (sem reimplementar o fix), e a prova de NÍVEL DE CENA integrada (render-rule) foi entregue como follow-up (test_017_noop_render_cena.gd na main).",
    ],
    requirementKeys: ["RF-170", "RNF-170"],
    priority: "highest",
    storyPoints: 2,
    status: "done",
    assignee: null,
  },
  {
    key: "US-171",
    asA: "Jogador",
    iWant: "que atacar ou atirar num cativo não o conte como inimigo derrotado nem me dê pontos",
    soThat: "a pontuação e a contagem de inimigos reflitam apenas combate legítimo, não dano a quem eu deveria resgatar",
    acceptanceCriteria: [
      "Dado um cativo adjacente ao warrior, quando o warrior o ataca, então não é emitido ENEMY_DEFEATED e a pontuação não aumenta (vira não-evento ou falha de resgate).",
      "Dado um cativo na linha de tiro, quando o warrior atira nele, então não é emitido ENEMY_DEFEATED e a pontuação não aumenta, coerente com o tratamento de cativo já existente em _rescue.",
    ],
    requirementKeys: ["RF-171"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
  {
    key: "US-172",
    asA: "Jogador",
    iWant: "que um inimigo ranged posicionado na escada me ameace e dispare normalmente",
    soThat: "o nível _level_6 (com o arqueiro na posição da escada) seja jogável e desafiador como projetado",
    acceptanceCriteria: [
      "Dado um inimigo ranged posicionado exatamente na posição da escada, quando o warrior está no alcance e na linha, então o ranged calcula um facing válido (não-zero), dispara e causa dano.",
      "Dado o nível _level_6 do beginner_tower (Archer na pos 7 == escada 7), quando o warrior entra no alcance, então o arqueiro deixa de ser inerte e o disparo é exercido (provado por teste GUT).",
    ],
    requirementKeys: ["RF-172"],
    priority: "high",
    storyPoints: 3,
    status: "done",
    assignee: null,
  },
];
