---
sidebar_position: 6
title: pip e requirements.txt
---

# pip e requirements.txt

O laboratório está selado e vazio. Os reagentes do enunciado são duas bibliotecas externas:

- **`pandas`**: tabelas de dados, como planilhas, dentro do Python;
- **`numpy`**: contas rápidas com listas grandes de números.

O projeto não usa nenhuma das duas para calcular nada: `loading.py` só confere se estão
instaladas e mostra as versões. O assunto é **como** elas chegam ao ambiente, e como dizer a
outra pessoa quais bibliotecas o projeto precisa.

## O pip

O **pip** é o instalador de bibliotecas que vem com o Python. Ele baixa as bibliotecas do
**PyPI** (*Python Package Index*, [pypi.org](https://pypi.org)), o repositório público de
bibliotecas Python, e as instala na pasta `site-packages` do Python que o roda. Com o `lab_env`
ativado, o `pip` é o do ambiente:

```bash
pip --version
```

```text
pip 26.1.1 from /path/to/the-codex/lab_env/lib/python3.14/site-packages/pip (python 3.14)
```

O caminho mostra de onde o `pip` vem, e portanto para onde ele instala: o `lab_env`. Se aparecer
outro caminho, o ambiente não está ativado ([Ativar o ambiente](./03-ativar-o-ambiente.md)).

O `pip` que vem num ambiente novo costuma ser mais velho que o mais recente, e cada instalação
termina com um aviso `[notice] A new release of pip is available`. Atualizá-lo uma vez acaba com o
aviso:

```bash
python3 -m pip install --upgrade pip
```

A última linha da saída é `Successfully installed pip-` seguido do número da versão nova
(`pip-26.3`, aqui). `python3 -m pip` é o mesmo `pip`, chamado pelo Python do ambiente; é o jeito
recomendado de atualizar o próprio `pip`.

## O requirements.txt

Instalar à mão, biblioteca por biblioteca, não deixa registro do que o projeto precisa. O
`requirements.txt` é esse registro: um arquivo de texto com uma dependência por linha, que o `pip`
sabe ler. Crie `ex0/requirements.txt`:

```text title="ex0/requirements.txt"
pandas>=2.1
numpy>=1.25
```

Cada linha é o nome da biblioteca no PyPI e, opcionalmente, um **especificador de versão**:

| Especificador | Aceita |
|---|---|
| `pandas` | qualquer versão |
| `pandas>=2.1` | a 2.1 ou qualquer mais nova |
| `pandas==2.1.0` | só a 2.1.0, exatamente |
| `pandas>=2.1,<3` | da 2.1 até antes da 3 |

Os mínimos `2.1` e `1.25` são as versões da saída de exemplo do enunciado. Usar `>=` em vez de
`==` é escolha do tutorial: cada versão de uma biblioteca só instala nas versões do Python que
existiam na época dela, e a `pandas` 2.1.0 não tem pacote pronto para os Pythons mais novos. Com
`>=`, o `pip` escolhe uma versão que funciona no Python de quem instala, do 3.10 ao mais novo.

O `numpy` aparece na lista mesmo sendo instalado junto com a `pandas`, que depende dele: o
`loading.py` importa o `numpy` diretamente, e cada biblioteca que o código importa é declarada,
sem contar com a dependência de outra.

## O que o pip faz com o arquivo

`pip install -r ex0/requirements.txt` lê o arquivo e, **na hora de instalar**, escolhe a versão
mais nova de cada biblioteca que cumpre o especificador, junto com as **dependências
transitivas**: as bibliotecas de que as bibliotecas dependem (a `pandas` precisa de outras, além
do `numpy`). O arquivo diz **o que** instalar; a versão exata depende do dia e da máquina. É a
primeira frase da comparação que `loading.py` imprime:

```text
requirements.txt declares what to install; pip resolves it at install time.
```

A instalação em si fica para depois de escrever o `loading.py`, para ver o programa primeiro sem
as bibliotecas ([Instalar com o pip](./10-instalar-com-pip.md)).
