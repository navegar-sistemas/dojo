import type { IArchitectureDecision, IComponent } from "../types.ts";

export const decisions: IArchitectureDecision[] = [
  {
    key: "ADR-032",
    title: "Fronteira única de execução segura do código do jogador no PlayerScriptRunner (mecanismo a cargo do dev)",
    context:
      "O código do jogador é executado pelo PlayerScriptRunner (compile via GDScript.reload + play_turn via instance.call). A compilação já é guardada, mas play_turn não tem proteção: erro de runtime (método inexistente, null, tipo, assert) ou loop/recursão derruba/trava o jogo (RF-141/142). GDScript não tem try/catch, então o MECANISMO de captura é investigação do dev — esta decisão fixa apenas ONDE e O QUE, não COMO.",
    decision:
      "Concentrar TODA execução do código do jogador (compile + play_turn) atrás de uma fronteira única no PlayerScriptRunner que: captura falha de sintaxe (já existe), captura falha de runtime em play_turn e a transforma em estado de erro (has_error) + no-op do turno (RF-140/141), e protege contra execução que não termina (guarda de iteração/turno) (RF-142). Nenhuma falha do código do jogador propaga para crashar o processo. O mecanismo concreto (capturar texto do parse error, validar interface/sandbox antes do call, limitar a superfície chamável ao facade, guarda de iteração, estratégias seguras de call) é escolhido pelo dev na implementação.",
    consequences:
      "Jogo permanece responsivo diante de qualquer código do jogador; ponto único de robustez reaproveitado por todas as superfícies. Custo/risco: como GDScript não tem exceções, o dev precisa de uma estratégia de captura comprovada por teste (reproduzir o crash antes de corrigir). RNF-140 exige a prova por GUT.",
    status: "accepted",
    requirementKeys: ["RF-140", "RF-141", "RF-142", "RNF-140"],
    rejectedAlternatives: [
      {
        alternative: "Envolver instance.call em try/catch",
        reason: "GDScript não tem try/catch/exceções; a sugestão literal do Usuário não se aplica — o mecanismo precisa ser investigado, não prescrito.",
      },
      {
        alternative: "Validar semanticamente a lógica do jogador antes de rodar",
        reason: "Fora de escopo: o objetivo é não-crash + reporte, não julgar a correção da lógica.",
      },
    ],
  },
  {
    key: "ADR-033",
    title: "Reporte legível centralizado na ErrorView e abrangência das 3 superfícies",
    context:
      "O erro precisa chegar legível ao jogador (causa/linha quando a engine fornecer) tanto na compilação quanto no runtime (RF-143), e isso vale em todos os caminhos que rodam código do jogador: game_controller, replay (009) e sandbox (010) (RF-144).",
    decision:
      "O resultado de erro do PlayerScriptRunner (compile ou runtime) carrega uma mensagem legível (com causa/linha quando disponível) consumida pela ErrorView já existente; os 3 caminhos (game_controller, 009, 010) usam o MESMO runner endurecido, herdando a robustez e o reporte sem duplicar lógica.",
    consequences:
      "Mensagem útil em vez da genérica; cobertura uniforme das superfícies. Custo: padronizar o formato da mensagem de erro e fiar a ErrorView nos 3 caminhos.",
    status: "accepted",
    requirementKeys: ["RF-143", "RF-144"],
    rejectedAlternatives: [
      {
        alternative: "Tratamento de erro separado por tela",
        reason: "Duplicaria a lógica e arriscaria divergência; o runner único é o ponto natural.",
      },
    ],
  },
];

export const components: IComponent[] = [
  {
    name: "SafeExecutionBoundary",
    responsibility:
      "Fronteira de execução segura do código do jogador no PlayerScriptRunner (camada Application): captura falhas de sintaxe e de runtime em play_turn, protege contra execução que não termina, expõe has_error + mensagem legível (causa/linha quando disponível) e garante no-op do turno em vez de crash. Reusada por game_controller, replay (009) e sandbox (010). O mecanismo de captura é definido na implementação (dev).",
    dependsOn: [],
    requirementKeys: ["RF-140", "RF-141", "RF-142", "RF-143", "RF-144", "RNF-140"],
  },
];
