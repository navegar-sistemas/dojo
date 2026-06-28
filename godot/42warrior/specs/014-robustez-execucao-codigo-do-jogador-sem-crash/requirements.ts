import type { IRequirement } from "../types.ts";

export const requirements: IRequirement[] = [
  {
    key: "RF-140",
    kind: "functional",
    description:
      "Código do jogador com erro de SINTAXE não crasha nem trava o jogo: a falha de compilação é capturada, o runner fica em estado de erro (has_error / não instancia) e o jogo segue responsivo para editar e rodar de novo.",
    priority: "highest",
    rationale: "CLR-001. Comportamento já parcialmente guardado na compilação; consolidado como requisito.",
  },
  {
    key: "RF-141",
    kind: "functional",
    description:
      "Código que COMPILA mas falha em RUNTIME durante play_turn (método inexistente, acesso a null, tipo errado, assert) não crasha o jogo: a falha é capturada, o turno vira no-op/erro reportado e o jogo segue jogável.",
    priority: "highest",
    rationale: "CLR-001/004: lacuna real — instance.call(play_turn) hoje não é protegido.",
  },
  {
    key: "RF-142",
    kind: "functional",
    description:
      "Código do jogador com loop/recursão que não termina não trava o jogo: a execução de um turno é interrompida com segurança e reportada como erro, mantendo o jogo responsivo.",
    priority: "high",
    rationale: "CLR-001/004: loop infinito é um dos caminhos de crash/trava a cobrir.",
  },
  {
    key: "RF-143",
    kind: "functional",
    description:
      "Todo erro do código do jogador (compilação ou runtime) é exibido de forma legível na ErrorView já existente, incluindo causa/linha quando a engine fornecer essa informação.",
    priority: "high",
    rationale: "CLR-002: a mensagem genérica atual não ajuda; o jogador precisa entender o erro.",
  },
  {
    key: "RF-144",
    kind: "functional",
    description:
      "A robustez (não-crash + reporte) vale em TODOS os caminhos que rodam código do jogador: a tela de jogo (game_controller), a seleção/replay (009) e o sandbox (010).",
    priority: "high",
    rationale: "CLR-003: qualquer superfície que execute o código do jogador deve ser endurecida.",
  },
  {
    key: "RNF-140",
    kind: "non_functional",
    description:
      "A robustez é provada por testes GUT cobrindo os 3 caminhos de erro — (a) sintaxe inválida, (b) runtime (método inexistente/null/tipo), (c) loop/recursão — em TODOS o runner NÃO crasha (has_error/no-op) e reporta mensagem; o crash relatado é reproduzido por teste antes da correção; a suíte permanece 100% verde.",
    priority: "high",
    rationale: "CLR-004: critério comportamental verificável, sem prescrever mecanismo.",
  },
];
