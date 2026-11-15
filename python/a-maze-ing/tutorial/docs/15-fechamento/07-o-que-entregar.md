---
sidebar_position: 7
title: O que entregar
---

# O que entregar

A entrega é um **repositório Git**: a pasta do projeto com o histórico de versões, enviada para o
servidor de entrega. O enunciado é claro: só o que está dentro do repositório é avaliado, e vale
conferir duas vezes o nome de cada arquivo. Esta página lista o que entra e o que fica de fora;
a [próxima](./09-enviar-e-conferir.md) mostra como enviar e provar, numa cópia nova, que a
entrega funciona sozinha.

## O que entra

A raiz do repositório tem exatamente estes arquivos, com estes nomes:

| Arquivo | O que é |
|---|---|
| `a_maze_ing.py` | o programa; o enunciado exige esse nome |
| `mazegen/` | o gerador reutilizável |
| `amazeing/` | a aplicação: configuração, arquivo de saída, desenho e menu |
| `config.txt` | a configuração padrão, com um comentário antes de cada chave |
| `Makefile` | os atalhos `install`, `run`, `debug`, `clean`, `lint`, `lint-strict` e `build` |
| `pyproject.toml` | a descrição do pacote `mazegen` e de como construí-lo |
| `.flake8` | as pastas que o verificador de estilo flake8 ignora (`.venv`, `build`, `dist`) |
| `.gitignore` | a lista de arquivos gerados que o Git ignora |
| `README.md` | a apresentação do projeto |
| `LICENSE.md` | a licença MIT, com o seu login na linha de copyright |
| `mazegen-1.0.0-py3-none-any.whl` | o pacote pronto para instalar (*wheel*), gerado por `make build` |
| `mazegen-1.0.0.tar.gz` | o pacote com os fontes (*sdist*), gerado por `make build` |

O wheel e o sdist ficam **no repositório**, mesmo sendo gerados: o enunciado exige o arquivo do
pacote na raiz. Ao mesmo tempo, tudo o que é preciso para reconstruí-lo também está lá
(`pyproject.toml`, `mazegen/`, `README.md`, `LICENSE.md`), porque a avaliação o reconstrói
([O roteiro da avaliação](./08-o-roteiro-da-avaliacao.md)).

## O que não entra

O `.gitignore` lista o que é gerado ao rodar ou construir o projeto, e que por isso não vai para
o repositório ([parte 3](../03-ambiente/05-flake8-e-gitignore.md)):

```text
.venv/
__pycache__/
*.pyc
.mypy_cache/
build/
dist/
*.egg-info/
maze.txt
```

- `.venv/` é o ambiente virtual, recriado por `make install` em cada máquina.
- `__pycache__/`, `*.pyc` e `.mypy_cache/` são arquivos que o Python e o mypy criam para ir mais
  rápido na próxima vez.
- `build/`, `dist/` e `*.egg-info/` são restos da construção do pacote; os arquivos que importam
  já foram copiados para a raiz.
- `maze.txt` é o arquivo de saída do `config.txt`, regravado a cada execução.

Também não entram programas de teste: o enunciado sugere escrever testes para conferir o projeto,
mas diz que eles não são entregues nem avaliados.

## Conferir a lista de arquivos

O Git só leva para o servidor os arquivos que ele acompanha. `git add -A` marca para o próximo
registro de versão todos os arquivos da pasta, menos os que o `.gitignore` ignora; depois disso,
`git ls-files` lista exatamente os que o Git acompanha. A
[próxima página](./09-enviar-e-conferir.md) explica o `git add` com calma e registra a versão.

```bash
git add -A
git ls-files
```

```text
.flake8
.gitignore
LICENSE.md
Makefile
README.md
a_maze_ing.py
amazeing/__init__.py
amazeing/domain/__init__.py
amazeing/domain/entities/__init__.py
amazeing/domain/entities/view_state.py
amazeing/domain/value_objects/__init__.py
amazeing/domain/value_objects/generated_maze.py
amazeing/domain/value_objects/maze_config.py
amazeing/errors.py
amazeing/repositories/__init__.py
amazeing/repositories/config_repository.py
amazeing/repositories/maze_repository.py
amazeing/services/__init__.py
amazeing/services/render_service.py
amazeing/ui/__init__.py
amazeing/ui/menu.py
amazeing/use_cases/__init__.py
amazeing/use_cases/generate_maze.py
amazeing/use_cases/ports.py
amazeing/utils/__init__.py
amazeing/utils/ansi.py
amazeing/utils/box.py
amazeing/utils/value_parser.py
config.txt
mazegen-1.0.0-py3-none-any.whl
mazegen-1.0.0.tar.gz
mazegen/__init__.py
mazegen/entities/__init__.py
mazegen/entities/maze.py
mazegen/errors.py
mazegen/generator.py
mazegen/py.typed
mazegen/services/__init__.py
mazegen/services/braider.py
mazegen/services/carver.py
mazegen/services/solver.py
mazegen/value_objects/__init__.py
mazegen/value_objects/cell.py
mazegen/value_objects/direction.py
mazegen/value_objects/pattern42.py
pyproject.toml
```

Confira os nomes letra por letra. Um `a-maze-ing.py` (com hífen) ou um `Readme.md` não é o
arquivo que o avaliador procura.
