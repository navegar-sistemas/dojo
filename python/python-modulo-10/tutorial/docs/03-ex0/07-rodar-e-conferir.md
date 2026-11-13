---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex0/lambda_spells.py) - <<'FIM'

Testing artifact sorter...
Fire Staff (92 power) comes before Crystal Orb (85 power)

Testing spell transformer...
* fireball * * heal * * shield *
FIM
```

- `<(python3 ex0/lambda_spells.py)` entrega ao `diff` a saída do programa como se fosse um
  arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: a saída copiada do
  enunciado, começando pela linha vazia. Cole o bloco inteiro, até a linha `FIM`; sem ela, o
  terminal fica esperando mais linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema.

## Lambdas e defs

```bash
grep -c "lambda" ex0/lambda_spells.py
grep -n "def " ex0/lambda_spells.py
```

```text
6
1:def artifact_sorter(artifacts: list[dict]) -> list[dict]:
6:def power_filter(mages: list[dict], min_power: int) -> list[dict]:
10:def spell_transformer(spells: list[str]) -> list[str]:
14:def mage_stats(mages: list[dict]) -> dict:
27:def main() -> None:
```

O `grep` procura um texto nos arquivos: com `-c`, conta as linhas que o contêm; com `-n`, mostra
cada linha encontrada com o número dela. São seis linhas com lambda, e os únicos `def` são as
quatro funções do enunciado e o `main`.

## As outras duas funções

A demonstração não usa `power_filter` nem `mage_stats`. Este teste importa as funções do arquivo e
as chama com dados próprios:

```bash
PYTHONPATH=ex0 python3 -B - <<'FIM'
from lambda_spells import artifact_sorter, mage_stats, power_filter
mages = [
    {"name": "Alex", "power": 90, "element": "fire"},
    {"name": "Riley", "power": 55, "element": "ice"},
    {"name": "Sage", "power": 72, "element": "wind"},
]
print(power_filter(mages, 70))
print(power_filter(mages, 100))
print(mage_stats(mages))
print(mage_stats([]))
artifacts = [
    {"name": "Crystal Orb", "power": 85, "type": "focus"},
    {"name": "Fire Staff", "power": 92, "type": "weapon"},
]
print(artifact_sorter(artifacts)[0]["name"])
print(artifacts[0]["name"])
FIM
```

- `PYTHONPATH=ex0`, escrito antes do comando, diz ao Python em que pasta procurar os módulos
  importados: assim o `from lambda_spells import ...` acha o arquivo `ex0/lambda_spells.py`. A
  variável só vale para este comando;
- o `-` no lugar do nome de um arquivo manda o Python ler o programa da entrada, e o `<<'FIM'`
  escreve o programa nela, como no `diff`;
- o `-B` impede que o Python grave na pasta `ex0` a pasta de cache `__pycache__`, que ele cria
  ao importar um arquivo;
- importar o arquivo não roda a demonstração, por causa do `if __name__ == "__main__":`.

```text
[{'name': 'Alex', 'power': 90, 'element': 'fire'}, {'name': 'Sage', 'power': 72, 'element': 'wind'}]
[]
{'max_power': 90, 'min_power': 55, 'avg_power': 72.33}
{'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
Fire Staff
Crystal Orb
```

- o filtro com 70 fica com Alex (90) e Sage (72); com 100, com ninguém;
- a média de 90, 55 e 72 é 72,333..., arredondada para `72.33`;
- a lista vazia dá os zeros ([A lista vazia](./04-estatisticas.md#a-lista-vazia));
- as duas últimas linhas mostram que `artifact_sorter` não muda a lista recebida: a lista
  ordenada começa pelo Fire Staff, e a original continua começando pelo Crystal Orb.

## Com dados do gerador

O gerador de dados ([O gerador de dados](../01-ambiente/05-o-gerador-de-dados.md)) imprime as
listas `artifacts`, `mages` e `spells` como código Python. As três linhas abaixo foram coladas
de uma execução dele, sem mudança:

```bash
PYTHONPATH=ex0 python3 -B - <<'FIM'
from lambda_spells import artifact_sorter, mage_stats, power_filter, spell_transformer
artifacts = [{'name': 'Crystal Orb', 'power': 120, 'type': 'weapon'}, {'name': 'Fire Staff', 'power': 115, 'type': 'accessory'}, {'name': 'Storm Crown', 'power': 64, 'type': 'relic'}, {'name': 'Earth Shield', 'power': 115, 'type': 'focus'}]
mages = [{'name': 'Morgan', 'power': 52, 'element': 'wind'}, {'name': 'Sage', 'power': 58, 'element': 'shadow'}, {'name': 'Storm', 'power': 97, 'element': 'wind'}, {'name': 'Sage', 'power': 88, 'element': 'fire'}, {'name': 'Jordan', 'power': 98, 'element': 'lightning'}]
spells = ['meteor', 'tornado', 'freeze', 'darkness']
for artifact in artifact_sorter(artifacts):
    print(artifact)
print(power_filter(mages, 90))
print(mage_stats(mages))
print(spell_transformer(spells))
FIM
```

```text
{'name': 'Crystal Orb', 'power': 120, 'type': 'weapon'}
{'name': 'Fire Staff', 'power': 115, 'type': 'accessory'}
{'name': 'Earth Shield', 'power': 115, 'type': 'focus'}
{'name': 'Storm Crown', 'power': 64, 'type': 'relic'}
[{'name': 'Storm', 'power': 97, 'element': 'wind'}, {'name': 'Jordan', 'power': 98, 'element': 'lightning'}]
{'max_power': 98, 'min_power': 52, 'avg_power': 78.6}
['* meteor *', '* tornado *', '* freeze *', '* darkness *']
```

- o Fire Staff e o Earth Shield têm o mesmo poder, 115, e ficaram na ordem em que vinham na
  lista: a ordenação é estável;
- `power_filter` mantém a ordem da lista original (Storm antes de Jordan), porque `filter` não
  reordena nada;
- a média de 52, 58, 97, 88 e 98 é exatamente 78,6, e `round` não acrescenta zeros: `78.6`.

Com os dados de outra execução do gerador, os valores mudam, e as mesmas regras valem.
