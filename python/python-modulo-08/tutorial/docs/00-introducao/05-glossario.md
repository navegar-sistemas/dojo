---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`.env`** | arquivo com variáveis de configuração no formato `NOME=valor`, carregado pelo programa ao iniciar; guarda segredos e não vai para o repositório | [O arquivo .env](../05-ex2/02-o-arquivo-env.md) |
| **`.env.example`** | modelo do `.env`, com as mesmas variáveis e sem os segredos; vai para o repositório | [Os arquivos de apoio](../05-ex2/03-os-arquivos-de-apoio.md) |
| **`.gitignore`** | arquivo com os nomes que o Git deve ignorar | [Os arquivos de apoio](../05-ex2/03-os-arquivos-de-apoio.md) |
| **`.mypy_cache`** | pasta que o mypy cria onde roda, para conferir mais rápido da próxima vez | [A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md) |
| **`__file__`** | variável com o caminho do arquivo Python que está rodando | [A conferência de segurança](../05-ex2/06-a-conferencia-de-seguranca.md) |
| **`__version__`** | atributo onde a maioria das bibliotecas guarda o número da própria versão | [Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md) |
| **ambiente (de um programa)** | o conjunto de variáveis `NOME=valor` que um programa recebe ao começar | [Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md) |
| **ambiente virtual (venv)** | pasta com um Python e um `site-packages` só de um projeto | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md) |
| **`Any`** | type hint que quer dizer "qualquer tipo"; o mypy aceita qualquer uso | [Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md) |
| **API** | serviço na internet que entrega dados a programas | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **array** | lista de números do numpy, em que as contas valem para todos os itens de uma vez | [A análise](../04-ex1/07-a-analise.md) |
| **ativar (um venv)** | `source .../bin/activate`: faz `python3` e `pip` serem os do venv neste terminal | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar) |
| **barra invertida** | o caractere `\`, que num texto Python começa um código especial; `\\` é a barra em si | [Fora do venv](../03-ex0/03-fora-do-venv.md) |
| **cache (do Poetry)** | pasta de dados do Poetry, fora do projeto, onde ficam os ambientes que ele cria | [Rodar com o Poetry](../04-ex1/11-rodar-com-poetry.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `$?` mostra o do último comando | [Pré-requisitos](./03-pre-requisitos.md#o-código-de-saída) |
| **constante** | valor fixo do programa, com nome em maiúsculas, como `OUTPUT` | [Conferir as dependências](../04-ex1/05-conferir-as-dependencias.md) |
| **`DataFrame`** | tabela do pandas: colunas com nome e linhas numeradas pelo índice | [A análise](../04-ex1/07-a-analise.md) |
| **dependência** | biblioteca de que um programa (ou outra biblioteca) precisa para rodar | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md) |
| **desenvolvimento** | o computador de quem escreve o programa | [Desenvolvimento e produção](../05-ex2/07-desenvolvimento-e-producao.md) |
| **`diff`** | comando que compara dois textos e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **`export`** | comando do terminal que cria uma variável para todos os comandos seguintes | [Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **global (Python)** | o Python do sistema, fora de qualquer ambiente virtual | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md) |
| **hardcoded** | escrito direto no código, como um segredo num texto do programa | [A conferência de segurança](../05-ex2/06-a-conferencia-de-seguranca.md) |
| **`ImportError`** | erro de um `import` que falha; `ModuleNotFoundError` é um tipo dele | [Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md) |
| **`importlib.import_module`** | importa um módulo pelo nome, escrito num texto, e o devolve | [Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md) |
| **local / remoto** | banco de dados na própria máquina (`localhost`, SQLite) ou em outra, na rede | [Mostrar a configuração](../05-ex2/05-mostrar-a-configuracao.md) |
| **lock (`poetry.lock`)** | arquivo do Poetry com a versão exata de cada pacote, para cada versão de Python | [pip e Poetry](../04-ex1/02-pip-e-poetry.md) |
| **log** | mensagem que um programa registra sobre o que faz; o nível (`DEBUG`, `WARNING`...) diz quanto ele registra | [O problema do exercício 2](../05-ex2/01-o-problema.md) |
| **média móvel** | média de uma janela de valores que anda pela série; aqui, dos 50 pontos até cada um | [A análise](../04-ex1/07-a-analise.md) |
| **módulo** | arquivo de código que entra no programa com `import` | [Pré-requisitos](./03-pre-requisitos.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`NaN`** | "não é um número": o valor de uma conta que não tem resultado, como a média de dados que faltam | [A análise](../04-ex1/07-a-analise.md) |
| **override (sobreposição)** | variável do ambiente que vale mais que o valor do `.env` | [A conferência de segurança](../05-ex2/06-a-conferencia-de-seguranca.md) |
| **pacote** | biblioteca com nome e versão, pronta para ser instalada | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md) |
| **`PATH`** | variável com a lista de pastas onde o terminal procura os comandos | [Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md) |
| **pip** | o instalador de pacotes que vem com o Python e com todo ambiente virtual | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md) |
| **Poetry** | gerenciador de projetos: resolve e trava as versões e cria o ambiente do projeto | [pip e Poetry](../04-ex1/02-pip-e-poetry.md) |
| **produção** | o servidor onde o programa roda de verdade, para os usuários | [Desenvolvimento e produção](../05-ex2/07-desenvolvimento-e-producao.md) |
| **prompt** | o começo da linha onde se digita no terminal; mostra o venv ativado entre parênteses | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar) |
| **`pyproject.toml`** | arquivo padrão de descrição de um projeto Python, lido pelo Poetry | [O pyproject.toml](../04-ex1/04-o-pyproject-toml.md) |
| **PyPI** | o repositório público de pacotes Python, de onde o pip baixa | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md) |
| **`pyvenv.cfg`** | arquivo que transforma uma pasta num ambiente virtual | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md) |
| **registro (*commit*)** | versão dos arquivos guardada no histórico de um repositório Git, com uma mensagem, um autor e um código | [Entregar](../06-fechamento/02-entregar.md#o-autor-dos-registros) |
| **repositório** | pasta cujo histórico de versões é guardado pelo Git, com uma cópia num serviço de hospedagem | [O Python](../01-ambiente/01-o-python.md#o-git) |
| **`requirements.txt`** | lista de dependências no formato do pip, uma por linha | [O requirements.txt](../04-ex1/03-o-requirements-txt.md) |
| **restrição de versão** | limite para as versões aceitas de um pacote, como `>=1.25.0` | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md#versões) |
| **segredo** | valor que não pode ser público, como uma senha ou uma chave de API | [O problema do exercício 2](../05-ex2/01-o-problema.md) |
| **semente (*seed*)** | número que fixa a sequência de um gerador de números aleatórios | [A análise](../04-ex1/07-a-analise.md) |
| **`site-packages`** | pasta onde o pip instala os pacotes de um Python | [Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md) |
| **`source`** | roda um script dentro do terminal atual, como o `activate` | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar) |
| **stub** | arquivo só com os type hints de uma biblioteca | [Importar pelo nome](../02-conceitos/03-importar-pelo-nome.md) |
| **`sys.prefix` / `sys.base_prefix`** | a pasta do ambiente em uso / a do Python global de onde ele veio; diferentes só dentro de um venv | [O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#o-python-sabe-onde-está) |
| **TOML** | formato de texto para configuração, com tabelas `[nome]` e chaves `chave = valor` | [O pyproject.toml](../04-ex1/04-o-pyproject-toml.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `name: str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **variável de ambiente** | par `NOME=valor` do ambiente de um programa, lido com `os.getenv` | [Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md) |
