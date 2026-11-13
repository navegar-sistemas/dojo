---
sidebar_position: 3
title: A demonstração
---

# A demonstração

A segunda metade do arquivo mostra o modelo funcionando e imprime a saída do enunciado: uma
função que mostra uma estação e o `main`. As duas entram no fim do arquivo, depois de
`SpaceStation`.

## Mostrar a estação

```python
def show_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Non-operational"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")
```

- `show_station` recebe uma `SpaceStation` já criada. Como o objeto só existe se passou na
  validação, a função não confere nada: cada campo tem o tipo e o limite certos;
- `status` usa uma **expressão condicional**, `a if condição else b`: vale `"Operational"` se a
  estação está em operação, e `"Non-operational"` se não está. O enunciado só mostra o caso
  `Operational`; o texto do outro caso é escolha do tutorial;
- `{station.power_level}%` imprime o `float` como o Python o escreve, `85.5`, seguido do `%`.

## O main

```python
def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 30),
    )
    print("Valid station created:")
    show_station(station)
    print()
    print("=" * 40)
    try:
        # crew_size=25 is above le=20: Pydantic refuses to build the object.
        SpaceStation(
            station_id="ISS002",
            name="Overcrowded Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 15, 10, 30),
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
```

### A estação válida

- `"=" * 40` repete o `=` 40 vezes, a linha do enunciado;
- a estação válida é criada pelo construtor, com os dados da saída do enunciado. A data vai como
  `datetime(2024, 1, 15, 10, 30)`, do tipo certo, para o mypy aceitar a chamada
  ([E pelo construtor?](../02-conceitos/04-conversao-de-tipos.md#e-pelo-construtor)). A data não
  aparece na saída, e o valor é escolha do tutorial;
- `is_operational` e `notes` ficam de fora e recebem os padrões, `True` e `None`;
- a chamada ocupa várias linhas, um argumento por linha: dentro de parênteses, o Python aceita
  quebrar a linha, e a vírgula depois do último argumento é permitida;
- `print()` sem argumento imprime a linha vazia que separa os dois blocos da saída.

### A estação inválida

- a segunda estação tem `crew_size=25`, acima do limite `le=20`. O construtor lança
  `ValidationError` e não devolve objeto nenhum; por isso a chamada nem é guardada numa variável;
- o `except ValidationError` captura o erro: é o tratamento de exceções que o enunciado pede para
  proteger os dados. O dado inválido não vira objeto, e o programa segue até o fim;
- `error.errors()[0]["msg"]` é a mensagem do primeiro (e aqui único) erro:
  `Input should be less than or equal to 20` ([ValidationError](../02-conceitos/02-validationerror.md));
- as duas linhas do `except` só rodam se o erro acontecer: se a estação inválida fosse aceita,
  nenhuma das duas apareceria na saída.

O mypy aceita a segunda chamada: `25` é um `int`, o tipo do campo. O limite de 20 não é um tipo,
é uma regra do Pydantic, conferida só quando o programa roda.

### O if do fim

`if __name__ == "__main__":` roda o `main` só quando o arquivo é executado direto, e não quando
outro arquivo o importa: `__name__` é uma variável que o Python preenche com `"__main__"` no
arquivo que foi rodado. Os testes da página [Rodar e conferir](./05-rodar-e-conferir.md) importam
o modelo sem rodar a demonstração.
