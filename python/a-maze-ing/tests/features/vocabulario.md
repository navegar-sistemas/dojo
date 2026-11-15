# Vocabulário de passos

Todo passo de um cenário `@automatizado` (e de um `Contexto`) é uma das frases abaixo, com os
parâmetros preenchidos. Cada frase vira **uma** função em `tests/step_defs/`, registrada com
`parsers.parse` do pytest-bdd. `make faltantes` lista as frases que ainda não têm função. Os
números têm lacunas (V03, V17 e V63 saíram por não serem usados); os IDs existentes não mudam. Os
cenários `@manual` não têm passos: o roteiro de inspeção fica na descrição do cenário, uma
linha por item começando com `- `, e eles ficam fora de `make run`. Assim nem o pytest-bdd nem
a extensão Cucumber do VS Code procuram função para esse texto.

O texto fixo das frases não usa `.`, `(`, `)`, `*`, `\` nem `|`: com um desses caracteres, a
extensão Cucumber do VS Code lê a string Python do passo como expressão regular, não casa os
parâmetros `{...}` e marca o passo como indefinido. Por isso as frases dizem `arquivo Python` e
`maze_analyzer`, sem `.py`. A regra vale também para o nome das propriedades de V72, que faz
parte do texto fixo.

## Tipos de parâmetro

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

## Regras de execução

- Comandos (inclusive os de V50 e V55) rodam com `cwd` = `project/`, ou a cópia criada por V02
  (`clone limpo`, `clone do remoto`), ou a pasta definida por V05.
- `PATH`: nos estados `instalado`, `clone limpo` e `clone do remoto` começa pelo `.venv/bin` do
  repositório do cenário; no estado `atual` é o `PATH` de quem roda a suíte, cujo `python3`
  precisa ser 3.10 ou posterior (a rodada para no início quando não é).
- Tempo limite de 30 s: o grupo de processos do comando morre e o resultado fica marcado como
  estourado (V51); a saída é lida por mais 2 s, e um processo noutra sessão que ainda segure o
  stdout é abandonado com a saída lida até ali.
- Antes de rodar `a_maze_ing.py <config>`, o `OUTPUT_FILE` desse config vai para a reserva da
  V16 e volta no fim do teste; um caminho que a V16 já preparou fica como ela deixou.
- O git da suíte (V02, V60) roda sem a configuração global e de sistema de quem executa
  (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, sem as variáveis `GIT_DIR`,
  `GIT_TEMPLATE_DIR` e afins) e com `core.excludesFile`, hooks e assinatura de commit
  desligados: nem um ignore global nem o `info/exclude` de um modelo de `git init` escondem um
  `.gitignore` incompleto do projeto. A URL de `clone do remoto` precisa funcionar sem essa
  configuração (SSH com a chave em `~/.ssh` ou URL pública).
- No estado `atual`, o git de `project/` é o do monorepo `dojo`: o `.gitignore` da raiz do
  `dojo` (que ignora `.mypy_cache` em qualquer pasta) vale também ali. As conferências de
  `é ignorado pelo git` e `não é ignorado pelo git` usam o estado `clone limpo`.
- Os tipos da V16 que dependem de `chmod` (`sem permissão de leitura` e `diretório sem
  permissão de escrita`, inclusive pela situação `arquivo de configuração sem permissão de
  leitura` da V18) pulam o cenário quando a suíte roda como root, que a permissão não barra.
- V36–V38 usam `private/maze_analyzer.py`, que vem com o subject e não é versionado; sem ele o
  passo falha citando o caminho que falta.
- O config é um objeto (linhas + destino, padrão `cfg.txt` em `project/`, apagado no fim do
  teste junto com as pastas pai que a gravação criou); só é gravado em disco num passo `Quando`
  ou ao iniciar o programa, para que o `Contexto` possa ser alterado pelo cenário. O destino
  nunca é `config.txt`.
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
- O parâmetro de V60, V75 e V80 chama `situacao`, não `estado`: `estado` é o nome da fixture
  do cenário, que todo passo recebe.

## Critérios dos passos

O que cada passo confere onde a coluna "O que a função faz" do catálogo não fixa tudo.

- Labirintos: os passos `Então` sobre labirinto valem para `labirintos` mais o labirinto de
  cada item de `execucoes`, sem repetir o mesmo; sem nenhum, o passo falha. As propriedades que
  dependem do config usam o config atual do cenário. O "42" esperado é o da D07 para as
  dimensões da grade e, num labirinto da classe, também o `pattern` dela. V69 e as propriedades
  de formato do arquivo falham sobre um labirinto da classe, que não tem rodapé.
- V22 e V23 gravam `labirinto_de_teste.txt` na pasta do cenário. Os modelos de V23 estão em
  `tests/fixtures/`, com a origem de cada um em `suporte/labirinto.py`.
- V37: o arquivo analisado é o `OUTPUT_FILE` da execução que produziu o labirinto atual, se o
  disco ainda tem o mesmo texto; senão, o texto do labirinto vai para um arquivo temporário. V84
  e V85 também rodam o analyzer quando ele ainda não rodou; V85 compara o `PERFECT` sem
  diferenciar caixa.
- V73 em `modo Pac-Man`: o relato é o da primeira checagem que falha, nesta ordem: rotas
  independentes, becos reais, canto ou centro fechado, células inalcançáveis; sem falha,
  `aceito`. Em `coerência das paredes`, vários pares incoerentes são separados por `; `.
- V67 aplica `re.search` sem flags (as expressões já têm `^` e `$`); a linha da grade é a linha
  crua do arquivo e, num labirinto da classe, o hexadecimal minúsculo.
- V71 exige pelo menos 2 execuções; "diferentes entre si" exige todas distintas duas a duas.
- Catálogo (V19): um caso por linha de Exemplos de cada cenário de erro de 03, 04, 05, 07, 08 e
  13 que roda o programa; cada caso guarda o que a mensagem cita (o do cenário ou, sem ele, o da
  D01). V47 roda cada caso num estado próprio, desfeito logo depois.
- V04 cria o venv numa pasta temporária, com o `python3` do `PATH` do cenário; os comandos dele
  não entram em `resultados`. V05 resolve a pasta contra a raiz do repositório.
- V26 e V44 conferem a expressão com `ast` (uma chamada a `MazeGenerator` só com literais e
  parâmetros da I09) antes do `eval`; entrada e saída do labirinto vêm dos literais (`entry`
  ausente = `(0, 0)`, `exit` ausente = canto inferior direito). `só MazeError escapa do
  construtor` testa a expressão do cenário e uma lista fixa de valores e tipos errados.
- Renderização: os blocos são as linhas com ESC, cortadas em 2 × HEIGHT + 1; `49` e o reset
  contam como sem cor; a cor das paredes é a do canto `(0, 0)`. `células do 42` são as células
  de valor F do arquivo; `células do caminho` excluem entrada e saída. `seguida do menu` exige
  as 5 linhas do menu da figura e o prompt logo depois do bloco. `nova renderização abaixo da
  anterior` proíbe sequência CSI que não seja SGR. `paredes em rodízio` só vale numa sessão:
  cada `1`, `2` ou `3` enviado é uma renderização e só o `3` avança a cor.
- Sessão: V27 falha se o programa terminar antes do primeiro prompt; V28 `visível` também
  confere que o ciano apareceu; V46 espera o prompt ou o fim depois de EOF e SIGINT.

## Catálogo

| ID | Tipo | Frase | O que a função faz | Usa → produz |
|---|---|---|---|---|
| V01 | given | `o arquivo "{arquivo}" na raiz do repositório` | confere que existe; caminho relativo à raiz do repositório (inclusive em subpasta, como `mazegen/__init__.py`); aceita glob (`mazegen-*`) | → alvos |
| V02 | given | `o repositório no estado "{estado}"` | prepara o repositório (lista de estados) | → repo |
| V04 | given | `um virtualenv novo "{venv}" em que rodou {comandos:L}` | cria o venv e roda os comandos nele; exige código 0 | repo → venvs |
| V05 | given, when | `o ambiente de execução é o virtualenv "{venv}" na pasta "{pasta}"` | os próximos comandos usam o `PATH` do venv e o `cwd` pasta, relativa à raiz do repositório do cenário, a mesma base da V16 (`"."` = a raiz) | venvs → ambiente |
| V06 | given | `o código-fonte de {alvos:L}` | lista os `.py` dos alvos, relativos à raiz do repositório do cenário (`"."` = a raiz inteira); pastas `.venv`, `build`, `dist` e `__pycache__` ficam de fora em qualquer nível; alvo inexistente ou sem nenhum `.py` falha | → fontes |
| V07 | given | `o config {origem:Origem}` | carrega o config base (`CONFIG_BASE` de `suporte/config.py`) ou o `config.txt` do repositório | → config |
| V08 | given | `o config {origem:Origem} salvo em "{arquivo}"` | igual a V07, com outro destino; a gravação cria as pastas pai que faltam | → config |
| V09 | given | `o config base com {pares:L}` | parte do config base e aplica cada `CHAVE=valor` (troca a linha da chave ou acrescenta no fim) | → config |
| V10 | given | `o config com {pares:L}` | aplica os pares sobre o config atual (depois de um `Contexto`) | usa config |
| V11 | given | `o config sem a chave "{chave}"` | remove as linhas da chave | usa config |
| V12 | given | `o config com a linha {n:d} trocada por "{linha}"` | troca a linha número n (começa em 1) | usa config |
| V13 | given | `o config com a linha da chave "{chave}" trocada por "{linha}"` | troca a linha da chave; `""` equivale a removê-la | usa config |
| V14 | given | `o config com a linha "{linha}" {posicao:Pos}` | insere a linha no início ou no fim | usa config |
| V15 | given | `o config escrito com a variação "{variacao}"` | transforma o texto na hora de gravar (lista de variações) | usa config |
| V16 | given | `o caminho "{caminho}" preparado como "{tipo}"` | cria arquivo ou diretório especial (lista de tipos) e, menos em `inexistente`, as pastas pai que faltam; um original que existia (arquivo ou pasta) vai para uma reserva; no fim restaura permissões, apaga o que o teste criou, inclusive as pastas pai, e devolve o original; desliga nesse caminho a gravação automática do config e a reserva do `OUTPUT_FILE` (V29) | → preparados |
| V18 | given, when | `a situação de erro "{situacao}"` | combina V16, V11 e V09 conforme a situação (lista), agindo sobre o config atual e o seu destino: inexistente e sem permissão de leitura → V16 no destino; chave ausente → sem `WIDTH`; valor inválido → `WIDTH=abc`; parâmetros impossíveis → `EXIT=0,0` (igual à entrada); OUTPUT_FILE → `diretorio_inexistente/maze.txt` | config, preparados |
| V19 | given | `os casos de erro do catálogo da suíte` | carrega o catálogo de casos de erro de `tests/suporte/`: um caso por cenário de erro de 03, 04, 05, 07, 08 e 13 | → catalogo |
| V20 | given | `um labirinto gerado pelo {gerador:Gerador} com o config base` | gera pelo programa (entrada `"4"`) ou pela classe `MazeGenerator` | → labirintos |
| V21 | given | `um labirinto gerado pelo {gerador:Gerador} com o config base mais {pares:L}` | igual a V20, com os pares aplicados | → labirintos |
| V22 | given | `o labirinto de teste com a grade "{grade}", entrada "{entrada}" e saída "{saida}"` | grava um arquivo de saída; linhas da grade separadas por ` / `; caminho do rodapé calculado por BFS; quando a BFS não chega à saída (grades `F7` e `F / E`), a linha do caminho fica vazia | → labirintos |
| V23 | given | `o labirinto de teste "{modelo}"` | arquivo pronto (lista de modelos; o exemplo do subject fica em `tests/fixtures/`) | → labirintos |
| V24 | given | `a célula de dígito "{digito}"` | célula isolada a partir do dígito | → celula |
| V25 | given | `a célula com as paredes fechadas "{paredes}"` | célula isolada a partir das paredes | → celula |
| V26 | given | `o gerador "{expressao}"` | avalia `MazeGenerator(...)` com literais (`eval` só com `MazeGenerator` no escopo) e guarda o texto | → gerador |
| V27 | given | `o programa iniciado com "{comando}"` | grava o config, abre o processo e espera o primeiro prompt | config → sessao |
| V28 | given | `o programa iniciado com "{comando}", com o caminho {vis:Visib}` | como V27; `visível` envia `"2"`; `oculto` confere que não há ciano | → sessao |
| V29 | when | `eu executo {comandos:L}` | grava o config e roda cada comando com stdin vazio; o resultado guarda o `OUTPUT_FILE` do config passado a `a_maze_ing.py`, reservado antes da execução (regras de execução) | → resultado, resultados |
| V30 | when | `eu executo {comandos:L} com a entrada {linhas:L}` | como V29, com as linhas no stdin, cada uma terminada em `\n` | → resultado, resultados |
| V31 | when | `eu executo {comandos:L} {n:d} vezes com a entrada {linhas:L}` | repete V30 n vezes | → execucoes |
| V32 | when | `eu gero o labirinto` | `python3 a_maze_ing.py <destino do config>` com a entrada `"4"` | → resultado, labirintos |
| V33 | when | `eu gero o labirinto {n:d} vezes` | repete V32; cada passo `Quando` de repetição (V31, V33–V35, V43, V47) substitui a lista de execuções anterior | → execucoes |
| V34 | when | `eu gero o labirinto com cada um de {pares:L}` | uma geração por par, cada uma sobre uma cópia do config | → execucoes |
| V35 | when | `eu gero o labirinto com cada seed de {inicio:d} a {fim:d}` | uma geração por seed | → execucoes |
| V36 | when | `eu gero o labirinto e o analiso com o maze_analyzer` | V32 seguido de V37 | → analise |
| V37 | when | `eu analiso o labirinto com o maze_analyzer` | roda `private/maze_analyzer.py` sobre o arquivo atual | → resultado, analise |
| V38 | when | `eu analiso o labirinto com o maze_analyzer "{opcoes}"` | como V37, com as opções | → analise |
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
| V56 | then | `a linha da saída que contém "{a}" também contém "{b}"` | toda linha de stdout + stderr que contém `a` também contém `b`; falha se nenhuma linha contém `a` | resultado ou sessao |
| V57 | then | `a mensagem de erro cita {itens:L}` | stderr com uma linha, começando com `Error: `, contendo os itens na ordem | resultado |
| V58 | then | `a mensagem de erro explica "{motivo}"` | casa a expressão do motivo (I21) | resultado |
| V59 | then | `o resultado da execução é "{resultado}"` | `sucesso` (sem estourar o tempo limite, código 0, nenhuma linha de stderr com `Error:` além de `Error: maze too small for the "42" pattern` (D06, I10) e o `OUTPUT_FILE` do config gravado com conteúdo) ou `erro citando A, B[; motivo: M]` (código 1 e as regras de V57 e V58) | resultado |
| V60 | then | `o caminho "{caminho}" {situacao:EstadoCaminho}` | `exists`, `git check-ignore`, `git ls-files` ou tamanho > 0; aceita glob | repo |
| V61 | then | `o arquivo "{arquivo}" {verbo:Contem} {textos:L}` | procura as strings no arquivo lido sem converter quebras de linha (`newline=""`), para `\r` ser detectável | repo |
| V62 | given, then | `o arquivo "{arquivo}" {tem:TemLinha} que casa com a expressão "{regex}"` | `re.search` com `re.M` | repo |
| V64 | then | `a seção "{secao}" do README contém {textos:L}` | do título `#… secao` até o próximo título do mesmo nível | repo |
| V65 | then | `o metadado "{campo}" do pacote "{arquivo}" é "{valor}"` | lê `METADATA`/`PKG-INFO` com `email.parser`; aceita glob e confere cada arquivo | repo |
| V66 | then | `o pacote "{arquivo}" confirma "{propriedade}"` | propriedades do pacote (lista); aceita glob e confere cada arquivo | repo |
| V67 | then | `{alvo:Alvo} casa com a expressão "{regex}"` | aplica a expressão a cada item do alvo | labirintos, resultado, lido |
| V68 | then | `a grade do labirinto tem {largura:d} colunas e {altura:d} linhas` | dimensões do labirinto atual | labirintos |
| V69 | then | `a linha {n:d} do rodapé é "{texto}"` | n de 1 a 3 | labirintos |
| V70 | then | `o arquivo de saída é idêntico byte a byte ao gerado com o config base` | gera também com o config base e compara os bytes | labirintos |
| V71 | then | `os resultados são {relacao:Relacao} em "{aspecto}"` | compara as execuções aos pares no aspecto (lista) | execucoes |
| V72 | then | `<sujeito> confirma "<propriedade>"` | cada propriedade da lista fechada do sujeito é um passo próprio, com a frase inteira escrita no decorador (`@then('a análise estática confirma "open sempre dentro de with"')`); a propriedade que varia num Esquema do Cenário (`docstring em cada <definicao>`) é um passo com parâmetro | conforme o sujeito |
| V73 | then | `o validador da suíte relata "{relato}" em "{verificacao}"` | compara o texto que o validador devolve | labirintos |
| V74 | then | `o validador da suíte conta {n:d} "{item}"` | conta os itens (lista) | labirintos |
| V75 | then | `a célula "{celula}" {situacao:EstadoCelula}` | célula dada como `"x,y"` | labirintos |
| V76 | then | `pelo menos uma das células {celulas:L} é alcançável a partir da entrada` | alcançável e sem valor F | labirintos |
| V77 | then | `todas as células da "{borda}" têm a parede "{direcao}" fechada` | percorre a borda | labirintos |
| V78 | then | `as células de valor F ocupam as colunas "{colunas}" e as linhas "{linhas}"` | intervalos como `"6 a 8 e 10 a 12"` | labirintos |
| V79 | then | `o dígito da célula é "{digito}"` | sobre a célula; compara sem diferenciar maiúsculas | celula |
| V80 | then | `as paredes {situacao:FA} da célula são "{paredes}"` | sobre a célula | celula |
| V81 | then | `a célula tem {n:d} paredes fechadas` | sobre a célula | celula |
| V82 | then | `o bit {bit:d} da célula está ligado` | sobre a célula | celula |
| V83 | then | `a linha "{rotulo}" do maze_analyzer {op:Op} {textos:L}` | rótulo = início da linha da saída do analyzer; `começa com` e `contém` valem para o valor, o resto da linha depois do rótulo, dos espaços e do `:` (`Independent loops: 0 / 228 possible` → `0 / 228 possible`); roda o analyzer se ainda não rodou | analise |
| V84 | then | `o número na linha "{rotulo}" do maze_analyzer é {cmp:Cmp} {n:d}` | primeiro inteiro do valor (V83) | analise |
| V85 | then | `o veredito do maze_analyzer corresponde ao PERFECT do config` | `True` → `PERFECT maze`; `False` → `Pac-Man-USABLE` | analise, config |
| V86 | then | `na última renderização, as posições de "{elemento}" têm a cor "{cor}"` | todas as posições do elemento têm a cor | resultado ou sessao |
| V87 | then | `na última renderização, a cor "{cor}" só aparece em "{elemento}"` | a cor não aparece fora do elemento | resultado ou sessao |
| V88 | then | `na última renderização, nenhuma posição tem a cor "{cor}"` | ausência da cor | resultado ou sessao |
| V89 | then | `na última renderização, as células de dígito "{digito}" mostram exatamente as paredes "{paredes}"` | exige pelo menos uma célula com o dígito | resultado, labirintos |
| V90 | then | `o programa continua em execução` | `poll() is None` | sessao |
| V91 | then | `o programa aguarda no prompt "{prompt}"` | processo vivo e o prompt é a última coisa impressa | sessao |
| V92 | then | `o construtor levanta "{excecao}"` | tipo da exceção guardada | excecao |
| V93 | then | `a mensagem da exceção cita {trechos:L}` | `str(excecao)` contém os trechos | excecao |
| V94 | when | `eu leio "{arquivo}"` | seleciona os arquivos que casam (aceita glob; nenhum arquivo falha); os passos Então leem deles o texto, os metadados ou a lista de conteúdo | → lido |
| V95 | given | `o exemplo de uso da docstring de "{modulo}" salvo em "{arquivo}"` | extrai o bloco de código da seção `Example:` da docstring do módulo (I22) e grava no arquivo | → preparados |

## Listas fechadas

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
| Presenca | `presente`, `ausente` (só na propriedade `42 {presenca:Presenca}` de V72, que não pode casar com as propriedades fixas que começam com `42 `) |
| V02 estado | `atual` (`cwd` em `project/`); `instalado` (`make install`, uma vez por sessão); `clone limpo` (`git archive HEAD` rodado em `project/` e extraído numa pasta temporária, ou seja, o que está commitado, sem as mudanças da árvore de trabalho, seguido de `git init`, `git add` e `git commit` só nessa cópia, porque a raiz do git é `dojo`); `clone do remoto` (`git clone --depth 1 $AMAZEING_REMOTE` numa pasta temporária; sem a variável, ou com ela vazia, o cenário é pulado com a mensagem que diz qual variável falta) |
| V15 variação | `uma linha vazia entre cada par`, `espaços em volta do igual`, `espaços no fim de cada linha`, `finais de linha CRLF`, `sem quebra de linha depois da última linha`, `chave WIDTH minúscula`, `todas as chaves minúsculas`, `chave HEIGHT capitalizada`, `perfect=true minúsculo` |
| V16 tipo | `inexistente`, `diretório` (pasta vazia), `diretório sem permissão de escrita` (pasta vazia com `chmod 500`), `sem permissão de leitura` (config base com `chmod 000`), `não UTF-8` (config base precedido de um comentário acentuado, em latin-1), `vazio`, `bytes binários aleatórios`, `só espaços e tabulações`, `BOM UTF-8 + config base`, `config base com WIDTH de 100000 dígitos`, `só WÍDTH=20 e HEÍGHT=15, com acento`, `pasta com a_maze_ing.py, amazeing/ e config.txt` (cópia desses três itens da raiz do repositório do cenário, sem `__pycache__`), `diretório pai criado` (só a pasta pai passa a existir; o caminho continua inexistente) |
| V18 situação | `arquivo de configuração inexistente`, `arquivo de configuração sem permissão de leitura`, `chave obrigatória ausente`, `valor inválido`, `parâmetros impossíveis`, `OUTPUT_FILE num diretório inexistente` |
| V23 modelo | `exemplo do subject`, `exemplo do subject com o rodapé anotado`, `perfeito do config base`, `perfeito do config base com uma parede interna aberta` |
| V46 evento | `EOF`, `SIGINT`, `1 segundo sem entrada` |
| V58 motivo | `arquivo não encontrado`, `arquivo não é UTF-8`, `chave obrigatória ausente`, `entrada igual à saída`, `tamanho sem tabuleiro Pac-Man`, `coordenada no padrão 42` (palavras-chave na I21) |
| V71 aspecto | `arquivo de saída`, `grade`, `solução`, `células de valor F`, `saída exibida` |
| V72 o validador da suíte | `valores de 0 a 15`, `bits na convenção N=1, E=2, S=4, W=8`, `x é a coluna e y é a linha`, `entrada e saída válidas`, `entrada diferente da saída`, `x de entrada e saída dentro da largura`, `y de entrada e saída dentro da altura`, `toda célula fora do 42 alcançável`, `borda fechada`, `paredes coerentes`, `vizinhas leste-oeste coerentes` (bit E de (x, y) = bit W de (x+1, y)), `vizinhas norte-sul coerentes` (bit S de (x, y) = bit N de (x, y+1)), `inalcançáveis são as células do 42`, `células F em dois componentes 4-conexos`, `componente da esquerda com a forma do 4`, `componente da direita com a forma do 2`, `células F iguais ao padrão 42`, `nenhuma célula F fora do padrão`, `42 sem passagem aberta`, `glifos 3x5 com uma coluna livre entre os dígitos`, `42 presente`, `42 ausente`, `42 com margem de corredor`, `42 fora dos cantos`, `centro livre do 42`, `árvore geradora fora do 42`, `caminho único entre entrada e saída`, `ramos fora da solução terminam em beco`, `solução atravessa só paredes abertas`, `solução não sai da grade`, `solução não entra no 42`, `solução termina na saída`, `solução mais curta`, `solução sem célula repetida`, `solução válida e mais curta`, `pelo menos 2 rotas independentes`, `no máximo 2 becos reais`, `zero becos reais`, `sem área aberta 3x3`, `blocos 2x2, 2x3 e 3x2 abertos aceitos` (o validador não recusa o labirinto por área aberta e ele tem pelo menos um bloco 2x2 aberto; a aceitação de 2x3 e 3x2 é provada pelas grades de teste de V22 com V73 em `áreas abertas`), `modo igual ao PERFECT do config`, `rodapé com ENTRY, EXIT e caminho válido`, `labirinto válido conforme o config` (dimensões, valores, borda, coerência, entrada e saída, "42" por D06/D07, conectividade, sem 3x3, solução válida e mais curta, modo), `uma linha vazia logo após a grade`, `exatamente 3 linhas após a linha vazia`, `arquivo termina com quebra de linha`, `linha vazia contém só a quebra de linha`, `nenhuma linha com espaço no fim` |
| V72 a renderização | `cada renderização seguida do menu`, `nova renderização abaixo da anterior, seguida do menu`, `2 × HEIGHT + 1 linhas`, `2 × WIDTH + 1 posições de 2 caracteres por linha`, `só caracteres ASCII`, `cores por sequências ANSI de fundo`, `cada linha termina com o reset ANSI`, `última sequência ANSI é o reset`, `paredes iguais às do arquivo de saída`, `entrada e saída iguais às do rodapé`, `caminho do arquivo marcado em ciano`, `caminho marcado liga entrada e saída por paredes abertas`, `caminho marcado com o comprimento da busca em largura`, `cinco cores distintas para entrada, saída, 42, caminho e paredes`, `paredes em rodízio branco, amarelo, verde, azul`, `labirinto diferente do da renderização anterior` |
| V72 a análise estática | `open sempre dentro de with`, `anotação de retorno em toda definição`, `docstring em cada módulo`, `docstring em cada função`, `docstring em cada método`, `docstring em cada classe`, `docstrings com aspas triplas duplas`, `resumo de uma frase terminado em ponto`, `linha em branco entre resumo e descrição`, `seção Args: nas funções com parâmetros`, `seção Returns: nas funções que retornam valor`, `coleções vazias com tipo anotado` (também nas atribuições desempacotadas, como `a, b = [], []`), `testes usam pytest ou unittest`, `sem supressão de flake8 nem mypy` (comentários, lidos pelo `tokenize`, que casam com `(?i)#\s*noqa\b\|#\s*flake8[:=]\s*noqa\|#\s*type:\s*ignore\|#\s*mypy:`), `mazegen só importa a biblioteca padrão` (todo import absoluto está em `sys.stdlib_module_names` ou é `mazegen.*`), `sem MiniLibX` |
| V72 o módulo mazegen | `uma única classe pública de geração`, `grid e solution preenchidos após generate`, `solution pública e documentada`, `grid público com as paredes de cada célula`, `mesmos parâmetros geram a mesma grade`, `grade igual à do arquivo de saída`, `só MazeError escapa do construtor` |
| V72 o catálogo de casos de erro | `nenhum caso termina com Traceback`, `nenhum caso estoura o tempo limite`, `mensagem começa com Error:`, `mensagem cita o arquivo, a linha ou a chave`, `mensagem sem nome de exceção do Python` (as três últimas pulam o caso de uso errado da linha de comando, I12) |
| V66 propriedade | `contém o código do módulo`, `contém a docstring de mazegen/__init__.py`, `README como descrição longa`, `instala e importa MazeGenerator num virtualenv novo`, `formato produzido por python -m build`, `mesma versão no nome dos arquivos`, `versão igual à do pyproject.toml`, `LICENSE.md incluído`, `nada do build ignorado pelo git` |
| V73 relato | em `coerência das paredes`: `coerente`, `incoerente entre (x,y) e (x,y)`; em `áreas abertas`: `aceito`, `recusado: área 3x3`; em `modo Pac-Man`: `recusado: N rota(s) independente(s)` |
| V74 item | `células de valor F`, `janelas 2x2 abertas`, `células alcançáveis`, `letras da solução` |
| V77 borda / direção | `primeira linha`, `última coluna`, `última linha`, `primeira coluna` / `Norte`, `Leste`, `Sul`, `Oeste` |
| Paredes (V25, V80, V89) | `nenhuma` ou direções em lista com vírgulas e "e": `Norte`, `Norte e Sul`, `Norte, Leste, Sul e Oeste` |
| V83/V84 rótulo | `Verdict:`, `Reachable region`, `Independent loops`, `Dead-ends`, `Corners + centre`, `Wall coherence`, `Entry` |
| V86–V88 elemento / cor | `entrada`, `saída`, `células do caminho`, `passagens do caminho`, `células do 42`, `paredes` (as posições de parede fechada e todos os cantos entre 4 células, I02) / `branco`, `amarelo`, `verde`, `azul`, `magenta`, `vermelho`, `ciano`, `cinza` (códigos SGR na I21) |
| V65 campo | `Name`, `Version`, `License-Expression` |
| V45 linhas | `1` regenerar, `2` mostrar/ocultar o caminho, `3` trocar a cor das paredes, `4` sair; inválidas usadas: `9`, `abc`, `""`, `-1` |
| V91 prompt | `Choice? (1-4): ` |
| V92 exceção | `MazeError` |
| V26/V44 expressão | só `MazeGenerator(...)` com literais, na assinatura da I09 |
| V29–V31 comandos | `make install`, `make run`, `make debug`, `make clean`, `make lint`, `make lint-strict`, `make build`, `make -n <regra>`; `test -f …`, `test $(…) = $(…)`; `git ls-files …`, `git check-ignore …`, `git fetch`, `git status --porcelain`, `git rev-parse …`; `python3 a_maze_ing.py …`, `python3 -X dev a_maze_ing.py …`, `python a_maze_ing.py …`, `python3 -c '…'`, `python -c '…'`; `.venv/bin/python -c '…'`, `.venv/bin/python -m flake8 …`, `.venv/bin/python -m mypy …`, `.venv/bin/python -m build …`, `.venv/bin/flake8 .`, `.venv/bin/mypy …`, `mypy …`; `pip install …`, `python -m build`; redirecionamento `< /dev/null > arquivo`. O analyzer roda por V36–V38, nunca por V29 |
