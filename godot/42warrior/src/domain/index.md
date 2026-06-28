# `src/domain/` — Núcleo de regras (Domain)

O coração do jogo: todas as regras, em **GDScript puro** (`extends RefCounted`), sem
nenhuma dependência da engine Godot. É testável isoladamente e determinístico (mesma
entrada → mesma saída).

> Documentação explicada para humanos: [`/documentation`](../../documentation/README.md).
> Aqui ficam os `index.md` curtos por pasta.

## Subdomínios

| Pasta | Responsabilidade |
|---|---|
| [`world/`](world/index.md) | O "tabuleiro": direção, espaço e o estado imutável do nível. |
| [`units/`](units/index.md) | O warrior e os inimigos/refém, com saúde e atributos. |
| [`combat/`](combat/index.md) | A IA das unidades (polimórfica) e a fase de reação dos inimigos. |
| [`turn/`](turn/index.md) | A resolução de um turno: ações, aplicação, eventos e resultado. |
| [`senses/`](senses/index.md) | As consultas que o jogador faz ao ambiente (sem gastar turno). |

## Princípios em vigor

- **Imutabilidade**: estado/unidades não mudam; operações devolvem novas instâncias.
- **CQS**: sentidos só leem; ações só comandam.
- **Responsabilidade única**: um arquivo = uma classe; um método = uma tarefa.
- **Sem dependência da engine**: garantido por `scripts/arch_guard.sh`.
