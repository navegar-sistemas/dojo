---
sidebar_position: 5
title: Glossário
---

# Glossário

| Termo | O que é | Onde |
|---|---|---|
| **`$'\xff'`** | no bash e no zsh, escreve um argumento com um byte que não forma texto em UTF-8, o de valor 255 | [O uso](../03-ex0/02-o-uso.md) |
| **`&&`** | entre dois comandos, roda o segundo só se o primeiro deu certo | [Entregar](../07-fechamento/02-entregar.md) |
| **`*`** | num caminho, vale qualquer sequência de caracteres: `ex0/*.py` são todos os `.py` da pasta `ex0` | [Rodar e conferir do exercício 3](../06-ex3/07-rodar-e-conferir.md) |
| **`..`** | num caminho, a pasta de cima | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **`<(...)`** | entrega a saída de um comando a outro como se fosse um arquivo, por um pipe | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **`<<'FIM'`** | entrega ao comando as linhas seguintes, até a linha `FIM` | [A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md) |
| **`__name__`** | variável que vale `"__main__"` quando o arquivo é rodado e o nome do módulo (o nome do arquivo sem `.py`) quando ele é importado | [O uso](../03-ex0/02-o-uso.md) |
| **ambiente virtual (venv)** | pasta com um Python e bibliotecas só deste projeto; aqui guarda o flake8 e o mypy | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **`apt`** | o instalador de programas do Debian e do Ubuntu | [O Python](../01-ambiente/01-o-python.md) |
| **argumento** | cada palavra do comando que roda o programa; o programa as recebe em `sys.argv` | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **arquivo** | conjunto de dados guardado no disco, com um nome | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **assinatura** | a linha do `def`: nome, parâmetros com tipos e tipo do retorno | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **atributo** | valor guardado num objeto e lido com ponto, como `file.closed` | [O with](../06-ex3/02-o-with.md) |
| **`bool`** | o tipo dos valores `True` e `False` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **buffer** | área de memória onde a escrita espera antes de ir para o destino | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **caminho absoluto** | caminho que começa com `/` e parte da raiz | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **caminho relativo** | caminho que não começa com `/` e parte da pasta atual | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **`cat`** | comando do terminal que imprime o conteúdo de um arquivo; com `-v`, mostra os caracteres invisíveis | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md), [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **chave SSH** | par de arquivos que identifica o seu computador para o serviço que hospeda o repositório `git`, no lugar da senha | [Entregar](../07-fechamento/02-entregar.md) |
| **`chmod`** | comando que muda as permissões de um arquivo | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **classe** | o tipo de um objeto, como `TextIOWrapper` para o objeto arquivo | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **`close()`** | método que fecha o arquivo e despeja o buffer | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **codificação (*encoding*)** | regra que traduz bytes em caracteres; quase sempre UTF-8 | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **código de saída** | número que um programa devolve ao terminar: `0` é sucesso; `echo $?` mostra o do último programa | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **configuração de idioma** | ajuste do sistema que diz idioma e codificação, como `pt_BR.UTF-8`; até o Python 3.14, decide a codificação padrão do `open()` | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **construtor** | o tipo chamado como função para criar um valor dele, como `str(25)` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`cp`** | comando que copia arquivos | [Entregar](../07-fechamento/02-entregar.md) |
| **descritor** | o número de um fluxo: 0 entrada, 1 saída, 2 erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`/dev/full`** | arquivo especial do Linux que simula um disco cheio | [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
| **`/dev/null`** | arquivo especial que descarta tudo o que recebe e, lido, está vazio | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`diff`** | comando que compara duas listas de linhas e mostra só as diferenças | [Rodar e conferir do exercício 0](../03-ex0/06-rodar-e-conferir.md) |
| **`echo`** | comando que imprime um texto | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **enunciado (*subject*)** | o documento oficial que diz o que o projeto deve entregar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`EOFError`** | exceção do `input()` quando a entrada acaba sem nenhum caractere para ler (`Ctrl+D` numa linha vazia, arquivo vazio) | [Pedir o nome](../04-ex1/04-pedir-o-nome.md) |
| **Errno** | número do erro que o sistema operacional devolve, como `[Errno 2]` | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **`/etc/sudoers`** | arquivo de configuração do `sudo` que só o administrador lê; o exemplo de arquivo inacessível | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **exceção** | objeto que descreve um erro, com um tipo e uma mensagem | [Pré-requisitos](./03-pre-requisitos.md) |
| **`finally`** | bloco que roda sempre que o `try` termina, com erro ou sem erro | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **flake8** | ferramenta que confere o estilo do código | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`flush()`** | método que despeja o buffer no destino na hora | [Escrever no stderr](../05-ex2/03-escrever-no-stderr.md) |
| **fluxo (*stream*)** | canal de comunicação do programa: entrada padrão, saída padrão ou saída de erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`for` no terminal** | `for f in ...; do ...; done` repete os comandos entre `do` e `done` para cada nome da lista | [Conferir tudo](../07-fechamento/01-conferir-tudo.md) |
| **f-string** | texto com `f` antes das aspas e valores dentro de `{}`, como `f"Accessing file '{name}'"` | [Pré-requisitos](./03-pre-requisitos.md) |
| **funções autorizadas** | as únicas funções prontas do Python que cada exercício pode chamar | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **gerenciador de contexto** | objeto que sabe o que fazer ao entrar e ao sair de um bloco `with` | [O with](../06-ex3/02-o-with.md) |
| **git** | programa que guarda e envia versões de arquivos; a entrega usa `git clone`, `add`, `commit` e `push` | [O Python](../01-ambiente/01-o-python.md) |
| **`grep`** | comando que procura um texto em arquivos e imprime as linhas em que o acha | [Rodar e conferir do exercício 2](../05-ex2/06-rodar-e-conferir.md) |
| **herdar** | um tipo de exceção herda de outro quando é um caso particular dele; o `except` do tipo de cima captura também os de baixo | [Pré-requisitos](./03-pre-requisitos.md) |
| **`import`** | instrução que traz um módulo para o programa | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **`is`** | compara se dois valores são o mesmo objeto; é o jeito certo de perguntar por `None` | [O main](../04-ex1/06-o-main.md) |
| **`isprintable()`** | método de `str` que diz se todos os caracteres do texto podem ser impressos | [O uso](../03-ex0/02-o-uso.md) |
| **`KeyboardInterrupt`** | exceção lançada quando a pessoa aperta `Ctrl+C` | [Pedir o nome](../04-ex1/04-pedir-o-nome.md) |
| **`ls -l`** | lista arquivos com as permissões, o dono e o grupo | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **mensagem de uso (*usage*)** | a linha que mostra como rodar o programa, como `Usage: ex0/ft_ancient_text.py <file>` | [O uso](../03-ex0/02-o-uso.md) |
| **método** | função que pertence a um valor e é chamada com ponto, como `file.read()` | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **`mkdir`** | comando que cria pastas; com `-p`, não reclama se a pasta já existe | [A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md) |
| **modo de abertura** | segundo argumento do `open()`: `"r"` para ler, `"w"` para escrever | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **módulo** | conjunto de código que vem com o Python e entra no programa com `import`, como `sys` | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **mypy** | ferramenta que confere os tipos anotados no código, sem rodá-lo | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`None`** | o valor que quer dizer "nada" | [Devolver o texto](../04-ex1/02-devolver-o-texto.md) |
| **objeto arquivo** | o que `open()` devolve: representa o arquivo aberto e tem os métodos para usá-lo | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **`OSError`** | tipo das falhas que o sistema operacional devolve; pai de `FileNotFoundError`, `PermissionError` e `IsADirectoryError` | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **pasta (diretório)** | lugar que guarda arquivos e outras pastas | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **pasta atual** | a pasta em que o terminal está; `pwd` a mostra | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **PEP 8** | o guia de estilo padrão do Python, que o flake8 confere | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **permissões** | o que o dono, o grupo e os outros podem fazer com um arquivo: ler, escrever, executar | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **pip** | o instalador de bibliotecas do Python | [O ambiente virtual](../01-ambiente/03-o-ambiente-virtual.md) |
| **pipe (`\|`)** | liga a saída padrão de um comando à entrada padrão do seguinte | [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **`printf`** | comando que imprime um texto; nele, `\n` é uma quebra de linha e `\0`, o caractere nulo | [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **raiz** | a pasta mais de fora de todas, escrita `/` | [Arquivos e caminhos](../02-arquivos/01-arquivos-e-caminhos.md) |
| **ramo (*branch*)** | a sequência de registros em que o `git` está trabalhando, como `master` ou `main` | [Entregar](../07-fechamento/02-entregar.md) |
| **`read()`** | método que lê o arquivo inteiro e devolve um `str` | [read e o texto](../02-arquivos/03-read-e-o-texto.md) |
| **`readline()`** | método que lê uma linha, com o `\n` | [Ler sem input](../05-ex2/04-ler-sem-input.md) |
| **recurso** | algo que o sistema reserva para o programa e precisa ser devolvido, como um arquivo aberto | [close e o recurso](../02-arquivos/04-close-e-o-recurso.md) |
| **redirecionar** | mandar um fluxo para um arquivo ou outro comando, com `>`, `2>`, `<` ou `\|` | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`repr()`** | mostra um valor como ele seria escrito no código, com os caracteres invisíveis à mostra | [read e o texto](../02-arquivos/03-read-e-o-texto.md) |
| **`rm`** | comando que apaga arquivos; com `-rf`, apaga uma pasta com tudo o que há dentro, sem pedir confirmação | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **root** | o administrador do sistema, que lê qualquer arquivo | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md) |
| **`rstrip()`** | método de `str` que tira do fim do texto os caracteres indicados, como o `\n` | [Ler sem input](../05-ex2/04-ler-sem-input.md) |
| **`splitlines()`** | método de `str` que divide o texto em linhas, sem os `\n` | [Transformar o texto](../04-ex1/03-transformar-o-texto.md) |
| **`str \| None`** | type hint de um valor que pode ser um `str` ou `None` | [Devolver o texto](../04-ex1/02-devolver-o-texto.md) |
| **`sudo`** | roda um comando como administrador; pede a sua senha | [O Python](../01-ambiente/01-o-python.md) |
| **`sys.argv`** | lista com o caminho do programa e os argumentos | [Os argumentos do terminal](../02-arquivos/06-os-argumentos-do-terminal.md) |
| **`sys.stdin`, `sys.stdout`, `sys.stderr`** | os três fluxos: entrada padrão, saída padrão e saída de erro | [Os três fluxos](../05-ex2/02-os-tres-fluxos.md) |
| **`tail -n`** | comando que mostra só as últimas linhas da saída: `tail -n 2`, as duas últimas | [Rodar e conferir do exercício 1](../04-ex1/08-rodar-e-conferir.md) |
| **`TextIOWrapper`** | a classe (o tipo) do objeto arquivo aberto em modo texto | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **traceback** | relatório de erro que o Python imprime quando uma exceção não é capturada | [Pré-requisitos](./03-pre-requisitos.md) |
| **travar (*crash*)** | parar no meio com a mensagem de erro do próprio Python, o traceback | [O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md) |
| **tupla** | sequência entre parênteses, como `(True, "ok")` | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **type hint** | anotação do tipo de um parâmetro, variável ou retorno, como `file_name: str` | [Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md) |
| **`typing.IO[str]`** | o type hint de um arquivo aberto que lê e escreve `str` | [open e o objeto arquivo](../02-arquivos/02-open-e-o-objeto-arquivo.md) |
| **`UnicodeDecodeError`** | exceção lançada quando bytes não formam texto: na leitura de um arquivo com `read()` e, até o Python 3.14, na entrada, com `input()` e `readline()`; herda de `ValueError` | [Quando o open falha](../02-arquivos/05-quando-o-open-falha.md), [Pedir o nome](../04-ex1/04-pedir-o-nome.md) |
| **`UnicodeEncodeError`** | exceção lançada quando um texto não pode virar bytes; até o Python 3.14, na configuração de idioma mais comum, o `print` de um argumento com byte inválido a lança | [O uso](../03-ex0/02-o-uso.md) |
| **valor padrão** | valor que um parâmetro recebe quando quem chama não passa nada | [A assinatura](../06-ex3/03-a-assinatura.md) |
| **`ValueError`** | exceção de um valor inválido, como `int("abc")`; o `open()` a lança para um nome com o caractere nulo | [Pré-requisitos](./03-pre-requisitos.md), [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
| **`with`** | instrução que fecha o arquivo sozinha quando o bloco termina | [O with](../06-ex3/02-o-with.md) |
| **`write()`** | método que escreve um `str` no arquivo, sem acrescentar quebra de linha | [Gravar o arquivo](../04-ex1/05-gravar-o-arquivo.md) |
