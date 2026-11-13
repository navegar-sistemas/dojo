---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo** ([O Python](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o código e aponta o que foge do
  estilo padrão do Python: linha com mais de 79 caracteres, falta de linha em branco entre
  funções, `import` que não é usado. O código entregue não pode ter nenhum aviso dele (só o
  exercício 1 aceita avisos sobre `import`, do flake8 e do mypy).
- **Type hints em todo o código, conferidos pelo mypy.** Um *type hint* é a anotação do tipo de
  cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o programa que
  confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **O tratamento de exceções protege os dados.** Um erro previsível (uma biblioteca que falta, uma
  configuração ausente, um arquivo que não pode ser gravado) não pode derrubar o programa no meio
  do caminho com uma mensagem incompreensível: o programa o captura e explica o que houve.
- **Tipos e funções embutidos liberados.** Todos os tipos padrão (`int`, `str`, `list`, `dict`...)
  com todos os seus métodos, e todas as funções que o Python oferece sem `import` (`print`, `len`,
  `isinstance`...).
- **Testar em ambientes diferentes**: com e sem ambiente virtual, com e sem as bibliotecas
  instaladas. Cada exercício termina rodando o programa nessas situações.

Cada exercício tem, além disso, a sua lista de **módulos** autorizados (um módulo é um arquivo de
código que entra no programa com `import`).

## Os três exercícios

| Exercício | Entrega | O que o programa precisa fazer | Autorizado |
|---|---|---|---|
| 0 | `construct.py` | detectar se roda dentro de um ambiente virtual; mostrar informações do Python em uso; se não houver venv, ensinar a criar e ativar um; mostrar a diferença entre o lugar onde os pacotes são instalados no Python global e no venv ([Exercício 0](../03-ex0/01-o-problema.md)) | `sys`, `os`, `site`, `print()` |
| 1 | `loading.py`, `requirements.txt`, `pyproject.toml` | analisar "dados da Matrix" gerados com numpy, manipulados com pandas e desenhados num gráfico com matplotlib; ter os arquivos de dependências do pip e do Poetry; detectar quais bibliotecas estão instaladas, mostrar as versões delas e, se faltar alguma, explicar como instalar com o pip e com o Poetry ([Exercício 1](../04-ex1/01-o-problema.md)) | `pandas`, `requests`, `matplotlib`, `numpy`, `sys`, `importlib` |
| 2 | `oracle.py`, `requirements.txt`, `.env.example`, `.gitignore` | ler cinco variáveis de configuração do ambiente e de um arquivo `.env` (com a biblioteca python-dotenv), tratar configuração ausente, mostrar a diferença entre desenvolvimento e produção, e deixar o `.env` fora do Git ([Exercício 2](../05-ex2/01-o-problema.md)) | `os`, `sys`, `python-dotenv`, operações com arquivos |

Para cada exercício, o enunciado mostra uma saída de exemplo. Diferentemente de outros projetos,
essas saídas mudam de máquina para máquina: elas trazem caminhos de pastas e números de versão. A
página [O resultado final](./04-o-resultado-final.md) mostra a saída de cada programa pronto e diz
o que varia.

## Entrega

Os arquivos da tabela, com esses nomes e nessas pastas, num repositório Git. O ambiente virtual
**não** é entregue: quem baixa o projeto cria um novo com `python3 -m venv`. O arquivo `.env`, que
guarda segredos, também não. O objetivo não é só fazer o código funcionar, mas entender o porquê
das ferramentas: por que os ambientes virtuais importam, as diferenças entre o pip e o Poetry,
como as variáveis de ambiente deixam um programa seguro e configurável, e por que o `.env` fica no
`.gitignore` ([Perguntas de revisão](../06-fechamento/03-perguntas-de-revisao.md)).

## O que o enunciado cita sem explicar

- **Pacote** e **dependência**: uma biblioteca instalável, e uma biblioteca de que um programa
  precisa para rodar ([Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md)).
- **Global**: o Python do sistema, fora de qualquer ambiente virtual
  ([O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md)).
- **Ativar** um ambiente virtual: fazer o terminal usar o Python do venv quando se digita
  `python3` ([O ambiente virtual por dentro](../02-conceitos/02-o-ambiente-virtual-por-dentro.md#ativar-e-desativar)).
- **`site-packages`**: a pasta onde o pip instala as bibliotecas de um Python
  ([Pacotes e o pip](../02-conceitos/01-pacotes-e-o-pip.md)).
- **numpy, pandas e matplotlib**: três bibliotecas de análise de dados muito usadas: cálculo com
  listas de números, tabelas e gráficos ([A análise](../04-ex1/07-a-analise.md)). **requests** é
  uma biblioteca para acessar a internet; o enunciado a autoriza, mas ela só é necessária para
  buscar dados de uma API, e o tutorial não busca.
- **API** (*Application Programming Interface*): aqui, um serviço na internet que entrega dados
  a programas.
- **Variável de ambiente**, **`.env`**, **`.gitignore`** e **segredo**
  ([Variáveis de ambiente](../02-conceitos/04-variaveis-de-ambiente.md) e
  [O arquivo .env](../05-ex2/02-o-arquivo-env.md)).
- **Desenvolvimento e produção**: o computador de quem escreve o programa, e o servidor onde ele
  roda de verdade, para os usuários.
- **Pipeline de dados**, **engenharia de dados**, **Zion**, **mainframe**, **Oráculo**: o cenário
  do enunciado. Um *pipeline* de dados é o caminho que os dados percorrem, da origem até o
  resultado; o enunciado usa a palavra para dizer que os três programas são as primeiras peças de
  um sistema assim.
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo, conferido e testado antes de ser usado.
