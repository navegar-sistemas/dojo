import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-076 — Glossário por-nível (entidades + termos de score) (RF-080/081/082) ──
  {
    key: "T-084",
    storyKey: "US-076",
    summary: "Implementar o GlossaryCatalog: resolve do LevelState as entidades do nível (nome+descrição) e das regras de pontuação os termos de score (nome+definição+valor do nível)",
    definitionOfDone:
      "O catálogo entrega, por nível, as entidades presentes e os termos de pontuação com valores; em dois níveis distintos os conjuntos diferem conforme o LevelState (RF-082).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-085",
    storyKey: "US-076",
    summary: "Implementar a GlossaryTab renderizando as entidades e os termos de pontuação do GlossaryCatalog",
    definitionOfDone:
      "Ao abrir a aba 'Glossário', cada entidade do nível aparece com nome+descrição e cada termo de score com nome+definição+valor do nível quando aplicável (RF-080, RF-081).",
    status: "done",
    dependsOn: ["T-084"],
    parallel: false,
    assignee: null,
  },
  // ── US-077 — Aba no painel da 007, não-bloqueante (RF-083) ───────────────────────
  {
    key: "T-086",
    storyKey: "US-077",
    summary: "Adicionar a aba 'Glossário' à estrutura de abas do painel do editor (EditorPanelTabs da 007), ao lado da aba 'API'",
    definitionOfDone:
      "O painel do editor exibe a aba 'Glossário' ao lado da 'API' sem refazer a estrutura; alternar para ela não troca de tela, não recria a arena e preserva o texto (RF-083). Requer a 007 implementada.",
    status: "done",
    dependsOn: ["T-085"],
    parallel: false,
    assignee: null,
  },
  // ── US-078 — Data-driven sem hardcode/domínio (RNF-072) ──────────────────────────
  {
    key: "T-087",
    storyKey: "US-078",
    summary: "Garantir que a aba 'Glossário' e o catálogo não têm listas hardcoded por nível e não importam src/domain",
    definitionOfDone:
      "Busca por lista de entidades/score hardcoded em scripts de cena da aba retorna 0 ocorrências e busca por load/preload/new de src/domain retorna 0 ocorrências (RNF-072).",
    status: "done",
    dependsOn: ["T-084"],
    parallel: true,
    assignee: null,
  },
];
