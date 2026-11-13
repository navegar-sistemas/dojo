---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## A saída

```bash
python3 ex4/decorator_mastery.py
```

```text
Testing spell timer...
Casting fireball...
Spell completed in 0.104 seconds
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

A terceira linha muda a cada execução: o `time.sleep(0.1)` garante pelo menos 0,1 segundo, e o
resto depende da máquina e do que mais ela está fazendo no momento. Valores como `0.100`, `0.101`
ou `0.105` são normais; o enunciado mostra `0.101`. Por isso a comparação com o enunciado é feita
em duas partes: as linhas fixas com o `diff`, e a linha do tempo pelo formato.

## As linhas fixas

```bash
diff <(python3 ex4/decorator_mastery.py | sed '3d') - <<'FIM'
Testing spell timer...
Casting fireball...
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
FIM
```

`sed '3d'` apaga (`d`, de *delete*) a linha 3 da saída antes da comparação, e o texto esperado é o
do enunciado sem a linha do tempo. Sem nenhuma linha impressa, todas as outras linhas são iguais
às do enunciado ([o diff explicado](../03-ex0/07-rodar-e-conferir.md#comparar-com-o-enunciado)).

## A linha do tempo

```bash
python3 ex4/decorator_mastery.py | sed -n '3p' | grep -E '^Spell completed in [0-9]+\.[0-9]{3} seconds$'
```

```text
Spell completed in 0.104 seconds
```

- `sed -n '3p'` imprime (`p`) só a linha 3; o `-n` cala as outras;
- `grep -E` imprime a linha se ela combina com o padrão, uma **expressão regular**: `^` é o começo
  da linha, `[0-9]+` um ou mais algarismos, `\.` um ponto de verdade, `[0-9]{3}` exatamente três
  algarismos e `$` o fim da linha.

A linha aparece quando tem o formato do enunciado, com três casas decimais; o número, de novo,
muda a cada execução. Sem nada impresso, o formato estaria errado.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex4
.venv/bin/mypy --disallow-untyped-defs ex4
```

```text
Success: no issues found in 1 source file
```

## wraps e o validador numa função comum

O teste confere que os decoradores mantêm os nomes e aplica `power_validator` a uma função solta,
com o poder por posição e por nome (`PYTHONPATH`, `-B` e o `-` com `<<'FIM'` estão explicados em
[Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md#as-outras-duas-funções)):

```bash
PYTHONPATH=ex4 python3 -B - <<'FIM'
from decorator_mastery import MageGuild, fireball, power_validator
print(fireball.__name__, MageGuild.cast_spell.__name__)


@power_validator(min_power=20)
def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


print(heal("Ally", 25))
print(heal("Ally", power=5))
print(MageGuild().cast_spell(spell_name="Flash", power=10))
FIM
```

```text
fireball cast_spell
Heal restores Ally for 25 HP
Insufficient power for this spell
Successfully cast Flash with 10 power
```

- sem o `@wraps`, os dois nomes seriam `wrapper`;
- o validador funciona numa função comum, com o mínimo 20: o poder 25 passa, e o 5 (passado por
  nome) é recusado sem que o corpo de `heal` rode;
- no método, com os dois argumentos por nome, o poder é achado em `kwargs`. O poder 10 é igual ao
  mínimo e passa: a regra é "maior ou igual".

## Falhar e depois acertar

O exemplo do enunciado tem um feitiço que sempre falha e outro que acerta de primeira. Este teste
cria feitiços que falham um número escolhido de vezes antes de acertar, com uma closure que conta
as tentativas ([mage_counter](../05-ex2/02-mage-counter.md)):

```bash
PYTHONPATH=ex4 python3 -B - <<'FIM'
from collections.abc import Callable
from decorator_mastery import retry_spell


def make_flaky(failures: int) -> Callable:
    attempts = 0

    @retry_spell(max_attempts=3)
    def flaky_spell() -> str:
        nonlocal attempts
        attempts += 1
        if attempts <= failures:
            raise RuntimeError("fizzle")
        return f"Success on attempt {attempts}"

    return flaky_spell


print(make_flaky(2)())
print(make_flaky(3)())
FIM
```

```text
Spell failed, retrying... (attempt 1/3)
Spell failed, retrying... (attempt 2/3)
Success on attempt 3
Spell failed, retrying... (attempt 1/3)
Spell failed, retrying... (attempt 2/3)
Spell casting failed after 3 attempts
```

- com 2 falhas, a terceira tentativa acerta, e o resultado dela é devolvido normalmente;
- com 3 falhas, as três tentativas se esgotam, e o decorador devolve a mensagem de falha.

## Com dados do gerador

As quatro linhas de dados foram coladas de uma execução do gerador:

```bash
PYTHONPATH=ex4 python3 -B - <<'FIM'
from decorator_mastery import MageGuild
test_powers = [20, 10, 12, 18]
spell_names = ['freeze', 'fireball', 'flash', 'meteor']
mage_names = ['Ash', 'Casey', 'Phoenix', 'Rowan', 'Luna', 'Jordan']
invalid_names = ['Jo', 'A', 'Alex123', 'Test@Name']
guild = MageGuild()
for spell, power in zip(spell_names, test_powers):
    print(guild.cast_spell(spell, power))
print(guild.cast_spell("meteor", 9))
print(list(map(MageGuild.validate_mage_name, mage_names)))
print(list(map(MageGuild.validate_mage_name, invalid_names)))
print(guild.validate_mage_name("Mage Lord"))
FIM
```

```text
Successfully cast freeze with 20 power
Successfully cast fireball with 10 power
Successfully cast flash with 12 power
Successfully cast meteor with 18 power
Insufficient power for this spell
[True, True, True, True, True, True]
[False, False, False, False]
True
```

- os quatro poderes sorteados nesta execução são todos pelo menos 10; o `9`, acrescentado pelo
  tutorial, mostra a recusa. O gerador sorteia poderes de 5 a 30, e outras execuções trazem
  poderes abaixo do mínimo;
- `map` aceita o método estático como qualquer função: `MageGuild.validate_mage_name` é passado
  sem parênteses. Os nomes válidos dão `True`; os quatro inválidos, fixos no gerador, dão `False`
  (curto demais, curto demais, algarismos, `@`);
- o método estático também pode ser chamado por um objeto, `guild.validate_mage_name(...)`, e um
  nome com espaço é válido.
