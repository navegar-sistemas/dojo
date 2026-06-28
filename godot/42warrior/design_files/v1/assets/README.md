# 42 WARRIOR — Asset Pack (Fases 1–3)

Remake glitch de **Ruby Warrior** para a Game Jam da **École 42**.
Pixel art, PNG transparente, resolução nativa (use **Nearest** / sem filtro no Godot 4).

## Conceito
"A Torre é um sistema da 42 corrompido por um glitch." O herói é um **aluno-daemon**
(de óculos, com um flail de mouse-USB e um escudo-teclado) que o jogador programa
(`play_turn`) para limpar a corrupção, resgatar processos presos e subir até a raiz `/`.
Inimigos e chefe são inspirados em **pessoas reais da 42** (com permissão).

## Paleta
| Uso | Hex |
|---|---|
| Void / fundo | `#0A0A0B` |
| Painel grafite | `#15161A`, `#22242B` |
| Texto / branco | `#F2F2F2` |
| Cinza linha | `#8A8F98` |
| Ciano (glitch) | `#00F0FF` |
| Magenta (glitch) | `#FF2BD6` |
| Verde-fósforo (sucesso) | `#00FF66` |
| Vermelho-rubi (perigo / RGB split) | `#FF003C` |

## Tipografia
- Títulos / logo: **Press Start 2P** · UI / código / HUD: **JetBrains Mono**

---

## FASE 1 — Sprites base

### Personagens (PNG estático, frame idle)
- `hero.png` (48×48) — **o aluno 42** (óculos, camiseta roxa, flail mouse-USB, escudo-teclado). Único "limpo".
- `enemy_cadet.png` (48×48) — **cadete corrompida** (1º inimigo) · olho-ciber VERDE, vest tática.
- `enemy_dev.png` (48×48) — **o ARQUEIRO** (aluno real, foto) · olho-ciber CIANO, jaqueta + lanyard, arco recurvo + flecha.
- `boss_director.png` (48×48) — **a diretora** (CHEFE FINAL) · olho-ciber MAGENTA, camiseta listrada.
- `enemy_sludge.png` / `enemy_sludge_thick.png` (32×32) — bug data-blob / memory leak.
- `enemy_archer.png` (32×32) — sentinela de firewall (variante abstrata). `enemy_wizard.png` (32×32) — kernel daemon.
- `captive.png` (48×48) — **cativo enjaulado** (aluno 42 atrás de barras de energia + `{ }`, SOS).

### Cenário (tiles 32×32)
`tile_floor` · `tile_floor_corrupt` (pixel-sort) · `tile_wall` (rack RAM) ·
`tile_stairs` (portal de diretório) · `tile_door` · `tile_void` (data rain).

### UI / HUD (16×16)
`ui_hp` `ui_sword` `ui_bow` `ui_shield` `ui_key` `ui_code` `ui_api` `ui_book` `ui_gear`
`ui_play` `ui_pause` `ui_step` `ui_speed` `ui_clock` `ui_vol_on` `ui_vol_off`
`ui_check` `ui_star` `ui_lock` `ui_gem` `ui_skull`.

### Key art & FX
`key_art.png` (120×56) · `logo_42.png` (44×26) · `fx_glitch_overlay.png` (64×64, tileável) ·
`fx_hero_glitch_1..4.png` (48×48) · `fx_arrow.png` (24×8) — flecha projétil pra animação de tiro do arqueiro.

---

## FASE 2 — Animações (`assets/anim/`)

Sprite sheets **horizontais** (frames lado a lado, 48×48 cada). `manifest.json` lista tudo.

| Personagem | Animações (nº de frames) |
|---|---|
| hero | idle(4) walk(6) attack(5) hurt(4) death(6) |
| enemy_cadet | idle(4) walk(6) cast(5) hurt(4) death(6) |
| enemy_dev (arqueiro) | idle(4) walk(6) shoot(5) hurt(4) death(6) |
| boss_director | idle(4) cast(5) hurt(4) death(6) |

Arquivo: `assets/anim/<personagem>_<anim>.png`.

**Godot:** `AnimatedSprite2D` / `SpriteFrames`. Para um sheet, `hframes = nº de frames`,
`vframes = 1`; crie uma animação com os N frames. Velocidade sugerida ~6–8 fps
(idle mais lento, hurt/cast mais rápido).

---

## FASE 3 — Telas de UI (mockups)

9 mockups de referência no catálogo (`RubyWarrior 42 - Asset Pack.dc.html`), seção **TELAS**:
1. Menu inicial (boot + logo + opções) · 2. Tela de jogo CORE (status bar + arena + editor + console) ·
3. Transição de nível · 4. Resultado/pontuação (grade S, ace) · 5. Conclusão + créditos ·
6. Seleção dos 9 andares (✓/★/🔒) · 7. Referência da API · 8. Glossário · 9. Sandbox/tutorial.

Os mockups são HTML/CSS (layout 1280×720, 16:9) usando os assets reais — referência visual
para implementar as cenas no Godot.

---

## Integração Godot 4
- Import de cada PNG: Texture → **Filter OFF**, **Mipmaps OFF**. Escale por inteiros (2x/3x).
- Personagens 48×48 ocupam ~1.5 tile (tiles 32×32) — normal; ancore pelos pés.
- Overlay glitch: `CanvasLayer` + blend **Add/Screen**, textura `fx_glitch_overlay.png` em tile 64px.
- Convenção: `hero` · `enemy_*` · `boss_*` · `tile_*` · `ui_*` · `assets/anim/<ent>_<anim>.png`.

## Roster sugerido (data-driven)
- 1º inimigo: `enemy_cadet` · meio: `enemy_dev`, `enemy_sludge`, `enemy_archer`, `enemy_wizard` ·
  chefe (andar 9): `boss_director` · aliado a resgatar: `captive`.
