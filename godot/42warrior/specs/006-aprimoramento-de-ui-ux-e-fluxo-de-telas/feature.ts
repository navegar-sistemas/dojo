import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "006-aprimoramento-de-ui-ux-e-fluxo-de-telas",
  name: "Aprimoramento de UI UX e fluxo de telas",
  problem: `A apresentação entregue até aqui (feature 002) não alcança a referência do Ruby Warrior: o jogador vê algo visualmente pobre e distante do que se espera de um jogo, sem coesão. Pior, há um bug grave de navegação — as telas (menu, editor de código, arena, transição, resultado) renderizam SOBREPOSTAS umas às outras em vez de uma por vez, deixando a tela de jogo ilegível. Para a game jam, o que o jogador e o jurado VEEM é o produto; uma apresentação quebrada e empilhada anula o motor sofisticado por baixo. Esta feature eleva a apresentação a uma identidade visual coesa (inspirada no Ruby Warrior, com cara da 42) e conserta o fluxo de telas para uma navegação limpa, com a arena em destaque, editor de código retrátil e animações de feedback por ação.`,
  productRequirementKeys: ["PR-007", "PR-008"],
  goals: [
    "Corrigir a sobreposição de telas: um gerenciador de navegação garante UMA tela ativa por vez (menu, jogo, transição de nível, resultado, conclusão da torre), removendo/ocultando a anterior na troca — nada de telas empilhadas.",
    "Tela de jogo com layout 'arena em destaque': o corredor da masmorra ocupa o foco; HUD no topo (nível/HP/turno); console de turnos embaixo com controles (play/pause/passo/velocidade); editor de código retrátil que desliza por cima/lateral via botão '</> Código'.",
    "Identidade visual coesa inspirada no Ruby Warrior com liberdade de adaptação (não réplica): paleta, tiles de masmorra de pedra, sprites do warrior, inimigos (sludge, thick sludge, archer, wizard), cativo e escada — com cara da 42.",
    "Animações de feedback por ação/turno acionadas pelos turn_events do domínio: andar, atacar, levar dano, descansar/curar, defender/pivotar, resgatar, atirar e morrer.",
    "Assets e código organizados para troca/evolução fácil: registro central data-driven (sprites/animações/caminhos por entidade e por ação), desacoplado da lógica de cena, com pontos de troca documentados para a arte definitiva da 42.",
    "Integrar assets gráficos livres da internet (jogo não-comercial, licença irrelevante) através do registro, substituindo o que estiver pobre ou placeholder.",
  ],
  outOfScope: [
    "Áudio (SFX e trilha) — feature 005 / PR-009; explicitamente fora desta feature.",
    "Motor de turnos, API do warrior, combate, níveis e pontuação (PR-001..006) — a apresentação apenas consome estado/eventos do domínio, sem mover regra de jogo para a cena.",
    "Novas funcionalidades do editor de código (feature 003) e do painel de debug (feature 004) — aqui só a INTEGRAÇÃO visual deles na tela de jogo (editor retrátil), não novos recursos de edição/inspeção.",
    "Novos níveis ou mudança de conteúdo da beginner tower (PR-004).",
  ],
  productDecisions: [
    "Fidelidade 'inspirada, com adaptação livre' (não réplica pixel-perfect): Ruby Warrior como base + identidade da 42 (CLR-002).",
    "Layout da tela de jogo: arena em destaque, editor de código retrátil, console de turnos com controles (CLR-003).",
    "Fluxo de uma-tela-por-vez para corrigir a sobreposição reportada (CLR-004).",
    "Assets gráficos livres da internet — jogo não-comercial, licença não importa (CLR-005).",
    "Apresentação data-driven (registro de assets/animações) para troca e evolução fáceis (CLR-001).",
  ],
  phase: "implementing",
  createdAt: "2026-06-28",
};
