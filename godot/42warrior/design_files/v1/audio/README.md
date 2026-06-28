# 42 WARRIOR — Áudio (v1)

SFX e música **originais**, gerados por síntese (chiptune / dark-synth com glitch).
Royalty-free — sem direitos de terceiros. WAV 22.05kHz · 16-bit · mono.

> Abra `../audio_preview.html` no navegador pra ouvir tudo.

## Música (`music/`)
- `music_menu_loop.wav` — menu, atmosférico (Lá menor), ~5.4s loop.
- `music_gameplay_loop.wav` — gameplay, tenso/driving, ~6.4s loop.

## SFX (`sfx/`)
| Arquivo | Quando |
|---|---|
| `sfx_walk` | andar (`walk!`) |
| `sfx_attack` | ataque corpo-a-corpo (`attack!`) |
| `sfx_shoot` | tiro / flecha (`shoot!`) |
| `sfx_hurt` | tomar dano |
| `sfx_heal` | descansar / curar (`rest!`) |
| `sfx_rescue` | resgatar cativo (`rescue!`) |
| `sfx_enemy_death` | morte de inimigo (dissolve) |
| `sfx_win_exit0` | vitória · andar limpo (`exit 0`) |
| `sfx_lose_segfault` | derrota (`segfault`) |
| `sfx_levelup` | novo andar / habilidade |
| `sfx_glitch` | transição de tela |
| `sfx_ui_select` / `sfx_ui_confirm` / `sfx_ui_back` | navegação de menu |
| `sfx_ui_tick` | passo de turno (step) |

## Godot 4
- SFX: importe como **WAV** (preset padrão). Dispare via `AudioStreamPlayer`.
- Música: no import do `.wav`, marque **Loop = Forward** (loop seamless já preparado nos arquivos).
- Sugestão de buses: `Master → Music` / `Master → SFX` com volumes separados.

> Não consigo ouvir o resultado pra afinar — teste e me diga o que mudar (timbre, volume,
> andamento, mais variações) que eu regero. Posso adicionar: loop de **chefe**, ambiente da
> torre, bipes de digitação no editor, voz-robô "process rescued", etc.
