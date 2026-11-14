---
sidebar_position: 5
title: test_watering_system
---

# test_watering_system

A função de teste roda os dois testes da saída esperada: plantas válidas e plantas com um nome
inválido. O enunciado a escreve como `test_watering_system()`, sem parâmetros; as listas de
plantas ficam dentro dela.

```python
def test_watering_system() -> None:
    tests = (
        ("valid", ("Tomato", "Lettuce", "Carrots")),
        ("invalid", ("Tomato", "lettuce", "Carrots")),
    )
    for label, plants in tests:
        print(f"\nTesting {label} plants...")
        print("Opening watering system")
        try:
            for plant_name in plants:
                water_plant(plant_name)
        except PlantError as error:
            print(f"Caught PlantError: {error}")
            print(".. ending tests and returning to main")
            return
        finally:
            print("Closing watering system")
```

## Os dois testes numa tupla

`tests` é uma tupla de pares. Cada par tem o **rótulo** do teste, usado no título
(`Testing valid plants...`), e a tupla de plantas a regar. Na segunda, `lettuce` está com
minúscula de propósito.

`for label, plants in tests:` separa cada par em duas variáveis: na primeira volta, `label` é
`"valid"` e `plants` é `("Tomato", "Lettuce", "Carrots")`. Os dois testes seguem o mesmo roteiro,
que fica escrito uma vez só.

## O roteiro de um teste

1. Imprime o título e `Opening watering system`: o sistema "abre".
2. O `try` rega as plantas, uma por uma.
3. Se uma planta for inválida, `water_plant` lança `PlantError`; o resto das plantas é pulado e o
   `except` imprime o erro e o aviso `.. ending tests and returning to main` ("encerrando os
   testes e voltando ao main").
4. O `return` dentro do `except` sai da função **inteira**, não só do teste atual: se houvesse um
   terceiro teste, ele não rodaria. É o "stop the test and immediately return to main"
   do enunciado ("interrompa o teste e volte imediatamente ao main").
5. Em qualquer caso, o `finally` imprime `Closing watering system` antes de seguir, inclusive
   antes do `return` sair da função (página [finally](./02-finally.md)).

## O que acontece em cada teste

| Teste | Plantas regadas | O `except` roda? | O `finally` roda? | Depois |
|---|---|---|---|---|
| `valid` | Tomato, Lettuce, Carrots | não | sim | o laço segue para o próximo teste |
| `invalid` | Tomato (e para em `lettuce`) | sim | sim | o `return` volta para o main |

## O main

O main imprime o título, roda os testes e, quando a função volta, imprime a conclusão:

```python
if __name__ == "__main__":
    print("=== Garden Watering System ===")
    test_watering_system()
    print("\nCleanup always happens, even with errors!")
```

A última linha só aparece porque o erro foi tratado: a função voltou ao main normalmente, e o
sistema já tinha sido fechado pelo `finally`.
