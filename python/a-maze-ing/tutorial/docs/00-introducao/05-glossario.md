---
sidebar_position: 5
title: Glossário
---

# Glossário

Ao longo do tutorial aparecem muitos termos novos: do labirinto, das contas com bits, do Python,
das ferramentas e da arquitetura. Cada página explica os seus, mas um termo explicado lá atrás
pode ser esquecido. Esta página reúne os termos, cada um com uma frase e o link para a página que
o explica em detalhe.

## O labirinto

| Termo | Significado |
|---|---|
| **grade** | o retângulo de células que forma o labirinto, com `WIDTH` colunas e `HEIGHT` linhas. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **célula** | um quadradinho da grade. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **lado** | cada uma das quatro bordas de uma célula: **Norte** (em cima), **Leste** (à direita), **Sul** (embaixo) e **Oeste** (à esquerda). [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **parede** | um lado fechado: não dá para passar por ali. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **passagem** | um lado aberto entre duas células vizinhas: dá para andar de uma para a outra. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **borda** | os lados que dão para fora da grade; são sempre paredes, inclusive na entrada e na saída. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **coordenada `x,y`** | o endereço de uma célula: `x` é a posição na horizontal (a coluna) e `y` na vertical (a linha), contando de 0 a partir do canto de cima à esquerda; no código, `grid[y][x]`. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **vizinha** | a célula colada a outra por um dos quatro lados; uma célula da borda tem menos vizinhas. [Veja](../05-maze/03-vizinhos.md) |
| **coerência** | a regra de que duas células vizinhas concordam sobre a parede que dividem. [Veja](../01-o-problema/01-a-grade-e-as-celulas.md) |
| **entrada e saída** | duas células escolhidas no arquivo de opções; o caminho mais curto vai de uma à outra. [Veja](../01-o-problema/03-o-arquivo-de-configuracao.md) |
| **corredor** | uma célula livre do labirinto, que dá para alcançar andando; só as células do "42" não são corredores. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **o "42"** | o número 42 desenhado no meio do labirinto por 18 células com as quatro paredes fechadas, fora do labirinto. [Veja](../01-o-problema/06-o-padrao-42.md) |
| **beco sem saída** | uma célula com uma única abertura: quem entra só sai por onde entrou. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **beco real** | um beco que tem pelo menos uma parede dando para uma célula livre, e que por isso dá para abrir; é o que conta na regra "no máximo dois becos". [Veja](../08-braider/01-becos-sem-saida.md) |
| **beco cercado** | um beco em que todas as paredes fechadas dão para a borda da grade ou para o "42": não há parede que dê para abrir, e ele não conta como beco real. Exemplo: as duas células dentro das curvas do "2", cercadas pelo "42" em três lados, que todo "42" cria. [Veja](../08-braider/01-becos-sem-saida.md) |
| **ciclo** | um caminho que dá a volta e termina na célula onde começou; existe quando há duas rotas diferentes entre duas células. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **rotas independentes** | ciclos que não são combinação de outros; o tabuleiro Pac-Man precisa de pelo menos dois. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **labirinto perfeito** | labirinto sem nenhum ciclo: entre duas células existe exatamente um caminho. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **árvore geradora** | o nome, em teoria dos grafos, de um conjunto de ligações que conecta tudo sem formar ciclo; é a forma de um labirinto perfeito. [Veja](../06-carver/01-labirinto-perfeito.md) |
| **tabuleiro Pac-Man** | labirinto com ciclos e quase sem becos, onde quem foge sempre tem outra rota; o enunciado o chama de modo padrão. [Veja](../01-o-problema/05-perfeito-e-pac-man.md) |
| **braiding** | ("trançar") transformar um labirinto perfeito num tabuleiro Pac-Man, abrindo paredes dos becos e criando ciclos. [Veja](../01-o-problema/09-sem-saloes-e-o-braiding.md) |
| **área aberta 3x3 (salão)** | um bloco de 3x3 células sem nenhuma parede por dentro; proibido pelo enunciado. [Veja](../01-o-problema/09-sem-saloes-e-o-braiding.md) |
| **janela** | no código, um bloco 3x3 da grade que o programa examina para ver se virou um salão. [Veja](../05-maze/07-areas-abertas-3x3.md) |
| **caminho mais curto** | a menor sequência de passos da entrada à saída, escrita com as letras `N`, `E`, `S`, `W`. [Veja](../07-solver/01-busca-em-largura.md) |
| **arquivo de configuração** | o arquivo de texto com as opções (`WIDTH`, `HEIGHT`, `ENTRY`, ...), uma `CHAVE=valor` por linha; o do projeto é o `config.txt`. [Veja](../01-o-problema/03-o-arquivo-de-configuracao.md) |
| **arquivo de saída** | o arquivo de texto em que o programa grava o labirinto, um caractere hexadecimal por célula. [Veja](../01-o-problema/04-o-arquivo-de-saida.md) |
| **quadro** | a grade de caracteres do desenho no terminal, com `2 × HEIGHT + 1` linhas de `4 × WIDTH + 1` caracteres; no código, três tabelas: os caracteres, as cores do texto e as cores do fundo. [Veja](../13-tela/02-a-grade-de-caracteres.md) |
| **canto** | no desenho do terminal, o caractere onde até quatro paredes se encontram: linha par e coluna múltipla de 4. [Veja](../13-tela/02-a-grade-de-caracteres.md#onde-cada-pedaço-cai) |
| **interior e centro da célula** | no desenho do terminal, os três caracteres da célula `x,y` (linha `2y + 1`, colunas `4x + 1` a `4x + 3`); o do meio, coluna `4x + 2`, é o centro, por onde passa a linha do caminho. [Veja](../13-tela/02-a-grade-de-caracteres.md#onde-cada-pedaço-cai) |
| **camada do desenho** | cada etapa em que o `RenderService` escreve por cima da base do desenho: paredes e cantos, o "42", entrada e saída, caminho. Não é o mesmo que as camadas da arquitetura. [Veja](../13-tela/02-a-grade-de-caracteres.md#as-camadas-do-desenho) |

## Números e algoritmos

| Termo | Significado |
|---|---|
| **bit** | um dígito binário, 0 ou 1. Cada lado de uma célula ocupa um bit: 1 = parede, 0 = passagem. [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **binário** | o jeito de escrever números só com 0 e 1; cada casa, da direita para a esquerda, vale o dobro da anterior (1, 2, 4, 8). No Python, um número binário se escreve com `0b` na frente: `0b1001` é 9. [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **hexadecimal** | o jeito de escrever números de 0 a 15 com um só caractere: `0` a `9` e depois `a` (10) a `f` (15). [Veja](../01-o-problema/02-paredes-em-bits.md) |
| **operações de bit** | `&` ("e" bit a bit), `\|` ("ou" bit a bit) e `~` (inverte os bits): as contas que perguntam por uma parede, abrem e fecham. [Veja](../01-o-problema/08-ler-e-mudar-paredes.md) |
| **divisão inteira (`//`)** | a divisão que joga fora a parte quebrada: `13 // 2` dá `6`. [Veja](../01-o-problema/06-o-padrao-42.md) |
| **semente (seed)** | um número que fixa o sorteio: com a mesma semente, o programa gera sempre o mesmo labirinto. [Veja](../06-carver/04-a-seed.md) |
| **grafo** | um desenho de pontos ligados por traços; num labirinto, cada célula é um ponto e cada passagem um traço. [Veja](../05-maze/06-contar-ciclos.md) |
| **backtracker** | o algoritmo que cava o labirinto perfeito: anda sorteando caminhos e volta atrás quando fica sem saída. [Veja](../06-carver/02-recursive-backtracker.md) |
| **pilha** | uma lista em que só se mexe numa ponta, o topo: o último que entra é o primeiro que sai. [Veja](../06-carver/02-recursive-backtracker.md) |
| **recursão** | uma função que chama a si mesma; o `Carver` usa uma pilha no lugar dela. [Veja](../06-carver/06-a-versao-recursiva.md) |
| **BFS** | busca em largura: o algoritmo que acha o caminho mais curto explorando primeiro as células mais próximas. [Veja](../07-solver/01-busca-em-largura.md) |
| **fila** | uma lista em que se entra por uma ponta e se sai pela outra: o primeiro que entra é o primeiro que sai; em Python, um `collections.deque`. [Veja](../07-solver/01-busca-em-largura.md) |

## Python

| Termo | Significado |
|---|---|
| **módulo** | um arquivo `.py`; `mazegen/errors.py` é o módulo `mazegen.errors`. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **pacote** | uma pasta com um arquivo `__init__.py`, que o Python importa pelo nome; `mazegen/` é o pacote `mazegen`. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **`__init__.py`** | o arquivo que faz de uma pasta um pacote; o código dele roda na primeira vez que o pacote é importado. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **docstring** | o texto entre `"""` logo no começo de um módulo, classe ou função, que documenta o que ele faz. [Veja](../03-ambiente/07-pacotes-do-mazegen.md) |
| **anotação de tipo** | a indicação do tipo de um parâmetro ou retorno, como em `def soma(a: int, b: int) -> int:`; o mypy confere. [Veja](./03-pre-requisitos.md) |
| **compreensão de lista** | (*list comprehension*) um laço `for` entre colchetes que monta uma lista: `[n * 2 for n in range(4)]`; com chaves, monta um conjunto (compreensão de conjunto). [Veja](./03-pre-requisitos.md) |
| **função geradora** | uma função com `yield`, que entrega os valores um de cada vez em vez de montar uma lista inteira. [Veja](../05-maze/02-consultar-a-grade.md) |
| **expressão geradora** | uma compreensão entre parênteses, que produz os itens um de cada vez para quem a consome. [Veja](../04-value-objects/05-pattern42-posicao.md) |
| **f-string** | um texto com `f` antes das aspas, em que cada `{nome}` é trocado pelo valor da variável. [Veja](../09-gerador/02-validar-os-parametros.md) |
| **exceção** | um objeto de erro: o código o levanta com `raise`, e quem chamou o captura com `try`/`except`. [Veja](../04-value-objects/01-maze-error.md) |
| **decorador** | a linha com `@` em cima de um `def` ou `class`, que muda o jeito de usar o que vem abaixo. [Veja](../04-value-objects/03-direction-propriedades.md) |
| **`@property`** | decorador que faz um método ser lido como atributo, sem parênteses. [Veja](../04-value-objects/03-direction-propriedades.md) |
| **`@classmethod`** | decorador de um método chamado pela classe, que recebe a classe em `cls`. [Veja](../04-value-objects/05-pattern42-posicao.md) |
| **`@staticmethod`** | decorador de um método que não usa o objeto nem a classe. [Veja](../08-braider/04-a-regra-do-3x3.md) |
| **Enum e IntEnum** | uma classe com uma lista fechada de valores com nome; no `IntEnum`, os valores também são números inteiros. [Veja](../04-value-objects/02-direction-bits.md) |
| **dataclass** | uma classe marcada com `@dataclass`, que ganha sozinha o construtor e a comparação a partir dos campos. [Veja](../04-value-objects/04-cell.md) |
| **`frozen=True`** | opção da dataclass que impede mudar os campos depois de criado o objeto. [Veja](../04-value-objects/04-cell.md) |
| **`slots=True`** | opção da dataclass que reserva espaço só para os campos declarados, sem aceitar atributos novos. [Veja](../04-value-objects/04-cell.md) |
| **hash** | um número calculado a partir do conteúdo de um objeto, que o `set` e o `dict` usam para achá-lo rápido. [Veja](../04-value-objects/04-cell.md) |
| **`frozenset`** | o conjunto (`set`) imutável do Python. [Veja](../04-value-objects/05-pattern42-posicao.md) |
| **`__contains__`** | o método que o Python chama para responder `x in objeto`. [Veja](../04-value-objects/06-pattern42-consulta.md) |
| **`Protocol`** | um recurso de `typing` que descreve os métodos que um objeto precisa ter, sem herança. [Veja](../12-geracao-e-saida/03-a-porta-maze-repository.md) |
| **`__all__`** | a lista dos nomes que um pacote oferece a quem o importa: a API pública dele. [Veja](../09-gerador/05-documentacao-do-modulo.md) |
| **bytecode** | a tradução que o Python faz de um módulo na primeira importação, guardada em `__pycache__`. [Veja](../03-ambiente/09-makefile-empacotar.md#clean) |
| **traceback** | a listagem de erro que o Python imprime quando uma exceção não é tratada; o programa nunca deve mostrá-la ao usuário. [Veja](../14-menu-e-main/05-a-barreira-de-erros.md) |
| **stdout e stderr** | as duas saídas de texto de um programa: a normal e a de erros. [Veja](../01-o-problema/03-o-arquivo-de-configuracao.md) |
| **código de saída** | o número que o programa devolve ao terminar: 0 é sucesso, outro valor é erro; no terminal, aparece com `echo $?`. [Veja](../01-o-problema/03-o-arquivo-de-configuracao.md) |
| **`sys.argv`** | a lista com os argumentos da linha de comando; o `main` do projeto recebe `sys.argv[1:]`, sem o nome do script. [Veja](../14-menu-e-main/04-o-composition-root.md) |
| **UTF-8** | a tabela mais usada para transformar letras em bytes num arquivo de texto. [Veja](../11-configuracao/05-abrindo-o-arquivo.md) |

## Ferramentas e entrega

| Termo | Significado |
|---|---|
| **ambiente virtual (venv)** | uma pasta `.venv` com um Python e bibliotecas só deste projeto, separados do resto do computador. [Veja](../03-ambiente/01-o-ambiente-virtual.md) |
| **`pip`** | o programa que baixa e instala bibliotecas Python. [Veja](../03-ambiente/01-o-ambiente-virtual.md) |
| **Makefile** | arquivo com atalhos de comandos: `make install`, `make run`, `make lint`... [Veja](../03-ambiente/10-o-que-e-um-makefile.md) |
| **alvo** | o nome de uma regra do Makefile, usado no terminal: o `lint` de `make lint`. [Veja](../03-ambiente/10-o-que-e-um-makefile.md) |
| **depurador (`pdb`)** | o programa que vem com o Python para rodar outro passo a passo; a regra `debug` o usa. [Veja](../03-ambiente/02-makefile-instalar-e-rodar.md) |
| **lint** | verificar o código sem executá-lo, à procura de erros e de desvios do padrão. [Veja](../03-ambiente/03-makefile-limpar-verificar-empacotar.md) |
| **flake8** | ferramenta de lint que confere o estilo do código. [Veja](../03-ambiente/03-makefile-limpar-verificar-empacotar.md) |
| **PEP 8** | o guia de estilo oficial do Python: linhas de até 79 caracteres, espaços em volta de operadores... [Veja](../03-ambiente/03-makefile-limpar-verificar-empacotar.md) |
| **mypy** | ferramenta que confere as anotações de tipo do código. [Veja](../03-ambiente/03-makefile-limpar-verificar-empacotar.md) |
| **`pyproject.toml`** | o arquivo que descreve o pacote do gerador: nome, versão e como construí-lo; escrito no formato **TOML**. [Veja](../03-ambiente/04-pyproject.md) |
| **`.gitignore`** | a lista de arquivos gerados que o git não guarda. [Veja](../03-ambiente/05-flake8-e-gitignore.md) |
| **wheel (`.whl`) e sdist (`.tar.gz`)** | os dois formatos de arquivo em que um pacote Python é distribuído e instalado com `pip`. [Veja](../09-gerador/08-o-pacote.md) |
| **licença MIT** | a licença do projeto: permite a qualquer um usar, copiar e redistribuir o gerador. [Veja](../09-gerador/06-a-licenca.md) |
| **`maze_analyzer.py`** | o verificador que acompanha o enunciado: lê um arquivo de saída e diz se o labirinto cumpre as regras. [Veja](../16-bonus/03-conferir-com-o-analyzer.md) |
| **ANSI** | as sequências de caracteres especiais que mandam o terminal mudar de cor. [Veja](../10-utilitarios/08-sequencias-ansi.md) |
| **SGR** | a sequência ANSI que escolhe as cores do texto e do fundo (*Select Graphic Rendition*). [Veja](../10-utilitarios/08-sequencias-ansi.md) |
| **cor RGB (de 24 bits)** | uma cor dada por três números de 0 a 255, as quantidades de vermelho, verde e azul; os três juntos ocupam 24 bits. [Veja](../10-utilitarios/08-sequencias-ansi.md) |
| **ASCII** | a tabela básica que numera 128 caracteres: letras sem acento, dígitos, pontuação, o espaço e caracteres de controle. [Veja](../10-utilitarios/08-sequencias-ansi.md) |
| **Unicode** | a tabela que numera os caracteres de todas as escritas; os 128 primeiros são os da tabela ASCII. [Veja](../10-utilitarios/09-caracteres-de-caixa.md) |
| **caractere de caixa** | um caractere feito para desenhar molduras (`━`, `┃`, `┏`...), cujos traços encostam nas bordas e se emendam com os do vizinho. [Veja](../10-utilitarios/09-caracteres-de-caixa.md) |
| **braço** | num caractere de caixa, a linha que sai do centro até uma das bordas; cada braço tem um bit, como as paredes (Norte = 1, Leste = 2, Sul = 4, Oeste = 8). [Veja](../10-utilitarios/09-caracteres-de-caixa.md) |

## Arquitetura

| Termo | Significado |
|---|---|
| **camada** | um grupo de classes com o mesmo papel, num dos anéis da arquitetura; não confundir com a camada do desenho. [Veja](../02-arquitetura/01-por-que-camadas.md) |
| **Clean Architecture** | ("arquitetura limpa") o estilo de organizar o código em anéis, com as regras no centro e os detalhes (arquivos, terminal) na borda. [Veja](../02-arquitetura/01-por-que-camadas.md) |
| **regra de dependência** | o código de uma camada importa a própria camada e os anéis mais para dentro, nunca mais para fora; camadas diferentes do mesmo anel não se importam. [Veja](../02-arquitetura/03-regra-de-dependencia.md) |
| **inversão de dependência** | o centro declara o que precisa (uma porta), e a borda fornece; assim o centro não importa a borda. [Veja](../02-arquitetura/07-a-porta-e-a-inversao.md) |
| **domínio** | os dados com que a aplicação trabalha (a configuração lida, o labirinto pronto, o estado da tela), sem arquivo e sem terminal. [Veja](../03-ambiente/08-pacotes-do-amazeing.md) |
| **value object** | um objeto que é só um valor: não muda depois de criado e é comparado pelo conteúdo (ex.: uma coordenada). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **método de fábrica** | um método que recebe os dados, aplica a regra de criação e devolve o objeto pronto. [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **entidade** | um objeto cujo estado muda, mas que protege as próprias regras (ex.: a grade de paredes). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **service** | uma classe que só executa uma operação, sem guardar estado (ex.: o algoritmo que cava). [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **use case** | uma operação completa da aplicação, num único método `execute`. [Veja](../02-arquitetura/04-papeis-das-classes.md) |
| **porta (port)** | a descrição do que uma classe precisa de outra (os métodos e os tipos), sem dizer quem vai fornecer. [Veja](../12-geracao-e-saida/03-a-porta-maze-repository.md) |
| **fachada** | uma classe que fica na frente de várias outras e oferece um jeito simples de usá-las; aqui, o `MazeGenerator`. [Veja](../09-gerador/01-a-fachada.md) |
| **repository** | a classe que lê ou grava arquivos; a única camada que mexe em disco. [Veja](../02-arquitetura/06-os-outros-papeis.md) |
| **retrato** | um value object com tudo o que se sabe de um labirinto pronto, tirado de uma vez: o `GeneratedMaze`. [Veja](../12-geracao-e-saida/01-o-retrato-generated-maze.md) |
| **composition root** | o ponto do programa que cria todas as peças e as liga; aqui, a função `main` do `a_maze_ing.py`. [Veja](../14-menu-e-main/04-o-composition-root.md) |

## As classes do projeto

| Classe | O que faz |
|---|---|
| `MazeError` | o erro do gerador: um parâmetro impossível ou um tabuleiro que não deu certo. [Veja](../04-value-objects/01-maze-error.md) |
| `Direction` | os quatro lados de uma célula, cada um com o seu bit. [Veja](../04-value-objects/02-direction-bits.md) |
| `Cell` | a posição `x,y` de uma célula. [Veja](../04-value-objects/04-cell.md) |
| `Pattern42` | as células do "42" para um tamanho de grade. [Veja](../04-value-objects/05-pattern42-posicao.md) |
| `Maze` | a grade de paredes, com as perguntas e as mudanças que se faz nela. [Veja](../05-maze/01-a-grade-de-paredes.md) |
| `Carver` | o algoritmo que cava o labirinto perfeito. [Veja](../06-carver/01-labirinto-perfeito.md) |
| `Solver` | o algoritmo que acha o caminho mais curto. [Veja](../07-solver/01-busca-em-largura.md) |
| `Braider` | o algoritmo que transforma o labirinto perfeito num tabuleiro Pac-Man. [Veja](../08-braider/01-becos-sem-saida.md) |
| `MazeGenerator` | a fachada do gerador: a única classe que outro projeto precisa usar. [Veja](../09-gerador/01-a-fachada.md) |
| `AppError` | o erro da aplicação, com as variações `ConfigError` e `OutputError`. [Veja](../10-utilitarios/05-a-hierarquia-app-error.md) |
| `ValueParser` | converte o texto de uma opção em número, `True`/`False` ou coordenada. [Veja](../10-utilitarios/02-inteiros-sem-surpresa.md) |
| `Ansi` | as cores RGB do desenho e a sequência que aplica um par de cores, a do texto e a do fundo. [Veja](../10-utilitarios/04-cores-ansi.md) |
| `Box` | os caracteres de caixa do desenho, escolhidos pela soma dos braços. [Veja](../10-utilitarios/09-caracteres-de-caixa.md) |
| `MazeConfig` | as opções lidas do arquivo de configuração, já validadas. [Veja](../11-configuracao/01-o-value-object-maze-config.md) |
| `FileConfigRepository` | lê o arquivo de configuração e devolve um `MazeConfig`. [Veja](../11-configuracao/05-abrindo-o-arquivo.md) |
| `GeneratedMaze` | o retrato do labirinto pronto: grade, entrada, saída, caminho e "42". [Veja](../12-geracao-e-saida/01-o-retrato-generated-maze.md) |
| `MazeRepository` | a porta que diz como um labirinto é gravado. [Veja](../12-geracao-e-saida/03-a-porta-maze-repository.md) |
| `FileMazeRepository` | grava o labirinto no arquivo de saída. [Veja](../12-geracao-e-saida/05-gravando-o-arquivo.md) |
| `GenerateMaze` | o use case que gera um labirinto, grava e devolve o retrato. [Veja](../12-geracao-e-saida/06-o-caso-de-uso-generate-maze.md) |
| `ViewState` | o estado da tela: caminho visível ou não e a cor atual das paredes. [Veja](../13-tela/01-o-estado-da-tela.md) |
| `RenderService` | transforma o labirinto nas linhas do terminal: caracteres de caixa com cores RGB. [Veja](../13-tela/02-a-grade-de-caracteres.md) |
| `Menu` | mostra o labirinto e o menu e responde às escolhas do usuário. [Veja](../14-menu-e-main/01-o-laco-do-menu.md) |
