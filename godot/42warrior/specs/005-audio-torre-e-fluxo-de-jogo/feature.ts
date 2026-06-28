import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "005-audio-torre-e-fluxo-de-jogo",
  name: "Audio torre e fluxo de jogo",
  problem: `Falta o fluxo que liga os niveis num jogo de torre completo e o audio. Hoje nao ha menu inicial, telas de transicao entre niveis, tela de resultado, creditos nem progresso salvo, e nao ha nenhum som. Sem isso a beginner tower nao e jogavel de ponta a ponta e perde o polimento que a jam cobra. Estes itens foram confirmados no escopo (CLR-003) e sao o "resto" a fechar depois das prioridades 1-3.`,
  productRequirementKeys: ["PR-008", "PR-009"],
  goals: [
    "Menu inicial; iniciar ou continuar a torre conforme o progresso salvo em user://.",
    "Telas de transicao entre niveis (descricao + habilidades novas + narrativa), avanco automatico na vitoria e reinicio do nivel.",
    "Tela de resultado/pontuacao por nivel e creditos ao concluir a torre.",
    "SFX por evento de turno (andar, atacar, levar dano, descansar, resgatar, atirar, vitoria, derrota) e trilha de fundo, com controle de volume basico.",
    "Persistir o progresso na torre localmente (user://) entre sessoes.",
    "Usar assets de audio CC0 (licenca livre), com pontos de troca para audio tematico da 42.",
  ],
  outOfScope: [
    "Renderizacao do nivel (feature 002), editor (003) e debug (004).",
    "Mixer de audio avancado por canal alem do volume basico; dublagem/voz.",
    "Ranking online ou persistencia em servidor.",
  ],
  productDecisions: [
    "Audio completo (SFX + musica) integrado de verdade nesta entrega (ratificado em CLR-003 da feature 001).",
    "Progresso da torre persistido localmente em user://.",
    "Assets de audio CC0, trocaveis pelo audio tematico da 42.",
  ],
  phase: "done",
  createdAt: "2026-06-27",
};
