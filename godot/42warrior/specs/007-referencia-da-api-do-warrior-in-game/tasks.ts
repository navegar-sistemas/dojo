import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-074 — Painel com abas, não-bloqueante (RF-072, RF-073) ────────────────────
  {
    key: "T-080",
    storyKey: "US-074",
    summary: "Refatorar o CodeEditorPanel da 006 numa estrutura de abas (TabContainer): aba 'Editor' + aba 'API', extensível p/ 'Glossário' (008)",
    definitionOfDone:
      "O painel do editor expõe abas; alternar entre 'Editor' e 'API' não troca de tela, não recria a arena e preserva o texto digitado (teste de alternância confirma estado intacto).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-075 — Catálogo data-driven sem hardcode/domínio (RNF-070, RNF-071) ─────────
  {
    key: "T-081",
    storyKey: "US-075",
    summary: "Implementar o WarriorApiCatalog: resolve as ações/sentidos do nível a partir da fachada do warrior (camada Application), com assinatura + descrição",
    definitionOfDone:
      "O catálogo entrega a API do nível a partir da fachada; busca por lista de API hardcoded em scripts de cena retorna 0 ocorrências (RNF-070).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-082",
    storyKey: "US-075",
    summary: "Garantir que os scripts da aba de referência não importam src/domain (acesso via camada Application)",
    definitionOfDone:
      "Busca por load/preload/new de classes de src/domain nos scripts da aba 'API' retorna 0 ocorrências; a aba consome o catálogo via Application (RNF-071).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  // ── US-073 — Aba 'API' por-nível com assinatura+descrição (RF-070, RF-071) ────────
  {
    key: "T-083",
    storyKey: "US-073",
    summary: "Implementar a ApiReferenceTab: renderiza a lista do WarriorApiCatalog (ação/sentido + assinatura + descrição) na aba 'API' do painel",
    definitionOfDone:
      "Ao abrir a aba 'API', cada item exibe assinatura + descrição e a lista corresponde ao que o nível disponibiliza; em dois níveis diferentes as listas diferem conforme a fachada (RF-070, RF-071).",
    status: "done",
    dependsOn: ["T-080", "T-081"],
    parallel: false,
    assignee: null,
  },
];
