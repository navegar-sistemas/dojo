---
sidebar_position: 6
title: Reconstruir o pacote
---

# Reconstruir o pacote

O enunciado exige que o gerador reutilizável seja entregue como um **pacote Python**: um arquivo
chamado `mazegen-...`, na raiz do repositório, que se instala com `pip install`. Este projeto
entrega dois, `mazegen-1.0.0-py3-none-any.whl` (o *wheel*, pronto para instalar) e
`mazegen-1.0.0.tar.gz` (o *sdist*, os fontes empacotados), criados pelo `make build`
([parte 9](../09-gerador/08-o-pacote.md)). Eles precisam ser gerados de novo **depois** do
README final. Esta página mostra por quê, como gerar e como conferir o resultado.

## Por que gerar de novo

O `pyproject.toml` declara `readme = "README.md"`. Ao gerar o pacote, o README inteiro é copiado
para dentro dele, como a descrição longa (no arquivo `METADATA` do wheel e no `PKG-INFO` do
sdist). Um wheel gerado antes do README final carrega o README antigo.

O mesmo vale para qualquer mudança no `mazegen/` depois do último build: o wheel na raiz precisa
ter exatamente o código entregue.

## `make build`

Na raiz do projeto:

```bash
make build
```

A regra `build` do `Makefile` ([parte 9](../09-gerador/08-o-pacote.md)) faz três coisas:

1. apaga a pasta `dist/`, onde ficam os pacotes gerados, para não sobrar nenhum antigo;
2. roda `python -m build`, a ferramenta oficial que gera o sdist e o wheel. Ela trabalha num
   ambiente separado, criado só para isso, onde baixa e instala o `setuptools`, a biblioteca que
   de fato monta o pacote seguindo o `pyproject.toml`;
3. copia os dois arquivos de `dist/` para a raiz do projeto.

O fim da saída:

```text
adding 'mazegen-1.0.0.dist-info/licenses/LICENSE.md'
adding 'mazegen-1.0.0.dist-info/METADATA'
adding 'mazegen-1.0.0.dist-info/WHEEL'
adding 'mazegen-1.0.0.dist-info/top_level.txt'
adding 'mazegen-1.0.0.dist-info/RECORD'
removing build/bdist.macosx-26.0-arm64/wheel
Successfully built mazegen-1.0.0.tar.gz and mazegen-1.0.0-py3-none-any.whl
cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .
```

O nome da pasta temporária `build/bdist...` muda com o sistema operacional; o resto é igual. A
saída não pode ter nenhuma linha de `warning` (aviso).

## Conferir o wheel

Um wheel é um arquivo zip com outra extensão. `unzip -l` lista o que há dentro sem extrair nada:

```bash
unzip -l mazegen-1.0.0-py3-none-any.whl
```

```text
mazegen/__init__.py
mazegen/errors.py
mazegen/generator.py
mazegen/py.typed
mazegen/entities/__init__.py
mazegen/entities/maze.py
mazegen/services/__init__.py
mazegen/services/braider.py
mazegen/services/carver.py
mazegen/services/solver.py
mazegen/value_objects/__init__.py
mazegen/value_objects/cell.py
mazegen/value_objects/direction.py
mazegen/value_objects/pattern42.py
mazegen-1.0.0.dist-info/licenses/LICENSE.md
mazegen-1.0.0.dist-info/METADATA
mazegen-1.0.0.dist-info/WHEEL
mazegen-1.0.0.dist-info/top_level.txt
mazegen-1.0.0.dist-info/RECORD
```

(A saída do `unzip` tem também tamanhos e datas; aqui ficaram só os nomes.) Só entrou o
`mazegen`, mais a pasta `mazegen-1.0.0.dist-info` com os dados do pacote. Nada de `amazeing/`,
`a_maze_ing.py` ou `config.txt`: a aplicação não faz parte do módulo reutilizável.

Para conferir que o README novo está lá dentro, procure a primeira linha dele no arquivo
`METADATA`, a ficha do pacote:

```bash
unzip -p mazegen-1.0.0-py3-none-any.whl mazegen-1.0.0.dist-info/METADATA | grep -n 'This project'
```

`unzip -p` escreve na tela o conteúdo de um arquivo de dentro do zip, sem extrair nada. O
`grep -n 'This project'` mostra só as linhas que contêm essa palavra, com o número da linha na
frente:

```text
12:*This project has been created as part of the 42 curriculum by macoelho.*
```

As 11 primeiras linhas do `METADATA` são os dados do pacote (nome, versão, autor, licença...);
a cópia do README começa na linha 12, com a frase exigida pelo enunciado e o seu login.

Na avaliação, o aluno reconstrói o pacote a partir dos fontes, a pedido do avaliador; o roteiro
está em [O roteiro da avaliação](./08-o-roteiro-da-avaliacao.md), a última página desta parte.
