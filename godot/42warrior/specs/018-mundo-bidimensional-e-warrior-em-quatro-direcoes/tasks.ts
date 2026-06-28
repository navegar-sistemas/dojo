import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // US-180 — LevelState 2D unificado
  {
    key: "T-180",
    storyKey: "US-180",
    summary:
      "Refatorar LevelState para coordenada 2D (linha,coluna) sobre grade R×C; 1×N = caso R=1 (modelo unificado, sem caminho 1D duplicado); posições fora de [0,R-1]×[0,C-1] = parede.",
    definitionOfDone:
      "Testes de domínio do LevelState 2D verdes: posição como (linha,coluna), nível 1×N lido como R=1 com comportamento idêntico ao corredor, e coordenada fora dos limites classificada como parede.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // US-181 — Direction 4 direções
  {
    key: "T-181",
    storyKey: "US-181",
    summary:
      "Estender Direction para as 4 direções absolutas (norte/sul/leste/oeste) com delta de passo 2D por direção; pivot() gira o facing entre as 4 (não só 180°).",
    definitionOfDone:
      "Testes de Direction verdes: delta correto por direção (ex.: cima=(-1,0), direita=(0,+1)), pivot gira entre as 4 direções, e cálculo de passo determinístico (sem RNG).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  // US-182 — Space + sentidos + passo 2D
  {
    key: "T-182",
    storyKey: "US-182",
    summary:
      "Adaptar Space e os sentidos (feel/look/direction_of/direction_of_stairs) e o cálculo de passo (step_of/position_toward) para operar em coordenadas 2D, sem efeito colateral (sentidos não consomem turno).",
    definitionOfDone:
      "Testes verdes dos sentidos 2D (feel/look inspecionam a célula na direção; direction_of/_stairs apontam o alvo 2D) e do passo por direção; asserção de que sentidos não alteram estado/turno.",
    status: "done",
    dependsOn: ["T-180", "T-181"],
    parallel: false,
    assignee: null,
  },
  // US-183 — API 4 direções + retrocompat
  {
    key: "T-183",
    storyKey: "US-183",
    summary:
      "Atualizar warrior_facade/warrior_api_catalog/glossário para expor as 4 direções e o pivot 4-direções, preservando os scripts e níveis beginner (1×N como R=1) sem alteração do código do jogador.",
    definitionOfDone:
      "Catálogo/glossário descrevem as 4 direções e o pivot; suíte dos scripts beginner 1×N permanece verde sem alteração; semântica forward/backward preservada no subcaso R=1.",
    status: "todo",
    dependsOn: ["T-182"],
    parallel: false,
    assignee: null,
  },
  // US-184 — Apresentação 2D
  {
    key: "T-184",
    storyKey: "US-184",
    summary:
      "TileMap 2D linhas×colunas (estende a TileMapArena 32px da 016 para R×C) + câmera (011) acompanhando o warrior nos 2 eixos + animações de virar/andar nas 4 direções.",
    definitionOfDone:
      "Prova de render headless da cena 2D verde: TileMap exibe R×C, câmera segue nos 2 eixos, e a animação correspondente é exibida ao virar/andar em cada uma das 4 direções.",
    status: "todo",
    dependsOn: ["T-180"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-185",
    storyKey: "US-184",
    summary:
      "level_loader aceita layout de nível 2D (grade R×C), mantendo a leitura de níveis 1×N como R=1; reference_solutions dos níveis refletem o mundo 2D.",
    definitionOfDone:
      "Testes verdes de carregamento de um layout 2D R×C e de leitura de um layout 1×N como R=1; reference_solutions 2D validados pelo runner.",
    status: "todo",
    dependsOn: ["T-180"],
    parallel: true,
    assignee: null,
  },
  // US-185 — Não-regressão + cobertura 2D
  {
    key: "T-186",
    storyKey: "US-185",
    summary:
      "Bateria de não-regressão e cobertura do 2D: ≥1 teste por direção (4), paredes nas bordas de uma grade R×C, sentidos 2D, e o caso R=1 (beginner) preservado; rodar check.sh.",
    definitionOfDone:
      "check.sh verde com a suíte de domínio 100% e features 001–016 sem regressão; cobertura 2D presente (4 direções, bordas R×C, sentidos 2D) e o corredor 1×N coberto.",
    status: "todo",
    dependsOn: ["T-182", "T-183", "T-184", "T-185"],
    parallel: false,
    assignee: null,
  },
];
