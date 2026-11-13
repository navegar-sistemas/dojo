---
sidebar_position: 3
title: power_validator
---

# power_validator

`power_validator` recebe um poder mínimo e devolve um decorador que barra os feitiços lançados com
poder abaixo dele. É o formato de três camadas de
[Decoradores com parâmetros](../02-conceitos/07-decoradores-com-parametros.md). A função entra
depois de `spell_timer`:

```python
def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs["power"] if "power" in kwargs else args[-1]
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

## Onde está o poder

O `wrapper` recebe os argumentos como `*args` e `**kwargs` e precisa achar entre eles o poder. O
enunciado não diz como; o decorador vale para uma função comum (`fireball(target, power)`) e
também para o método `cast_spell(self, spell_name, power)`, que tem um argumento a mais na frente,
o `self`. Nos dois, o poder é o **último** parâmetro. A regra escolhida pelo tutorial:

- se o poder veio por nome (`power=15`), ele está em `kwargs["power"]`;
- se não, é o último argumento posicional, `args[-1]` (o índice `-1` é o último item de uma
  tupla ou lista).

`"power" in kwargs` pergunta se a chave existe no dicionário, e a expressão condicional
`a if condição else b` escolhe entre os dois casos numa linha.

Essa regra vale para funções em que o poder é o último parâmetro, como no contrato dos feitiços.
Outra opção seria descobrir a posição pelo nome do parâmetro com o módulo `inspect`, fora da lista
de autorizados do exercício.

## A conferência

- poder menor que `min_power`: o `wrapper` devolve `"Insufficient power for this spell"` e a
  função original **não roda**;
- poder maior ou igual: o `wrapper` chama a função com os mesmos argumentos e devolve o resultado
  dela.

`wrapper` lembra `func` (da camada do meio) e `min_power` (da camada de fora) por closure.

## Usar

Na classe da [próxima página](./05-mage-guild.md), o método `cast_spell` é decorado assim:

```python
    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"
```

`power_validator(min_power=10)` roda primeiro e devolve o `decorator` configurado com 10; o
`decorator` recebe `cast_spell` e devolve o `wrapper` ([MageGuild](./05-mage-guild.md)).
