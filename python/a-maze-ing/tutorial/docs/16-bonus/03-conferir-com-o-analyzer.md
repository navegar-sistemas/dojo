---
sidebar_position: 3
title: Conferir com o analisador
---

# Conferir com o analisador

Afirmar que o tabuleiro não tem becos não basta: na avaliação, o bônus precisa ser mostrado. O
enunciado já diz como: com o `maze_analyzer.py` e a opção `--max-dead-ends 0`. Esta página
mostra como rodar o analisador e como ler o que ele imprime.

## O que é o `maze_analyzer.py`

É um programa em Python que vem junto com o enunciado do projeto. Ele lê um arquivo de saída (o
`maze.txt` que o programa grava, com um dígito hexadecimal por célula e, no fim, a entrada, a
saída e o caminho; [parte 1](../01-o-problema/04-o-arquivo-de-saida.md)) e confere:

- se as paredes são **coerentes**: se duas células vizinhas dizem a mesma coisa sobre a parede
  que dividem;
- se o labirinto é **perfeito** (um único caminho, sem ciclos), como `PERFECT=True` exige;
- ou se é um tabuleiro de Pac-Man **utilizável**: tudo alcançável, cantos e centro abertos,
  ciclos suficientes e poucos becos, como o modo padrão exige.

Ele vem junto com o enunciado: baixe-o no mesmo lugar onde está o PDF do enunciado. A folha de avaliação (a lista de perguntas que o
avaliador segue na defesa) manda rodá-lo nos arquivos de saída dos dois modos. Ele não faz parte
da entrega: deixe-o fora do repositório, por exemplo na pasta acima da raiz do projeto. Os
comandos abaixo supõem que ele está lá, em `../maze_analyzer.py`.

## As opções

```text
python3 maze_analyzer.py <output_file> [--min-loops N] [--max-dead-ends N]
```

O `<output_file>` é o caminho do arquivo de saída. As partes entre colchetes são opcionais:

- `--min-loops N` (padrão `2`): quantos ciclos independentes (rotas alternativas) o tabuleiro
  precisa ter;
- `--max-dead-ends N` (padrão `2`): quantos becos **reais** são tolerados. Os becos cercados pelo
  "42", que não podem ser abertos ([página 1](./01-o-tabuleiro-sem-becos.md)), nunca contam.

Sem as opções, o analisador confere a regra obrigatória do modo Pac-Man. Com
`--max-dead-ends 0`, confere o bônus.

## Rodar

O `config.txt` do projeto (`PERFECT=False`) tem a linha `# SEED=42` comentada, e por isso cada
execução sorteia um labirinto diferente. Para um resultado que se repete, os comandos abaixo, na
raiz do projeto, fazem uma cópia do `config.txt` com a semente ligada, geram o labirinto com
ela, passam o `maze.txt` ao analisador e apagam a cópia. O `config.txt` não muda.

```bash
sed 's/^# SEED=42$/SEED=42/' config.txt > bonus_seed.txt
printf '4\n' | .venv/bin/python a_maze_ing.py bonus_seed.txt > /dev/null
.venv/bin/python ../maze_analyzer.py maze.txt --max-dead-ends 0
rm bonus_seed.txt
```

- O `sed` copia o `config.txt` para o `bonus_seed.txt`, trocando a linha `# SEED=42` por
  `SEED=42`. A instrução `s/A/B/` quer dizer "substitua o texto A pelo texto B" em cada linha;
  aqui A é `^# SEED=42$` e B é `SEED=42`. O `^` marca o começo da linha e o `$`, o fim: juntos,
  exigem a linha inteira igual. Sem o `#`, a semente fixa o sorteio, e o labirinto sai sempre o
  mesmo.
- `printf '4\n' |` responde `4` ("sair") ao menu, como se alguém tivesse digitado; o programa gera
  o labirinto, grava o `maze.txt` (o `OUTPUT_FILE` da cópia) e termina
  ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)). `> /dev/null` descarta o desenho.
- O analisador roda com o Python do ambiente virtual; é o mesmo que o
  `python3 maze_analyzer.py <output_file>` do enunciado.

A saída:

```text
Maze size        : 20 x 15 (300 cells)
Entry            : (0, 0)   Exit: (19, 14) (reachable)
Reachable region : 282 cells (0 corridor(s) unreachable)
Independent loops: 32 / 228 possible (path ratio 14%)
Dead-ends        : 0 real + 2 enclosed by the '42' (tolerated)
Corners + centre : all reachable
Wall coherence   : OK (all shared walls match)

Verdict: Pac-Man-USABLE: fully connected, corners and centre reachable, 32 independent routes; no real dead-end -> bonus-grade (perfectly braided).
```

## Ler o relatório

| Linha | O que diz | O que confirma |
|---|---|---|
| `Maze size` | 20 x 15, 300 células | o tamanho do config |
| `Entry` | entrada `(0, 0)`, saída `(19, 14)`, alcançável | dá para ir da entrada à saída |
| `Reachable region` | 282 células alcançáveis, 0 corredores fora | 282 = 300 menos as 18 do "42": toda célula livre é alcançável a partir da entrada |
| `Independent loops` | 32 ciclos independentes, de 228 possíveis | bem acima dos 2 exigidos |
| `Dead-ends` | 0 reais e 2 cercados pelo "42", tolerados | **nenhum beco real**: o bônus |
| `Corners + centre` | todos alcançáveis | os quatro cantos e o centro são corredores |
| `Wall coherence` | OK | toda parede compartilhada está igual nas duas células |
| `Verdict` | o veredito | a conclusão de tudo |

Os números da linha `Independent loops`:

- **32** é o número de ciclos independentes do labirinto. Cada parede que o *braiding* abre num
  beco liga duas células que já estavam ligadas por outro caminho, e por isso cria exatamente um
  ciclo novo. O labirinto perfeito desta semente tinha 32 becos reais
  ([página 1](./01-o-tabuleiro-sem-becos.md)), e nenhum deles era vizinho de outro; por isso o
  *braiding* abriu uma parede em cada um: foram 32 aberturas e 32 ciclos, muito mais que os 2 que
  ele busca. Quando dois becos se tocam, uma única abertura entre eles resolve os dois (o
  *braiding* pula o beco que já ganhou uma segunda passagem), e sobram menos ciclos que becos.
- **228** é o máximo possível: os ciclos que existiriam com todas as paredes entre as 282 células
  alcançáveis abertas.
- **path ratio 14%** é a divisão das duas: 32 / 228 ≈ 0,14. Diz quão "aberto" o tabuleiro está,
  de 0% (labirinto perfeito) a 100% (sem nenhuma parede por dentro).

O veredito é o que conta. Ele começa com `Pac-Man-USABLE` ("utilizável como Pac-Man") e termina
com `no real dead-end -> bonus-grade (perfectly braided)` ("nenhum beco real: nível de bônus,
perfeitamente trançado").

Se o labirinto tivesse um beco real, o fim do veredito seria outro:

- com as opções padrão: `1 real dead-end(s) within tolerance (0 would be bonus-grade)` ("1 beco
  real, dentro da tolerância; 0 seria nível de bônus");
- com `--max-dead-ends 0`: o veredito inteiro viraria `Not Pac-Man-ready` ("não serve como
  Pac-Man"), porque a tolerância passou a ser zero.

## Sem semente

Sem `SEED`, cada execução com o `config.txt` (`make run`) gera um labirinto diferente, e o
número de ciclos muda de uma para outra (em quatro execuções seguidas: 35, 31, 28 e 29). O que
se repete é a linha `0 real + 2 enclosed by the '42'` e o veredito com
`bonus-grade (perfectly braided)`.

## Na defesa

O avaliador pode pedir para ver o bônus funcionando. O caminho mais curto é o desta página:
`make run`, sair com `4`, rodar o analisador no `maze.txt` com `--max-dead-ends 0` e mostrar o
veredito. O
README traz o mesmo comando na seção **Bonus**
([parte 15](../15-fechamento/04-time-bonus-e-recursos.md)).

Se vier a pergunta seguinte, "o código garante zero becos?", a resposta está na
[página anterior](./02-por-que-nao-e-garantido.md): não garante, porque a regra obrigatória do
3x3 tem prioridade; o que o código garante é no máximo 2, e o resultado medido é zero.
