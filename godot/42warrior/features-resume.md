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

- [ ] **007 — Referência da API do warrior in-game** · spec `done` · **código em branch `feature/007` (NÃO integrado)** · prioridade #1 do PO
  - Aba/painel de API no editor (`warrior_api_catalog` + `api_reference_tab`) p/ o jogador descobrir sentidos/ações disponíveis. Falta: concluir tasks + review + **integrar na main**.

- [ ] **008 — Glossário de termos in-game** · spec `done` · **código não iniciado**
  - Glossário dos termos do jogo. Aguardando implementação (após 007).

- [ ] **009 — Seleção e replay de níveis** · spec `done` · **código em branch `feature/009` (NÃO integrado)**
  - Escolher/refazer níveis já jogados. Falta: review + **integrar na main** (na vez, após 007/008).

- [ ] **010 — Nível introdutório sandbox** · spec `done` · **código não iniciado** · **bloqueado por prioridade do PO** (só após 007→008→009)
  - Nível de onboarding/sandbox (menor valor). Implementa por último.

## O que falta (visão rápida)

1. Implementar/integrar **007 → 008 → 009 → 010** nesta ordem (definida pelo PO). Specs prontas; falta **código na main** (007/009 já em branch; 008/010 não iniciados).
2. Cada feature: review da feature → merge na main → push.
3. Fechar o **aceite runtime da 006** (rodar o jogo: 1 tela após transição, sem vazamento de nós, animações, console).

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

---
> Fonte de verdade do status de spec: `specs/*.ts` (campo `phase`). Integração: presença do código na `main`.
