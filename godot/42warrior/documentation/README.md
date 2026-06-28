# 42 Warrior — Documentação

Remake do jogo de programação **Ruby Warrior** (beginner tower, 9 níveis), ambientado
no universo da 42, feito em **Godot + GDScript** para a game jam da 42SP.

No jogo, o jogador **não controla o herói diretamente**: ele escreve a lógica que o
warrior executa **uma ação por turno** (sentir o ambiente e reagir).

> **Estado atual:** apenas o **Sprint 1 (núcleo de domínio)** está implementado — toda a
> lógica de regras, pura e testável, **sem nenhuma tela ainda**. Veja o roadmap em
> [`05-estado-e-roadmap.md`](05-estado-e-roadmap.md).

## Índice

| Documento | O que cobre |
|---|---|
| [`01-arquitetura.md`](01-arquitetura.md) | As camadas (Clean Architecture), por que o domínio é separado da engine, e os princípios do projeto. |
| [`02-dominio-referencia.md`](02-dominio-referencia.md) | Cada classe do domínio explicada, com **paralelo em TypeScript** para quem não conhece GDScript. |
| [`03-fluxo-de-turno.md`](03-fluxo-de-turno.md) | Como um turno é resolvido do começo ao fim (o coração do jogo). |
| [`04-como-rodar-e-testar.md`](04-como-rodar-e-testar.md) | Como rodar os testes e as verificações de qualidade. |
| [`05-estado-e-roadmap.md`](05-estado-e-roadmap.md) | O que está pronto, o que falta (Sprints 2 e 3) e decisões de design tomadas. |
| [`06-glossario.md`](06-glossario.md) | Tradução Ruby Warrior ↔ nomes neste projeto. |

## Visão de 30 segundos

```
O jogador escreve:  "se sinto inimigo na frente, ataco; senão, ando"
        │
        ▼
 TurnResolver  ── aplica a ação → checa vitória → inimigos reagem → checa derrota
        │
        ▼
 Novo estado do nível + lista de eventos ("andou", "levou 3 de dano", ...)
        │
        ▼
 (futuro Sprint 3) as telas em Godot animam esses eventos
```

## Mapa rápido do código

```
src/domain/            ← REGRAS PURAS (não dependem da Godot) — pronto
  world/                 o "tabuleiro"
    direction.gd           direção forward/backward
    space.gd               o que há numa casa da grade
    level_state.gd         estado imutável do nível
  units/                 warrior + 6 tipos de unidade
  combat/                a "IA" de cada inimigo + reação dos inimigos
    unit_behavior.gd / melee_/ ranged_/ inert_behavior.gd
    enemy_phase.gd
  turn/                  a resolução do turno
    turn_resolver.gd       orquestra o turno inteiro
    action_applier.gd      aplica a ação do warrior
    turn_result.gd         resultado (estado + eventos + desfecho)
    turn_event.gd          eventos observáveis de um turno
    actions/               comandos do warrior (walk/attack/rest)
  senses/                consultas do jogador (feel/look/listen/...)

test/domain/           ← 51 testes automatizados (todos verdes)
scripts/               ← test.sh / lint.sh / arch_guard.sh / check.sh
specs/                 ← a especificação do projeto (skill "spec")
```

> A organização é **por subdomínio** (world, units, combat, turn, senses) — cada arquivo
> num grupo com significado de jogo. Em GDScript as classes são globais (via `class_name`),
> então a pasta é só organização: nenhum arquivo depende do caminho do outro.
