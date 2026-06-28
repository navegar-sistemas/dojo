import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  {
    key: "T-210",
    storyKey: "US-210",
    summary:
      "WebRendererConfig: definir em project.godot o override rendering/renderer/rendering_method.web=\"gl_compatibility\", mantendo Forward+ no desktop. Conferir que o 2D (TileMap/sprites/HUD) não depende de recursos Forward+-only.",
    definitionOfDone:
      "project.godot tem rendering_method.web=gl_compatibility; desktop permanece Forward+; o jogo renderiza no WebGL2 (verificado no smoke web do T-214).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-211",
    storyKey: "US-210",
    summary:
      "WebExportPreset: criar o preset \"Web\" no export_presets.cfg + instalar os export templates do Godot 4.7 no ambiente de build; gerar o artefato HTML5/WASM (index.html + .wasm + .pck).",
    definitionOfDone:
      "Existe o preset Web; o export produz o build HTML5/WASM que ABRE e inicia o jogo no navegador.",
    status: "done",
    dependsOn: ["T-210"],
    parallel: false,
    assignee: null,
  },
  {
    key: "T-212",
    storyKey: "US-211",
    summary:
      "AudioGestureGate: ajustar o AudioManager para iniciar/retomar o áudio no 1º gesto do usuário (autoplay-block), preservando o comportamento desktop atual.",
    definitionOfDone:
      "No web o áudio inicia após o 1º gesto (não fica mudo); no desktop o áudio segue como hoje (0 regressão).",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-213",
    storyKey: "US-211",
    summary:
      "WebPersistenceAdapter: garantir/validar que user:// (player_code_store + level_progress_store/progress_store) persiste no web (IndexedDB) entre reloads; tratar o flush assíncrono se necessário, sem alterar o desktop.",
    definitionOfDone:
      "Código do jogador e progresso gravados no web sobrevivem a reload da página (user://→IndexedDB); desktop inalterado.",
    status: "done",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-214",
    storyKey: "US-212",
    summary:
      "WebSmokeHarness: montar o smoke web — abrir o build no navegador, executar ≥1 turno do código do jogador no WASM (runtime GDScript), conferir persistência user://, validar o glitch shader (WebGL2) + perf; rodar check.sh desktop p/ 0-regressão.",
    definitionOfDone:
      "Smoke web REAL verde (sem pending): o warrior executa ≥1 turno do código do jogador no WASM + progresso salvo + glitch shader renderiza no WebGL2 com ≥30 fps alvo; check.sh desktop 100% verde, 0 regressão 001–020.",
    status: "todo",
    dependsOn: ["T-210", "T-211", "T-212", "T-213"],
    parallel: false,
    assignee: null,
  },
];
