import type { ITask } from "../types.ts";

export const tasks: ITask[] = [
  // ── FUNDAÇÕES P0 — INDEPENDENTES (dependsOn:[], parallel:true) → 1 por dev ──
  {
    key: "T-160",
    storyKey: "US-160",
    summary:
      "F2: AnimatedEntityRegistry + AnimatedSprite2D dos 4 personagens, acionados por turn_events, ancorados pelos pés.",
    definitionOfDone:
      "AnimatedEntityRegistry lê o anim/manifest.json e constrói os SpriteFrames de hero/enemy_cadet/enemy_dev/boss_director (idle/walk/attack|shoot|cast/hurt/death, 48x48, velocidades do brief; death não-loop). As entidades usam AnimatedSprite2D com mapa turn_event→animação e ancoragem bottom-center na célula de 32px; o shoot do arqueiro spawna fx_arrow no frame de release. DoD = PROVA DE RENDER (instancia game.tscn, renderiza ≥1 frame, assere AnimatedSprite2D ativo + animação correta por evento + ancoragem) + GUT; suíte 100% verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-161",
    storyKey: "US-161",
    summary: "F1: TileMapArena 32px nativo consumindo os tiles do pack, célula→tile do estado do nível.",
    definitionOfDone:
      "TileMapArena (TileMapLayer 32px, TileSet com tile_floor/tile_wall/tile_stairs — e void/corrupt quando aplicável) mapeia célula→tile a partir do estado/dimensões do nível, um personagem por célula, sem reamostrar (Nearest), escala inteira (TILE_SIZE=32, sem regredir a 64). Não altera regra. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere floor_layer com tiles REALMENTE desenhados na grade 32px) + GUT; suíte 100% verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-162",
    storyKey: "US-162",
    summary: "F3: FourStateButton (4 estados via ui_*) e migração dos controles existentes.",
    definitionOfDone:
      "Componente FourStateButton com StyleBox/textura por estado data-driven dos ui_*: normal (borda ciano) / hover (preenchido+glow) / pressed (escurecido, +1px) / disabled (cinza). Os controles existentes migram para ele. DoD = teste que assere os 4 estados refletem a interação real + PROVA DE RENDER da barra de controles; suíte 100% verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  // ── TELAS P0 — dependem das fundações; paralelizáveis entre si ──
  {
    key: "T-163",
    storyKey: "US-163",
    summary: "Tela de JOGO (CORE) fiel ao mockup: status bar + arena + console + editor retrátil.",
    definitionOfDone:
      "Cena de jogo fiel ao mockup: topo = status bar terminal (LVL/HP via ui_hp/TURN via ui_clock/SCORE via ui_gem, vol+gear); centro = arena TileMap (reusa T-161) com personagem por célula animado (reusa T-160) + overlay glitch (reusa GlitchPostProcess da 015); inferior = console de turnos + controles (reusa T-162); editor retrátil lateral (toggle </>, começa visível). Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere as 3 zonas + arena com tiles/sprites posicionados) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: ["T-160", "T-161", "T-162"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-164",
    storyKey: "US-164",
    summary: "Tela Menu inicial fiel ao mockup (boot log + key art + opções).",
    definitionOfDone:
      "Menu inicial fiel: fundo void + boot log fake (`$ ./42warrior --boot`, [WARN] corruption detected) + key_art.png + opções (Jogar/Continuar destacada ciano, Selecionar nível, Áudio, Sobre/Créditos via T-162). Tipografia Press Start 2P/JetBrains Mono via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere elementos-chave do mockup) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: ["T-162"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-165",
    storyKey: "US-165",
    summary: "Tela Seleção de níveis fiel ao mockup (grade 3×3 com estados).",
    definitionOfDone:
      "Seleção: grade 3×3 dos 9 andares com estado (ui_check concluído, ui_star ace, ui_lock bloqueado, andar atual destacado ciano, andar 9 = chefe magenta), reusando T-162. Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere a grade + estados) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: ["T-162"],
    parallel: true,
    assignee: null,
  },
  // ── TELAS P1 — secundárias; paralelizáveis ──
  {
    key: "T-166",
    storyKey: "US-166",
    summary: "Tela Resultado/Pontuação fiel ao mockup.",
    definitionOfDone:
      "Resultado: `>> RUN COMPLETE`, grade (S/A/…) grande + estrelas (ui_star), stats (SCORE/TIME BONUS/TURNS/ACE), botões PRÓXIMO/REPLAY (T-162). Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere elementos-chave) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: ["T-162"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-167",
    storyKey: "US-167",
    summary: "Tela Transição de nível fiel ao mockup (card com glitch).",
    definitionOfDone:
      "Transição: card central `/sys/memory/segment_NN`, ANDAR NN com RGB split, descrição curta, badge de nova habilidade, prompt `> ENTER` (entra/sai com glitch, reusa FX da 015). Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere elementos-chave) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-168",
    storyKey: "US-168",
    summary: "Tela Sandbox/Tutorial fiel ao mockup (grade limpa).",
    definitionOfDone:
      "Sandbox/tutorial: grade LIMPA (sem corrupção) com herói + portal (reusa T-160/T-161), tooltips passo a passo, badge MODO SANDBOX. Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere a grade limpa + tooltips) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: ["T-160", "T-161"],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-169",
    storyKey: "US-169",
    summary: "Tela Glossário fiel ao mockup.",
    definitionOfDone:
      "Glossário: lista de termos (cadete, cativo, ace, turno, andar, corrupção, daemon) + definição, fiel ao mockup. Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere a lista) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-170",
    storyKey: "US-170",
    summary: "Tela Referência da API fiel ao mockup (man-page).",
    definitionOfDone:
      "Referência da API: painel man-page com SENTIDOS (feel/look/health/listen/direction_of_stairs) e AÇÕES (walk!/attack!/rest!/rescue!/pivot!/shoot!) e direção :forward/:backward, fiel ao mockup. Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere as seções) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
  {
    key: "T-171",
    storyKey: "US-171",
    summary: "Tela Conclusão/Créditos fiel ao mockup.",
    definitionOfDone:
      "Conclusão: terminal `SYSTEM RESTORED` / `exit 0` com créditos rolando, fiel ao mockup. Tipografia via Theme. DoD = PROVA DE RENDER (renderiza ≥1 frame, assere o terminal + créditos) + suíte verde, 0 regressão.",
    status: "todo",
    dependsOn: [],
    parallel: true,
    assignee: null,
  },
];
