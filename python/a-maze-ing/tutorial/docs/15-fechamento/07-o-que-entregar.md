---
sidebar_position: 7
title: O que entregar
---

# O que entregar

Só o que está no repositório Git é avaliado. A raiz do repositório de entrega tem exatamente
estes arquivos, com estes nomes:

| Arquivo | O que é |
|---|---|
| `a_maze_ing.py` | o programa; o subject exige esse nome |
| `mazegen/` | o gerador reutilizável |
| `amazeing/` | a aplicação: config, arquivo de saída, desenho e menu |
| `config.txt` | a configuração padrão, com um comentário antes de cada chave |
| `Makefile` | `install`, `run`, `debug`, `clean`, `lint`, `lint-strict` e `build` |
| `pyproject.toml` | metadados e build do pacote `mazegen` |
| `.flake8` | exclusões do flake8 (`.venv`, `build`, `dist`) |
| `.gitignore` | os artefatos do Python que não entram no repositório |
| `README.md` | o README final |
| `LICENSE.md` | a licença MIT, com o seu login no copyright |
| `mazegen-1.0.0-py3-none-any.whl` | o wheel, gerado por `make build` |
| `mazegen-1.0.0.tar.gz` | o sdist, gerado por `make build` |

O wheel e o sdist ficam **versionados**: o subject exige o arquivo do pacote na raiz do
repositório. Ao mesmo tempo, tudo que é preciso para reconstruí-lo também está lá
(`pyproject.toml`, `mazegen/`, `README.md`, `LICENSE.md`), porque a avaliação o reconstrói.

## O que não entra

O `.gitignore` deixa de fora o que é gerado ou pessoal:

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

- `.venv/` é recriado por `make install` em cada máquina.
- `build/`, `dist/` e `*.egg-info/` são restos do build; os arquivos que importam já foram
  copiados para a raiz.
- `maze.txt` é o `OUTPUT_FILE` do `config.txt`, regravado a cada execução.

Também não entram testes: o subject pede programas de teste para verificar o projeto, mas eles
não são submetidos nem avaliados. Se você os escreveu, mantenha-os fora do repositório de
entrega.

## Conferir a árvore

```bash
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

Confira os nomes letra por letra: o subject pede atenção a eles, e um `a-maze-ing.py` ou um
`Readme.md` não é o arquivo que o avaliador procura.

## Rodar a entrega num clone novo

Antes, no seu repositório, `git status --porcelain` não pode imprimir nada: tudo commitado e
enviado. O último passo é fazer o que o avaliador vai fazer, numa pasta nova:

```bash
git clone <url-do-seu-repositório> entrega
cd entrega
make install
make lint
printf '4\n' | make run
```

- `make install` cria o `.venv` do zero e instala as ferramentas.
- `make lint` termina sem nenhuma linha do flake8 e com `Success: no issues found` do mypy.
- `make run` desenha o labirinto, e a opção `4` sai com código 0.

Se algum desses passos depende de algo que só existe na sua máquina (um arquivo ignorado, uma
ferramenta instalada fora do `.venv`), o clone limpo é onde isso aparece.
