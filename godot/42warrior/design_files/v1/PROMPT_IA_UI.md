# PROMPT — Implementação da UI/UX do "42 WARRIOR" (Godot 4)

> Cole este prompt na IA que vai implementar a interface e as cenas no Godot.
> Os assets de design estão em: **`res://desing_files/v1/`** (extraídos do .zip do asset pack).

---

## 1. Quem você é / objetivo

Você é um(a) dev Godot 4 implementando a **UI/UX e as cenas visuais** de **42 WARRIOR**,
um remake de **Ruby Warrior** feito para a **Game Jam da École 42** (tema: **glitch**).
Todo o **design, a arte e os mockups já existem** (pasta `desing_files/v1/`). Seu trabalho é
**implementar fielmente** esse design em cenas Godot — não reinventar a estética.

O jogo é **2D top-down, grid-based**: o jogador escreve `play_turn(warrior)` e o herói executa
a lógica por turnos para limpar a torre. Já existe (ou existirá) um registro **data-driven** de
assets por entidade × ação — organize as cenas para consumir isso.

---

## 2. Conceito (mantenha o tom)

**"A Torre é um sistema da École 42 corrompido por um glitch."** Os 9 andares da torre são
segmentos de memória de um mainframe infectado. O herói é um **aluno-daemon** (um processo
com forma de aluno da 42) que sobe até a raiz `/` limpando a corrupção e resgatando processos.

Três camadas visuais sempre juntas: **dungeon top-down** + **cultura 42** (terminal/CLI, P&B,
ASCII, ícone "42") + **glitch art** (RGB split, scanlines, datamosh, vermelho-rubi).
Tom: técnico/hacker com humor de dev (`segfault`, `process rescued`, `exit 0`).

---

## 3. Design system (siga à risca)

### Paleta
| Uso | Hex |
|---|---|
| Void / fundo | `#0A0A0B` |
| Painel grafite | `#15161A` · `#22242B` |
| Texto / branco | `#F2F2F2` |
| Cinza linha | `#8A8F98` |
| Ciano (glitch / ativo) | `#00F0FF` |
| Magenta (glitch) | `#FF2BD6` |
| Verde-fósforo (sucesso/terminal) | `#00FF66` |
| Vermelho-rubi (perigo / RGB split) | `#FF003C` |

**Regra de ouro:** cenário e UI vivem em **P&B / grafite**; cor neon entra **só** em
feedback, glitch, HP e estados ativos. Não "colorir por colorir".

### Tipografia
- **Press Start 2P** → títulos, logo, números grandes (HUD).
- **JetBrains Mono** (ou IBM Plex Mono / Fira Code) → UI, código, HUD, logs.
- Detalhes: cursor `▌` piscando, prompts `$` / `>`, caixas estilo terminal `┌─ ─┐`.

### Princípios
Pixel-art nítida (**nearest-neighbor, sem anti-alias**) · legibilidade da grade acima de tudo ·
glitch como tempero (nunca atrapalha a jogabilidade) · coerência entre todos os assets.

---

## 4. Import no Godot (obrigatório)

Para **todo** PNG: Import → **Filter: OFF**, **Mipmaps: OFF** (preset "2D Pixel").
Escale por **inteiros** (2x / 3x). Personagens são **48×48** (ocupam ~1,5 tile); **ancore pelos pés**
(centralizado embaixo) ao colocar na grade de 32px. Tiles **32×32**, ícones **16×16**.

---

## 5. Inventário de assets (`desing_files/v1/`)

### Personagens 48×48 (frame idle estático na raiz; animações em `anim/`)
- `hero.png` — **herói**, aluno da 42 (óculos, camiseta roxa, flail de mouse-USB, escudo-teclado). Único "limpo".
- `enemy_cadet.png` — **cadete corrompida** = **1º inimigo** (olho-ciber VERDE, vest tática).
- `enemy_dev.png` — **o ARQUEIRO** (aluno real, olho-ciber CIANO, jaqueta + lanyard, arco recurvo + flecha).
- `boss_director.png` — **a diretora** = **CHEFE FINAL** (olho-ciber MAGENTA, camiseta listrada P&B).
- `captive.png` — **cativo** a resgatar: aluno enjaulado atrás de barras de energia + chaves `{ }`, com SOS.

### Inimigos abstratos 32×32 (entidades alternativas / corrupção pura)
- `enemy_sludge.png` (bug data-blob) · `enemy_sludge_thick.png` (memory leak) ·
  `enemy_archer.png` (sentinela firewall — variante) · `enemy_wizard.png` (kernel daemon).

### Tiles 32×32
- `tile_floor.png` (chão placa-mãe) · `tile_floor_corrupt.png` (variante glitch/pixel-sort) ·
  `tile_wall.png` (rack de RAM) · `tile_stairs.png` (portal de diretório / próximo andar) ·
  `tile_door.png` · `tile_void.png` (fundo, scanlines + data rain).

### UI / HUD 16×16
`ui_hp` `ui_sword`(ataque) `ui_bow`(tiro) `ui_shield`(defesa/pivot) `ui_key`(resgate)
`ui_code`(`</>`) `ui_api`(`{ }`) `ui_book`(glossário) `ui_gear`(settings)
`ui_play` `ui_pause` `ui_step` `ui_speed` `ui_clock`(turno) `ui_vol_on` `ui_vol_off`
`ui_check`(✓) `ui_star`(★ ace) `ui_lock`(🔒) `ui_gem` `ui_skull`(perigo).

### Key art & FX
- `key_art.png` (120×56) — lockup "42 WARRIOR" com RGB split (use no menu/título).
- `logo_42.png` (44×26) — marca "42".
- `fx_glitch_overlay.png` (64×64, **tileável**) — overlay de scanlines+ruído. Use num `CanvasLayer`
  por cima da tela, `material` com blend **Add/Screen**, textura em **tile**, opacidade ~0.2–0.4,
  leve drift/flicker animado.
- `fx_hero_glitch_1..4.png` (48×48) — frames de glitch do herói (efeito hurt / idle corrompido).
- `fx_arrow.png` (24×8) — **flecha projétil** para a animação de tiro do arqueiro.

---

## 6. Animações (`desing_files/v1/anim/`)

Cada arquivo é um **sprite sheet horizontal** (frames lado a lado, **48×48** cada).
Veja `anim/manifest.json` (`{name, anim, frames, fw:48, fh:48}`).

| Personagem | Animações (nº de frames) |
|---|---|
| `hero` | idle(4) · walk(6) · attack(5) · hurt(4) · death(6) |
| `enemy_cadet` | idle(4) · walk(6) · cast(5) · hurt(4) · death(6) |
| `enemy_dev` (arqueiro) | idle(4) · walk(6) · **shoot(5)** · hurt(4) · death(6) |
| `boss_director` | idle(4) · cast(5) · hurt(4) · death(6) |

Arquivo: `anim/<personagem>_<anim>.png`.

**Setup Godot:** use `AnimatedSprite2D` + `SpriteFrames`, ou `Sprite2D` com `hframes = nº de frames`.
Para cada sheet: `hframes = frames`, `vframes = 1`; crie a animação com os N frames na ordem.
Velocidades sugeridas: idle ~5 fps · walk ~8 fps · hurt/shoot/cast ~10 fps · death ~8 fps (não loop).
A animação **shoot** do arqueiro mostra a flecha saindo; sincronize o spawn de um `fx_arrow.png`
como projétil (Area2D) no frame de release (frame 3).

Disparo dos estados via `turn_event` do jogo (idle quando parado, walk ao andar, attack/shoot/cast
ao agir, hurt ao tomar dano, death ao morrer).

---

## 7. As 9 telas (mockups de referência)

Os layouts visuais de cada tela estão no catálogo HTML do asset pack (seção **TELAS**).
Implemente cada uma como cena Godot (`Control` + `CanvasLayer` para HUD/overlay). Resolução base
de design **1920×1080** (16:9 escalável; use `canvas_items` stretch). Toda tela tem overlay global
de scanlines sutil (`fx_glitch_overlay`).

1. **Menu inicial** — fundo void + boot log fake (`$ ./42warrior --boot`, linhas subindo, `[WARN]
   corruption detected`) + `key_art.png` + opções: **▶ Jogar/Continuar** (destacada ciano),
   **≡ Selecionar nível**, **⚙ Áudio**, **ⓘ Sobre/Créditos**.
2. **Tela de jogo (CORE)** — a mais importante. Três zonas:
   - **Topo (status bar terminal):** `LVL 03/09` · `HP` (corações `ui_hp`, último apagado) ·
     `TURN 07` (`ui_clock`) · `SCORE 1240` (`ui_gem`) · à direita `ui_vol_on` + `ui_gear`.
   - **Centro:** a **arena em grade** (TileMap), **um personagem por bloco** — herói, inimigos,
     cativo, portal, cada um numa célula. Glitch overlay por cima.
   - **Inferior:** **console de turnos** (log estilo terminal: `> turn 6 · feel: enemy ahead →
     attack! (-3)`) + controles `ui_step` `ui_play` `ui_pause` `ui_speed`.
   - **Editor de código retrátil** na lateral (desliza com botão `</>`): syntax highlight de
     GDScript, nº de linha, botões **▶ Rodar · ↺ Resetar · 👁 Solução**. Começa visível.
3. **Transição de nível** — card central: `/sys/memory/segment_03`, **ANDAR 03** (com RGB split),
   descrição curta, badge **⊕ NOVA HABILIDADE · attack!**, prompt `> ENTER`. Entra/sai com glitch.
4. **Resultado / pontuação** — `>> RUN COMPLETE`, **grade S** grande + estrelas (`ui_star`),
   stats (SCORE / TIME BONUS / TURNS / ACE), botões **PRÓXIMO** / **↺ REPLAY**.
5. **Conclusão + créditos** — terminal: `SYSTEM RESTORED`, `exit 0`, créditos rolando.
6. **Seleção de níveis** — grade 3×3 dos 9 andares com estado: ✓ concluído (`ui_check`),
   ★ ace (`ui_star`), 🔒 bloqueado (`ui_lock`), andar atual destacado ciano, andar 9 = CHEFE (magenta).
7. **Referência da API** — painel man-page: **SENTIDOS** (`feel`, `look`, `health`, `listen`,
   `direction_of_stairs`) e **AÇÕES** (`walk!`, `attack!`, `rest!`, `rescue!`, `pivot!`, `shoot!`),
   com direção `:forward` / `:backward`.
8. **Glossário** — lista de termos (cadete, cativo, ace, turno, andar, corrupção, daemon) + definição.
9. **Sandbox / tutorial** — nível de onboarding, **grade limpa (sem corrupção)**, herói + portal,
   tooltips passo a passo (`↳ digite warrior.walk! →`). Badge **MODO SANDBOX**.

---

## 8. Componentes & feedback

- **Botões** em 4 estados: normal (borda ciano) · hover (preenchido ciano + glow) · pressed
  (escurecido, +1px) · disabled (cinza). Hover com micro-glitch na borda.
- **Painéis/janelas:** moldura de terminal com title bar (3 dots vermelho/amarelo/verde + nome do
  arquivo), 9-slice nos cantos.
- **Transições de tela:** RGB split + datamosh + estática rápida.
- **Combate:** ataque = impacto neon + leve chromatic aberration; dano = flash branco + glitch no
  sprite + screen-shake mínimo; morte = dissolução em pixel-sort/static (já refletido nos sheets
  `*_death`). Cura/resgate = partículas verdes / abertura de `{ }`.
- **Ambiente:** flicker ocasional de tiles, data rain no fundo, glitch idle no logo.

---

## 9. Convenções de nomes (data-driven)
`hero` · `enemy_<nome>` · `boss_<nome>` · `tile_<nome>` · `ui_<nome>` · `fx_<nome>`
Animações: `anim/<entidade>_<acao>.png`. Telas: `screen_<nome>` nas cenas.

### Roster sugerido
1º inimigo → `enemy_cadet` · meio → `enemy_dev` (arqueiro), `enemy_sludge`, `enemy_archer`,
`enemy_wizard` · chefe (andar 9) → `boss_director` · aliado a resgatar → `captive`.

---

## 10. O que entregar
1. Cena de cada uma das 9 telas (escaláveis 16:9), fiéis aos mockups.
2. HUD reutilizável (status bar + console + controles) como cena/Control.
3. `AnimatedSprite2D`/`SpriteFrames` montados para hero + 3 personagens (todas as animações do manifest).
4. TileMap da arena (32px) consumindo `tile_*`, com um personagem por célula.
5. `CanvasLayer` de glitch global (`fx_glitch_overlay`, blend Add/Screen).
6. Sistema de botões com os 4 estados.

**Não** altere a paleta, a tipografia nem a identidade. Em dúvida, siga os mockups e o `README.md`
da pasta `desing_files/v1/`.
