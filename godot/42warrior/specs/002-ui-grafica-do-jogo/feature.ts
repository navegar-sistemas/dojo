import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "002-ui-grafica-do-jogo",
  name: "UI grafica do jogo",
  problem: `O jogo nao tem apresentacao grafica de verdade. O render atual e procedural (game_view.gd desenha formas via _draw) — nenhum sprite, tile ou animacao — e nao se parece com a referencia do Ruby Warrior (cavaleiro de armadura, slime verde, escada dourada, masmorra de pedra). Para a game jam, o que o jogador e o jurado VEEM e o produto: sem o jogo grafico, o motor sofisticado por baixo nao aparece. Esta e a prioridade numero 1 da correcao de rumo.`,
  productRequirementKeys: ["PR-007"],
  goals: [
    "Renderizar o corredor da masmorra como TileMap de tiles de pedra (chao, paredes laterais, fundo escuro), dimensionado pelo width do nivel.",
    "Sprites distintos para warrior, sludge, thick sludge, archer, wizard, captive e escada, posicionados na grade pela posicao/direcao do estado do nivel.",
    "Animacoes de feedback por turno (andar, atacar, levar dano, descansar, resgatar, atirar, morrer) acionadas a partir dos turn_events que o dominio ja emite.",
    "HUD legivel: saude do warrior (coracao + valor), numero do turno, descricao do nivel e pontuacao.",
    "Integrar um asset pack de pixel-art CC0 (licenca livre) com pontos de troca documentados para a arte definitiva da 42.",
    "Substituir o game_view.gd procedural mantendo a Clean Architecture: a cena consome estado/eventos da Application, sem regra de jogo na camada de apresentacao.",
  ],
  outOfScope: [
    "Arte definitiva da 42 — esta entrega usa asset pack CC0 com pontos de troca; a arte final e posterior.",
    "Audio (feature 005), editor de codigo (feature 003) e painel de debug (feature 004).",
    "Efeitos cinematograficos/particulas avancadas alem do feedback de turno legivel.",
  ],
  productDecisions: [
    "Apresentacao 2D top-down em grade (ratificado em CLR-002 da feature 001).",
    "Assets de pixel-art CC0 nesta entrega, trocaveis pela arte 42 (decisao de usuario, 2026-06-27).",
    "Render procedural por _draw e explicitamente insuficiente e sera substituido (PR-007 reescrito nesta sessao).",
  ],
  phase: "done",
  createdAt: "2026-06-27",
};
