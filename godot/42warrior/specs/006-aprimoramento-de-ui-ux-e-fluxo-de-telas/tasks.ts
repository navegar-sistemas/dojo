import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── US-060 — ScreenManager uma-tela-por-vez (RF-060/061, RNF-062) ────────────────
  {
    key: "T-060",
    storyKey: "US-060",
    summary: "Criar o ScreenManager (autoload/Node) com change_to(scene) que monta a nova tela sob o root de UI e libera a anterior",
    definitionOfDone:
      "ScreenManager existe com a API change_to(scene); após uma chamada, há exatamente 1 tela de topo viva sob o root de UI (teste/inspeção de contagem de nós confirma == 1).",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-061",
    storyKey: "US-060",
    summary: "Migrar todos os call-sites de troca de tela (menu→jogo→resultado→menu/conclusão) para ScreenManager.change_to",
    definitionOfDone:
      "Busca por add_child de cenas de tela fora do ScreenManager retorna 0 ocorrências; todas as transições atuais passam pelo gerenciador (grep + execução das transições sem sobreposição).",
    status: "done",
    dependsOn: ["T-060"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-062",
    storyKey: "US-060",
    summary: "Garantir liberação (queue_free) da tela anterior e ausência de vazamento ao longo do ciclo de telas",
    definitionOfDone:
      "Após o ciclo completo menu→jogo→resultado→menu, a contagem de telas de topo vivas volta ao baseline de 1 (teste de contagem de nós antes/depois é igual).",
    status: "done",
    dependsOn: ["T-060"],
    parallel: true,
    assignee: null,
  },
  // ── US-061 — Layout 'arena em destaque' da tela de jogo (RF-062) ─────────────────
  {
    key: "T-063",
    storyKey: "US-061",
    summary: "Montar o GameScreen com a arena central como maior elemento, HUD fixo no topo e a faixa do console embaixo",
    definitionOfDone:
      "Ao abrir a tela de jogo, a arena é o maior elemento da tela e o HUD fixo (nível, HP, turno) aparece no topo, com a faixa do console na base (verificação visual/screenshot).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-064",
    storyKey: "US-061",
    summary: "Integrar a arena (DungeonView) na região central do GameScreen, montado via ScreenManager",
    definitionOfDone:
      "A tela de jogo é montada por ScreenManager.change_to e a arena ocupa a região central sem nenhuma outra tela de topo sobreposta (verificação visual da tela de jogo legível).",
    status: "done",
    dependsOn: ["T-063", "T-061"],
    parallel: false,
    assignee: null,
  },
  // ── Sprint 2 "Salto visual" ──────────────────────────────────────────────────────
  // ── US-062 — Registro data-driven de assets (RF-068, RNF-060) ────────────────────
  {
    key: "T-065",
    storyKey: "US-062",
    summary: "Definir o recurso EntityAssetRegistry mapeando entidade→sprite, (entidade, ação)→animação e tiles do corredor por ID/caminho",
    definitionOfDone:
      "EntityAssetRegistry existe como recurso de dados e resolve sprite/animação/tile por ID; busca por caminho de asset hardcoded em scripts de cena retorna 0 ocorrências.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-066",
    storyKey: "US-062",
    summary: "Fazer a cena (DungeonTileView/EntityAnimator) resolver todo sprite/animação/tile via o EntityAssetRegistry",
    definitionOfDone:
      "Trocar o sprite de uma entidade alterando apenas o registro ou o arquivo referenciado reflete no jogo com 0 edições em scripts .gd de cena (teste de troca via registro).",
    status: "done",
    dependsOn: ["T-065"],
    parallel: false,
    assignee: null,
  },
  // ── US-063 — Sprites coesos das 7 entidades + assets da internet (RF-065, RF-069) ─
  {
    key: "T-067",
    storyKey: "US-063",
    summary: "Obter da internet e registrar sprites coesos (inspirados no Ruby Warrior) das 7 entidades: warrior, sludge, thick sludge, archer, wizard, captive, escada",
    definitionOfDone:
      "As 7 entidades têm sprite definido no EntityAssetRegistry, com arquivos de arte presentes no projeto; nenhuma entidade fica sem sprite no registro.",
    status: "done",
    dependsOn: ["T-065"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-068",
    storyKey: "US-063",
    summary: "Renderizar cada entidade por Sprite2D resolvido do registro, substituindo qualquer render por forma geométrica procedural",
    definitionOfDone:
      "Em execução, cada uma das 7 entidades aparece com seu sprite do registro e há 0 desenho procedural de entidade por _draw (inspeção visual + grep).",
    status: "done",
    dependsOn: ["T-067"],
    parallel: false,
    assignee: null,
  },
  // ── US-064 — Corredor em tiles de masmorra (RF-066) ──────────────────────────────
  {
    key: "T-069",
    storyKey: "US-064",
    summary: "Renderizar o corredor com tiles de masmorra (chão/parede/fundo) do registro em TileMap dimensionado pelo width do LevelState",
    definitionOfDone:
      "O corredor usa tiles do registro e reflete o width do LevelState; busca por render procedural por _draw do corredor retorna 0 ocorrências (inspeção visual + grep).",
    status: "done",
    dependsOn: ["T-065"],
    parallel: true,
    assignee: null,
  },
  // ── US-065 — Animações por TurnEvent, domínio intacto (RF-067, RNF-061) ───────────
  {
    key: "T-070",
    storyKey: "US-065",
    summary: "Mapear cada TurnEvent (attacked/rested/pivoted/moved/took_damage/rescued/shot/died) para sua animação no EntityAnimator e dispará-la na sprite da entidade afetada",
    definitionOfDone:
      "Cada tipo de TurnEvent aciona a animação correspondente na sprite certa, com ataque, cura e defesa entre elas (teste/inspeção por tipo de evento).",
    status: "done",
    dependsOn: ["T-067"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-071",
    storyKey: "US-065",
    summary: "Garantir que os scripts de cena consomem o estado só via a camada Application, sem importar classes de src/domain",
    definitionOfDone:
      "Busca por load/preload/new de classes de src/domain em scripts de cena retorna 0 ocorrências; a cena consome o TurnResult via a camada Application.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  // ── US-066 — Editor como overlay toggleável (RF-063) ─────────────────────────────
  {
    key: "T-072",
    storyKey: "US-066",
    summary: "Adicionar botão toggle no HUD para abrir/fechar o painel de código como overlay sobre a arena",
    definitionOfDone:
      "HUD exibe botão '</> Código'; ao pressionar, CodeEditorPanel alterna visibilidade sem trocar de tela; arena permanece visível ao fundo.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-073",
    storyKey: "US-066",
    summary: "Preservar texto do editor ao fechar e reabrir o overlay",
    definitionOfDone:
      "Fechar e reabrir o painel de código mantém intacto o texto digitado no CodeEdit (não reinicia nem apaga o conteúdo).",
    status: "done",
    dependsOn: ["T-072"],
    parallel: false,
    assignee: null,
  },
  // ── US-067 — Controles de reprodução e console de eventos (RF-064) ───────────────
  {
    key: "T-074",
    storyKey: "US-067",
    summary: "Verificar que play/pause/passo-a-passo/velocidade e listagem de turn_events já estão funcionais",
    definitionOfDone:
      "ExecutionControls (play/pause, step, speed slider) e TurnConsole (lista eventos por turno em ordem) funcionam conforme RF-064; verificado por inspeção de código e teste manual.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
  // ── US-068 — Theme consistente em todas as telas (RNF-063) ───────────────────────
  {
    key: "T-075",
    storyKey: "US-068",
    summary: "Criar Theme.tres e aplicar como tema padrão a todas as 5 telas e ao HUD",
    definitionOfDone:
      "Arquivo assets/theme/game_theme.tres existe; todas as 5 cenas (main_menu, game, level_transition, level_result, tower_complete) e o HUD referenciam o tema; 0 cores/fontes hardcoded avulsas fora do tema.",
    status: "done",
    dependsOn: [],
    parallel: false,
    assignee: null,
  },
];
