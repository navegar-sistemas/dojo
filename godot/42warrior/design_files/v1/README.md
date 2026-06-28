# 42 WARRIOR — Design Files v1

Pacote completo de design/arte do remake de **Ruby Warrior** (École 42 Game Jam · tema glitch).
Coloque esta pasta em `res://desing_files/v1/` no projeto Godot.

## Estrutura

```
42warrior_design_v1/
├── assets/                         # todos os sprites/tiles/UI (PNG nativo, transparente)
│   ├── hero.png, enemy_*.png, boss_director.png, captive.png   # personagens 48×48 / 32×32
│   ├── tile_*.png                  # cenário 32×32
│   ├── ui_*.png                    # ícones HUD 16×16
│   ├── key_art.png, logo_42.png, fx_*.png                      # key art + efeitos
│   ├── anim/                       # sprite sheets de animação + manifest.json
│   └── README.md                   # detalhamento dos assets + dicas Godot
├── fonts/                          # fontes (OFL) prontas pra importar no Godot
│   ├── PressStart2P-Regular.ttf    # títulos / logo
│   ├── JetBrainsMono-Regular.ttf   # UI / código / HUD
│   ├── JetBrainsMono-Medium.ttf
│   ├── JetBrainsMono-Bold.ttf
│   └── *-OFL.txt                   # licenças
├── RubyWarrior 42 - Asset Pack.dc.html   # MOCKUPS das 9 telas + catálogo visual (abra no navegador)
├── support.js                      # runtime do mockup (precisa estar ao lado do .html)
├── PROMPT_IA_UI.md                 # prompt pronto pra IA implementar a UI/UX
└── README.md                       # este arquivo
```

## Como ver os mockups das 9 telas
Abra **`RubyWarrior 42 - Asset Pack.dc.html`** no navegador (duplo-clique). Ele mostra:
catálogo de todos os assets, **animações tocando**, folha de estilo (paleta + tipografia +
estados de botão) e os **mockups das 9 telas de UI** (seção TELAS). Mantenha `support.js` e a
pasta `assets/` ao lado do `.html`. *(As fontes carregam via internet; offline elas caem pra
um monospace padrão — a disposição continua igual. Pra usar as fontes locais, aponte pros .ttf
em `fonts/`.)*

## Fontes
- **Press Start 2P** (OFL) — títulos, logo, números grandes do HUD.
- **JetBrains Mono** (OFL) — UI, código, HUD, logs. Pesos Regular/Medium/Bold inclusos.

No Godot 4: importe os `.ttf` como `FontFile` (já vêm com import 2D adequado). Licenças OFL em `fonts/`.

## Próximo passo
Passe o **`PROMPT_IA_UI.md`** (+ esta pasta) pra IA que vai implementar a interface no Godot.
Ele explica conceito, design system, inventário de assets, animações, as 9 telas e a integração.
