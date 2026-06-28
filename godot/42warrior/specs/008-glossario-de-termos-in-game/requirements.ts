import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Funcionais (PR-003 Entidades + PR-006 Pontuação) ─────────────────────────────
  {
    key: "RF-080",
    kind: "functional",
    description:
      "A aba 'Glossário' (no painel do editor da feature 007) define as ENTIDADES presentes no nível atual (ex.: sludge, thick sludge, archer, wizard, captive, escada), cada uma com nome + descrição curta. Verificável: a aba lista exatamente as entidades do LevelState atual, cada uma com nome e descrição.",
    priority: "highest",
    rationale: "CLR-001/CLR-002 (008) + PR-003: clareza semântica das entidades para o iniciante, sem sair do jogo.",
  },
  {
    key: "RF-081",
    kind: "functional",
    description:
      "A aba 'Glossário' define os TERMOS DE PONTUAÇÃO relevantes (time bonus, rescue bonus, ace/clear bonus) com nome + definição curta + os VALORES NUMÉRICOS do nível atual quando aplicável. Verificável: cada termo de score exibido tem nome, definição e, quando aplicável, o valor numérico daquele nível.",
    priority: "highest",
    rationale: "CLR-001 (008) + PR-006: ajudar o jogador a entender e otimizar o score (liga com a feature 009).",
  },
  {
    key: "RF-082",
    kind: "functional",
    description:
      "O conteúdo do glossário é data-driven do LevelState (entidades presentes) e das regras de pontuação: mostra SÓ as entidades do nível atual, não o catálogo completo da tower. Verificável: em dois níveis com entidades diferentes, a aba exibe conjuntos diferentes, coerentes com cada LevelState.",
    priority: "high",
    rationale: "CLR-002 (008): por-nível, data-driven; coerente com o 'por nível' da feature 007.",
  },
  {
    key: "RF-083",
    kind: "functional",
    description:
      "A aba 'Glossário' vive no MESMO painel com abas estabelecido pela feature 007 (aba ao lado da aba 'API'), não como tooltip nem painel separado, e é não-bloqueante (não troca de tela, não recria a arena, não perde o código). Verificável: o painel do editor exibe a aba 'Glossário' ao lado da aba 'API', e alternar para ela preserva arena e texto.",
    priority: "high",
    rationale: "CLR-001 (008): aba no painel da 007 (não tooltip); reusa a estrutura de abas da 007.",
  },
  // ── Não-funcional ────────────────────────────────────────────────────────────────
  {
    key: "RNF-072",
    kind: "non_functional",
    description:
      "O conteúdo do glossário (entidades e termos de pontuação) é resolvido do LevelState e das regras de pontuação, sem lista hardcoded por nível em scripts de cena, e a aba não importa classes de src/domain (acesso via camada Application). Verificável: 0 listas de entidades/score hardcoded em scripts .gd de cena da aba e 0 ocorrências de load/preload/new de src/domain.",
    priority: "high",
    rationale: "CLR-002 (008) + CONV-002: data-driven e domínio independente da engine; a aba é adaptador puro de saída.",
  },
];
