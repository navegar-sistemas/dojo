import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  // ── Fluxo e navegação de telas (PR-008) — corrige a sobreposição ───────────────
  {
    key: "RF-060",
    kind: "functional",
    description:
      "Um gerenciador de navegação (ScreenManager) mantém exatamente UMA tela ativa por vez: menu, jogo, transição de nível, resultado de nível e conclusão da torre. Ao navegar, a tela anterior é liberada (queue_free) ou ocultada antes/ao montar a próxima — em nenhum instante duas telas de topo ficam visíveis ao mesmo tempo. Verificável: após qualquer transição, o número de telas de topo visíveis sob o root de UI é exatamente 1.",
    priority: "highest",
    rationale: "CLR-004 / PR-008: corrige o bug de telas sobrepostas reportado; a raiz é telas montadas sem liberar/ocultar a anterior.",
  },
  {
    key: "RF-061",
    kind: "functional",
    description:
      "Toda troca de tela passa pelo ScreenManager: nenhum script monta uma tela de topo via add_child fora dele. Os pontos atuais que instanciam/mostram uma tela sem remover a anterior são migrados para o gerenciador. Verificável: busca por add_child de cenas de tela fora do ScreenManager retorna 0 ocorrências.",
    priority: "highest",
    rationale: "CLR-004 / PR-008: elimina os caminhos que produzem a sobreposição (Image #7).",
  },
  // ── Tela de jogo: arena em destaque + editor retrátil (PR-007 / CLR-003) ───────
  {
    key: "RF-062",
    kind: "functional",
    description:
      "A tela de jogo usa o layout 'arena em destaque': o corredor da masmorra ocupa a área principal (foco visual); HUD fixo no topo (nível, HP em coração + valor, turno); console de turnos na faixa inferior. Verificável: ao abrir a tela de jogo, a arena é o maior elemento da tela e nenhuma outra tela de topo está sobreposta a ela.",
    priority: "highest",
    rationale: "CLR-003: layout escolhido pelo usuário (arena em destaque).",
  },
  {
    key: "RF-063",
    kind: "functional",
    description:
      "Um botão '</> Código' na tela de jogo abre/fecha o editor de código, que desliza como overlay por cima/lateral da arena. Fechado, o editor não ocupa área e a arena fica plena; aberto, sobrepõe parcialmente sem trocar de tela nem recriar a arena nem perder o código digitado. Verificável: alternar o botão mostra/esconde o painel preservando o estado da arena e do texto.",
    priority: "high",
    rationale: "CLR-003: editor retrátil para imersão na batalha sem espaço fixo.",
  },
  {
    key: "RF-064",
    kind: "functional",
    description:
      "A faixa inferior da tela de jogo apresenta o console de turnos (eventos em ordem) com controles de execução: play, pause, passo-a-passo e ajuste de velocidade, que dirigem o avanço dos turnos já existente. Verificável: cada controle altera o estado de reprodução e o console lista os turn_events na ordem em que ocorreram.",
    priority: "high",
    rationale: "CLR-003: composição da tela de jogo, reaproveitando a inspeção da feature 004.",
  },
  // ── Identidade visual coesa, inspirada (PR-007 / CLR-002) ──────────────────────
  {
    key: "RF-065",
    kind: "functional",
    description:
      "Cada entidade tem sprite com identidade visual coesa inspirada no Ruby Warrior, com liberdade de adaptação (cara da 42): warrior, sludge, thick sludge, archer, wizard, captive e escada. Os sprites compartilham paleta e estilo entre si, substituindo qualquer render pobre/placeholder. Verificável: as 7 entidades têm sprite definido no registro e nenhuma é desenhada por forma geométrica procedural.",
    priority: "highest",
    rationale: "CLR-002 / PR-007: visual coeso e inspirado, não réplica pixel-perfect.",
  },
  {
    key: "RF-066",
    kind: "functional",
    description:
      "O corredor é renderizado com tiles de masmorra (chão de pedra, paredes, fundo) coesos com a identidade visual e dimensionado pelo width do nível. Verificável: o corredor reflete o tamanho do LevelState e usa tiles do registro, sem render procedural por _draw.",
    priority: "high",
    rationale: "PR-007: cenário inspirado e coeso, substituindo o procedural.",
  },
  {
    key: "RF-067",
    kind: "functional",
    description:
      "Os TurnEvents do domínio disparam animações nas sprites, incluindo explicitamente ataque (attacked), cura/descanso (rested) e defesa/pivô (pivoted), além de andar (moved), levar dano (took_damage), resgatar (rescued), atirar (shot) e morrer (died/defeated). A cena assina os eventos e aciona as animações sem conter regra de jogo. Verificável: cada tipo de TurnEvent mapeia para uma animação acionável; ataque, cura e defesa estão entre elas.",
    priority: "highest",
    rationale: "CLR-001: animações de ataque, cura, defesa etc. acionadas pelos turn_events (pedido explícito do usuário).",
  },
  // ── Apresentação data-driven e assets (PR-007 / CLR-001, CLR-005) ──────────────
  {
    key: "RF-068",
    kind: "functional",
    description:
      "Um registro central (recurso de dados) mapeia entidade→sprite e (entidade, ação)→animação por caminho/ID, desacoplado da lógica de cena; trocar um asset significa alterar o registro/arquivo, sem editar scripts de cena. Verificável: a cena resolve sprites e animações via o registro e não há caminhos de asset hardcoded espalhados pelos scripts de cena.",
    priority: "highest",
    rationale: "CLR-001: apresentação data-driven para troca e evolução fáceis (extensibilidade pedida).",
  },
  {
    key: "RF-069",
    kind: "functional",
    description:
      "Os assets gráficos (sprites, tiles, frames de animação) são obtidos da internet — qualquer licença, por ser jogo não-comercial — e integrados via o registro, substituindo placeholders. Verificável: os arquivos de asset existem no projeto, são referenciados pelo registro, e as entidades e o cenário os exibem em execução.",
    priority: "high",
    rationale: "CLR-005: assets livres da internet, licença irrelevante.",
  },
  // ── Não-funcionais ─────────────────────────────────────────────────────────────
  {
    key: "RNF-060",
    kind: "non_functional",
    description:
      "Trocar ou adicionar o sprite/animação de qualquer das 7 entidades exige alterar apenas 1 ponto — o registro de assets (ou os arquivos por ele referenciados) — com 0 edições em scripts de cena; os pontos de troca são documentados. Verificável: 0 ocorrências de caminho de asset hardcoded fora do registro em scripts .gd de cena.",
    priority: "highest",
    rationale: "CLR-001: alterações futuras fáceis — requisito explícito do usuário.",
  },
  {
    key: "RNF-061",
    kind: "non_functional",
    description:
      "As cenas e scripts de apresentação não importam nem instanciam classes de src/domain diretamente: todo acesso ao estado ocorre via a camada Application (LevelState, TurnEvents, WarriorFacade). Verificável: 0 ocorrências de load/preload/new de classes de src/domain em scripts de cena.",
    priority: "highest",
    rationale: "CONV-002: domínio independente da engine; a cena é adaptador puro de saída.",
  },
  {
    key: "RNF-062",
    kind: "non_functional",
    description:
      "A navegação não vaza nós: após um ciclo completo de telas (menu→jogo→resultado→menu), o número de telas de topo vivas na árvore retorna ao baseline (1 ativa), sem acúmulo de instâncias anteriores. Verificável: contagem de nós de tela após o ciclo é igual à do início.",
    priority: "high",
    rationale: "CLR-004: a sobreposição vinha de telas não liberadas; previne a regressão do bug.",
  },
  {
    key: "RNF-063",
    kind: "non_functional",
    description:
      "1 único Theme do Godot (paleta + família tipográfica compartilhadas) é definido como recurso e aplicado às 5 telas (menu, jogo, transição, resultado, conclusão) e ao HUD, garantindo coesão visual. Verificável: as 5 telas referenciam o mesmo Theme e há 0 cores/fontes avulsas hardcoded fora dele.",
    priority: "medium",
    rationale: "CLR-002: o 'completamente diferente' atual decorre de peças desconexas; coesão é o alvo.",
  },
];
