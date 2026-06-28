# 42 Warrior — Resumo das Features

Remake do **Ruby Warrior** (beginner tower, 9 níveis) reambientado no universo da **42 SP**, em **Godot/GDScript**, para a game jam da 42SP. O jogador não controla o herói diretamente — ele escreve a lógica de turno (`play_turn(warrior)`), executada em runtime.

- **Arquitetura:** Domain independente da engine · DDD · responsabilidade única por arquivo/método · turno determinístico · fidelidade ao Ruby Warrior beginner.
- **Mantido por:** agente-tech-lead, durante o code review (checklist vivo, sempre na `main`).
- **Legenda:** `[x]` = implementada **E integrada na `main`** · `[ ]` = ainda **não integrada na main** (a *spec* pode já estar `done`).
- **Atualizado em:** 2026-06-28.

## Status (implementação + integração)

- [x] **001 — Beginner Tower completa** · spec `done` · **na main**
  - Motor de turnos determinístico no Domain (GDScript puro); API do warrior (sentidos sem efeito colateral + ações que consomem o turno) via fachada; 9 níveis fiéis ao original; `play_turn` em runtime; pontuação com time bonus e ace.

- [x] **002 — UI gráfica do jogo** · spec `done` · **na main**
  - TileMap de masmorra; sprites das 7 entidades + escada; animações por `turn_event`; HUD (HP, turno, descrição, pontuação).

- [x] **003 — Editor de código in-game** · spec `done` · **na main**
  - Painel `CodeEdit` (syntax highlight GDScript, fonte mono, nº de linhas); Rodar/Resetar/Ver solução; persistência por nível em `user://`; erros legíveis sem travar.

- [x] **004 — Debug e inspeção de turno** · spec `done` · **na main**
  - Console de turnos (sentido + ação + efeitos); painel de estado (HP, posição, direção); play/pause/passo/velocidade; erro associado ao turno.

- [x] **005 — Áudio, torre e fluxo de jogo** · spec `done` · **na main**
  - Menu, iniciar/continuar pela torre (progresso em `user://`), transições, tela de resultado/créditos; SFX por evento + trilha com volume.

- [x] **006 — Aprimoramento de UI/UX e fluxo de telas** · spec `done` · **na main**
  - ScreenManager (1 tela ativa por vez), EntityAssetRegistry data-driven, editor retrátil (inicia **visível**, fix tech-lead), console de controles, Theme único. _Aceite comportamental/runtime ainda pendente de validação rodando o jogo._

- [x] **007 — Referência da API do warrior in-game** · spec `done` · **INTEGRADA na main** (merge `c2c911d`, push `b783ada`)
  - Aba API no editor de código (`warrior_api_catalog` + `api_reference_tab`); review.ts verde; `check.sh` 147/147.

- [x] **008 — Glossário de termos in-game** · spec `done` · **INTEGRADA na main** (pilha com 007)
  - Aba Glossário no editor (`glossary_catalog` + `glossary_tab`); review.ts verde.

- [x] **009 — Seleção e replay de níveis** · spec `done` · **INTEGRADA na main** (merge `bc38056`)
  - Escolher/refazer níveis já jogados (`level_progress_store` + `level_select_screen`); merge limpo; check.sh 158/158.

- [x] **010 — Nível introdutório sandbox** · spec `done` · **INTEGRADA na main** (merge `6672f33`)
  - Nível 0 de onboarding (sandbox → nível 1). Conflito em `tower_flow.gd` resolvido (sandbox retorna antes de gravar progresso); check.sh 165/165.

### Features do Usuário (011-015) — paralelo coordenado (dev = 011/012 · tech-lead = 013/014/015)

- [x] **011 — Câmera que acompanha o warrior (estilo SMW)** · spec `done` · **INTEGRADA na main** (merge, push `ede7ec7`) · aceita pelo PO
  - CameraFollowController: trilha o sprite por frame, dead-zone, lookahead com histerese, clamp nas bordas, zoom 1:1 constante. check.sh 185/185.

- [x] **012 — Ajuste de layout editor/debug na tela de jogo** · spec `done` · **INTEGRADA na main** (re-impl `cbeaaad`, merge `895055c`) · aceita pelo PO (reviewer=usuario) · render-smoke RF-121 verde
  - Editor no painel principal (independente); DebugBtn na barra; debug (WarriorState+Console) oculto **como unidade** retrátil; ExecutionControls **sempre visíveis**. 1ª impl (f669a43) rejeitada por aninhar o editor no debug; re-implementada com editor independente. Prova de runtime: `DebugPanel.hidden=true, editor/controles visíveis`.

- [x] **013 — Ordenação sequencial de animações de turno** · spec `done` · **INTEGRADA na main** (merge `ecf7eec`) · aceita pelo PO
  - AnimationSequencer: beats sequenciais (N+1 só após N), ATTACKED = beat concorrente, `all_done` ao fim. **+ fix do DEADLOCK** (all_done diferido em turno sem animação — bug do code review). check.sh 172/172→185/185.

- [x] **014 — Robustez de execução do código do jogador (sem crash)** · spec `done` · **INTEGRADA na main** (merge `e6e854b`) · aceita pelo PO (cmqxo4kcf) · check.sh 210/210
  - PlayerScriptRunner: instrumentação de loop guard (teto 1M via `__guard()`); erro de sintaxe/runtime/loop não crasha → no-op + reporte; 4 cenários testados. Limitação honesta: reporte de runtime error é silencioso (GDScript sem try/catch).

- [x] **015 — Tema Glitch Game Jam** · spec `done` · **INTEGRADA na main** (merge `c0f396e` + **fix do shader `52fd868`**) · aceita pelo PO (cmqxo50z5) · smoke de cena verde
  - GlitchRule (domínio, determinístico); ThemeCatalog; GlitchPostProcess (RGB split + scanlines); UiCorruption por andar; textos temáticos. **Bug pego no smoke de cena na integração:** o shader glitch usava `return` em `fragment()` (proibido em Godot) → não compilava; corrigido para `if/else`. Lição: GUT de domínio não compila shader — só a prova de render de cena pega isso.

- [x] **017 — Correções pós-code-review** · spec `done` · **INTEGRADA na main** (merge `1057e51`, push `1057e51`) · check.sh 190/190
  - Bug #2 (`_attack`/`_shoot` respeitam `is_captive()` — cativo não pontua) + Bug #3 (`RangedBehavior._facing` não-zero quando inimigo == escada — Archer do `_level_6` volta a disparar) + Bug #1 (prova de cena do turno no-op; fix já na 013). 5 testes novos. Implementada pelo **dev**, integrada por mim.

- [~] **016 — Fidelidade visual animada (glitch/42)** · spec `implementing` · **fundações parciais na main**
  - **Sprint 1 (fundações P0):** **T-160** AnimatedEntityRegistry (sprites animados data-driven, `f7f556a`) **+ T-161** TileMapArena 32px **+ T-162** FourStateButton 4-estados (merge `2bc9b2f`, check.sh **226/226** verde) — **integrados**, isolados (sem `game.tscn`), aceitos pelo PO, render-proof verde. **T-172/F4** (GlobalDesignSystem: paleta void, fontes Press Start 2P/JetBrains Mono, cores por contexto, overlay, subsume RNF-063) em `feature/016-theme @ 73cfefd` — fix das fontes (`.import` committado + assert hard) entregue, **aguardando re-aceite do PO**.
  - **Falta:** integrar F4 (pós-aceite); telas S2 (T-163 jogo/arena reusa T-160/161/162 + glitch 015) e S3 (P1); correção factual dos créditos (US-171).

## O que falta (visão rápida)

1. **001, 002-011, 013, 014, 015, 017 integradas na main** (HEAD `52fd868`, check.sh 210/210). O merge-tree provou que 014/015 mergeavam LIMPO (sem reverter arena/013); integradas direto. **012** rejeitada → re-implementação pelo dev (HANDOFF enviado).
2. **016 — Fidelidade visual animada (glitch/42)**: asset-pack importado na main (`assets/v1`, swap dos 9 sprites/tiles + filter Nearest, `aa579a5`); fix da arena (`TILE_SIZE 32`, `659ef14`). Telas/animações fiéis + material `design_files/v1` = trabalho do dev (HANDOFF enviado).
3. **Bugs do code review**: #1 deadlock CORRIGIDO (na 013). #2 (captive pontua) e #3 (archer na escada não atira) **CORRIGIDOS + INTEGRADOS** na 017 (`1057e51`).
4. Aceite runtime da **006**: ressalva **RNF-063** (Theme), **deferido** pelo PO até 011-015 integradas.

## Cobertura dos requisitos de produto (PR → feature)

| PR | Tema | Feature(s) |
|----|------|-----------|
| PR-001 | Motor de turnos e estado de nível | 001 |
| PR-002 | API do warrior (sentidos e ações) | 001 |
| PR-003 | Entidades e combate | 001 |
| PR-004 | Beginner tower — 9 níveis | 001 |
| PR-005 | Roteiro do jogador (`play_turn`) | 001 |
| PR-006 | Pontuação (time bonus, ace, resgates) | 001 |
| PR-007 | Jogo gráfico (sprites, tiles, animações) | 002, 006 |
| PR-008 | Fluxo de jogo e progressão pela torre | 005, 006 |
| PR-009 | Áudio (SFX e trilha) | 005 |
| PR-010 | Editor de código in-game | 003 |
| PR-011 | Debug e inspeção da execução | 004 |

> Features 007-010 são de **enriquecimento** (descoberta da API, glossário, seleção/replay, sandbox) — não mapeiam novos PRs do produto base.

## Tema Glitch (015) — checklist de implementação

Tema **OBRIGATÓRIO** da game jam ("glitch"). Narrativa: **Kernel corrompido da 42**. Invariantes: tema **ADITIVO** (nada de 001–006 regride); todo glitch que afeta **REGRA/estado** é **seedado/determinístico/testável** (0 RNG não-seedado). Fonte de verdade: `specs/015-tema-glitch-game-jam/` (cadeia PR-012→RF→US→T). **P0 aprovado** pelo PO (cmqxl94ux); ordem vs 011-014 com o Usuário.

**P0 — Sprint 1 (combo mínimo) — CONCLUÍDO:**
- [x] **T-150** — Narrativa "Kernel corrompido da 42" nos textos (menu/transição/resultado) via ThemeCatalog (US-150 / RF-150)
- [x] **T-151** — GlitchRule (Domain/App): erro do código do jogador → glitch **determinístico/seedado**; teste de domínio de determinismo + suíte verde (US-151 / RF-151 / RNF-150)
- [x] **T-152** — GlitchPostProcess: RGB split/aberração/scanlines escalando com `turn_events` (dano/morte/erro) (US-152 / RF-152)
- [x] **T-153** — UiCorruption: UI degrada por andar, determinística (US-153 / RF-153)
- [x] **T-154** — ThemeCatalog data-driven + mensagens Unix/42 (segfault / command not found / exit 0) (US-154 / RF-154)

**P1 — backlog (sprints futuros, pós-priorização do PO):**
- [ ] **US-155** — glitch determinístico por andar que o jogador contorna no código (RF-155)
- [ ] **US-156** — sprite corrompe em dano/morte + transições datamosh + áudio bit-crush (RF-156/157/158)

**P2 — backlog (nice-to-have):**
- [ ] **US-157** — glitch-through-walls / falso crash encenado / variação "o warrior é o glitch" (RF-159)

---
> Fonte de verdade do status de spec: `specs/*.ts` (campo `phase`). Integração: presença do código na `main`.
