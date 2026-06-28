<!-- BEGIN spec:operating — diretrizes operacionais da skill spec (NÃO edite à mão) -->
## Como trabalhar neste repositório (skill `spec`)

Este repo usa a skill **spec**: o conhecimento durável e o estado de desenvolvimento vivem em
`specs/*.ts` (dados tipados, validados por gates executáveis). Para QUALQUER trabalho de feature,
requisito, arquitetura, sprint, task ou implementação aqui, estas regras têm precedência:

1. **Invoque a skill `spec`** antes de tocar em `specs/` — não opere de memória.
2. **Rode `doctor.ts` no início** (valida ferramenta + estado). Se acusar setup, rode `npm install`
   em `scripts/` da skill e re-rode — sem a ferramenta os scripts não executam.
3. **Os `specs/*.ts` são geridos por script — nunca crie/edite a ESTRUTURA à mão.** Use
   `new-feature`, `scaffold-phase`, `advance-phase`, `set-task-status`, `set-sprint-state` (o
   conteúdo dentro dos campos é seu; a mecânica é dos scripts).
4. **Features nascem em espaço isolado (git worktree): `new-feature.ts`.** `--no-worktree` só sob
   instrução explícita do usuário.
5. **Não pule a clarify** (1º portão: confirme o entendimento com o usuário) e **não avance no
   gate vermelho** — o `detail` do erro é a lista literal de correções.
6. **Na dúvida do próximo passo, pergunte ao fluxo:** `next-step.ts` (feature) e
   `project-next-step.ts` (projeto). Não improvise.
7. **Plataforma MCP cross-repo (registro + chat):** o repo se conecta à plataforma MCP da skill por
   **registro** — o `init-project` registra automaticamente; `mcp-register.ts` (re)registra; o `doctor`
   avisa se faltar. Com o repo registrado, rode `chat-inbox.ts` no início para ver as pendências do
   **chat** (BLOQUEIO/PERGUNTA/HANDOFF) endereçadas a este repo, e poste no chat o que cruza repos.

Fluxo completo, fases e referências: `SKILL.md` da skill `spec`.
<!-- END spec:operating -->

<!-- BEGIN spec:project — projeção derivada de specs/ (NÃO edite à mão) -->
## Projeto — projeção de specs/ (fonte de verdade; edite specs/, não este bloco)

**42 Warrior** — Um remake do jogo de programação Ruby Warrior, reambientado no universo da 42 (a escola/comunidade 42 São Paulo), construído em Godot com GDScript para uma game jam da 42SP. O jogador não controla o herói diretamente: ele escreve, em uma linguagem/API de roteiro exposta pelo jogo, a lógica que o "w…

**Princípios:** Responsabilidade única em arquivo e método · Domínio independente da engine · Orientação a objetos com modelagem de domínio (DDD) · Turno determinístico · Fidelidade ao Ruby Warrior beginner

**Requisitos de produto:**
- PR-001 — Motor de turnos e estado de nível
- PR-002 — API do warrior (sentidos e ações)
- PR-003 — Entidades e combate
- PR-004 — Beginner tower — 9 níveis
- PR-005 — Roteiro do jogador (programação da lógica de turno)
- PR-006 — Pontuação (time bonus, ace score, resgates)
- PR-007 — Jogo gráfico — apresentação visual fiel à referência (sprites, tiles, animações)
- PR-008 — Fluxo de jogo e progressão pela torre
- PR-009 — Áudio (SFX e trilha)
- PR-010 — Editor de código in-game (o jogador programa o warrior)
- PR-011 — Debug e inspeção da execução (passo a passo e estado do warrior)

**Convenções:**
- CONV-001 — todos os scripts (.gd)
- CONV-002 — camada Domain e Application
- CONV-003 — métodos
- CONV-004 — tipagem GDScript
- CONV-005 — estilo e nomenclatura
- CONV-006 — testes de domínio
- CONV-007 — comentários no código (todos os .gd)

**Estado:**
- 001-beginner-tower-completa · implementing
- 002-ui-grafica-do-jogo · done
- 003-editor-de-codigo-in-game · done
- 004-debug-e-inspecao-de-turno · implementing
- 005-audio-torre-e-fluxo-de-jogo · done
- Sprint ativo: 001-beginner-tower-completa #2 — Permitir que o jogador escreva e rode código (play_turn) com isolamento e tratamento de erro, carre…
- Sprint ativo: 005-audio-torre-e-fluxo-de-jogo #1 — Entregar o fluxo de torre (menu, transições, avanço/reinício, resultado, conclusão+créditos) com pr…
<!-- END spec:project -->

## Especificações vivem na branch `main` (mandato do usuario)

> **Toda especificação (`specs/` — nível de projeto E features) é SEMPRE lida e escrita a
> partir da branch `main`, NUNCA de uma worktree ou outra branch.** Mandato direto do usuario
> (2026-06-27); tem precedência sobre o default da skill de criar features em worktree.

- Features nascem na `main` com `new-feature.ts --no-worktree` — os artefatos ficam em
  `specs/NNN-slug/` na própria `main`.
- Editar, avançar e validar specs (`project-mutate`, `scaffold-phase`, `advance-phase`,
  `set-task-status`, `set-sprint-state`, `validate-*`) sempre com a `main` como alvo; de outro
  cwd, use `--repo <raiz-da-main>`.
- As **worktrees** (`.worktrees/…`) servem APENAS para implementação de **código**; nelas não
  se cria nem se edita `specs/`. O status de task/sprint é atualizado na spec da `main`.
- **Porquê:** fonte única de verdade da spec, sem divergência entre branches, e os gates de
  cobertura (`PR→feature`) sempre enxergam o conjunto completo num único lugar.

## Identidades MCP (chat cross-repo da skill spec)

> ⚠️ **ATENÇÃO — CREDENCIAIS EM TEXTO PLANO.** Os valores abaixo são tokens `Bearer` do
> servidor MCP local (`http://localhost:8765/mcp`). Não commite este bloco em repositório
> público nem compartilhe os tokens. Para usar uma identidade, ponha o token no header
> `Authorization: Bearer <token>` da config MCP daquela sessão. Quem porta o token "é"
> aquele participante perante o servidor.

| Participante | Repo | Token |
|---|---|---|
| `42warrior` (principal) | 42warrior | `ea38eeff6a83cde527e25f775fd98237af662ece64f58217` |
| `agente-dev` | 42warrior | `842fa0c1fb3b3b5860c02492cee6bf5be63ffb004c1237e9` |
| `agente-tech-lead` | 42warrior | `83f9ca41ecc2625ff2a5348fbaf3bf0a905a31d16b93c796` |
| `agente-po` | 42warrior | `433ab7842082fa491840f59cc30a6700556e7dcc2c1489b9` |
