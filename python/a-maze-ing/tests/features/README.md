# Casos de teste do A-Maze-ing (Gherkin)

Cada requisito do subject A-Maze-ing v2.3 (`en.subject.pdf`, tradução `pt_br.subject.md`) tem
pelo menos um cenário: obrigatórios, recomendados, opcionais, bônus e informativos. Os
arquivos seguem a ordem de implementação.

Os cenários `@automatizado` são executados pelo pytest-bdd: cada passo usa uma frase do
[vocabulário de passos](#vocabulário-de-passos), e cada frase tem uma função Python em
`tests/step_defs/`. A suíte fica em `a-maze-ing/tests/`, fora de `project/`, porque o subject diz
que os testes não são submetidos (III.3) e a entrega é o que está no repositório (IX). A
configuração está em [Configuração da suíte](#configuração-da-suíte).

## Ordem

| # | Arquivo | Escopo |
|---|---|---|
| 00 | `00-contexto.feature` | capa, sumário, prefácio |
| 01 | `01-ambiente.feature` | Python 3.10+, venv, `.gitignore`, suíte de testes |
| 02 | `02-makefile.feature` | regras `install`, `run`, `debug`, `clean`, `lint`, `lint-strict` |
| 03 | `03-qualidade.feature` | flake8, mypy, type hints, docstrings, exceções, context managers |
| 04 | `04-uso-cli.feature` | comando, nome do arquivo principal, argumento único, erros de arquivo |
| 05 | `05-configuracao.feature` | formato `KEY=VALUE`, chaves obrigatórias, validação, config padrão |
| 06 | `06-grade-e-paredes.feature` | paredes por célula, entrada/saída, borda, coerência |
| 07 | `07-geracao-e-seed.feature` | aleatoriedade, seed, conectividade, classe geradora |
| 08 | `08-padrao-42.feature` | padrão "42", omissão em labirinto pequeno |
| 09 | `09-modo-perfeito.feature` | `PERFECT=True` |
| 10 | `10-caminho-mais-curto.feature` | caminho mais curto válido |
| 11 | `11-modo-pacman.feature` | `PERFECT=False` (tabuleiro Pac-Man) |
| 12 | `12-areas-abertas.feature` | corredores de no máximo 2 células, nenhum 3x3 aberto |
| 13 | `13-arquivo-de-saida.feature` | formato hexadecimal, rodapé, analyzer, exemplo do subject |
| 14 | `14-representacao-visual.feature` | renderização ASCII ou MLX |
| 15 | `15-interacoes.feature` | regenerar, mostrar/ocultar caminho, cores, sair |
| 16 | `16-modulo-reutilizavel.feature` | `MazeGenerator`, documentação, pacote `mazegen-*` |
| 17 | `17-licenca.feature` | `LICENSE.md` |
| 18 | `18-readme.feature` | `README.md` |
| 19 | `19-bonus.feature` | sem becos sem saída, vários algoritmos, animação |
| 20 | `20-uso-de-ia.feature` | Capítulo II — instruções sobre IA |
| 21 | `21-submissao-e-defesa.feature` | Capítulo IX — submissão e avaliação |

## Config base

"O config base" nos cenários é este arquivo; cada cenário diz só o que muda nele.

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

"A opção de sair pelo stdin" é a linha `4` (Quit) enviada ao menu; os testes a enviam para que
o programa termine sem intervenção humana.

## Referências

- "Raiz do repositório" nos cenários é a pasta `project/`, que vira a raiz do repositório entregue
  à 42.
- `@pdf-p09-L13-L15`: página **física** do PDF (p01–p20, a numeração do visualizador; o número
  impresso no rodapé é a página física − 1) e linhas 13 a 15 dessa página.
- Linha do PDF = n-ésima linha não vazia da página, de cima para baixo, contando o cabeçalho
  "A-Maze-ing … This is the way" nas páginas que o têm. Figuras não contam linha; são citadas
  como `@pdf-p11-figura`.
- `@md-L186`: linha 186 do `pt_br.subject.md`.
- Acima de cada cenário, `# pdf: "..."` é o trecho do PDF em inglês e `# md:  "..."` é o trecho
  correspondente do `pt_br.subject.md`, sem a marcação Markdown (marcador de lista, negrito,
  itálico, `>`). As aspas tipográficas do PDF (`’`, `‘`, `“`, `”`) aparecem como aspas retas.
  `# figura: "..."` é texto em inglês que só existe dentro de uma imagem; o `# md:` dela traz a
  descrição ou a legenda traduzida da figura.
- `# regua: "..."` é o trecho em inglês da régua de avaliação (`regua/regua_N.png`),
  `# regua-md: "..."` é o trecho correspondente de `regua/regua_N.pt_br.md` e `@regua-pN` é a
  página da régua. A régua é o roteiro do avaliador: os cenários a citam quando ela exige algo
  que o subject não detalha ou resolve uma dúvida do subject.

## Tags

| Tag | Significado |
|---|---|
| `@obrigatorio` | "must" no PDF, ou frase imperativa que define requisito do programa ou da entrega |
| `@recomendado` | "should", "recommended", "prefer" no PDF, e os conselhos dos Capítulos II e IX (a tradução usa "deve" nesses pontos; vale o PDF) |
| `@opcional` | "may", "optional", "can" |
| `@bonus` | Capítulo VIII ou recompensado como bônus |
| `@informativo` | contexto sem exigência própria |
| `@derivado` | consequência lógica de requisito, exemplo ou figura |
| `@decisao-Dnn` | o subject sozinho não define o comportamento; a tabela D diz o que vale e com que base |
| `@decisao-Inn` | o cenário é genérico ("a opção de regenerar", "a exceção do módulo"); a tabela I fixa o valor concreto |
| `@regua-pN` | o cenário cita a página N da régua de avaliação |
| `@automatizado` | verificável por pytest, subprocesso com stdin roteirizado, validador da suíte, `maze_analyzer.py`, `make` ou build em venv limpo |
| `@manual` | verificável por inspeção ou na defesa |

## Validador da suíte

O `maze_analyzer.py` termina com código 0 sempre que consegue ler o arquivo, mesmo com veredito
ruim: os testes leem a linha `Verdict:`. Ele não verifica borda fechada, áreas 3x3, entrada
diferente da saída, o caminho do rodapé, a forma do "42", saída em célula fechada nem o
formato estrito do texto. Esses itens exigem um validador próprio da suíte, citado nos
cenários como "o validador da suíte".

## Decisões

Todas as decisões estão tomadas. Critério: a implementação mais simples que cumpre o subject e
a régua de avaliação. A coluna "Outras opções" registra alternativas válidas; nenhuma delas é
necessária.

### Respondidas pelas fontes

A resposta está no subject, na régua de avaliação ou no `maze_analyzer.py`, que a régua manda
usar como critério.

| D | Dúvida | O que vale | Base |
|---|---|---|---|
| D03 | `PERFECT` obrigatória vs "the default" | a chave é obrigatória e a ausência é erro; `False` é o modo padrão e o valor do `config.txt` do repositório; `true`/`false` são aceitos em qualquer caixa | régua p2: `PERFECT` está entre "the expected keys", "Remove a mandatory key" é teste de erro e "(lower case is also OK)"; régua p3: "Pac-Man-USABLE verdict for the default one" |
| D08 | centro com dimensão par | dimensão ímpar → célula central; par → pelo menos uma das (até 4) células em volta do meio é corredor | analyzer (`_centre_candidates`) |
| D09 | "becos raros, um ou dois tolerados" | no máximo 2 becos reais; becos cercados só pelo "42" e pela borda não contam | analyzer (`--max-dead-ends`, padrão 2); régua p3: "A few dead-ends are tolerated" |
| D10 | "duas rotas independentes" | loops = passagens − células + 1 ≥ 2 na região alcançável | analyzer (`--min-loops`, padrão 2) |
| D11 | área aberta 3x3 | proibido bloco 3x3 com as 12 paredes internas abertas; blocos 2x2, 2x3 e 3x2 abertos são aceitos | régua p3: "There is no 3x3 or larger open zone without walls" |
| D12 | borda externa | 100% fechada, inclusive nas células de entrada e saída | régua p3: "Have walls all around the maze" |
| D13 | formato do rodapé | coordenadas `x,y` puras (`^\d+,\d+$`); `# entry (x,y)` do exemplo é anotação da imagem | subject (na figura da p11 a anotação está em cinza, fora da cor do dado) e analyzer (com a anotação ele não lê a entrada) |
| D22 | títulos das seções do README | "Description", "Instructions" e "Resources" escritos assim, em inglês | régua p1 (cita os três títulos entre aspas) |

### Escolhas onde nenhuma fonte define tudo

Os cenários com a tag `@decisao-Dnn` da linha seguem a coluna "Decisão". A coluna "Base" separa o
que vem de uma fonte do que é escolha.

| D | Pergunta | Decisão | Outras opções | Base |
|---|---|---|---|---|
| D01 | Como o programa reporta um erro? | imprime `Error: <causa>` em stderr e termina com código 1; a causa cita o arquivo, a linha ou a chave; erro de sintaxe no config: `Error: <arquivo>, line <n>: expected KEY=VALUE, got '<linha>'`; o uso errado da linha de comando tem mensagem própria (I12) | mensagem em stdout; outro código diferente de 0 | escolha; régua p2: "unexpected end of the program" zera a nota |
| D02 | Como se informa a seed? | chave extra opcional `SEED` (inteiro) no config, repassada a `random.Random(seed)`; sem a chave, `random.Random()` sem argumento; o `config.txt` do repositório traz `SEED` só comentada | seed fixa no `config.txt` do repositório; seed por argumento de linha de comando | escolha do nome; régua p3: "update the configuration file or the code to verify"; régua p2: o config padrão dá "a maze randomly generated" |
| D04 | Como o config é lido? | arquivo aberto com `encoding="utf-8-sig"` (aceita BOM; bytes que não são UTF-8 → erro citando o arquivo); cada linha passa por `strip()`; linha vazia e linha que começa com `#` são puladas; o resto é dividido no primeiro `=`; chave = `chave.strip().upper()`, valor = `valor.strip()`; linha sem `=` ou com chave vazia → erro de sintaxe (D01); chave repetida → vale a última; chave desconhecida → ignorada; comentário no fim da linha não existe (o valor fica inválido e a chave é acusada); chaves obrigatórias ausentes → um único erro que lista todas as que faltam, na ordem da tabela do subject | erro para chave desconhecida e para chave repetida; ler com `utf-8` sem aceitar BOM | régua p2 para as minúsculas ("lower case is also OK") e para a linha sem `=`; o resto é escolha |
| D05 | Quais parâmetros são impossíveis? | erro (D01) quando: WIDTH ou HEIGHT não é inteiro, é menor que 1 ou maior que 100; ENTRY ou EXIT não é `x,y` de inteiros, é negativo ou fica fora da grade; ENTRY = EXIT; ENTRY ou EXIT cai numa célula do "42"; `PERFECT=False` com (WIDTH − 1) × (HEIGHT − 1) < 2 (1xN, Nx1 e 2x2 não comportam 2 ciclos); `SEED` não é inteiro. A classe `MazeGenerator` faz as mesmas checagens de tamanho, coordenadas e modo no construtor e levanta `MazeError` (I09) | sem limite máximo (200x100 já leva ~9 s por geração e valores enormes estouram a memória); deslocar o "42" quando a entrada ou a saída cai nele | régua p3: "the entry or exit cells are outside the maze, width or height is negative"; o limite 100, o "42" e o Pac-Man impossível são escolha |
| D06 | O que acontece quando o "42" não cabe? | gera o labirinto sem o "42", imprime `Error: maze too small for the "42" pattern` em stderr (I10) e segue; código de saída 0 | encerrar com erro | subject p09 L33–L35 e régua p3 para gerar sem o "42" e avisar no terminal; o código 0 é escolha |
| D07 | Desenho e posição do "42" | os glifos 3x5 do exemplo do subject, com uma coluna livre entre eles (7x5 no total); canto superior esquerdo em x = (WIDTH − 7) // 2 e y = (HEIGHT − 5) // 2; existe só com WIDTH ≥ 9 e HEIGHT ≥ 7, o que deixa pelo menos uma célula de corredor em volta | glifos maiores ou proporcionais ao tamanho do labirinto; outra posição | escolha; a forma vem do exemplo da p11 |
| D14 | Caixa do hexadecimal no arquivo de saída | minúsculas (`format(valor, "x")`) | maiúsculas; o `maze_analyzer.py` aceita as duas | escolha; o exemplo do subject usa minúsculas |
| D15 | Como o teste confere o caminho mais curto? | valida os passos e o comprimento (= distância BFS), nunca a string exata; a tela mostra o mesmo caminho gravado no arquivo | comparar com uma string esperada | escolha para a comparação; régua p3 para tela = arquivo |
| D16 | O que acontece ao regenerar? | a mesma rotina da primeira geração: gera, grava `OUTPUT_FILE`, exibe; o gerador guarda um único `random.Random`, então com `SEED` a sequência de regenerações se repete; o estado do caminho (visível ou oculto) e a cor atual das paredes se mantêm; falha ao gravar → mesma mensagem de erro da abertura e código 1 | manter no arquivo só o primeiro labirinto | escolha; régua p3 confere o primeiro labirinto no arquivo e o caminho do arquivo igual ao da tela |
| D17 | Ctrl+C e fim da entrada (EOF) | `main` captura `KeyboardInterrupt` e `EOFError` em qualquer ponto, imprime uma linha vazia (o prompt do shell não fica colado) e termina com código 0 | código 130 no Ctrl+C | escolha; régua p2: "unexpected end of the program" zera a nota |
| D18 | "Terminal ASCII rendering" | só caracteres ASCII: cada posição do desenho são 2 espaços com cor de fundo ANSI (I02) | caracteres de bloco Unicode (`█`), como nas figuras do Capítulo V | escolha; subject p12 L04 diz "ASCII" |
| D19 | "Unique class" | uma única classe pública de geração, `MazeGenerator`; `MazeError` é a exceção pública do módulo; funções auxiliares internas são permitidas | tudo dentro de uma classe só | escolha |
| D20 | Os testes ficam no repositório de entrega? | não: a suíte fica em `a-maze-ing/tests/`, só no monorepo `dojo`; a entrega (`project/`) não tem `tests/`; a suíte passa no flake8 e no mypy rodados na própria pasta, com type hints; docstrings dispensadas (I16) | `tests/` dentro da entrega, passando no `flake8 .` e no `mypy .` da entrega (régua p1: "Other files can be present") | subject III.3: "Create test programs to verify project functionality (not submitted or graded)"; IX: "Only the work inside your repository will be evaluated"; o rigor de lint da suíte é escolha |
| D21 | Primeira linha do README | `*This project has been created as part of the 42 curriculum by <login>.*`, com `*` e ponto final; vários logins separados por `, ` | `_` no lugar de `*` | régua p1: "formatted exactly as"; o `*` é escolha |

### Decisões de implementação

Pontos em que o subject dá liberdade. Os cenários com a tag `@decisao-Inn` são genéricos ("a
opção de regenerar", "a exceção própria do módulo"); esta tabela fixa o valor concreto.

| I | Tema | Decisão | Outras opções |
|---|---|---|---|
| I01 | Exibição | terminal; sem MiniLibX (o pacote fornecido é binário de Linux) | janela MiniLibX |
| I02 | Desenho do labirinto | grade de (2 × HEIGHT + 1) linhas por (2 × WIDTH + 1) posições; cada posição são 2 espaços com cor de fundo ANSI: parede na cor atual (I04), corredor sem cor, entrada magenta, saída vermelha, caminho ciano, "42" cinza; entrada e saída têm prioridade sobre o caminho, que colore as células intermediárias e as passagens entre células consecutivas; cada linha termina com o reset `\x1b[0m`; o labirinto é impresso de novo a cada ação, sem limpar a tela | caracteres de caixa (`┼`, `─`, `│`); limpar a tela com ANSI; `curses` |
| I03 | Menu | o da figura do subject, lido com `input()`: `1` regenerar, `2` mostrar/ocultar o caminho, `3` trocar a cor das paredes, `4` sair (código 0); prompt `Choice? (1-4): `; opção inválida → `Invalid choice` e novo prompt; o caminho começa oculto; o estado do caminho e a cor atual se mantêm ao regenerar | teclas sem Enter (terminal em modo raw); opção para a cor do "42" |
| I04 | Cores das paredes | paleta fixa de fundos ANSI branco → amarelo → verde → azul, começando em branco, percorrida em rodízio pela opção `3`; nenhuma das quatro coincide com as cores fixas de I02 | o usuário digita a cor |
| I05 | Algoritmo do labirinto perfeito | recursive backtracker iterativo (pilha), a partir da entrada, sem entrar nas células do "42" | Prim; Kruskal |
| I06 | Modo Pac-Man | gera o perfeito e depois: (a) para cada beco sem saída, em ordem aleatória, abre uma parede para um vizinho que não é do "42" e não cria bloco 3x3 aberto; (b) abre paredes válidas aleatórias até haver 2 ciclos. O passo (a) também atende o bônus "sem becos" | gerar direto com ciclos; abrir uma fração fixa das paredes |
| I07 | Checagem do 3x3 | depois de abrir uma parede, percorrer todas as janelas 3x3 da grade; se alguma ficou toda aberta, desfazer (100x100 gera em ~2 s) | checar só as janelas em volta da parede aberta (mais rápido, mais código) |
| I08 | Caminho mais curto | busca em largura da entrada, vizinhos na ordem N, E, S, W; calculado uma vez por labirinto e usado no arquivo e na tela | A*; Dijkstra |
| I09 | API do módulo | `MazeGenerator(width, height, entry=(0, 0), exit=None, perfect=False, seed=None)`; o construtor valida os parâmetros (D05) e levanta `MazeError`; `exit=None` = canto inferior direito; `generate()` cria um labirinto novo a cada chamada; depois dela: `grid` (lista de linhas de inteiros com os mesmos bits do arquivo: N=1, E=2, S=4, W=8), `solution` (texto com `N`/`E`/`S`/`W`) e `pattern` (conjunto das células `(x, y)` do "42", vazio quando não coube) | classe `Cell`; estrutura em grafo; `solve()` separado |
| I10 | Mensagem do "42" omitido | `a_maze_ing.py` imprime `Error: maze too small for the "42" pattern` em stderr quando `pattern` vem vazio, e segue | o próprio módulo imprime |
| I11 | Organização dos arquivos | `mazegen/__init__.py` (docstring com a documentação do módulo; exporta `MazeGenerator` e `MazeError`), `mazegen/generator.py`, `mazegen/py.typed`; `a_maze_ing.py` com config, arquivo de saída, desenho, menu e `main`; na raiz também: `pyproject.toml`, `Makefile`, `.flake8`, `.gitignore`, `config.txt`, `README.md`, `LICENSE.md`, `mazegen-1.0.0-py3-none-any.whl` e `mazegen-1.0.0.tar.gz`; sem `tests/` (D20) | separar a aplicação num pacote (`config.py`, `output.py`, `render.py`) |
| I12 | Uso errado da linha de comando | `Usage: python3 a_maze_ing.py <config_file>` em stderr, código 1 | `argparse` |
| I13 | Pacote | `pyproject.toml` com `requires = ["setuptools>=77"]`, `name = "mazegen"`, `version = "1.0.0"` (única fonte da versão), `requires-python = ">=3.10"`, `readme = "README.md"`, `license = "MIT"`, `license-files = ["LICENSE.md"]` e o pacote `mazegen`; `make build` roda `python -m build` e copia o `.whl` e o `.tar.gz` de `dist/` para a raiz; a documentação do módulo entra no pacote pela docstring de `mazegen/__init__.py` | só o `.whl`; outro backend de build |
| I14 | Makefile, lint e `.gitignore` | `install` cria `.venv` com o `python3` do `PATH` e instala flake8, mypy e build (pytest fica na suíte, fora da entrega); `run`, `debug`, `lint`, `lint-strict` e `build` usam `.venv/bin/python`; não há regra `test`; `.flake8` e `[tool.mypy]` excluem `.venv`, `build` e `dist`; `# noqa` e `# type: ignore` são proibidos; `.gitignore`: `.venv/`, `__pycache__/`, `*.pyc`, `.mypy_cache/`, `build/`, `dist/`, `*.egg-info/`, `maze.txt` | `uv` ou `pipx` no lugar de venv + pip |
| I15 | Testes | pytest-bdd executa os `.feature` de `a-maze-ing/tests/features/`; uma função por frase do vocabulário em `tests/step_defs/`; fixtures, tipos de parâmetro e o hook de tags em `tests/conftest.py`; `tests/pytest.ini` com `filterwarnings = error`; o programa roda por subprocesso com `cwd` em `project/` e `mazegen` é importado por `pythonpath = ../project`; testes unitários comuns (gerador, solver, parser do config, validador) em `tests/unit/` | behave no lugar do pytest-bdd; pytest puro com os `.feature` só como roteiro |
| I16 | Docstrings | estilo Google, em todas as funções, métodos e classes de `a_maze_ing.py` e `mazegen/`; `tests/` dispensada (testes não são avaliados, III.3) | estilo NumPy; docstrings também nos testes |
| I17 | Licença | MIT | BSD-3-Clause; Apache-2.0 |
| I18 | Idioma do README do projeto | inglês | idioma principal do campus |
| I19 | Fora da primeira versão | cenários `@opcional` e `@bonus` que não fazem parte dela: cor própria para o "42", chave `ALGORITHM` com outros algoritmos, animação, chave de modo de exibição | implementar já na primeira versão |
| I20 | `config.txt` do repositório | `WIDTH=20`, `HEIGHT=15`, `ENTRY=0,0`, `EXIT=19,14`, `OUTPUT_FILE=maze.txt`, `PERFECT=False`, cada chave precedida de uma linha de comentário, e `# SEED=42` comentado no fim | seed ativa; outro tamanho |
| I21 | Textos e cores que os testes conferem | palavras-chave nas mensagens de erro (D01): arquivo inexistente → `not found`; arquivo que não é UTF-8 → `UTF-8`; chave obrigatória ausente → `missing`; entrada igual à saída → `differ`; tamanho sem tabuleiro Pac-Man → `Pac-Man`; coordenada no padrão → `"42"`; códigos SGR de fundo: branco `47`, amarelo `43`, verde `42`, azul `44`, magenta `45`, vermelho `41`, ciano `46`, cinza `100`; a mensagem de `MazeError` cita o nome do parâmetro da assinatura (`width`, `height`, `entry`, `exit`, `perfect`) | outras palavras-chave; cores de 256 tons |
| I22 | Documentação do módulo | docstring de `mazegen/__init__.py` com como instanciar, os parâmetros, `grid`, `solution`, `pattern` e uma seção `Example:` (estilo Google) com um bloco de código executável que termina em `print(gen.solution)`; o README principal repete o mesmo texto | `mazegen/README.md` separado |

## Vocabulário de passos

Todo passo de um cenário `@automatizado` (e de um `Contexto`) é uma das frases abaixo, com os
parâmetros preenchidos. Cada frase vira **uma** função em `tests/step_defs/`, registrada com
`parsers.parse` do pytest-bdd. Os números têm lacunas (V03 e V17 saíram por não serem usados);
os IDs existentes não mudam. Os cenários `@manual` têm texto livre e são pulados.

### Tipos de parâmetro

- `"{x}"` é sempre `"{x:Q}"`: texto entre aspas que aceita vazio e aspas escapadas. Padrão
  `(?:[^"\\]|\\.)*`; a conversão desfaz só `\"`, `\n`, `\r`, `\t` e `\x1b` (não usar
  `unicode_escape`: ele avisa sobre `\d`, e com `filterwarnings = error` o aviso derruba o teste).
- `{x:L}`: lista de itens entre aspas separados por `, ` ou ` e ` (`"WIDTH=9", "HEIGHT=7" e
  "EXIT=8,6"`); um item só também vale.
- `{x:d}`: inteiro.
- Enums (lista fechada mais abaixo): o padrão ordena as alternativas da mais longa para a mais
  curta, para `a saída` não engolir `a saída de erro`.
- Num Esquema do Cenário, `<coluna>` fica dentro das aspas; o pytest-bdd troca pelo valor antes
  de casar a frase.
- `Dado`, `Dada`, `Dados`, `Dadas` são a mesma palavra-chave; `E`/`Mas` herdam o tipo do passo
  anterior.

### Regras de execução

- Comandos (inclusive os de V50 e V55) rodam com `cwd` = `project/`, ou a cópia criada por V02
  (`clone limpo`, `clone do remoto`), ou a pasta definida por V05; `PATH` começando por
  `.venv/bin`; tempo limite de 30 s.
- O git da suíte (clone limpo, V60) roda sem a configuração global de quem executa:
  `core.excludesFile`, hooks e assinatura de commit desligados, para que um ignore global não
  esconda um `.gitignore` incompleto do projeto.
- O config é um objeto (linhas + destino, padrão `cfg.txt` em `project/`, apagado no fim do
  teste); só é gravado em disco num passo `Quando` ou ao iniciar o programa, para que o `Contexto`
  possa ser alterado pelo cenário. O destino nunca é `config.txt`.
- "Labirinto atual" é o último produzido: o `OUTPUT_FILE` de uma execução com código 0, o
  `grid`/`solution`/`pattern` de `generate()` ou um labirinto de teste. Os passos `Então` sobre
  labirinto valem para todos os labirintos gerados no cenário.
- Renderização: a saída padrão é dividida em blocos de 2 × HEIGHT + 1 linhas; cada posição são 2
  espaços com cor de fundo ANSI (I02, códigos na I21). Numa sessão, as propriedades de V72
  `a renderização` olham todas as renderizações da sessão (ex.: o rodízio de cores), e as que
  citam o arquivo de saída comparam com o `OUTPUT_FILE` atual.
- Valores das listas fechadas são comparados com o texto do passo antes da conversão de `Q`.
- Sessão interativa: `subprocess.Popen` com uma thread lendo a saída; cada envio espera o prompt
  `Choice? (1-4): ` (I03) ou o fim do processo.

### Catálogo

| ID | Tipo | Frase | O que a função faz | Usa → produz |
|---|---|---|---|---|
| V01 | given | `o arquivo "{arquivo}" na raiz do repositório` | confere que existe; caminho relativo à raiz do repositório (inclusive em subpasta, como `mazegen/__init__.py`); aceita glob (`mazegen-*`) | → alvos |
| V02 | given | `o repositório no estado "{estado}"` | prepara o repositório (lista de estados) | → repo |
| V04 | given | `um virtualenv novo "{venv}" em que rodou {comandos:L}` | cria o venv e roda os comandos nele; exige código 0 | repo → venvs |
| V05 | given, when | `o ambiente de execução é o virtualenv "{venv}" na pasta "{pasta}"` | os próximos comandos usam o `PATH` do venv e o `cwd` pasta (`"."` = repo) | venvs → ambiente |
| V06 | given | `o código-fonte de {alvos:L}` | lista os `.py` dos alvos; `"."` = `project/` sem `.venv`, `build` e `dist` | → fontes |
| V07 | given | `o config {origem:Origem}` | carrega o config base deste README ou o `config.txt` do repositório | → config |
| V08 | given | `o config {origem:Origem} salvo em "{arquivo}"` | igual a V07, com outro destino; cria a pasta pai se faltar | → config |
| V09 | given | `o config base com {pares:L}` | parte do config base e aplica cada `CHAVE=valor` (troca a linha da chave ou acrescenta no fim) | → config |
| V10 | given | `o config com {pares:L}` | aplica os pares sobre o config atual (depois de um `Contexto`) | usa config |
| V11 | given | `o config sem a chave "{chave}"` | remove as linhas da chave | usa config |
| V12 | given | `o config com a linha {n:d} trocada por "{linha}"` | troca a linha número n (começa em 1) | usa config |
| V13 | given | `o config com a linha da chave "{chave}" trocada por "{linha}"` | troca a linha da chave; `""` equivale a removê-la | usa config |
| V14 | given | `o config com a linha "{linha}" {posicao:Pos}` | insere a linha no início ou no fim | usa config |
| V15 | given | `o config escrito com a variação "{variacao}"` | transforma o texto na hora de gravar (lista de variações) | usa config |
| V16 | given | `o caminho "{caminho}" preparado como "{tipo}"` | cria arquivo ou diretório especial (lista de tipos); no fim restaura permissões e apaga; desliga a gravação automática do config nesse destino | → preparados |
| V18 | given, when | `a situação de erro "{situacao}"` | combina V16, V11 e V09 conforme a situação (lista), agindo sobre o config atual e o seu destino | config, preparados |
| V19 | given | `os casos de erro do catálogo da suíte` | carrega `CATALOGO_DE_ERROS` do `conftest.py`: um caso por cenário de erro de 03, 04, 05, 07, 08 e 13 | → catalogo |
| V20 | given | `um labirinto gerado pelo {gerador:Gerador} com o config base` | gera pelo programa (entrada `"4"`) ou pela classe `MazeGenerator` | → labirintos |
| V21 | given | `um labirinto gerado pelo {gerador:Gerador} com o config base mais {pares:L}` | igual a V20, com os pares aplicados | → labirintos |
| V22 | given | `o labirinto de teste com a grade "{grade}", entrada "{entrada}" e saída "{saida}"` | grava um arquivo de saída; linhas da grade separadas por ` / `; caminho do rodapé calculado por BFS | → labirintos |
| V23 | given | `o labirinto de teste "{modelo}"` | arquivo pronto (lista de modelos; o exemplo do subject fica em `tests/fixtures/`) | → labirintos |
| V24 | given | `a célula de dígito "{digito}"` | célula isolada a partir do dígito | → celula |
| V25 | given | `a célula com as paredes fechadas "{paredes}"` | célula isolada a partir das paredes | → celula |
| V26 | given | `o gerador "{expressao}"` | avalia `MazeGenerator(...)` com literais (`eval` só com `MazeGenerator` no escopo) e guarda o texto | → gerador |
| V27 | given | `o programa iniciado com "{comando}"` | grava o config, abre o processo e espera o primeiro prompt | config → sessao |
| V28 | given | `o programa iniciado com "{comando}", com o caminho {vis:Visib}` | como V27; `visível` envia `"2"`; `oculto` confere que não há ciano | → sessao |
| V29 | when | `eu executo {comandos:L}` | grava o config e roda cada comando com stdin vazio; se `a_maze_ing.py` saiu com 0, lê o `OUTPUT_FILE` | → resultado, resultados, labirintos |
| V30 | when | `eu executo {comandos:L} com a entrada {linhas:L}` | como V29, com as linhas no stdin, cada uma terminada em `\n` | → resultado, resultados, labirintos |
| V31 | when | `eu executo {comandos:L} {n:d} vezes com a entrada {linhas:L}` | repete V30 n vezes | → execucoes |
| V32 | when | `eu gero o labirinto` | `python3 a_maze_ing.py <destino do config>` com a entrada `"4"` | → resultado, labirintos |
| V33 | when | `eu gero o labirinto {n:d} vezes` | repete V32; cada passo `Quando` de repetição (V31, V33–V35, V43, V47) substitui a lista de execuções anterior | → execucoes |
| V34 | when | `eu gero o labirinto com cada um de {pares:L}` | uma geração por par, cada uma sobre uma cópia do config | → execucoes |
| V35 | when | `eu gero o labirinto com cada seed de {inicio:d} a {fim:d}` | uma geração por seed | → execucoes |
| V36 | when | `eu gero o labirinto e o analiso com o maze_analyzer.py` | V32 seguido de V37 | → analise |
| V37 | when | `eu analiso o labirinto com o maze_analyzer.py` | roda `tests/maze_analyzer.py` (cópia do `private/`, feita pelo `setup.sh`) sobre o arquivo atual | → resultado, analise |
| V38 | when | `eu analiso o labirinto com o maze_analyzer.py "{opcoes}"` | como V37, com as opções | → analise |
| V39 | when | `o validador da suíte lê o labirinto` | lê o arquivo atual ou o resultado da classe; numa sessão, relê o `OUTPUT_FILE` regravado pela última ação | → labirintos |
| V40 | when | `o validador da suíte converte a célula` | converte dígito em paredes e vice-versa (N=1, E=2, S=4, W=8) | usa celula |
| V41 | when | `a análise estática percorre o código-fonte` | `ast.parse` de cada fonte | fontes → arvores |
| V42 | when | `o gerador gera o labirinto` | `generate()` e leitura de `grid`, `solution`, `pattern` | gerador → labirintos |
| V43 | when | `eu gero o labirinto com {n:d} instâncias novas do gerador` | avalia a expressão de novo n vezes e gera | → execucoes |
| V44 | when | `eu tento criar o gerador "{expressao}"` | avalia a expressão e guarda a exceção | → excecao |
| V45 | when | `eu envio ao menu {linhas:L}` | escreve cada linha e espera o prompt ou o fim | usa sessao |
| V46 | when | `o evento "{evento}" acontece no menu` | `EOF` fecha o stdin; `SIGINT` envia o sinal; ou espera | usa sessao |
| V47 | when | `cada caso do catálogo é executado com tempo limite` | roda cada caso de V19 | catalogo → execucoes |
| V48 | then | `o código de saída é {codigo:d}` | confere o código; numa sessão, espera o processo terminar | resultado ou sessao |
| V49 | then | `todos os comandos terminam com código {codigo:d}` | confere todos os resultados do cenário | resultados |
| V50 | then | `o comando "{comando}" termina com código {codigo:d}` | roda o comando agora e confere | — |
| V51 | then | `o processo termina dentro do tempo limite` | confere que não houve timeout | resultado |
| V52 | then | `{fluxo:Fluxo} {verbo:Contem} {textos:L}` | `a saída` = stdout + stderr; "contém" exige todos, "não contém" proíbe todos | resultado ou sessao |
| V53 | then | `{fluxo:Fluxo} é "{texto}"` | igualdade depois de `strip()` | resultado ou sessao |
| V54 | then | `a saída de "{comando}" contém "{texto}"` | usa o resultado desse comando no cenário, ou roda agora | resultados |
| V55 | then | `a saída de "{comando}" é "{texto}"` | como V54, com igualdade depois de `strip()` | resultados |
| V56 | then | `a linha da saída que contém "{a}" também contém "{b}"` | acha a linha com `a` e confere `b` nela | resultado ou sessao |
| V57 | then | `a mensagem de erro cita {itens:L}` | stderr com uma linha, começando com `Error: `, contendo os itens na ordem | resultado |
| V58 | then | `a mensagem de erro explica "{motivo}"` | casa a expressão do motivo (I21) | resultado |
| V59 | then | `o resultado da execução é "{resultado}"` | `sucesso` ou `erro citando A, B[; motivo: M]` | resultado |
| V60 | then | `o caminho "{caminho}" {estado:EstadoCaminho}` | `exists`, `git check-ignore`, `git ls-files` ou tamanho > 0; aceita glob | repo |
| V61 | then | `o arquivo "{arquivo}" {verbo:Contem} {textos:L}` | procura as strings no arquivo lido sem converter quebras de linha (`newline=""`), para `\r` ser detectável | repo |
| V62 | given, then | `o arquivo "{arquivo}" {tem:TemLinha} que casa com a expressão "{regex}"` | `re.search` com `re.M` | repo |
| V63 | then | `nenhum arquivo .py do projeto contém "{texto}"` | percorre os `.py` de `project/` sem `.venv`, `build` e `dist` | repo |
| V64 | then | `a seção "{secao}" do README contém {textos:L}` | do título `#… secao` até o próximo título do mesmo nível | repo |
| V65 | then | `o metadado "{campo}" do pacote "{arquivo}" é "{valor}"` | lê `METADATA`/`PKG-INFO` com `email.parser`; aceita glob e confere cada arquivo | repo |
| V66 | then | `o pacote "{arquivo}" confirma "{propriedade}"` | propriedades do pacote (lista); aceita glob e confere cada arquivo | repo |
| V67 | then | `{alvo:Alvo} casa com a expressão "{regex}"` | aplica a expressão a cada item do alvo | labirintos, resultado, lido |
| V68 | then | `a grade do labirinto tem {largura:d} colunas e {altura:d} linhas` | dimensões do labirinto atual | labirintos |
| V69 | then | `a linha {n:d} do rodapé é "{texto}"` | n de 1 a 3 | labirintos |
| V70 | then | `o arquivo de saída é idêntico byte a byte ao gerado com o config base` | gera também com o config base e compara os bytes | labirintos |
| V71 | then | `os resultados são {relacao:Relacao} em "{aspecto}"` | compara as execuções aos pares no aspecto (lista) | execucoes |
| V72 | then | `{sujeito:Sujeito} confirma "{propriedade}"` | propriedade da lista fechada do sujeito | conforme o sujeito |
| V73 | then | `o validador da suíte relata "{relato}" em "{verificacao}"` | compara o texto que o validador devolve | labirintos |
| V74 | then | `o validador da suíte conta {n:d} "{item}"` | conta os itens (lista) | labirintos |
| V75 | then | `a célula "{celula}" {estado:EstadoCelula}` | célula dada como `"x,y"` | labirintos |
| V76 | then | `pelo menos uma das células {celulas:L} é alcançável a partir da entrada` | alcançável e sem valor F | labirintos |
| V77 | then | `todas as células da "{borda}" têm a parede "{direcao}" fechada` | percorre a borda | labirintos |
| V78 | then | `as células de valor F ocupam as colunas "{colunas}" e as linhas "{linhas}"` | intervalos como `"6 a 8 e 10 a 12"` | labirintos |
| V79 | then | `o dígito da célula é "{digito}"` | sobre a célula; compara sem diferenciar maiúsculas | celula |
| V80 | then | `as paredes {estado:FA} da célula são "{paredes}"` | sobre a célula | celula |
| V81 | then | `a célula tem {n:d} paredes fechadas` | sobre a célula | celula |
| V82 | then | `o bit {bit:d} da célula está ligado` | sobre a célula | celula |
| V83 | then | `a linha "{rotulo}" do maze_analyzer.py {op:Op} {textos:L}` | rótulo = início da linha da saída do analyzer; roda o analyzer se ainda não rodou | analise |
| V84 | then | `o número na linha "{rotulo}" do maze_analyzer.py é {cmp:Cmp} {n:d}` | primeiro inteiro da linha | analise |
| V85 | then | `o veredito do maze_analyzer.py corresponde ao PERFECT do config` | `True` → `PERFECT maze`; `False` → `Pac-Man-USABLE` | analise, config |
| V86 | then | `na última renderização, as posições de "{elemento}" têm a cor "{cor}"` | todas as posições do elemento têm a cor | resultado ou sessao |
| V87 | then | `na última renderização, a cor "{cor}" só aparece em "{elemento}"` | a cor não aparece fora do elemento | resultado ou sessao |
| V88 | then | `na última renderização, nenhuma posição tem a cor "{cor}"` | ausência da cor | resultado ou sessao |
| V89 | then | `na última renderização, as células de dígito "{digito}" mostram exatamente as paredes "{paredes}"` | exige pelo menos uma célula com o dígito | resultado, labirintos |
| V90 | then | `o programa continua em execução` | `poll() is None` | sessao |
| V91 | then | `o programa aguarda no prompt "{prompt}"` | processo vivo e o prompt é a última coisa impressa | sessao |
| V92 | then | `o construtor levanta "{excecao}"` | tipo da exceção guardada | excecao |
| V93 | then | `a mensagem da exceção cita {trechos:L}` | `str(excecao)` contém os trechos | excecao |
| V94 | when | `eu leio "{arquivo}"` | carrega texto, metadados ou lista de conteúdo; aceita glob | → lido |
| V95 | given | `o exemplo de uso da docstring de "{modulo}" salvo em "{arquivo}"` | extrai o bloco de código da seção `Example:` da docstring do módulo (I22) e grava no arquivo | → preparados |

### Listas fechadas

| Parâmetro | Valores |
|---|---|
| Origem | `base`, `do repositório` |
| Pos | `inserida no início`, `acrescentada no fim` |
| Gerador | `programa`, `módulo mazegen` |
| Visib | `oculto`, `visível` |
| Fluxo | `a saída`, `a saída padrão`, `a saída de erro` |
| Contem | `contém`, `não contém` |
| TemLinha | `tem uma linha`, `não tem nenhuma linha` |
| EstadoCaminho | `existe`, `não existe`, `é ignorado pelo git`, `não é ignorado pelo git`, `está versionado no git`, `não está vazio` |
| Alvo | `a solução`, `cada linha da grade`, `cada linha de coordenadas do rodapé`, `a linha 3 do rodapé`, `a primeira linha do README`, `o nome de cada arquivo selecionado`, `a última linha da saída padrão` |
| Relacao | `idênticos`, `diferentes entre si` |
| Sujeito | `o validador da suíte`, `a renderização`, `a análise estática`, `o módulo mazegen`, `o catálogo de casos de erro` |
| EstadoCelula | `não tem valor F`, `é alcançável a partir da entrada`, `tem as paredes externas fechadas` |
| FA | `fechadas`, `abertas` |
| Op | `começa com`, `contém` |
| Cmp | `pelo menos`, `no máximo` |
| V02 estado | `atual` (`cwd` em `project/`); `instalado` (`make install`, uma vez por sessão); `clone limpo` (cópia do que `git -C project ls-files` lista para uma pasta temporária, seguida de `git init`, `git add` e `git commit` só nessa cópia, porque a raiz do git é `dojo`); `clone do remoto` (`git clone $AMAZEING_REMOTE`; o cenário é pulado se a variável não existir) |
| V15 variação | `uma linha vazia entre cada par`, `espaços em volta do igual`, `espaços no fim de cada linha`, `finais de linha CRLF`, `sem quebra de linha depois da última linha`, `chave WIDTH minúscula`, `todas as chaves minúsculas`, `chave HEIGHT capitalizada`, `perfect=true minúsculo` |
| V16 tipo | `inexistente`, `diretório`, `diretório sem permissão de escrita`, `sem permissão de leitura` (config base com `chmod 000`), `não UTF-8`, `vazio`, `bytes binários aleatórios`, `só espaços e tabulações`, `BOM UTF-8 + config base`, `config base com WIDTH de 100000 dígitos`, `só WÍDTH=20 e HEÍGHT=15, com acento`, `pasta com a_maze_ing.py e config.txt`, `diretório pai criado` |
| V18 situação | `arquivo de configuração inexistente`, `arquivo de configuração sem permissão de leitura`, `chave obrigatória ausente`, `valor inválido`, `parâmetros impossíveis`, `OUTPUT_FILE num diretório inexistente` |
| V23 modelo | `exemplo do subject`, `exemplo do subject com o rodapé anotado`, `perfeito do config base`, `perfeito do config base com uma parede interna aberta` |
| V46 evento | `EOF`, `SIGINT`, `1 segundo sem entrada` |
| V58 motivo | `arquivo não encontrado`, `arquivo não é UTF-8`, `chave obrigatória ausente`, `entrada igual à saída`, `tamanho sem tabuleiro Pac-Man`, `coordenada no padrão 42` (palavras-chave na I21) |
| V71 aspecto | `arquivo de saída`, `grade`, `solução`, `células de valor F`, `saída exibida` |
| V72 o validador da suíte | `valores de 0 a 15`, `bits na convenção N=1, E=2, S=4, W=8`, `x é a coluna e y é a linha`, `entrada e saída válidas`, `entrada diferente da saída`, `x de entrada e saída dentro da largura`, `y de entrada e saída dentro da altura`, `toda célula fora do 42 alcançável`, `borda fechada`, `paredes coerentes`, `vizinhas leste-oeste coerentes` (bit E de (x, y) = bit W de (x+1, y)), `vizinhas norte-sul coerentes` (bit S de (x, y) = bit N de (x, y+1)), `inalcançáveis são as células do 42`, `células F em dois componentes 4-conexos`, `componente da esquerda com a forma do 4`, `componente da direita com a forma do 2`, `células F iguais ao padrão 42`, `nenhuma célula F fora do padrão`, `42 sem passagem aberta`, `glifos 3x5 com uma coluna livre entre os dígitos`, `42 presente`, `42 ausente`, `42 com margem de corredor`, `42 fora dos cantos`, `centro livre do 42`, `árvore geradora fora do 42`, `caminho único entre entrada e saída`, `ramos fora da solução terminam em beco`, `solução atravessa só paredes abertas`, `solução não sai da grade`, `solução não entra no 42`, `solução termina na saída`, `solução mais curta`, `solução sem célula repetida`, `solução válida e mais curta`, `pelo menos 2 rotas independentes`, `no máximo 2 becos reais`, `zero becos reais`, `sem área aberta 3x3`, `blocos 2x2, 2x3 e 3x2 abertos aceitos`, `modo igual ao PERFECT do config`, `rodapé com ENTRY, EXIT e caminho válido`, `labirinto válido conforme o config` (dimensões, valores, borda, coerência, entrada e saída, "42" por D06/D07, conectividade, sem 3x3, solução válida e mais curta, modo), `uma linha vazia logo após a grade`, `exatamente 3 linhas após a linha vazia`, `arquivo termina com quebra de linha`, `linha vazia contém só a quebra de linha`, `nenhuma linha com espaço no fim` |
| V72 a renderização | `cada renderização seguida do menu`, `nova renderização abaixo da anterior, seguida do menu`, `2 × HEIGHT + 1 linhas`, `2 × WIDTH + 1 posições de 2 caracteres por linha`, `só caracteres ASCII`, `cores por sequências ANSI de fundo`, `cada linha termina com o reset ANSI`, `última sequência ANSI é o reset`, `paredes iguais às do arquivo de saída`, `entrada e saída iguais às do rodapé`, `caminho do arquivo marcado em ciano`, `caminho marcado liga entrada e saída por paredes abertas`, `caminho marcado com o comprimento da busca em largura`, `cinco cores distintas para entrada, saída, 42, caminho e paredes`, `paredes em rodízio branco, amarelo, verde, azul`, `labirinto diferente do da renderização anterior` |
| V72 a análise estática | `open sempre dentro de with`, `anotação de retorno em toda definição`, `docstring em cada função`, `docstring em cada método`, `docstring em cada classe`, `docstrings com aspas triplas duplas`, `resumo de uma frase terminado em ponto`, `linha em branco entre resumo e descrição`, `seção Args: nas funções com parâmetros`, `seção Returns: nas funções que retornam valor`, `coleções vazias com tipo anotado`, `testes usam pytest ou unittest`, `mazegen não importa a_maze_ing`, `sem MiniLibX` |
| V72 o módulo mazegen | `uma única classe pública de geração`, `grid e solution preenchidos após generate()`, `solution pública e documentada`, `grid público com as paredes de cada célula`, `mesmos parâmetros geram a mesma grade`, `grade igual à do arquivo de saída`, `só MazeError escapa do construtor` |
| V72 o catálogo de casos de erro | `nenhum caso termina com Traceback`, `nenhum caso estoura o tempo limite`, `mensagem começa com Error:`, `mensagem cita o arquivo, a linha ou a chave`, `mensagem sem nome de exceção do Python` (as três últimas pulam o caso de uso errado da linha de comando, I12) |
| V66 propriedade | `contém o código do módulo`, `contém a docstring de mazegen/__init__.py`, `README como descrição longa`, `instala e importa MazeGenerator num virtualenv novo`, `formato produzido por python -m build`, `mesma versão no nome dos arquivos`, `versão igual à do pyproject.toml`, `LICENSE.md incluído`, `nada do build ignorado pelo git` |
| V73 relato | em `coerência das paredes`: `coerente`, `incoerente entre (x,y) e (x,y)`; em `áreas abertas`: `aceito`, `recusado: área 3x3`; em `modo Pac-Man`: `recusado: N rota(s) independente(s)` |
| V74 item | `células de valor F`, `janelas 2x2 abertas`, `células alcançáveis`, `letras da solução` |
| V77 borda / direção | `primeira linha`, `última coluna`, `última linha`, `primeira coluna` / `Norte`, `Leste`, `Sul`, `Oeste` |
| Paredes (V25, V80, V89) | `nenhuma` ou direções em lista com vírgulas e "e": `Norte`, `Norte e Sul`, `Norte, Leste, Sul e Oeste` |
| V83/V84 rótulo | `Verdict:`, `Reachable region`, `Independent loops`, `Dead-ends`, `Corners + centre`, `Wall coherence`, `Entry` |
| V86–V88 elemento / cor | `entrada`, `saída`, `células do caminho`, `passagens do caminho`, `células do 42`, `paredes` / `branco`, `amarelo`, `verde`, `azul`, `magenta`, `vermelho`, `ciano`, `cinza` (códigos SGR na I21) |
| V65 campo | `Name`, `Version`, `License-Expression` |
| V45 linhas | `1` regenerar, `2` mostrar/ocultar o caminho, `3` trocar a cor das paredes, `4` sair; inválidas usadas: `9`, `abc`, `""`, `-1` |
| V91 prompt | `Choice? (1-4): ` |
| V92 exceção | `MazeError` |
| V26/V44 expressão | só `MazeGenerator(...)` com literais, na assinatura da I09 |
| V29–V31 comandos | `make install`, `make run`, `make debug`, `make clean`, `make lint`, `make lint-strict`, `make build`, `make -n <regra>`; `test -f …`, `test $(…) = $(…)`; `git ls-files …`, `git check-ignore …`, `git fetch`, `git status --porcelain`, `git rev-parse …`; `python3 a_maze_ing.py …`, `python3 -X dev a_maze_ing.py …`, `python a_maze_ing.py …`, `python3 -c '…'`, `python -c '…'`; `.venv/bin/python -c '…'`, `.venv/bin/python -m flake8 …`, `.venv/bin/python -m mypy …`, `.venv/bin/python -m build …`, `.venv/bin/flake8 .`, `.venv/bin/mypy …`, `mypy …`; `pip install …`, `python -m build`; redirecionamento `< /dev/null > arquivo`. O analyzer roda por V36–V38, nunca por V29 |

## Configuração da suíte

### Estrutura

```text
a-maze-ing/
├── project/              ← entrega da 42 (sem tests/)
├── private/              ← subject, régua, maze_analyzer.py
└── tests/                ← suíte, só no monorepo dojo
    ├── .gitignore        ← .venv/, __pycache__/, .pytest_cache/, maze_analyzer.py
    ├── requirements.txt  ← pytest==9.2.0, pytest-bdd==9.0.1, flake8==7.4.1, mypy==2.4.1
    ├── .flake8, mypy.ini ← lint da suíte (mypy --strict; o pacote parse tem stubs sem py.typed)
    ├── pytest.ini
    ├── maze_analyzer.py  ← cópia de private/maze_analyzer.py feita pelo setup.sh; fora do git
    ├── conftest.py       ← tipos de parâmetro, fixtures, hook de tags, CATALOGO_DE_ERROS
    ├── step_defs/        ← uma função por frase do vocabulário
    ├── unit/             ← testes unitários do gerador, solver, parser do config e validador
    ├── fixtures/         ← exemplo de saída do subject (grade 25x20 + rodapé)
    └── features/         ← os .feature e este README
```

### `pytest.ini`

```ini
[pytest]
bdd_features_base_dir = features
pythonpath = ../project
testpaths = step_defs unit
filterwarnings = error
markers =
    obrigatorio: requisito "must" do subject
    recomendado: requisito "should" do subject
    opcional: requisito "may" do subject
    bonus: bônus do Capítulo VIII
    informativo: contexto sem exigência própria
    derivado: consequência de requisito, exemplo ou figura
    automatizado: executado pela suíte
    manual: verificado por inspeção ou na defesa
```

### Hook de tags (`conftest.py`)

`pytest_bdd_apply_tag(tag, function)`:

- `manual` → aplica `pytest.mark.manual` e `pytest.mark.skip(reason="verificação manual")`; devolve
  `True` (o marcador permite `-m manual` e `-m "not manual"`);
- `decisao-I19` → `pytest.mark.skip(reason="fora da primeira versão (I19)")`; devolve `True`;
- tags que começam com `pdf-`, `md-`, `regua-` ou `decisao-` → não viram marcador; devolve
  `True` (são referências; com hífen não serviriam para `-m`);
- qualquer outra → devolve `None` (o pytest-bdd cria o marcador, já registrado no `pytest.ini`).

### `maze_analyzer.py`

O `setup.sh` copia `private/maze_analyzer.py` para `tests/maze_analyzer.py` quando a cópia não
existe, e o `.gitignore` da suíte a mantém fora do git: o `private/` é material do subject e não vai para o
remoto. No `conftest.py`, o caminho é uma constante (`Path(__file__).parent / "maze_analyzer.py"`);
se o arquivo não existir, os passos do analyzer falham com mensagem que manda rodar o `setup.sh`.

### Variável de ambiente

| Variável | Valor | Ausente |
|---|---|---|
| `AMAZEING_REMOTE` | URL do repositório de entrega | o cenário com `clone do remoto` é pulado |

### Primeiros passos

1. `sh tests/setup.sh` (a partir de `a-maze-ing/`): cria `step_defs/`, `unit/` e `fixtures/`,
   move `test_hello.py` para `unit/`, copia o `maze_analyzer.py`, cria `requirements.txt`,
   `.gitignore` e `pytest.ini` (só se não existirem), cria `.venv` com Python 3.14 e instala
   pytest e pytest-bdd. Pode rodar de novo.
2. `conftest.py` com o hook de tags descrito acima. Ele vem antes de tudo: sem ele, as tags de
   referência (`@pdf-…`) viram marcadores desconhecidos e, com `filterwarnings = error`, a coleta
   para.
3. `step_defs/test_features.py` com `scenarios(".")`: liga todos os `.feature` de `features/`
   (o caminho é relativo a `bdd_features_base_dir`).
4. `--generate-missing` lista os passos sem função; cada frase do catálogo vira uma função.

### Comandos

```sh
cd a-maze-ing/tests

.venv/bin/pytest --generate-missing --feature features   # lista passos sem função e imprime o esqueleto
                                                          # (lista também os passos dos cenários @manual: ignore esses)
.venv/bin/pytest -m "not manual"                          # roda os cenários automatizados
.venv/bin/pytest -m "not manual" -v --gherkin-terminal-reporter
.venv/bin/pytest -m "not manual" --cucumberjson=relatorio.json
.venv/bin/pytest -m "obrigatorio and not manual"          # só os obrigatórios
.venv/bin/pytest -m manual -rs                            # lista os manuais (checklist da defesa)
.venv/bin/flake8 . && .venv/bin/mypy .                    # lint da suíte (D20)
```
