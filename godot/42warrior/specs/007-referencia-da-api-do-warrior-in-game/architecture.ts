import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-020",
    title: "Estrutura de abas no painel do editor retrátil (006); 'API' como 1ª aba, extensível p/ 'Glossário'",
    context:
      "A 007 deve expor a referência da API DENTRO do painel do editor retrátil da feature 006 (botão '</> Código'), não num painel separado no HUD (CLR-001), e no MESMO painel que depois receberá a aba 'Glossário' da 008 (CLR-002). O painel atual do editor (CodeEditorPanel da 006) mostra só o editor; precisa virar um contêiner de abas sem perder o comportamento não-bloqueante (RF-073) nem o texto digitado.",
    decision:
      "Introduzir uma estrutura de abas (TabContainer/Tabs do Godot) no painel do editor retrátil: a aba 'Editor' (código) e a aba 'API' (referência) coexistem no mesmo painel. A 007 estabelece a estrutura de abas e adiciona a aba 'API'; a 008 acrescenta depois a aba 'Glossário' à mesma estrutura. Alternar de aba não troca de tela, não recria a arena e preserva o texto do editor (as abas compartilham o mesmo painel já montado).",
    consequences:
      "Discoverability da API na superfície do editor (PR-002 sobre PR-010), sem nova tela; o painel fica extensível (008 só adiciona uma aba). RF-070/072/073 atendidos. Custo: refatorar o CodeEditorPanel da 006 para hospedar abas (a aba 'Editor' passa a ser uma das abas), preservando o estado.",
    status: "accepted",
    requirementKeys: ["RF-070", "RF-072", "RF-073"],
    rejectedAlternatives: [
      {
        alternative: "Painel separado de API com botão próprio no HUD",
        reason:
          "CLR-001 pediu explicitamente a referência DENTRO do painel do editor (contexto de quem está escrevendo o código), não um segundo painel competindo por espaço no HUD.",
      },
      {
        alternative: "Tooltip de API sobre os elementos da arena",
        reason:
          "Tooltip não comporta uma lista navegável de assinaturas+descrições por nível e não casa com a aba 'Glossário' da 008 (que também não é tooltip).",
      },
    ],
  },
  {
    key: "ADR-021",
    title: "Catálogo de API data-driven da fachada do warrior por nível; aba como adaptador puro de saída",
    context:
      "O conteúdo da aba 'API' é POR NÍVEL — só as ações/sentidos que o nível disponibiliza (revelação progressiva, CLR-001/RF-071) — e não pode ser uma lista hardcoded (RNF-070) nem importar src/domain (RNF-071). A fonte da verdade da API é a fachada do warrior exposta pela camada Application.",
    decision:
      "Um provider WarriorApiCatalog resolve, a partir da fachada/contrato do warrior do nível atual (camada Application), o conjunto de ações e sentidos disponíveis, com assinatura e descrição curta de cada um. A aba 'API' (ApiReferenceTab) apenas renderiza o que o catálogo entrega — é adaptador puro de saída, sem regra nem caminho hardcoded e sem instanciar classes de src/domain. Trocar/estender a API significa mudar a fachada, e a aba reflete automaticamente.",
    consequences:
      "Conteúdo por-nível coerente com a fachada (RF-071); 0 lista de API hardcoded em cena (RNF-070); 0 import de src/domain na apresentação (RNF-071). Custo: definir/expor o contrato da fachada de forma legível (assinatura+descrição) consumível pela apresentação via Application.",
    status: "accepted",
    requirementKeys: ["RF-071", "RNF-070", "RNF-071"],
    rejectedAlternatives: [
      {
        alternative: "Lista fixa de toda a API da beginner tower, mostrada igual em todos os níveis",
        reason:
          "Quebra a revelação progressiva (CLR-001/RF-071): o iniciante veria comandos que o nível ainda não habilita, confundindo em vez de guiar.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "EditorPanelTabs",
    responsibility:
      "Estrutura de abas (TabContainer) dentro do painel do editor retrátil da 006: hospeda a aba 'Editor' e a aba 'API' (e, na 008, a aba 'Glossário'). Alternar abas não troca de tela, não recria a arena e preserva o texto do editor.",
    dependsOn: [],
    requirementKeys: ["RF-072", "RF-073"],
  },
  {
    name: "ApiReferenceTab",
    responsibility:
      "Aba 'API' que lista as ações e sentidos do warrior disponíveis no nível atual, cada um com assinatura + descrição curta. Adaptador puro de saída: renderiza o que o WarriorApiCatalog entrega, sem regra de jogo.",
    dependsOn: ["EditorPanelTabs", "WarriorApiCatalog"],
    requirementKeys: ["RF-070", "RF-071"],
  },
  {
    name: "WarriorApiCatalog",
    responsibility:
      "Provider data-driven que resolve, da fachada/contrato do warrior do nível atual (camada Application), o conjunto de ações/sentidos disponíveis com assinatura e descrição. Sem lista hardcoded e sem importar classes de src/domain.",
    dependsOn: [],
    requirementKeys: ["RF-071", "RNF-070", "RNF-071"],
  },
];
