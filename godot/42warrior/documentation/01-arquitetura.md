# 01 — Arquitetura

## As três camadas (Clean Architecture)

O projeto é organizado em camadas, e a regra de ouro é: **as dependências apontam para
dentro**. Camadas de fora conhecem as de dentro, nunca o contrário.

```
┌───────────────────────────────────────────────────────────┐
│  Presentation (Godot)   — telas, sprites, input, áudio     │  ← Sprint 3 (não feito)
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Application — casos de uso, carregar nível, rodar    │  │  ← Sprint 2 (não feito)
│  │  o código do jogador, progressão da torre             │  │
│  │  ┌───────────────────────────────────────────────┐   │  │
│  │  │  Domain — REGRAS PURAS do jogo                 │   │  │  ← Sprint 1 (PRONTO)
│  │  │  turno, combate, sentidos, unidades, pontuação │   │  │
│  │  └───────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### Por que separar assim?

Em um projeto **TypeScript** bem feito, você não coloca regra de negócio dentro de um
componente React. Você tem uma camada `domain/` que não importa `react` nem `express` —
ela só sabe das regras. Aqui é igual: o **Domain não importa nada da Godot**.

Benefícios concretos:

1. **Testável sozinho.** Dá para testar todas as regras sem abrir um jogo, sem renderizar
   nada — por isso já temos 51 testes rodando em milissegundos.
2. **Determinístico.** Mesma entrada → mesma saída, sempre. Isso é possível porque o
   domínio não depende de tempo, aleatoriedade ou estado da tela.
3. **A tela é um detalhe trocável.** Amanhã dá para trocar a apresentação (2D, 3D, web)
   sem tocar em uma linha das regras.

## Como isso é garantido (não é só promessa)

Existe um script — `scripts/arch_guard.sh` — que **reprova automaticamente** se qualquer
arquivo do domínio tentar:

- estender um tipo da árvore de cenas da Godot (`extends Node`, `Control`, etc.), ou
- usar API de cena/UI (`get_node`, `get_tree`, `$`, `.tscn`).

Em GDScript, classes de domínio estendem `RefCounted` (um objeto puro em memória, sem
relação com a árvore de nós visual) — o equivalente a uma `class` comum em TypeScript.

## Conceitos de design aplicados

### Imutabilidade
Objetos de estado **não mudam**: operações devolvem uma **nova** instância. É o mesmo
princípio do `const novo = { ...velho, x: 1 }` no front-end moderno (Redux/React).

```typescript
// TypeScript (analogia)
const moved = state.withWarriorPosition(2); // state original intacto
```

Isso elimina bugs de "alguém alterou o estado por baixo dos panos" e é o que torna o jogo
determinístico e fácil de testar.

### CQS — separar consulta de comando
- **Sentidos** (`feel`, `look`, `health`...) só **leem** — nunca mudam o jogo, nunca
  gastam o turno.
- **Ações** (`walk`, `attack`, `rest`) **mudam** o estado e gastam o turno.

Misturar os dois (um método que lê *e* altera) é proibido — mantém o turno previsível.

### Polimorfismo no lugar de `if` gigante
Cada tipo de inimigo sabe se comportar sozinho (ver
[`02-dominio-referencia.md`](02-dominio-referencia.md), seção *Behaviors*), em vez de um
`if (tipo == "sludge") ... else if (tipo == "archer") ...` que cresceria sem controle.

## Princípios do projeto (resumidos)

1. **Responsabilidade única** — cada arquivo e cada método fazem uma coisa só.
2. **Domínio independente da engine** — regras não conhecem a Godot.
3. **Orientação a objetos / DDD** — entidades e value objects com nomes do jogo.
4. **Turno determinístico** — pureza e imutabilidade.
5. **Fidelidade ao Ruby Warrior** — as regras seguem o original; o tema 42 entra na arte.
