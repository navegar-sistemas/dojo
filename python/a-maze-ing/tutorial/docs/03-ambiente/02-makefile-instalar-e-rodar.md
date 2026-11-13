---
sidebar_position: 3
title: "Makefile: instalar e rodar"
---

# Makefile: instalar e rodar

O `Makefile` guarda os comandos do projeto como atalhos: cada **regra** é um nome seguido de
comandos, e `make <nome>` roda esses comandos
([página anterior](./10-o-que-e-um-makefile.md)). Esta página escreve as três primeiras regras:
`install`, que cria o ambiente virtual e instala as ferramentas, `run`, que roda o programa, e
`debug`, que o roda passo a passo. Cada trecho entra no fim do arquivo `Makefile`, na ordem em
que aparece.

## As variáveis

```makefile
VENV = .venv
PY = $(VENV)/bin/python
```

Um `Makefile` pode ter variáveis: `NOME = valor` define, e `$(NOME)` é trocado pelo valor na
hora de rodar. Aqui, `PY` vale `.venv/bin/python`, o Python do ambiente virtual (explicado na
[primeira página desta parte](./01-o-ambiente-virtual.md)). Toda regra usa `$(PY)`, então o caminho do
Python aparece num lugar só.

## `.PHONY`

```makefile
.PHONY: install run debug clean lint lint-strict build
```

O `make` nasceu para compilar programas, e por isso trata o alvo como o **nome de um arquivo**
que a regra produz. Se já existe um arquivo ou pasta com aquele nome, ele conclui que a regra já
foi feita e não roda nada.

Isso atrapalha aqui: o empacotamento cria uma pasta `build/`, e sem esta linha `make build`
responderia `'build' is up to date` sem fazer nada. A linha `.PHONY` lista os alvos que **não**
são arquivos, e sim comandos, e que por isso rodam sempre.

## `install`

```makefile
install:
	python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --no-cache-dir --upgrade pip
	$(PY) -m pip install --quiet flake8==7.4.1 mypy==2.4.1 build==1.6.1
```

1. Cria o `.venv` com o `python3` do sistema. É o único lugar onde o Python do sistema é usado.
2. Atualiza o próprio `pip` de dentro do `.venv` (`--upgrade pip`), porque o `pip` que vem num
   ambiente novo costuma ser antigo.
3. Instala as três ferramentas.

As opções do `pip`:

- `--quiet`: não imprime o progresso, só erros e avisos;
- `--no-cache-dir`: não guarda os arquivos baixados na pasta de cache do usuário, uma pasta fora
  do projeto onde o `pip` guarda o que baixa para não baixar de novo.

O `--no-cache-dir` aparece só na linha que atualiza o `pip`, e isso é uma escolha do projeto. O
`pip` novo é baixado uma vez para dentro do `.venv` e não precisa ficar guardado em outro lugar.
Na linha das três ferramentas, o cache ajuda: depois de apagar o `.venv`, um novo
`make install` reaproveita os arquivos já baixados em vez de baixá-los de novo.

O `==7.4.1` fixa a versão exata de cada ferramenta. É uma escolha do projeto, que protege o
"zero avisos" do lint: uma versão nova do flake8 ou do mypy pode trazer uma regra nova e acusar
um código que ontem passava. Com a versão presa, o resultado do lint só muda quando o código
muda.

## `run`

```makefile
run:
	$(PY) a_maze_ing.py config.txt
```

Roda o programa com o arquivo de opções padrão. O enunciado manda executar
`python3 a_maze_ing.py config.txt`; a regra faz o mesmo com o Python do `.venv`.

O `a_maze_ing.py` só é escrito na [parte 14](../14-menu-e-main/04-o-composition-root.md): até lá,
`make run` falha porque o arquivo não existe.

## `debug`

```makefile
debug:
	$(PY) -m pdb a_maze_ing.py config.txt
```

Roda o mesmo comando dentro do `pdb`, o **depurador** que vem com o Python: um programa que
executa o seu código passo a passo e deixa parar em qualquer ponto para olhar o valor das
variáveis. O programa para antes da primeira linha e espera ordens:

| Comando | Faz |
|---|---|
| `n` | executa a linha atual e para na próxima |
| `s` | entra na função chamada na linha atual |
| `c` | continua até o fim ou até um ponto de parada |
| `b arquivo:linha` | marca um ponto de parada naquela linha |
| `p expressão` | imprime o valor de uma expressão, como `p config.width` |
| `q` | sai |

## Experimente

Com os trechos desta página no `Makefile`, na raiz do projeto:

```bash
make install
make -n run debug
```

O `make install` precisa de internet e leva alguns segundos. Ele imprime cada comando antes de
rodá-lo, e o `--quiet` cala o `pip`:

```text
python3 -m venv .venv
.venv/bin/python -m pip install --quiet --no-cache-dir --upgrade pip
.venv/bin/python -m pip install --quiet flake8==7.4.1 mypy==2.4.1 build==1.6.1
```

`make -n` imprime os comandos que rodaria, sem executá-los. Dá para ver as variáveis já trocadas
pelo valor:

```text
.venv/bin/python a_maze_ing.py config.txt
.venv/bin/python -m pdb a_maze_ing.py config.txt
```
