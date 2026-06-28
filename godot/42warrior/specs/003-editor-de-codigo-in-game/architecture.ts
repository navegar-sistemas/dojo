import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-001",
    title: "Editor como nó de UI desacoplado, falando com o motor só via PlayerScriptRunner",
    context:
      "O jogador precisa digitar e rodar GDScript dentro do jogo, mas a apresentação não pode acessar o estado do mundo nem conter regra (CONV-002/RNF-030). O motor de compilação/execução já existe (PlayerScriptRunner, feature 001).",
    decision:
      "O painel do editor é um nó de UI (CodeEdit + controles) que apenas captura o texto-fonte e o entrega ao PlayerScriptRunner; resultado e erros voltam como dados. Nenhuma referência a LevelState/unidades dentro do editor.",
    consequences:
      "Editor testável e substituível sem tocar no motor; preserva a separação de camadas. Custo: formalizar o contrato de entrada/saída (source → resultado|erro) na fronteira da Application.",
    status: "accepted",
    requirementKeys: ["RF-030", "RF-031", "RNF-030"],
  },
  {
    key: "ADR-002",
    title: "Código do jogador persistido por nível em user:// por um store dedicado",
    context:
      "O jogador não pode perder seu código entre sessões (RF-034) e o código não deve poluir o repositório (RNF-031).",
    decision:
      "Um PlayerCodeStore encapsula ler/gravar o código por nível em user://; o editor usa o store e nunca toca o sistema de arquivos diretamente.",
    consequences:
      "Persistência isolada e testável; trocar o backend de save não afeta o editor. Custo: definir a chave de save por nível e tratar ausência de save (cai no esqueleto).",
    status: "accepted",
    requirementKeys: ["RF-034", "RNF-031"],
  },
  {
    key: "ADR-003",
    title: "Erros de compilação/runtime como dado de saída, exibidos sem travar o jogo",
    context:
      "O código do jogador é entrada não confiável; um erro não pode travar o jogo (RF-035; RF-012 da feature 001).",
    decision:
      "O PlayerScriptRunner retorna um resultado que distingue sucesso de erro (compilação/runtime), com mensagem e linha quando disponível; o editor renderiza isso num ErrorView ao lado do código.",
    consequences:
      "Falhas viram feedback legível e o loop de jogo continua. Custo: padronizar o formato do erro retornado pelo runner.",
    status: "accepted",
    requirementKeys: ["RF-035"],
  },
];

export const components: IComponent[] = [
  {
    name: "CodeEditorPanel",
    responsibility:
      "Nó de UI com CodeEdit (syntax highlight, numeração) e botões Rodar/Resetar/Ver solução; orquestra o ciclo editar → rodar → ver erro.",
    dependsOn: ["PlayerCodeStore", "LevelSkeletonProvider", "ErrorView"],
    requirementKeys: ["RF-030", "RF-031", "RF-032", "RF-033"],
  },
  {
    name: "PlayerCodeStore",
    responsibility:
      "Lê e grava o código do jogador por nível em user://; entrega o esqueleto do nível quando não há save.",
    dependsOn: ["LevelSkeletonProvider"],
    requirementKeys: ["RF-034", "RNF-031"],
  },
  {
    name: "LevelSkeletonProvider",
    responsibility:
      "Fornece o esqueleto inicial por nível: assinatura play_turn(warrior) + comentário das habilidades disponíveis até aquele nível. Lê os dados de nível da feature 001 (BeginnerTower) via Application.",
    dependsOn: [],
    requirementKeys: ["RF-036"],
  },
  {
    name: "ErrorView",
    responsibility:
      "Renderiza, junto ao editor, as mensagens de erro de compilação/runtime vindas do PlayerScriptRunner (feature 001), sem travar o jogo.",
    dependsOn: [],
    requirementKeys: ["RF-035"],
  },
];
