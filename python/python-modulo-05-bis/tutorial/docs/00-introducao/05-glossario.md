---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`__all__`** | lista, num módulo ou `__init__.py`, dos nomes que formam a interface pública; o flake8 considera usados os nomes dela | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| **`__init__.py`** | arquivo que transforma uma pasta num pacote; roda no `import` do pacote e cria os nomes da interface dele | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| **`__name__`** | variável que vale `"__main__"` no arquivo rodado com `python3`, e o nome do módulo num arquivo importado | [Módulo e import](../04-conceitos/01-modulo-e-import.md) |
| **`__pycache__`** | pasta de cache que o Python cria ao importar um módulo; não é entregue | [Módulo e import](../04-conceitos/01-modulo-e-import.md#a-pasta-__pycache__) |
| **`__version__`** | atributo em que quase toda biblioteca guarda a sua versão | [loading.py](../02-ex0/08-loading.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só de um projeto, separada do Python global | [O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md) |
| **ambiente global** | o Python do sistema, fora de qualquer ambiente virtual | [O problema do exercício 0](../02-ex0/01-o-problema.md) |
| **ativar** | `source lab_env/bin/activate`: faz `python3` e `pip` serem os do ambiente naquele terminal | [Ativar o ambiente](../02-ex0/03-ativar-o-ambiente.md) |
| **atributo** | nome guardado dentro de um objeto, lido com ponto, como `sigil.WORD` | [Módulo e import](../04-conceitos/01-modulo-e-import.md) |
| **`AttributeError`** | exceção de um nome que não existe no objeto, como `alchemy.create_earth` | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| **biblioteca externa** | código de outras pessoas que precisa ser instalado, como `pandas` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **chave de API** | a senha que um programa usa para falar com outro serviço; aqui, `API_KEY` | [O problema do exercício 1](../03-ex1/01-o-problema.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Instalar com o pip](../02-ex0/10-instalar-com-pip.md) |
| **constante** | valor fixo do programa, com nome em maiúsculas, como `REAGENTS` | [loading.py](../02-ex0/08-loading.md) |
| **dependência** | biblioteca de que o projeto precisa para rodar | [O problema do exercício 0](../02-ex0/01-o-problema.md) |
| **dependência circular (import circular)** | dois módulos que importam um ao outro | [O import circular](../04-conceitos/05-o-import-circular.md) |
| **dependência transitiva** | biblioteca de que uma dependência depende, instalada junto | [pip e requirements.txt](../02-ex0/06-pip-e-requirements.md) |
| **desenvolvimento e produção** | o computador de quem escreve o programa, com dados de teste, e o lugar onde ele roda de verdade | [O problema do exercício 1](../03-ex1/01-o-problema.md) |
| **`diff`** | comando que compara dois textos linha a linha e mostra só as diferenças | [Rodar e conferir do exercício 0](../02-ex0/12-rodar-e-conferir.md) |
| **`.env`** | arquivo de texto com variáveis de ambiente, `NOME=valor`, lido pelo `python-dotenv` | [O arquivo .env e o python-dotenv](../03-ex1/03-o-arquivo-env-e-o-python-dotenv.md) |
| **`.env.example`** | modelo do `.env`, com os segredos em branco, que vai para o repositório | [O .gitignore e o .env.example](../03-ex1/04-o-gitignore.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **especificador de versão** | o trecho depois do nome da biblioteca que diz as versões aceitas, como `>=2.1` | [pip e requirements.txt](../02-ex0/06-pip-e-requirements.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`.gitignore`** | arquivo com os nomes que o git deve ignorar | [O .gitignore e o .env.example](../03-ex1/04-o-gitignore.md) |
| **import absoluto** | import pelo caminho completo a partir de uma pasta do `sys.path`, como `from alchemy.potions import ...` | [Absoluto e relativo](../04-conceitos/04-absoluto-e-relativo.md) |
| **import relativo** | import a partir do pacote do próprio arquivo, com pontos, como `from .elements import ...` | [Absoluto e relativo](../04-conceitos/04-absoluto-e-relativo.md) |
| **`importlib.import_module`** | função que importa um módulo a partir do nome num texto | [loading.py](../02-ex0/08-loading.md) |
| **`ImportError`** | exceção de um import que achou o módulo mas não o nome pedido; `ModuleNotFoundError` é um tipo dela | [O import circular](../04-conceitos/05-o-import-circular.md) |
| **interface de um pacote** | os nomes que existem direto no pacote, alcançados com `pacote.nome` | [O \_\_init\_\_.py de alchemy](../05-ex2/03-o-init-de-alchemy.md) |
| **`load_dotenv`** | função do `python-dotenv` que carrega um `.env` em `os.environ`, sem trocar o que já existe | [O arquivo .env e o python-dotenv](../03-ex1/03-o-arquivo-env-e-o-python-dotenv.md) |
| **módulo** | arquivo `.py` usado por outro com `import`; o nome é o do arquivo sem o `.py` | [Módulo e import](../04-conceitos/01-modulo-e-import.md) |
| **`ModuleNotFoundError`** | exceção de um import que não achou o módulo em nenhuma pasta do `sys.path` | [Onde o Python procura](../04-conceitos/02-onde-o-python-procura.md) |
| **módulo parcialmente inicializado** | módulo que já está em `sys.modules` mas cujo arquivo ainda não terminou de rodar | [O import circular](../04-conceitos/05-o-import-circular.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`os.environ`** | dicionário com as variáveis de ambiente que o programa recebeu | [Variáveis de ambiente](../03-ex1/02-variaveis-de-ambiente.md) |
| **pacote** | pasta de módulos com um `__init__.py` | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| **`PATH`** | lista de pastas onde o terminal procura os programas | [Ativar o ambiente](../02-ex0/03-ativar-o-ambiente.md) |
| **pip** | o instalador de bibliotecas do Python | [pip e requirements.txt](../02-ex0/06-pip-e-requirements.md) |
| **Poetry** | gerenciador de dependências que grava as versões exatas no `poetry.lock` e cria o ambiente do projeto | [Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md) |
| **`poetry.lock`** | arquivo do Poetry com a versão exata de cada biblioteca resolvida | [Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md#o-poetrylock) |
| **`pyproject.toml`** | arquivo de configuração padrão de projetos Python, escrito em TOML | [Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md) |
| **PyPI** | o repositório público de bibliotecas Python, de onde o `pip` baixa | [pip e requirements.txt](../02-ex0/06-pip-e-requirements.md) |
| **`python-dotenv`** | biblioteca que lê arquivos `.env`; importada como `dotenv` | [O arquivo .env e o python-dotenv](../03-ex1/03-o-arquivo-env-e-o-python-dotenv.md) |
| **`requirements.txt`** | arquivo com as dependências de um projeto, uma por linha, lido pelo `pip` | [pip e requirements.txt](../02-ex0/06-pip-e-requirements.md) |
| **saída padrão e saída de erros** | os dois canais de texto de um programa; o `print` vai para o primeiro, o traceback para o segundo | [ft_alembic_1.py](../05-ex2/05-ft-alembic-1.md) |
| **`site-packages`** | pasta onde as bibliotecas de um Python (ou de um ambiente) são instaladas | [O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md) |
| **subpacote** | pacote dentro de outro pacote, como `alchemy.transmutation` | [Pacote e \_\_init\_\_.py](../04-conceitos/03-pacote-e-init.md) |
| **`sys.base_prefix`** | a pasta do Python global de onde o ambiente veio | [O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md) |
| **`sys.executable`** | o caminho do executável do Python em uso | [construct.py](../02-ex0/04-construct.md) |
| **`sys.modules`** | dicionário dos módulos já carregados; um módulo entra nele antes de o arquivo rodar | [O import circular](../04-conceitos/05-o-import-circular.md) |
| **`sys.path`** | lista das pastas onde o Python procura os módulos; a primeira é a pasta do programa rodado | [Onde o Python procura](../04-conceitos/02-onde-o-python-procura.md) |
| **`sys.prefix`** | a pasta do ambiente em uso; igual a `sys.base_prefix` fora de um ambiente virtual | [O ambiente virtual por dentro](../02-ex0/02-o-ambiente-virtual-por-dentro.md) |
| **TOML** | formato de texto para configuração, com seções `[nome]` e linhas `chave = valor` | [Poetry e pyproject.toml](../02-ex0/07-poetry-e-pyproject.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `name: str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **valor padrão** | valor usado quando uma configuração falta; no Oráculo, sempre com um aviso | [Ler a configuração](../03-ex1/05-ler-a-configuracao.md) |
| **variável de ambiente** | par nome e valor que o terminal entrega a todo programa que inicia | [Variáveis de ambiente](../03-ex1/02-variaveis-de-ambiente.md) |
