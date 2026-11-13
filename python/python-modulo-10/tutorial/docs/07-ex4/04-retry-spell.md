---
sidebar_position: 4
title: retry_spell
---

# retry_spell

Um feitiço instável às vezes falha lançando uma exceção, e uma nova tentativa pode dar certo.
`retry_spell(max_attempts)` cria um decorador que repete a chamada até dar certo ou até gastar as
tentativas. A função entra depois de `power_validator`:

```python
def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print("Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator
```

## O laço de tentativas

- `range(1, max_attempts + 1)` dá os números das tentativas, de 1 até `max_attempts` (o fim do
  `range` não entra, por isso o `+ 1`);
- dentro do `try`, a chamada que dá certo sai do `wrapper` na hora, com `return`: o resultado da
  função é devolvido normalmente, e as tentativas restantes não acontecem;
- `except Exception` captura qualquer erro comum lançado pela função. `Exception` é a classe mãe
  de quase todas as exceções do Python (`ValueError`, `TypeError`, `RuntimeError`...);
- depois de uma falha, se ainda há tentativa pela frente, imprime a mensagem de nova tentativa;
- se o laço termina sem nenhum `return`, todas falharam, e o `wrapper` devolve a mensagem de
  falha.

## Por que a última falha não imprime "retrying"

O exemplo do enunciado, com 3 tentativas, mostra:

```text
Spell failed, retrying... (attempt 1/3)
Spell failed, retrying... (attempt 2/3)
Spell casting failed after 3 attempts
```

São três tentativas e só duas linhas de `retrying`: depois da terceira falha não há nova tentativa,
e a linha seguinte é a de falha. O `if attempt < max_attempts:` reproduz isso. "Tentar de novo até
`max_attempts` vezes" é lido como `max_attempts` tentativas **no total**, como mostram o
`(attempt n/3)` e o `after 3 attempts`.

| Tentativa | Resultado | Impresso |
|---|---|---|
| 1 | exceção | `Spell failed, retrying... (attempt 1/3)` |
| 2 | exceção | `Spell failed, retrying... (attempt 2/3)` |
| 3 | exceção | nada; o laço acaba e a função devolve `Spell casting failed after 3 attempts` |

A mensagem de nova tentativa foi dividida em dois textos seguidos, o segundo com `f`, para caber em
79 caracteres.
