import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Funcionais (PR-002 API + PR-010 editor in-game) ──────────────────────────────
  {
    key: "RF-070",
    kind: "functional",
    description:
      "A tela de jogo oferece uma aba 'API' DENTRO do painel do editor retrátil (feature 006, botão '</> Código'), que lista as ações e sentidos do warrior disponíveis NAQUELE nível, cada um com assinatura + descrição curta. Verificável: ao abrir a aba 'API', cada item exibido tem assinatura e descrição, e a lista corresponde ao que o nível disponibiliza.",
    priority: "highest",
    rationale: "CLR-001: aba no painel do editor da 006 (não painel separado no HUD); discoverability da API (PR-002) na superfície do editor (PR-010).",
  },
  {
    key: "RF-071",
    kind: "functional",
    description:
      "O conteúdo da aba 'API' é data-driven a partir da fachada do warrior / estado do nível: mostra SÓ as ações/sentidos que o nível atual expõe (revelação progressiva, estilo Ruby Warrior), não um catálogo fixo de toda a tower. Verificável: em dois níveis com fachadas diferentes, a aba 'API' exibe conjuntos diferentes, cada um coerente com a fachada do respectivo nível.",
    priority: "highest",
    rationale: "CLR-001: por-nível, data-driven da fachada (não fixo); acompanha a progressão de habilidades da beginner tower.",
  },
  {
    key: "RF-072",
    kind: "functional",
    description:
      "A aba 'API' vive no MESMO painel que receberá depois a aba 'Glossário' (feature 008): o painel tem estrutura de abas, e a 007 estabelece o painel/aba primeiro. Verificável: o painel do editor expõe uma estrutura de abas onde 'API' é uma aba, extensível para acrescentar 'Glossário'.",
    priority: "high",
    rationale: "CLR-002: mesmo painel com abas (API + Glossário); 007 estabelece a estrutura, 008 adiciona a aba depois.",
  },
  {
    key: "RF-073",
    kind: "functional",
    description:
      "Abrir/fechar (ou alternar para) a aba 'API' é não-bloqueante: não troca de tela, não recria a arena e não perde o código digitado no editor. Verificável: alternar para a aba 'API' e voltar preserva o estado da arena e o texto do editor.",
    priority: "high",
    rationale: "Coerente com o editor retrátil não-bloqueante da 006; a referência não interrompe a sessão de código.",
  },
  // ── Não-funcionais ───────────────────────────────────────────────────────────────
  {
    key: "RNF-070",
    kind: "non_functional",
    description:
      "A lista da aba 'API' é resolvida da fachada do warrior / dados do nível, sem catálogo hardcoded por nível em scripts de cena: adicionar/remover um método na fachada reflete na aba sem editar a cena. Verificável: 0 listas de API hardcoded em scripts .gd de cena.",
    priority: "highest",
    rationale: "CLR-001 + CONV-002: data-driven e sem duplicar a definição da API na apresentação.",
  },
  {
    key: "RNF-071",
    kind: "non_functional",
    description:
      "Os scripts de apresentação da aba 'API' não importam classes de src/domain: o conteúdo vem via a camada Application (a fachada/contrato do warrior). Verificável: 0 ocorrências de load/preload/new de classes de src/domain nos scripts da aba de referência.",
    priority: "high",
    rationale: "CONV-002/RNF-061 (006): domínio independente da engine; a aba é adaptador de saída.",
  },
];
