---
sidebar_position: 3
title: O requirements.txt
---

# O requirements.txt

O `requirements.txt` é a lista de dependências no formato do pip: um pacote por linha, com uma
restrição de versão opcional ([Versões](../02-conceitos/01-pacotes-e-o-pip.md#versões)). Crie
`ex1/requirements.txt`:

```text title="ex1/requirements.txt"
pandas>=2.1.0
numpy>=1.25.0
matplotlib>=3.7.2
```

O comando `pip install -r requirements.txt` (o `-r` quer dizer "leia os pacotes deste arquivo")
instala as três bibliotecas e tudo de que elas dependem.

## As versões

Os mínimos são as versões da saída de exemplo do enunciado (pandas 2.1.0, numpy 1.25.0,
matplotlib 3.7.2): versões com que o programa sabidamente funciona. Acima delas, o pip escolhe a
mais nova que serve para o Python em uso. Essa é a **escolha do tutorial**, e é ela que deixa o
mesmo arquivo funcionar do Python 3.10 ao 3.15: no 3.15 e no 3.14, o pip instala o numpy 2.5; no
3.10, que o numpy 2.5 não aceita, instala o numpy 2.2.

Fixar versões exatas (`numpy==2.5.4`, como as que o `pip freeze` lista) daria a todo mundo o
mesmo resultado, mas quebraria em todo Python em que aquela versão não existe. Guardar as versões
exatas para cada versão de Python é o trabalho do `poetry.lock`
([pip e Poetry](./02-pip-e-poetry.md)).

## O requests

O `requests` é autorizado, mas o programa não o usa, e por isso ele não está na lista: um
`requirements.txt` lista o que o programa precisa, e nada além disso.
