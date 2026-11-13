---
sidebar_position: 4
title: O pyproject.toml
---

# O pyproject.toml

O `pyproject.toml` é o arquivo padrão de descrição de um projeto Python: nome, versão, versões de
Python aceitas e dependências. O Poetry lê as dependências dele. Crie `ex1/pyproject.toml`:

```toml title="ex1/pyproject.toml"
[project]
name = "loading"
version = "0.1.0"
description = "Matrix data analysis"
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.1.0",
    "numpy>=1.25.0",
    "matplotlib>=3.7.2",
]

[tool.poetry]
package-mode = false
```

## O formato TOML

O arquivo é escrito em **TOML** (*Tom's Obvious Minimal Language*), um formato de texto para
configuração:

- `[project]` abre uma **tabela**: um grupo de chaves com nome. Tudo o que vem abaixo, até a
  próxima tabela, pertence a ela;
- `chave = valor` define uma chave. Textos vão entre aspas; `false` e `true` são booleanos;
- `[ ... ]` depois de um `=` é uma lista, que pode ocupar várias linhas, com vírgula depois de
  cada item;
- `[tool.poetry]` é a tabela `poetry` dentro da tabela `tool`, onde cada ferramenta guarda as suas
  opções.

## A tabela project

- `name`: o nome do projeto. O Poetry o usa no nome do ambiente virtual que cria;
- `version`: a versão do projeto. `0.1.0` é o costume para um projeto que está começando;
- `description`: uma frase sobre o projeto;
- `requires-python = ">=3.10"`: as versões de Python aceitas, as mesmas do enunciado. O Poetry usa
  essa faixa ao resolver as dependências: ele escolhe versões das bibliotecas para **cada**
  versão de Python da faixa e grava todas no `poetry.lock`
  ([Rodar com o Poetry](./11-rodar-com-poetry.md));
- `dependencies`: as mesmas três restrições do `requirements.txt`, cada uma entre aspas. Os dois
  arquivos dizem a mesma coisa, cada um no formato da sua ferramenta.

## package-mode = false

Por padrão, o Poetry trata o projeto como um **pacote** a ser publicado, e o `poetry install`
também tenta instalar o próprio projeto no ambiente, procurando uma pasta com o código dele. O
`loading.py` é um programa solto, e não uma biblioteca para outros usarem. `package-mode = false`
diz ao Poetry que ele só gerencia as dependências, sem instalar o projeto.

## O que não está no arquivo

O Poetry precisa da versão 2 ou mais nova para ler as dependências da tabela `[project]`; versões
antigas só liam uma tabela própria, `[tool.poetry.dependencies]`. Por isso o `.venv` das
ferramentas tem o `poetry>=2` ([As ferramentas](../01-ambiente/03-as-ferramentas.md)).

O comando `poetry check` confere se o arquivo está bem escrito; ele é rodado em
[Rodar com o Poetry](./11-rodar-com-poetry.md).
