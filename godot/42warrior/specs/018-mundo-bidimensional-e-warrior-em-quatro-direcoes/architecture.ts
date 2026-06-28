import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-180",
    title: "Modelo de mundo 2D UNIFICADO: posição linha×coluna, grade R×C, 1×N = R=1",
    context:
      "Hoje LevelState usa índice 1D num corredor 1×N (posições fora de [0,largura-1] são parede). Para o mundo 2D precisamos de coordenada linha×coluna numa grade R×C. Há duas vias: dual (manter 1D + adicionar 2D) ou unificar (1D vira subcaso do 2D).",
    decision:
      "UNIFICAR: LevelState passa a guardar a posição como coordenada 2D (linha,coluna) sobre uma grade R×C; o beginner 1×N é o caso especial R=1 (uma linha). O caminho 1D some — vira subcaso do 2D, sem código duplicado. Posições fora de [0,R-1]×[0,C-1] são parede. A transição de turno continua pura/determinística.",
    consequences:
      "Retrocompatibilidade do beginner por construção (níveis 1×N = mapas R=1); um só modelo de mundo/sentidos para manter e testar. Custo: refatorar LevelState e o que lê o índice 1D (Space, sentidos, passo) para 2D, com cobertura de regressão das 001–016.",
    status: "accepted",
    requirementKeys: ["RF-180", "RNF-180", "RNF-181"],
    rejectedAlternatives: [
      {
        alternative: "Caminho dual (1D do beginner intacto + 2D paralelo)",
        reason: "Duplica a lógica de mundo/sentidos e arrisca divergência entre os dois modelos; mais caro de manter e testar (decisão do Usuário/spec: unificar).",
      },
    ],
  },
  {
    key: "ADR-181",
    title: "Direction com 4 direções absolutas + delta de passo 2D; pivot gira entre elas",
    context:
      "Direction hoje é relativa (forward/backward; pivot só 180°). O 2D exige orientação/movimento absolutos nas 4 direções (cima/baixo/esquerda/direita), espelhando Intermediate/Advanced.",
    decision:
      "Direction representa as 4 direções absolutas (norte/sul/leste/oeste), cada uma com um delta de passo 2D (ex.: cima = (-1,0), direita = (0,+1)). pivot() gira o facing entre as 4 (não só 180°). Os deltas são a fonte única do cálculo de passo, mantendo o turno determinístico.",
    consequences:
      "Movimento e orientação absolutos; o passo deriva do delta da direção (sem RNG). Custo: estender Direction e ajustar pivot e quem assume só forward/backward.",
    status: "accepted",
    requirementKeys: ["RF-181"],
    rejectedAlternatives: [
      {
        alternative: "Manter Direction relativa e mapear 2D fora dela",
        reason: "Espalha a lógica de direção e quebra a clareza do facing absoluto que o 2D exige.",
      },
    ],
  },
  {
    key: "ADR-182",
    title: "Sentidos e cálculo de passo operando em 2D (Space, feel/look/direction_of/step_of)",
    context:
      "Space e os sentidos (feel/look/direction_of/direction_of_stairs) e o passo (step_of/position_toward) operam sobre índice 1D. Com o mundo 2D, precisam enxergar células 2D na direção apontada e calcular passos 2D.",
    decision:
      "Space e os sentidos passam a operar em coordenadas 2D: feel/look inspecionam a célula na direção apontada (delta 2D); direction_of/direction_of_stairs retornam a direção 2D rumo a um alvo; step_of/position_toward produzem a próxima posição 2D. Sentidos permanecem consultas sem efeito colateral (não consomem turno); só ações consomem.",
    consequences:
      "O núcleo do domínio enxerga o mundo 2D mantendo CQS (sentido = consulta, ação = comando) e determinismo. Custo: reescrever a aritmética de vizinhança/alvo em 2D, com testes por direção.",
    status: "accepted",
    requirementKeys: ["RF-182", "RNF-180"],
    rejectedAlternatives: [
      {
        alternative: "Adaptar só o passo e deixar os sentidos 1D",
        reason: "Sentidos 1D não enxergam linhas/colunas — o jogador não conseguiria perceber o mundo 2D para programar a lógica.",
      },
    ],
  },
  {
    key: "ADR-183",
    title: "API do jogador nas 4 direções com retrocompatibilidade do beginner (1×N = R=1)",
    context:
      "A API exposta ao jogador (warrior_facade, warrior_api_catalog, glossário) e o pivot precisam refletir as 4 direções, sem quebrar os scripts e níveis 1×N já entregues (001).",
    decision:
      "A fachada/catálogo/glossário expõem a orientação/movimento nas 4 direções; pivot gira nas novas direções; andar/sentir respeitam o facing 2D. RETROCOMPAT: como 1×N = R=1, os scripts e níveis beginner existentes continuam válidos sem alteração do código do jogador (o eixo extra simplesmente tem tamanho 1).",
    consequences:
      "Evolução da API sem regressão do beginner. Custo: atualizar as assinaturas/textos do catálogo e glossário e garantir que o subcaso R=1 preserva a semântica do forward/backward.",
    status: "accepted",
    requirementKeys: ["RF-183"],
    rejectedAlternatives: [
      {
        alternative: "API 2D separada (quebrando a do beginner)",
        reason: "Regrediria a 001 e exigiria reescrever os scripts do jogador — viola a retrocompat exigida.",
      },
    ],
  },
  {
    key: "ADR-184",
    title: "Apresentação e carregamento de níveis em 2D (TileMap linhas×colunas, câmera 2 eixos, level_loader 2D)",
    context:
      "A apresentação (TileMap, câmera, animações) e o level_loader assumem o corredor 1×N. O mundo 2D precisa renderizar linhas×colunas, mover a câmera nos 2 eixos, animar virar/andar nas 4 direções e carregar layouts 2D.",
    decision:
      "A apresentação renderiza o TileMap em linhas×colunas (reusa a TileMapArena 32px da 016 estendida a R×C), a câmera (011) acompanha o warrior nos 2 eixos, e as animações de virar/andar cobrem as 4 direções; reference_solutions refletem o 2D. O level_loader aceita um layout de nível 2D (grade R×C), lendo os níveis 1×N como R=1. A apresentação só LÊ estado/eventos; o domínio é intocado.",
    consequences:
      "O jogador vê e joga o mundo 2D, e mapas 2D podem ser carregados. Custo: estender TileMap/câmera/animações/level_loader a 2D, com prova de render de cena. Acoplado à arena 32px (016) e à câmera (011).",
    status: "accepted",
    requirementKeys: ["RF-184", "RNF-181"],
    rejectedAlternatives: [
      {
        alternative: "Renderizar só uma linha (manter a apresentação 1×N)",
        reason: "Não exibe o mundo 2D — o jogador não conseguiria jogar mapas R×C.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "GridWorld2D",
    responsibility:
      "Domínio: LevelState com posição 2D (linha×coluna) sobre grade R×C; 1×N = caso especial R=1 (modelo unificado). Limites e paredes em 2D; transição de turno pura/determinística. Cobertura de teste do 2D + regressão das 001–016.",
    dependsOn: [],
    requirementKeys: ["RF-180", "RNF-180", "RNF-181"],
  },
  {
    name: "Direction2D",
    responsibility:
      "Domínio: as 4 direções absolutas (norte/sul/leste/oeste) com delta de passo 2D; pivot gira entre elas. Fonte única do delta de movimento (sem RNG).",
    dependsOn: [],
    requirementKeys: ["RF-181"],
  },
  {
    name: "Space2D",
    responsibility:
      "Domínio: Space + sentidos (feel/look/direction_of/direction_of_stairs) e cálculo de passo (step_of/position_toward) em 2D; sentidos sem efeito colateral. Testes por direção.",
    dependsOn: ["GridWorld2D", "Direction2D"],
    requirementKeys: ["RF-182", "RNF-180", "RNF-181"],
  },
  {
    name: "WarriorApi2D",
    responsibility:
      "Aplicação: warrior_facade/warrior_api_catalog/glossário expõem orientação/movimento nas 4 direções (pivot 4-dir); retrocompat do beginner (scripts/níveis 1×N como R=1 funcionam sem alteração).",
    dependsOn: ["Space2D", "Direction2D"],
    requirementKeys: ["RF-183"],
  },
  {
    name: "Arena2DPresentation",
    responsibility:
      "Apresentação: TileMap em linhas×colunas (TileMapArena 32px estendida a R×C), câmera nos 2 eixos (011), animações de virar/andar nas 4 direções, reference_solutions 2D; level_loader aceita layout 2D (1×N = R=1). Só lê estado/eventos; não contém regra.",
    dependsOn: ["GridWorld2D"],
    requirementKeys: ["RF-184", "RNF-181"],
  },
];
