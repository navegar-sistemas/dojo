import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-013",
    title: "ScreenManager como única autoridade de navegação (uma-tela-por-vez)",
    context:
      "A build atual monta telas via add_child sem liberar/ocultar a anterior, produzindo telas de topo simultâneas e o jogo ilegível (bug de sobreposição reportado, CLR-004 / Image #7). Não há autoridade central de navegação: cada ponto (menu→jogo, jogo→resultado, resultado→menu/conclusão) instancia a próxima tela ad hoc, e é daí que nasce a sobreposição.",
    decision:
      "Introduzir um ScreenManager (autoload/Node) como ÚNICA autoridade de troca de telas, mantendo referência à tela de topo ativa sob um único root de UI. Em change_to(scene): instancia a nova tela, monta-a sob o root e só então libera (queue_free) a anterior — garantindo no máximo 1 tela de topo viva por vez. Todos os call-sites que hoje fazem add_child de cenas de tela são migrados para chamar o gerenciador; nenhum script monta tela de topo fora dele (a troca é pedida por sinal, não por instanciação direta).",
    consequences:
      "Sobreposição eliminada na raiz: após qualquer transição há exatamente 1 tela de topo visível (RF-060) e a busca por add_child de telas fora do ScreenManager retorna 0 (RF-061). Como a anterior é liberada, a contagem de telas vivas volta ao baseline após o ciclo menu→jogo→resultado→menu, sem vazamento (RNF-062). Custo: migrar os pontos de instanciação atuais e padronizar o contrato de 'pedir troca de tela'.",
    status: "accepted",
    requirementKeys: ["RF-060", "RF-061", "RNF-062"],
    rejectedAlternatives: [
      {
        alternative: "Cada tela libera a anterior por conta própria via get_tree().change_scene_to",
        reason:
          "change_scene troca a cena raiz inteira e descarta o contexto de jogo (LevelState/score) entre telas; além disso espalha a regra de liberação por N telas, reintroduzindo exatamente o risco de sobreposição que o bug original demonstrou.",
      },
      {
        alternative: "Empilhar todas as telas e apenas alternar a propriedade visible",
        reason:
          "Nós ocultos continuam vivos e se acumulam a cada navegação (vaza memória, viola RNF-062); e qualquer overlay translúcido voltaria a deixar duas telas legíveis ao mesmo tempo.",
      },
    ],
  },
  {
    key: "ADR-014",
    title: "Tela de jogo 'arena em destaque': HUD fixo, editor retrátil em overlay, console de turnos",
    context:
      "CLR-003 fixou o layout da tela de jogo: o corredor (arena) em foco visual, HUD no topo, console de turnos na faixa inferior, e o editor de código acessível sem ocupar área fixa. A tela precisa compor a inspeção de turno da feature 004 e o editor da feature 003 sem recriar a arena a cada interação nem perder o código digitado.",
    decision:
      "GameScreen organiza a tela em três regiões via Control: HUD fixo no topo (nível, HP em coração + valor, turno); a arena (DungeonTileView) como região central de maior área; e o TurnConsole na faixa inferior, com controles play/pause/passo-a-passo/velocidade que dirigem o avanço de turnos já existente e listam os turn_events em ordem. Um botão '</> Código' alterna o CodeEditorPanel, que desliza como overlay sobre a lateral da arena (animação show/hide), preservando o texto e o estado da arena, sem trocar de tela.",
    consequences:
      "A arena é o maior elemento e nunca fica sob outra tela de topo (RF-062); o editor é overlay retrátil que preserva estado quando fechado/aberto (RF-063); o console dirige a reprodução e ordena os eventos (RF-064), reusando a inspeção da 004. Custo: GameScreen coordena a visibilidade/animação do overlay e o estado de reprodução do console.",
    status: "accepted",
    requirementKeys: ["RF-062", "RF-063", "RF-064"],
    rejectedAlternatives: [
      {
        alternative: "Editor de código como painel fixo lado-a-lado, sempre ocupando metade da tela",
        reason:
          "CLR-003 pediu imersão na batalha com a arena em destaque; um painel fixo rouba área permanente da arena, contrariando o layout escolhido.",
      },
    ],
  },
  {
    key: "ADR-015",
    title: "TurnEvents → animações na cena; a cena observa o TurnResult, domínio intacto",
    context:
      "CLR-001 pediu, explicitamente, animações por ação — ataque, cura/descanso, defesa/pivô, além de andar, levar dano, resgatar, atirar e morrer — acionadas pelos TurnEvents do domínio. CONV-002 / RNF-061 exigem que a cena não importe classes de src/domain: todo acesso ao estado se dá pela camada Application (LevelState, TurnEvents, WarriorFacade).",
    decision:
      "Após cada resolução de turno, o fluxo entrega o TurnResult (próximo estado + lista de TurnEvent) ao EntityAnimator, que mapeia cada tipo de evento para uma animação (moved→walk, attacked→attack, rested→heal, pivoted→defend, took_damage→hurt, rescued→rescue, shot→shoot, died/defeated→die) e a despacha para a sprite da entidade afetada, enfileirando as animações do turno. A cena assina a saída da camada Application e não instancia nem importa nada de src/domain.",
    consequences:
      "Feedback visual por turno fiel, com ataque, cura e defesa explicitamente entre as animações (RF-067); o domínio permanece independente da engine — 0 load/preload/new de classes de src/domain em scripts de cena (RNF-061). Custo: EntityAnimator mantém o mapa evento→animação e a fila de reprodução do turno.",
    status: "accepted",
    requirementKeys: ["RF-067", "RNF-061"],
    rejectedAlternatives: [
      {
        alternative: "TurnResolver do domínio emitir sinais Godot diretamente para a cena",
        reason:
          "Acoplaria o domínio à engine (viola CONV-002/RNF-061). Os TurnEvents já são o contrato de saída do domínio; a cena consome o TurnResult, não o contrário.",
      },
    ],
  },
  {
    key: "ADR-016",
    title: "Registro data-driven de assets (sprite/animação/tiles) com arte livre da internet",
    context:
      "RF-065/066/068/069 e CLR-001/CLR-005 pedem identidade visual coesa inspirada no Ruby Warrior (com cara da 42) para as 7 entidades e o corredor em tiles, obtida de assets livres da internet (licença irrelevante por ser jogo não-comercial). RNF-060 é requisito explícito do usuário: trocar/adicionar o asset de qualquer entidade deve mexer em 1 ponto só, sem editar scripts de cena.",
    decision:
      "Um recurso de dados central — EntityAssetRegistry (ex.: .tres/.json) — mapeia entidade→sprite, (entidade, ação)→animação e os tiles do corredor (chão/parede/fundo) por caminho/ID, desacoplado da lógica de cena. DungeonTileView e EntityAnimator resolvem todo sprite/animação/tile exclusivamente via o registro; nenhum caminho de asset é hardcoded em script de cena. Os arquivos de arte vêm de packs livres da internet e são referenciados pelo registro, substituindo render procedural e placeholders.",
    consequences:
      "Visual coeso substituindo o procedural nas 7 entidades (RF-065) e no corredor em tiles dimensionado pelo width do nível (RF-066); apresentação data-driven (RF-068) com assets reais da internet em execução (RF-069); trocar qualquer asset = alterar só o registro/arquivos, com 0 edição em .gd de cena (RNF-060). Custo: manter o esquema do registro e o carregamento por ID na borda de apresentação.",
    status: "accepted",
    requirementKeys: ["RF-065", "RF-066", "RF-068", "RF-069", "RNF-060"],
    rejectedAlternatives: [
      {
        alternative: "Caminhos de asset como constantes espalhadas (preload) nos scripts de cada cena",
        reason:
          "Quebra RNF-060: trocar uma sprite exigiria caçar e editar preloads em vários .gd; o registro central garante o ponto único de troca pedido pelo usuário.",
      },
    ],
  },
  {
    key: "ADR-017",
    title: "1 único Theme do Godot aplicado às 5 telas e ao HUD",
    context:
      "CLR-002: a UI atual parece 'completamente diferente' entre telas porque usa peças desconexas — cores e fontes avulsas hardcoded por controle. RNF-063 quer coesão visual via 1 Theme compartilhado.",
    decision:
      "Definir 1 único recurso Theme (paleta + família tipográfica) e aplicá-lo às 5 telas (menu, jogo, transição de nível, resultado, conclusão da torre) e ao HUD; os controles herdam do Theme e os overrides locais de cor/fonte são removidos.",
    consequences:
      "Coesão visual entre telas e HUD, e troca de paleta/tipografia num ponto único: as 5 telas referenciam o mesmo Theme e restam 0 cores/fontes avulsas fora dele (RNF-063). Custo: extrair os estilos atuais para o Theme e remover os overrides locais.",
    status: "accepted",
    requirementKeys: ["RNF-063"],
    rejectedAlternatives: [
      {
        alternative: "Manter estilos por tela e apenas padronizar uma paleta de cores por convenção",
        reason:
          "Convenção não é verificável e regride: sem um Theme único referenciado, voltam cores/fontes avulsas — exatamente a causa da incoerência atual (CLR-002).",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "ScreenManager",
    responsibility:
      "Autoridade única de navegação: mantém a tela de topo ativa sob um root de UI e, em change_to(scene), monta a nova e libera (queue_free) a anterior, garantindo ≤1 tela de topo viva. Todos os pedidos de troca passam por ele.",
    dependsOn: [],
    requirementKeys: ["RF-060", "RF-061", "RNF-062"],
  },
  {
    name: "GameScreen",
    responsibility:
      "Tela de jogo no layout 'arena em destaque': compõe HUD fixo no topo, a arena (DungeonTileView) como região central, o TurnConsole na faixa inferior e o CodeEditorPanel como overlay retrátil; coordena visibilidade/animação do overlay sem recriar a arena.",
    dependsOn: ["DungeonTileView", "EntityAnimator", "TurnConsole", "CodeEditorPanel", "UiTheme"],
    requirementKeys: ["RF-062", "RF-063", "RF-064"],
  },
  {
    name: "CodeEditorPanel",
    responsibility:
      "Editor de código retrátil acionado pelo botão '</> Código'; desliza como overlay sobre a lateral da arena e preserva o texto digitado e o estado da arena ao abrir/fechar.",
    dependsOn: ["UiTheme"],
    requirementKeys: ["RF-063"],
  },
  {
    name: "TurnConsole",
    responsibility:
      "Console de turnos na faixa inferior: lista os turn_events em ordem e oferece controles de execução (play, pause, passo-a-passo, velocidade) que dirigem o avanço de turnos já existente.",
    dependsOn: ["UiTheme"],
    requirementKeys: ["RF-064"],
  },
  {
    name: "DungeonTileView",
    responsibility:
      "Renderiza o corredor com tiles de masmorra (chão/parede/fundo) resolvidos pelo registro de assets e dimensionado pelo width do LevelState, substituindo o render procedural por _draw.",
    dependsOn: ["EntityAssetRegistry"],
    requirementKeys: ["RF-066"],
  },
  {
    name: "EntityAnimator",
    responsibility:
      "Observa o TurnResult vindo da camada Application e despacha, para a sprite de cada entidade afetada, a animação mapeada a partir do tipo de TurnEvent (attack/heal/defend/walk/hurt/rescue/shoot/die); resolve sprites e animações via o registro e não importa classes de src/domain.",
    dependsOn: ["EntityAssetRegistry"],
    requirementKeys: ["RF-067", "RNF-061"],
  },
  {
    name: "EntityAssetRegistry",
    responsibility:
      "Recurso de dados central que mapeia entidade→sprite, (entidade, ação)→animação e os tiles do corredor por caminho/ID; ponto único de troca de assets (livres da internet), sem caminhos hardcoded em scripts de cena.",
    dependsOn: [],
    requirementKeys: ["RF-065", "RF-068", "RF-069", "RNF-060"],
  },
  {
    name: "UiTheme",
    responsibility:
      "1 único recurso Theme (paleta + família tipográfica) aplicado às 5 telas e ao HUD; os controles herdam dele, sem cores/fontes avulsas hardcoded.",
    dependsOn: [],
    requirementKeys: ["RNF-063"],
  },
];
