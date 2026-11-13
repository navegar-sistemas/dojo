---
sidebar_position: 2
title: Ordenar e filtrar
---

# Ordenar e filtrar

Crie o arquivo `ex0/lambda_spells.py` e escreva nele as duas funções desta página. As páginas
seguintes acrescentam o resto, sempre no fim do arquivo: `spell_transformer`, `mage_stats` e a
demonstração. O arquivo não tem nenhum `import`: tudo o que ele usa é embutido.

## artifact_sorter

```python
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact["power"],
                  reverse=True)
```

- `sorted` devolve uma lista **nova**, ordenada; a lista recebida continua na ordem original;
- `key=lambda artifact: artifact["power"]` diz por qual valor comparar: o poder de cada
  artefato;
- `reverse=True` inverte a ordem, do maior poder para o menor, como o enunciado pede
  (decrescente);
- a chamada não cabe em 79 caracteres e continua na linha de baixo. Dentro de parênteses, o
  Python aceita quebrar a linha, e o costume é alinhar a continuação logo depois do `(`.

Dois artefatos com o mesmo poder ficam na ordem em que chegaram, porque a ordenação do Python é
estável ([Lambda](../02-conceitos/02-lambda.md#o-que-aconteceu)).

## power_filter

```python
def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))
```

- `filter` fica com os magos para os quais a lambda devolve `True`: os de poder maior ou igual a
  `min_power`;
- a lambda usa `min_power`, um parâmetro de `power_filter`. Ela enxerga o nome porque foi escrita
  dentro de `power_filter` ([Escopo e closures](../02-conceitos/04-escopo-e-closures.md));
- `filter` devolve um iterador, e o enunciado pede uma lista: o `list(...)` em volta pede todos
  os itens e os guarda numa lista.

Com nenhum mago forte o bastante, o resultado é a lista vazia, `[]`.
