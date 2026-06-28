# 42 Warrior — Resumo das Features

Remake do **Ruby Warrior** (beginner tower, 9 níveis) reambientado no universo da **42 SP**, em **Godot/GDScript**, para a game jam da 42SP. O jogador não controla o herói diretamente — ele escreve a lógica de turno (`play_turn(warrior)`), executada em runtime.

- **Arquitetura:** Domain independente da engine · DDD · responsabilidade única por arquivo/método · turno determinístico · fidelidade ao Ruby Warrior beginner.
- **Fonte de verdade:** `specs/` (campo `phase` de cada `feature.ts`).
- **Legenda:** `[x]` concluída (`phase: done`) · `[ ]` em andamento.
- **Atualizado em:** 2026-06-28.

## Features

- [ ] **001 — Beginner Tower completa** · `implementing` · PR-001..009
  - Motor de turnos determinístico no Domain (GDScript puro, sem engine); API do warrior (sentidos sem efeito colateral + ações que consomem o turno) via fachada; entidades, combate, saúde e resgate.
  - 9 níveis fiéis ao gem original `ryanb/ruby-warrior`; execução do código do jogador (`play_turn`) em runtime contra a fachada; pontuação com time bonus e ace score.

- [x] **002 — UI gráfica do jogo** · `done` · PR-007
  - TileMap de masmorra de pedra dimensionado pelo nível; sprites de warrior, sludge, thick sludge, archer, wizard, cativo e escada; animações por `turn_event`; HUD legível (HP, turno, descrição, pontuação).
  - Asset pack pixel-art CC0 com pontos de troca documentados para a arte final da 42.

- [x] **003 — Editor de código in-game** · `done` · PR-010
  - Painel `CodeEdit` com syntax highlight de GDScript, fonte monoespaçada e numeração de linhas; botões Rodar / Resetar / Ver solução de referência.
  - Persistência do código do jogador por nível em `user://`; erros de compilação/runtime legíveis sem travar o jogo; esqueleto inicial por nível com as habilidades disponíveis.

- [ ] **004 — Debug e inspeção de turno** · `implementing` · PR-011
  - Console de turnos (o que o warrior sentiu + ação tomada + efeitos) a partir dos `turn_events`; painel de estado corrente (HP, posição, direção, estado do nível).
  - Controles de execução play / pause / passo-a-passo / velocidade; mensagens de erro associadas ao turno em que ocorreram.

- [x] **005 — Áudio, torre e fluxo de jogo** · `done` · PR-008, PR-009
  - Menu inicial; iniciar/continuar a torre conforme progresso salvo em `user://`; transições entre níveis; tela de resultado/pontuação e créditos ao concluir a torre.
  - SFX por evento de turno + trilha de fundo com controle de volume básico; assets de áudio CC0 com pontos de troca.

- [ ] **006 — Aprimoramento de UI/UX e fluxo de telas** · `implementing` · PR-007, PR-008
  - Corrige a sobreposição de telas (gerenciador de navegação: uma tela ativa por vez); layout "arena em destaque" com editor de código retrátil e console de turnos com controles.
  - Identidade visual coesa (inspirada no Ruby Warrior, com cara da 42); animações de feedback por ação; registro de assets/animações data-driven com pontos de troca.

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

---
> Status conforme o estado do projeto em `specs/` (projeção no `CLAUDE.md`).
