import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-180",
    kind: "functional",
    description:
      "O estado de nível (LevelState) representa a posição por coordenada 2D (linha×coluna) em vez de índice 1D, sobre uma grade R×C (R linhas, C colunas). O corredor 1×N do beginner é o caso especial R=1 (modelo UNIFICADO, sem caminho duplicado): níveis 1×N continuam válidos como mapas de 1 linha. Posições fora de [0,R-1]×[0,C-1] são parede.",
    priority: "highest",
    rationale: "CLR-001/003: mundo bidimensional unificado; 1×N = R=1 garante retrocompat por construção.",
  },
  {
    key: "RF-181",
    kind: "functional",
    description:
      "Direction passa a representar as 4 direções absolutas (cima/norte, baixo/sul, esquerda/oeste, direita/leste). O warrior aponta para uma delas; pivot() gira o facing entre as 4 direções (não só 180°). Cada direção mapeia para um delta de passo 2D (ex.: cima = linha-1, direita = coluna+1).",
    priority: "highest",
    rationale: "CLR-001: movimento/orientação absolutos nas 4 direções, espelhando Intermediate/Advanced.",
  },
  {
    key: "RF-182",
    kind: "functional",
    description:
      "Space, os sentidos (feel/look/direction_of/direction_of_stairs) e o cálculo de passo (step_of/position_toward) operam em 2D: feel/look inspecionam a célula/linha na direção apontada em coordenadas 2D; direction_of/direction_of_stairs retornam a direção 2D rumo a um alvo; step_of/position_toward produzem a próxima posição 2D. Tudo sem efeito colateral (sentidos não consomem turno).",
    priority: "highest",
    rationale: "CLR-004: os sentidos e o passo são o núcleo do domínio que precisa enxergar 2D.",
  },
  {
    key: "RF-183",
    kind: "functional",
    description:
      "A API do jogador (warrior_facade, warrior_api_catalog, glossário) expõe a orientação/movimento nas 4 direções: pivot gira nas novas direções e as ações de andar/sentir respeitam o facing 2D. Mantém RETROCOMPATIBILIDADE do beginner: scripts e níveis 1×N existentes (resolvidos como R=1) continuam funcionando sem alteração do código do jogador.",
    priority: "high",
    rationale: "CLR-004: a evolução não pode quebrar a API/scripts do beginner já entregue (001).",
  },
  {
    key: "RF-184",
    kind: "functional",
    description:
      "A apresentação e o carregamento de níveis suportam 2D: TileMap renderiza linhas×colunas; a câmera acompanha o warrior nos 2 eixos; as animações de virar/andar cobrem as 4 direções; reference_solutions dos níveis refletem o mundo 2D; o level_loader aceita um layout de nível 2D (grade R×C), mantendo a leitura dos níveis 1×N (R=1).",
    priority: "high",
    rationale: "CLR-004: vertical completa — o jogador precisa ver e jogar o mundo 2D, e carregar mapas 2D.",
  },
  {
    key: "RNF-180",
    kind: "non_functional",
    description:
      "O turno permanece DETERMINÍSTICO (0 fontes de aleatoriedade — 0 randi/randf/seed/Time no caminho de turno) e o domínio permanece INDEPENDENTE DE ENGINE: 0 imports/referências de engine (Node/SceneTree/Godot) em src/domain, verificável por grep/arch_guard. A resolução 2D de um turno é uma transição de estado pura.",
    priority: "highest",
    rationale: "Princípios 'Turno determinístico' e domínio engine-independente: invariantes sagradas, valem no 2D.",
  },
  {
    key: "RNF-181",
    kind: "non_functional",
    description:
      "Sem regressão: a suíte de domínio permanece 100% verde e as features 001–016 não regridem (check.sh verde). A movimentação 2D tem COBERTURA DE TESTE dedicada: ≥1 teste por direção (4 direções), paredes nas bordas de uma grade R×C, sentidos 2D (feel/look/direction_of_stairs) e o caso R=1 (beginner) preservado.",
    priority: "highest",
    rationale: "Invariante do Usuário (CLR-005): 0 regressão 001–016 + cobertura real do 2D; gates verdes antes de qualquer done.",
  },
];
