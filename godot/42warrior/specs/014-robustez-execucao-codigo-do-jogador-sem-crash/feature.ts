import type { IFeature } from "../types.ts";

export const feature: IFeature = {
  key: "014-robustez-execucao-codigo-do-jogador-sem-crash",
  name: "Robustez execucao codigo do jogador sem crash",
  problem:
    "Código do jogador com erro pode CRASHAR o jogo em vez de exibir um erro e seguir jogável. Verificado na fonte: o caminho de COMPILAÇÃO já é guardado (player_script_runner.gd: compile() faz GDScript.reload() e, se != OK, seta _error e não instancia; game_controller mostra via _editor.show_compile_error(); test_erro_de_compilacao_nao_trava passa) — erros de sintaxe básicos já são tratados. LACUNA 1 (provável causa do crash): play_turn(instance, facade) faz instance.call(\"play_turn\", facade) SEM proteção; código que COMPILA mas quebra em RUNTIME (método inexistente, acesso a null, tipo errado, recursão/loop infinito, assert) não é capturado. LACUNA 2: a mensagem é genérica (\"Erro de compilação...\"), sem linha/causa.",
  productRequirementKeys: ["PR-010"],
  goals: [
    "Nenhum código do jogador — com erro de SINTAXE ou de RUNTIME — pode crashar/travar o jogo: ele continua responsivo e o jogador pode editar e rodar de novo.",
    "O erro é exibido de forma legível na ErrorView já existente (idealmente com causa/linha quando a engine fornecer), tanto para falha de compilação quanto para falha em runtime durante play_turn.",
    "Vale para todo caminho que roda código do jogador: a tela de jogo (game_controller), a seleção/replay (009) e o sandbox (010).",
  ],
  outOfScope: [
    "Mudar a API ou o motor de turnos.",
    "Transformar GDScript em linguagem com exceções (não tem try/catch — o mecanismo correto é investigação do dev; o spec não o prescreve).",
    "Validar semanticamente a lógica do jogador (só impedir crash e reportar).",
    "Reescrever o editor (003) — só endurecer a execução e o reporte.",
  ],
  productDecisions: [],
  phase: "done",
  createdAt: "2026-06-28",
};
