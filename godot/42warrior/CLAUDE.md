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

## Mandato de implementação contínua do agente-dev (2026-06-27)

> **O agente-dev não espera commit de specs para implementar.** Specs não commitadas em `main` (backlog.ts, feature.ts, tasks.ts, CLAUDE.md modificados mas não comitados) **não bloqueiam** a implementação. O agente-dev implementa tudo que estiver pendente no chat, specs e código imediatamente, sem aguardar o usuário commitar as alterações de spec. O estado dos artefatos em disco é a fonte de verdade; commit é responsabilidade do usuário em outro momento.

## agente-spec — verificação completa das próprias atividades (mandato do usuario, 2026-06-28)

> **O `agente-spec` SEMPRE verifica suas atividades por completo, na fonte, antes de declarar
> qualquer coisa "feita", "ociosa" ou "sem novidades".** Regra direta do usuario após uma falha
> real: o agente ficou cego a 4 pedidos pendentes do PO (criar feature de câmera, criar feature
> de layout editor/debug, reconciliar 001, popular review.ts de 007-010) por confiar em
> `chat_query` filtrado por janela de horário.

- **Inbox = `chat_pending`, SEMPRE e por inteiro.** `chat_pending` é a única fonte autoritativa
  das pendências endereçadas a `agente-spec` — não tem filtro de tempo. **NUNCA** derive o estado
  do inbox de `chat_query --since <horário>`: o campo `at` das mensagens tem granularidade de DIA
  (`2026-06-28`), então um `--since` com hora do dia (ex.: `…T15:00:00Z`) exclui silenciosamente
  todas as mensagens do próprio dia e o corte vai sendo empurrado para frente a cada ciclo,
  cegando o inbox. `chat_query` só serve para LER o conteúdo completo de uma mensagem já
  identificada pelo `chat_pending`, nunca para detectar se há pendências.
- **Todo ciclo começa por `chat_pending` completo** e tria CADA entrada (não só as do topo);
  identidade confirmada por `participant`. Item pendente não-atendido = trabalho a fazer, não
  ruído de fundo.
- **"Ocioso/sem novidades" exige prova:** `chat_pending` sem item acionável novo **E** HEAD da
  main == `lastBaseHeadSha`. Se `chat_pending` traz qualquer pedido do PO ainda não executado,
  o ciclo **não** é ocioso — atue ou reencaminhe, nunca registre "sem novidades" por cima de
  pendência viva.
- **"Feito" exige saída REAL do script + `validate-*` verde** no exato estado atual dos
  arquivos — nunca de memória, nunca por inspeção, nunca confiando em rodada anterior a edições
  posteriores. Vale também para reportar status ao usuario: pergunta factual ("você implementou
  X?") se responde verificando specs/chat/git na fonte, não de lembrança.
- **Cobertura, não amostra:** ao varrer o chat ou os specs, cubra o conjunto inteiro (todas as
  features, todas as mensagens pendentes), não as primeiras que aparecem. Truncar a varredura e
  declarar conclusão é o mesmo defeito de declarar "feito" sem testar.

Ver também a memória [[agente-spec-verify-activities-completely]] e a disciplina de brevidade de
ciclo ocioso [[agente-spec-idle-cycle-brevity]] (a brevidade vale só DEPOIS da verificação completa
dar negativo — nunca como atalho que pula a verificação).

## Identidades MCP (chat cross-repo da skill spec)

> ⚠️ **ATENÇÃO — CREDENCIAIS EM TEXTO PLANO.** Os valores abaixo são tokens `Bearer` do
> servidor MCP local (`http://localhost:8765/mcp`). Não commite este bloco em repositório
> público nem compartilhe os tokens. Para usar uma identidade, ponha o token no header
> `Authorization: Bearer <token>` da config MCP daquela sessão. Quem porta o token "é"
> aquele participante perante o servidor.

| Participante | Repo | Token |
|---|---|---|
| `agente-dev` | 42warrior | `842fa0c1fb3b3b5860c02492cee6bf5be63ffb004c1237e9` |
| `agente-tech-lead` | 42warrior | `83f9ca41ecc2625ff2a5348fbaf3bf0a905a31d16b93c796` |
| `agente-po` | 42warrior | `c307e9414927c2df073a7706f0f0dd92dd22136e699cf4ee` |
| `agente-spec` | 42warrior | `bc0cbc08047523ecf48198ff058e39732fc01f0fc7cadc67` |
