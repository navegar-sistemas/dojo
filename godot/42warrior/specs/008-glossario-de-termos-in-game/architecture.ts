import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-022",
    title: "Aba 'Glossário' reusa a estrutura de abas do painel do editor (estabelecida pela 007)",
    context:
      "O glossário deve aparecer como ABA no MESMO painel da feature 007 (CLR-001/008), não como tooltip nem painel separado, e deve ser não-bloqueante (RF-083). A 007 (ADR-020) já introduz a estrutura de abas no painel do editor retrátil da 006, projetada para receber a aba 'Glossário'.",
    decision:
      "A 008 NÃO cria novo painel: adiciona a aba 'Glossário' à estrutura de abas (EditorPanelTabs) que a 007 estabelece. A 008 depende da 007 estar implementada primeiro (ordem confirmada no clarify). Alternar para a aba 'Glossário' não troca de tela, não recria a arena e preserva o texto do editor.",
    consequences:
      "Coesão com a 007 (mesmo painel, abas API + Glossário); RF-083 atendido sem nova estrutura. Custo/dependência: a 008 só integra depois da 007 (a estrutura de abas precisa existir).",
    status: "accepted",
    requirementKeys: ["RF-083"],
    rejectedAlternatives: [
      {
        alternative: "Painel de glossário separado, ou tooltip sobre as entidades na arena",
        reason:
          "CLR-001 (008) descartou tooltip (não cobre termos de pontuação) e painel separado; o glossário deve coabitar o painel da 007 em abas.",
      },
    ],
  },
  {
    key: "ADR-023",
    title: "Glossário data-driven do LevelState (entidades) + regras de pontuação (termos com valores do nível)",
    context:
      "O glossário é POR NÍVEL: define só as entidades presentes no nível atual (RF-080/RF-082) e os termos de pontuação com nome+definição+valores numéricos do nível quando aplicável (RF-081), sem hardcode e sem importar src/domain (RNF-072).",
    decision:
      "Um provider GlossaryCatalog resolve, do LevelState (entidades presentes) e das regras de pontuação (PR-006), o conteúdo do glossário: para cada entidade do nível, nome+descrição; para cada termo de score relevante, nome+definição+valor numérico do nível quando aplicável. A aba GlossaryTab apenas renderiza o que o catálogo entrega — adaptador puro, sem hardcode e sem instanciar classes de src/domain (acesso via Application).",
    consequences:
      "Conteúdo coerente com o nível (RF-080/081/082); 0 listas hardcoded e 0 import de domínio na apresentação (RNF-072). Custo: expor o LevelState/regras de pontuação de forma consumível pela apresentação via a camada Application.",
    status: "accepted",
    requirementKeys: ["RF-080", "RF-081", "RF-082", "RNF-072"],
    rejectedAlternatives: [
      {
        alternative: "Catálogo fixo de todas as entidades e termos da tower, igual em todos os níveis",
        reason:
          "Quebra o por-nível (RF-082): mostraria entidades/termos que o nível atual não contém, poluindo a referência do iniciante.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "GlossaryCatalog",
    responsibility:
      "Provider data-driven que resolve, do LevelState (entidades presentes) e das regras de pontuação (PR-006), o conteúdo do glossário: nome+descrição por entidade do nível e nome+definição+valor numérico por termo de score quando aplicável. Sem hardcode e sem importar src/domain (acesso via Application).",
    dependsOn: [],
    requirementKeys: ["RF-080", "RF-081", "RF-082", "RNF-072"],
  },
  {
    name: "GlossaryTab",
    responsibility:
      "Aba 'Glossário' adicionada à estrutura de abas do painel do editor (EditorPanelTabs da 007). Renderiza as entidades do nível e os termos de pontuação do GlossaryCatalog; adaptador puro de saída, não-bloqueante.",
    dependsOn: ["GlossaryCatalog"],
    requirementKeys: ["RF-080", "RF-081", "RF-083"],
  },
];
