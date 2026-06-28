import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "018-mundo-bidimensional-e-warrior-em-quatro-direcoes",
  name: "Mundo bidimensional e warrior em quatro direcoes",
  problem:
    "Hoje o 42 Warrior é fiel ao Ruby Warrior beginner: o mundo é um corredor 1×N (src/domain/world: a grade é 1×N, posições fora de [0, largura-1] são parede) e Direction (src/domain/world/direction.gd) é relativa (só forward/backward; vira 180° via pivot()). Isso impede mapas bidimensionais e movimento absoluto. O Usuário quer evoluir para um mundo 2D (grade linha×coluna, R×C) com o warrior apontando/andando nas 4 direções absolutas (cima/baixo/esquerda/direita), espelhando as torres Intermediate/Advanced do Ruby Warrior original (que já são 2D) — mantendo o beginner 1×N compatível, o turno determinístico e o domínio independente de engine.",
  productRequirementKeys: ["PR-013", "PR-001", "PR-002"],
  goals: [
    "Domínio 2D: LevelState passa de índice 1D para posição 2D (linha×coluna); grade R×C; Direction ganha as 4 direções absolutas; Space, sentidos (feel/look/direction_of/direction_of_stairs) e o cálculo de passo (step_of/position_toward) operam em 2D. Modelo UNIFICADO: 1×N = R×C com R=1 (sem caminho duplicado).",
    "API do jogador: warrior_facade/warrior_api_catalog/glossário com pivot girando nas 4 direções; retrocompatibilidade do beginner (níveis 1×N continuam funcionando, como mapas R=1).",
    "Apresentação + Níveis: TileMap 2D (linhas e colunas), câmera nos 2 eixos, animações de virar/andar nas 4 direções, reference_solutions atualizados; level_loader aceita layout 2D.",
    "Invariantes: turno determinístico (0 RNG), domínio sem dependência de engine, suíte de domínio 100% verde sem regressão das features 001–016, cobertura de teste para a movimentação 2D.",
  ],
  outOfScope: [
    "Não recriar conteúdo de níveis Intermediate/Advanced específicos do Ruby Warrior (a feature entrega a CAPACIDADE 2D + 4 direções e o suporte a layout 2D; quais níveis 2D existirão é decisão de produto posterior).",
    "Não remover nem quebrar a beginner tower (001) — ela permanece como caso 1×N (R=1).",
    "Não adicionar mecânicas novas além do mundo 2D + 4 direções (ex.: novas ações/sentidos fora do que o 2D exige).",
  ],
  productDecisions: [
    "Princípio 'Fidelidade ao Ruby Warrior beginner' AMPLIADO para 'Fidelidade ao Ruby Warrior' (beginner + Intermediate/Advanced 2D), por decisão do Usuário (project-mutate, proveniência usuario) — 2D é evolução, não ruptura.",
    "Modelo de mundo UNIFICADO (1×N = R×C com R=1) em vez de caminho dual — decisão técnica do agente-spec sob delegação do Usuário ('o mais rápido de implementar'); evita duplicar lógica de mundo/sentidos.",
  ],
  phase: "implementing",
  createdAt: "2026-06-28",
};
