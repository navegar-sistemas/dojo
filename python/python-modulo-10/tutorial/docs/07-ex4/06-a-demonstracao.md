---
sidebar_position: 6
title: A demonstração
---

# A demonstração

A demonstração precisa de três feitiços decorados e de um `main`. Eles entram no fim do arquivo,
depois de `MageGuild`:

```python
@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def unstable_spell() -> str:
    raise RuntimeError("The spell backfired")


@retry_spell(max_attempts=3)
def stable_spell() -> str:
    return "Waaaaaaagh spelled !"


def main() -> None:
    print("Testing spell timer...")
    result = fireball()
    print(f"Result: {result}")

    print("\nTesting retrying spell...")
    print(unstable_spell())
    print(stable_spell())

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("Jo"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Fireball", 5))


if __name__ == "__main__":
    main()
```

## Os feitiços de teste

- **`fireball`** espera 0,1 segundo com `time.sleep(0.1)`, como o enunciado sugere, e devolve
  `"Fireball cast!"`. Com `@spell_timer`, a chamada imprime `Casting fireball...` (o nome vem do
  `__name__` da função) e o tempo medido, perto de 0,1 segundo;
- **`unstable_spell`** sempre falha: `raise RuntimeError(...)` lança uma exceção a cada
  tentativa. `RuntimeError` é o tipo de exceção genérico para "algo deu errado ao rodar";
- **`stable_spell`** devolve o texto do enunciado na primeira tentativa, e o decorador não imprime
  nada.

Os três ficam no nível de cima do arquivo, decorados ao serem criados. São funções, e não
variáveis que guardam um estado.

## O main

- `result = fireball()` roda o feitiço; as duas linhas do cronômetro saem durante a chamada, e o
  `Result:` sai depois. Guardar o resultado numa variável antes de imprimir deixa essa ordem clara;
- `print(unstable_spell())` imprime as duas linhas de `retrying`, durante a chamada, e depois o
  texto devolvido, `Spell casting failed after 3 attempts`;
- o método estático é chamado pela classe, sem objeto; `cast_spell` precisa de um objeto, criado
  com `MageGuild()`. O poder 5 fica abaixo do mínimo, 10.

O primeiro `print` não tem `\n`, e a saída começa direto no `Testing spell timer...`, como no
exemplo do enunciado.
