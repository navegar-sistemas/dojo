# 05 — Estado atual e roadmap

## O que está PRONTO (Sprint 1 — núcleo de domínio)

Toda a lógica de regras do jogo, pura e testável:

- ✅ Grade do nível e estado imutável (`LevelState`, `Space`)
- ✅ Direção relativa (`Direction`)
- ✅ Unidades: warrior + sludge, thick sludge, archer, wizard, captive (`units/`)
- ✅ Combate e IA dos inimigos por polimorfismo (`combat/`)
- ✅ Ações do warrior: walk, attack (dano reduzido para trás), rest (`actions/`, `ActionApplier`)
- ✅ Resolução de turno determinística com vitória/derrota (`TurnResolver`)
- ✅ Sentidos: feel, look, listen, health, direction_of_stairs (`Senses`)
- ✅ Eventos de turno (`TurnEvent`) — base para animação e pontuação
- ✅ Infra de qualidade: 51 testes, lint, guard de arquitetura

**Qualidade:** 51/51 testes verdes · gdlint 0 violações · gdformat 0 diffs · arquitetura OK.

### Stories entregues
US-001 (estado), US-002 (turno), US-003 (vitória/derrota), US-004 (sentidos),
US-005 (ações básicas), US-007 (unidades/IA), US-016 (qualidade).

---

## O que FALTA

### Sprint 2 — Execução do jogador, níveis e pontuação
- ⬜ **`WarriorFacade`** — a "fachada" que o código do jogador enxerga: só os métodos da API
  (sentidos + ações), sem acesso ao estado interno. Garante também a regra "a **primeira**
  ação registrada no turno vence".
- ⬜ **`PlayerScriptRunner`** — compila o GDScript que o jogador escreve **em tempo de
  execução** e o roda a cada turno, tratando erros sem travar o jogo.
- ⬜ Ações restantes: **rescue!** (resgatar cativo), **pivot!** (virar), **shoot!** (atirar à distância).
- ⬜ **Os 9 níveis** como dados declarativos + um `LevelLoader` que monta cada um.
- ⬜ **Soluções-referência** (um código que vence cada nível) — servem de demo e de teste ponta-a-ponta.
- ⬜ **Pontuação**: pontos por inimigo/resgate + *time bonus* decrescente + comparação com o *ace score*.

### Sprint 3 — Apresentação, fluxo de torre e áudio (a parte visual)
- ⬜ Grade **2D top-down** com sprites (placeholders agora, arte da 42 depois).
- ⬜ HUD: vida, número do turno, descrição do nível, pontuação.
- ⬜ Fluxo: menu inicial, telas de transição entre níveis, vitória/reinício, créditos.
- ⬜ Progresso salvo entre sessões.
- ⬜ Áudio: efeitos sonoros e trilha.

> **É no Sprint 3 que o projeto vira um "jogo que dá pra ver e jogar".** Hoje ele é o motor.

---

## Decisões de design que valem revisar

| Decisão | Onde mudar | Observação |
|---|---|---|
| Valores de combate (warrior ataca 5; para trás = 2; rest cura 2) | `units/*.gd`, `turn/action_applier.gd` | Ajustáveis para balanceamento. |
| Archer/Wizard com alcance 3 e bloqueio de linha de tiro | `combat/ranged_behavior.gd` | Aproximação do original; pode calibrar. |
| Jogador escreve **código real** (não blocos) | decisão sua, registrada na spec | Executado via GDScript em runtime no Sprint 2. |
| Assets **placeholder** agora | Sprint 3 | Pontos de troca para a arte da 42. |

---

## Onde a especificação completa mora

Tudo isto está formalizado, com rastreabilidade, na pasta `specs/` (gerida pela skill
`spec`): requisitos de produto (PR), requisitos da feature (RF/RNF), decisões de
arquitetura (ADR), user stories (US) e tasks (T). O board pode ser consultado pelos
scripts da skill. Esta documentação em `documentation/` é a versão **explicada para
leitura humana**; a `specs/` é a versão **tipada e verificável por máquina**.
