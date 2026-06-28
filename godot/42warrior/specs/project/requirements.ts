import type { IProductRequirement } from "../types.ts";

export const requirements: IProductRequirement[] = [
  {
    key: "PR-001",
    title: "Motor de turnos e estado de nível",
    description:
      "O sistema simula um nível em grade onde, a cada turno, o warrior executa exatamente uma ação que transiciona o estado do mundo de forma determinística; inimigos reagem após a ação do warrior. Inclui o ciclo de jogo (loop de turnos), condições de vitória (alcançar a escada) e derrota (saúde zero).",
    priority: "highest",
  },
  {
    key: "PR-002",
    title: "API do warrior (sentidos e ações)",
    description: "O jogo expõe a API que a lógica do jogador usa para sentir e agir: sentidos sem efeito colateral (feel, look, listen, health, direction_of_stairs, direction_of) e ações que consomem o turno (walk!, attack!, rest!, rescue!, pivot!, shoot!), cada uma aceitando direção (forward/backward) onde aplicável.",
    priority: "highest",
    provenance: { author: "usuario", reason: "bind! e habilidade da intermediate tower, fora do escopo beginner-only confirmado (outOfScope/CLR); nenhuma RF/US a realiza. Alinhar produto antes do Sprint 2 congelar a superficie da WarriorFacade. Recomendado pelo agente-po, decidido sob mandato autonomo do usuario.", at: "2026-06-27" },
  },
  {
    key: "PR-003",
    title: "Entidades e combate",
    description:
      "Modelagem das unidades do jogo (warrior, sludge, thick sludge, archer, wizard, captive) com saúde, dano corpo-a-corpo e à distância, regeneração por descanso, ataque reduzido para trás, e regras de IA dos inimigos (sludge ataca adjacente; archer e wizard atacam à distância).",
    priority: "highest",
  },
  {
    key: "PR-004",
    title: "Beginner tower — 9 níveis",
    description:
      "Definição e carregamento dos 9 níveis da beginner tower (layout, posições de unidades, escada, descrição e habilidades introduzidas por nível), reproduzindo a curva de dificuldade do Ruby Warrior original.",
    priority: "highest",
  },
  {
    key: "PR-005",
    title: "Roteiro do jogador (programação da lógica de turno)",
    description:
      "O jogador fornece a lógica que controla o warrior a cada turno (equivalente a play_turn). O jogo executa essa lógica com segurança contra a API exposta, validando que no máximo uma ação seja efetivada por turno.",
    priority: "highest",
  },
  {
    key: "PR-006",
    title: "Pontuação (time bonus, ace score, resgates)",
    description:
      "Cálculo e exibição de pontuação por nível: pontos por derrotar inimigos e resgatar cativos, time bonus que decai por turno, e comparação com o ace score do nível para sinalizar uma execução ótima (ace).",
    priority: "high",
  },
  {
    key: "PR-007",
    title: "Jogo gráfico — apresentação visual fiel à referência (sprites, tiles, animações)",
    description: "A camada Godot renderiza o jogo com arte real (nao primitivas de _draw): sprites do warrior, dos inimigos (sludge, thick sludge, archer, wizard), do cativo e da escada; o corredor da masmorra como TileMap de tiles de pedra; animacoes de feedback por turno (andar, atacar, levar dano, descansar, resgatar, atirar, morrer); HUD com saude (coracao + valor), numero do turno, descricao do nivel e pontuacao; camera enquadrando o corredor. O alvo visual e a fidelidade a referencia do Ruby Warrior (cavaleiro de armadura, slime verde, escada dourada, masmorra de pedra). Nesta entrega os assets vem de um pack de pixel-art CC0 de licenca livre, integrados com pontos de troca para a arte definitiva da 42. Render procedural por formas geometricas e explicitamente insuficiente e nao satisfaz este requisito.",
    priority: "highest",
    provenance: { author: "usuario", reason: "Especifica arte real (asset pack CC0) e proibe placeholder procedural, conforme decisao do usuario nesta sessao.", at: "2026-06-27" },
  },
  {
    key: "PR-008",
    title: "Fluxo de jogo e progressão pela torre",
    description:
      "Navegação entre níveis: iniciar a torre, avançar ao próximo nível após a vitória, reiniciar nível, e telas de transição que comunicam habilidades novas e narrativa, persistindo o progresso do jogador na torre.",
    priority: "medium",
  },
  {
    key: "PR-009",
    title: "Áudio (SFX e trilha)",
    description: "O jogo reproduz efeitos sonoros para as ações e eventos de turno (andar, atacar, levar dano, descansar, resgatar, atirar, vitória, derrota) e uma trilha sonora de fundo, com controle de volume básico. Os assets de áudio são temáticos da 42 (placeholders trocáveis nesta entrega).",
    priority: "medium",
    provenance: { author: "usuario", reason: "Audio (SFX+musica) foi confirmado no escopo (CLR-003) e virou RF-019/US-015, mas nenhum PR o cobria (PR-007 e so visual). Criar PR-009 dedicado para rastreabilidade produto->feature, mantendo PR-007 = identidade visual. Recomendado pelo agente-po.", at: "2026-06-27" },
  },
  {
    key: "PR-010",
    title: "Editor de código in-game (o jogador programa o warrior)",
    description: "O jogo oferece, na própria tela, um editor onde o JOGADOR escreve a lógica de turno do warrior (play_turn) em GDScript, com syntax highlight, fonte monoespaçada e numeração de linhas; botões para Rodar (compila e executa contra a fachada do warrior), Resetar (volta ao esqueleto inicial do nível) e Ver solução de referência; o código do jogador é persistido por nível (user://) para não se perder entre sessões; erros de compilação e de runtime são exibidos de forma legível junto ao editor, sem travar o jogo. É a interface que torna o produto um jogo de PROGRAMAÇÃO: hoje o código vem embutido em reference_solutions e o jogador não tem onde digitar.",
    priority: "highest",
    provenance: { author: "usuario", reason: "Editor de codigo in-game nunca foi requisito; a clarify parou em compilar GDScript runtime e a implementacao usou solucoes hardcoded. Sem editor o jogador nao programa. Prioridade 2 do usuario.", at: "2026-06-27" },
  },
  {
    key: "PR-011",
    title: "Debug e inspeção da execução (passo a passo e estado do warrior)",
    description: "O jogador inspeciona o que sua lógica faz a cada turno: um log/console de turnos lista, em ordem, o que o warrior sentiu e a ação que tomou com seus efeitos (andou; atacou alvo causando N de dano; descansou recuperando N; levou dano; resgatou cativo; turno sem ação/erro); um painel mostra o estado corrente do warrior (HP, posição, direção) e do nível; controles de execução permitem play, pause, passo-a-passo (um turno por vez) e ajuste de velocidade; mensagens de erro do código do jogador aparecem associadas ao turno em que ocorreram. Hoje só existe um HUD com turno/HP e o desfecho final, sem nenhuma inspeção do percurso.",
    priority: "highest",
    provenance: { author: "usuario", reason: "Debug/inspecao nunca foi requisito; so existe HUD turno/HP e resultado final. Jogo de programacao precisa que o jogador veja o que sua logica fez por turno. Prioridade 3 do usuario.", at: "2026-06-27" },
  },
  {
    key: "PR-012",
    title: "Tema da game jam — Glitch (identidade 42)",
    description: "O jogo comunica o tema obrigatorio da game jam \"glitch\" em conceito, mecanica, estetica, audio e identidade visual da 42 (terminal/Unix, P&B com neon de acento, o \"42\"). O tema aparece na JOGABILIDADE, nao so decorativo: erros do codigo do jogador glitcham o mundo de forma DETERMINISTICA/seedada, e a corrupcao escala com o progresso na torre e com os eventos de turno. Aditivo: nao regride a mecanica core nem os 9 niveis canonicos.",
    priority: "highest",
    provenance: { author: "usuario", reason: "Decisao direta do Matheus: tema obrigatorio da game jam (glitch) e o criterio central da jam; registrar como PR de tema cross-cutting para rastreabilidade.", at: "2026-06-28" },
  },
  {
    key: "PR-013",
    title: "Mundo bidimensional — torres Intermediate/Advanced (grade RxC + 4 direcoes)",
    description: "O mundo evolui de corredor 1xN (beginner) para grade bidimensional linha x coluna (RxC), e o warrior aponta/anda nas 4 direcoes absolutas (cima/baixo/esquerda/direita), espelhando as torres Intermediate/Advanced do Ruby Warrior original. A beginner tower (1xN) permanece compativel como caso especial (R=1). Mantem turno deterministico e dominio independente de engine.",
    priority: "high",
    provenance: { author: "usuario", reason: "Decisao do Usuario (clarify feature 018): capacidade nova de produto — mundo 2D + 4 direcoes espelhando Intermediate/Advanced tower.", at: "2026-06-28" },
  },
  {
    key: "PR-014",
    title: "O jogo roda no navegador (Web/HTML5) sem perder a experiencia desktop",
    description: "O 42warrior e exportavel e jogavel no NAVEGADOR (Godot 4 Web/HTML5/WASM): renderer Compatibility no web (Forward+ preservado no desktop), preset Web, audio iniciando no 1o gesto do usuario, e persistencia user:// (codigo do jogador + progresso) via IndexedDB. O PILAR e que o warrior EXECUTA o codigo do jogador no WASM (GDScript em runtime) — provado por smoke-test web. Zero regressao na experiencia desktop.",
    priority: "high",
    provenance: { author: "usuario", reason: "Ordem direta do Matheus ('o projeto precisa ser exportado em html'); recorte do PO cmqxwb2zw produtizando como feature+PR.", at: "2026-06-28" },
  },
];
