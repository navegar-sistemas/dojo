---
sidebar_position: 1
title: O problema
---

# O problema

Medir o tempo de um feitiço, recusar feitiços com poder baixo, tentar de novo quando um feitiço
falha: são comportamentos que valem para muitos feitiços diferentes e não têm nada a ver com o que
cada feitiço faz. O exercício 4 escreve cada um como um **decorador**, que se aplica a qualquer
função com uma linha `@`, sem mexer no código dela
([Decoradores](../02-conceitos/06-decoradores.md)). E mostra um decorador que já vem com o
Python, o `@staticmethod`.

## O que o enunciado pede

Um arquivo `ex4/decorator_mastery.py`. Autorizados: `functools.wraps` e `staticmethod`.

As assinaturas do enunciado:

```python
def spell_timer(func: Callable) -> Callable
def power_validator(min_power: int) -> Callable
def retry_spell(max_attempts: int) -> Callable

class MageGuild:
  @staticmethod
  def validate_mage_name(name: str) -> bool
  def cast_spell(self, spell_name: str, power: int) -> str
```

| Peça | O que faz |
|---|---|
| `spell_timer(func)` | decorador que mede o tempo de execução: imprime `Casting nome_da_função...` antes, roda a função, imprime `Spell completed in X.XXX seconds` depois (três casas decimais) e devolve o resultado da função. Usa `functools.wraps` |
| `power_validator(min_power)` | **fábrica de decoradores** que confere o poder: se o poder é maior ou igual a `min_power`, roda a função normalmente; se não, devolve `"Insufficient power for this spell"`. O enunciado diz que ele é aplicado a uma função solta, mas também manda decorar com ele o método `cast_spell` ([power_validator](./03-power-validator.md#onde-está-o-poder)). Usa `functools.wraps` |
| `retry_spell(max_attempts)` | decorador que tenta de novo um feitiço que falhou: se a função lança uma exceção, tenta de novo, até `max_attempts` tentativas, imprimindo `Spell failed, retrying... (attempt n/max_attempts)`. Se todas falham, devolve `"Spell casting failed after max_attempts attempts"`; se uma dá certo, devolve o resultado dela |
| `MageGuild.validate_mage_name(name)` | método estático: um nome é válido se tem pelo menos 3 caracteres e só letras e espaços |
| `MageGuild.cast_spell(self, spell_name, power)` | método comum (de instância), decorado com `power_validator` com `min_power=10`: com poder válido, devolve `"Successfully cast spell_name with <power> power"`; senão, `"Insufficient power for this spell"` |

Nas mensagens, `nome_da_função`, `X.XXX`, `n`, `max_attempts`, `spell_name` e `<power>` são
trocados pelos valores de cada chamada. O enunciado sugere `time.sleep` (do módulo `time`, que
pausa o programa por alguns segundos) para simular um feitiço demorado.

## A saída esperada

```text
Testing spell timer...
Casting fireball...
Spell completed in 0.101 seconds
Result: Fireball cast!

Testing retrying spell...
Spell failed, retrying... (attempt 1/3)
Spell failed, retrying... (attempt 2/3)
Spell casting failed after 3 attempts
Waaaaaaagh spelled !

Testing MageGuild...
True
False
Successfully cast Lightning with 15 power
Insufficient power for this spell
```

- o tempo, `0.101`, muda a cada execução ([Rodar e conferir](./08-rodar-e-conferir.md));
- o teste de nova tentativa tem dois feitiços: um que sempre falha (três tentativas, duas linhas
  de `retrying` e a mensagem de falha) e outro que funciona de primeira (`Waaaaaaagh spelled !`);
- o teste da guilda confere um nome válido (`True`) e um inválido (`False`), e lança um feitiço
  com poder 15 (aceito) e outro com poder menor que 10 (recusado).

A saída não começa com linha vazia: no exemplo do enunciado, o primeiro `Testing` vem logo depois
do comando.
