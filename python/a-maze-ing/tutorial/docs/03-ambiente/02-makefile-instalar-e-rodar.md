---
sidebar_position: 2
title: "Makefile: instalar e rodar"
---

# Makefile: instalar e rodar

## O que é

O `Makefile` fica na raiz e guarda os comandos do projeto com nomes curtos: `make install`,
`make run`, `make lint`. O subject exige as regras `install`, `run`, `debug`, `clean` e `lint`, e
recomenda `lint-strict`. O projeto acrescenta `build`, que gera o pacote do `mazegen`.

Uma regra tem um nome, dois-pontos e, nas linhas de baixo, os comandos. Cada linha de comando
começa com um **TAB**, nunca com espaços: com espaços, o `make` para com
`missing separator`.

## As variáveis

```makefile
VENV = .venv
PY = $(VENV)/bin/python
```

`$(VENV)` e `$(PY)` são trocados pelo valor na hora de rodar. `PY` vale `.venv/bin/python`, o
Python do ambiente virtual. Toda regra usa `$(PY)`, então o caminho do interpretador aparece num
lugar só.

## `.PHONY`

```makefile
.PHONY: install run debug clean lint lint-strict build
```

Por padrão, o `make` trata o nome da regra como um arquivo a produzir: se já existe um arquivo
ou pasta com esse nome, ele considera a regra feita e não roda nada. As ferramentas de
empacotamento costumam criar uma pasta `build/`, e sem essa linha `make build` responderia
`'build' is up to date`. `.PHONY` diz que essas regras são comandos, não arquivos, e rodam
sempre.

## `install`

```makefile
install:
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --no-cache-dir --upgrade pip
	$(PY) -m pip install --quiet flake8==7.4.1 mypy==2.4.1 build==1.6.1
```

1. Cria o `.venv` com o `python3` do `PATH`. É o único lugar onde o Python do sistema é usado.
2. Atualiza o `pip` de dentro do `.venv`. `--no-cache-dir` não grava nada no cache do usuário.
3. Instala as três ferramentas, com versão fixa.

`$(PY) -m pip` roda o `pip` como módulo do Python do `.venv`; assim não há dúvida sobre qual
`pip` instala. `--quiet` deixa o `pip` mudo, salvo erros e avisos.

As versões fixas (`==`) protegem o "zero warnings": uma versão nova do flake8 ou do mypy pode
trazer uma regra nova e acusar um código que ontem passava. Com a versão presa, o resultado do
lint só muda quando o código muda.

## `run`

```makefile
run:
	$(PY) a_maze_ing.py config.txt
```

Roda o programa com o arquivo de configuração padrão. O subject manda executar
`python3 a_maze_ing.py config.txt`; a regra faz o mesmo com o Python do `.venv`. O
`a_maze_ing.py` só existe a partir da parte 14: até lá, `make run` falha por falta do arquivo.

## `debug`

```makefile
debug:
	$(PY) -m pdb a_maze_ing.py config.txt
```

Roda o mesmo comando dentro do `pdb`, o depurador que vem com o Python, como o subject pede. O
programa para antes da primeira linha e espera ordens:

| Comando | Faz |
|---|---|
| `n` | executa a linha atual |
| `s` | entra na função chamada na linha atual |
| `c` | continua até o fim ou até um ponto de parada |
| `b arquivo:linha` | marca um ponto de parada |
| `p expressão` | imprime um valor |
| `q` | sai |

## Experimente

Com o `Makefile` completo (próxima página) na raiz:

```bash
make install
make -n run debug
```

`make -n` imprime os comandos sem executá-los:

```text
.venv/bin/python a_maze_ing.py config.txt
.venv/bin/python -m pdb a_maze_ing.py config.txt
```
