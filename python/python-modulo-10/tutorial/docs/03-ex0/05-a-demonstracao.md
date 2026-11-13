---
sidebar_position: 5
title: A demonstração
---

# A demonstração

A última parte do arquivo imprime a saída do enunciado. Ela fica numa função `main`, para que as
listas de teste não sejam variáveis globais ([O def do main](./01-o-problema.md#o-def-do-main)).

```python
def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Ice Wand", "power": 70, "type": "accessory"},
    ]
    print("\nTesting artifact sorter...")
    first, second = artifact_sorter(artifacts)[:2]
    print(f"{first['name']} ({first['power']} power) comes before "
          f"{second['name']} ({second['power']} power)")

    print("\nTesting spell transformer...")
    print(" ".join(spell_transformer(["fireball", "heal", "shield"])))


if __name__ == "__main__":
    main()
```

## O teste da ordenação

- `artifacts` tem três artefatos fora de ordem: o enunciado mostra o Fire Staff (92) e o Crystal
  Orb (85); o Ice Wand (70) é do tutorial, para que a lista tenha um terceiro item que precisa ir
  para o fim;
- `artifact_sorter(artifacts)[:2]` ordena e pega os dois primeiros, os dois mais fortes;
  `first, second = ...` separa os dois em duas variáveis;
- a mensagem tem duas f-strings seguidas dentro do `print`: o Python junta textos escritos lado a
  lado num só (`"ab" "cd"` é `"abcd"`), e isso permite quebrar a linha longa. Dentro de uma
  f-string com aspas duplas, as chaves do dicionário vão entre aspas simples:
  `{first['name']}`.

## O teste da transformação

`spell_transformer` devolve a lista `['* fireball *', '* heal *', '* shield *']`, e
`" ".join(...)` junta os itens num texto só, separados por um espaço.

## As linhas vazias e o main

- o `\n` no começo de `"\nTesting artifact sorter..."` é uma **quebra de linha**: o `print`
  imprime uma linha vazia e depois o texto. É assim que sai a linha vazia do começo da saída, e a
  que separa os dois testes;
- `if __name__ == "__main__":` roda o `main` só quando o arquivo é executado com `python3`, e não
  quando outro arquivo o importa: `__name__` é uma variável que o Python preenche com
  `"__main__"` no arquivo que foi rodado. Os testes de [Rodar e conferir](./07-rodar-e-conferir.md)
  importam as funções sem disparar a demonstração;
- as linhas em branco entre os grupos de comandos do `main` só separam os testes para quem lê;
  elas não aparecem na saída.
