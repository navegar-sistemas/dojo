---
sidebar_position: 3
title: Algoritmo e módulo reutilizável
---

# Algoritmo e módulo reutilizável

O enunciado pede ao README duas explicações técnicas: **qual** algoritmo gera o labirinto e
**por que** ele foi escolhido; e **qual** parte do código pode ser reutilizada por outro projeto,
com a documentação curta de como usá-la. São as seções `Algorithm` e `Reusable module`.

## Algorithm

A seção tem um tópico por peça do gerador, cada um com o nome da técnica e o motivo da escolha.

- **Labirinto perfeito: *recursive backtracker* iterativo**
  ([parte 6](../06-carver/02-recursive-backtracker.md)). O README diz, em tópicos:
  - **o que faz**: anda de célula em célula, sorteando para qual vizinha ainda não visitada
    seguir e abrindo a parede entre as duas; quando fica sem saída, volta atrás pelo caminho até
    achar uma célula com vizinhas livres. Começa na entrada e nunca entra no "42";
  - **o nome da técnica**: é uma **busca em profundidade** aleatória, que vai sempre o mais longe
    possível antes de voltar;
  - **o "iterativo"**: o caminho de volta fica numa **pilha** explícita (uma lista em que se põe
    e se tira sempre do fim), e não em chamadas recursivas de função;
  - **os motivos**: a estrutura é só uma pilha e uma lista de vizinhas; cada célula entra e sai
    da pilha uma vez; e os corredores saem longos, com poucos **becos sem saída** (células com
    uma só abertura).
- **A comparação com números.** Num labirinto 20x15, nas sementes 1 a 100, o backtracker deixa
  de 24 a 37 becos reais, contra 74 a 95 do algoritmo de Kruskal e 77 a 97 do de Prim (dois
  outros geradores clássicos, citados no enunciado). Menos becos são menos paredes a abrir no
  modo Pac-Man, que precisa eliminá-los.
- **Tabuleiro Pac-Man: *braiding*** ("trançar"). O gerador faz o mesmo labirinto perfeito e
  depois abre uma parede em cada beco; se ainda faltarem ciclos (caminhos que voltam ao mesmo
  lugar por outra rota), abre paredes extras até haver 2
  ([parte 8](../08-braider/02-abrir-os-becos.md)). Se sobrarem mais de 2 becos reais ou menos de
  2 ciclos, o gerador refaz a grade, até 20 tentativas.
- **Nenhuma área aberta 3x3.** O enunciado proíbe um bloco de 3x3 células sem nenhuma parede por
  dentro. O README diz como a regra é cumprida **e como é conferida**: o labirinto perfeito não
  tem ciclos e por isso não comporta um 3x3 aberto, que teria vários; no modo Pac-Man, depois de
  cada parede aberta, `Maze.has_open_3x3` olha todos os blocos 3x3 da grade, e a abertura que
  completaria um é desfeita ([parte 8](../08-braider/04-a-regra-do-3x3.md)). O avaliador costuma
  perguntar isso, e a resposta já está escrita.
- **Caminho mais curto**: **busca em largura** a partir da entrada, olhando as vizinhas na ordem
  N, E, S, W. A busca em largura explora primeiro todas as células a 1 passo, depois as a 2
  passos, e assim por diante; por isso o primeiro caminho que chega à saída é o mais curto
  ([parte 7](../07-solver/01-busca-em-largura.md)).
- **O "42"**: o desenho dos dois algarismos, o tamanho do bloco e a fórmula da posição
  ([parte 1](../01-o-problema/06-o-padrao-42.md)).

"Por que" não é "porque é o mais conhecido". É o que o algoritmo traz de concreto ao projeto:
aqui, poucos becos, que é exatamente o que o modo padrão (Pac-Man) precisa eliminar. As partes 6
a 8 explicam cada escolha em detalhe; o README resume.

Se você mediu outros números, ou escolheu outro algoritmo, escreva os seus. O motivo precisa ser
verdadeiro para o **seu** código. Este trecho, na raiz do projeto, mede os becos do seu gerador
nas mesmas condições:

```bash
.venv/bin/python - <<'EOF'
from mazegen import MazeGenerator

counts = []
for seed in range(1, 101):
    gen = MazeGenerator(20, 15, perfect=True, seed=seed)
    gen.generate()
    ends = 0
    for y, row in enumerate(gen.grid):
        for x, walls in enumerate(row):
            open_sides = [bit for bit in (1, 2, 4, 8) if not walls & bit]
            if (x, y) not in gen.pattern and len(open_sides) == 1:
                ends += 1
    counts.append(ends - 2)
print(min(counts), "a", max(counts))
EOF
```

```text
24 a 37
```

Para cada semente, ele gera um labirinto perfeito e conta as células fora do "42" com um só
lado aberto (`open_sides` é a lista dos bits de parede que valem 0). O `- 2` tira os 2 becos
cercados pelo "42" ([parte 8](../08-braider/01-becos-sem-saida.md)), que todo labirinto 20x15
tem e que não contam. Os números de Kruskal e de Prim exigem escrever esses dois algoritmos à
parte, fora do projeto, e contar do mesmo jeito.

## Reusable module

O enunciado pede que o gerador fique numa classe só, num módulo que outro projeto possa importar
e instalar com `pip`, e que o README tenha uma documentação curta dele: como criar e usar o
gerador, com pelo menos um exemplo; como passar parâmetros (tamanho, semente); e como ler o
labirinto gerado e uma solução.

A seção começa dizendo **qual** parte é reutilizável:

```markdown
The reusable part of the project is the `mazegen` package; it is the only
code that goes into the wheel.
```

("A parte reutilizável é o pacote `mazegen`; é o único código que vai para o *wheel*.") O
**wheel** é o arquivo `.whl`, o formato pronto para instalar com `pip`
([parte 9](../09-gerador/08-o-pacote.md)).

Depois vem o mesmo texto da **docstring** de `mazegen/__init__.py`, o texto entre `"""` no começo
do pacote que o documenta ([parte 9](../09-gerador/05-documentacao-do-modulo.md)): cada parâmetro
do construtor com nome, tipo, valor padrão e exemplo; os erros que o construtor levanta; e os
atributos `grid` (as paredes), `solution` (o caminho) e `pattern` (as células do "42"), com o
jeito de ler cada um.

Repetir o texto, em vez de escrever outro, mantém uma documentação só: quem lê o README no
GitHub e quem digita `help(mazegen)` no Python, depois de instalar o pacote, leem a mesma coisa.

A diferença está no exemplo. Na docstring, ele vem recuado depois de `Example:`; no README, vai
num bloco de código Python, para aparecer destacado e ser fácil de copiar:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
walls = gen.grid[0][0]
print("north wall of (0, 0) closed:", bool(walls & 1))
print(len(gen.pattern), "cells draw the 42")
print(gen.solution)
```

Num ambiente com o pacote instalado, ele imprime:

```text
north wall of (0, 0) closed: True
18 cells draw the 42
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

O exemplo mostra as três coisas que o enunciado pede:

- **criar o gerador com parâmetros**: `width`, `height` e `seed`;
- **ler a estrutura**: `gen.grid[0][0]` são as paredes da célula `0,0`, e `walls & 1` testa o
  bit do Norte (vale 1), que está fechado, como toda a borda;
- **ler uma solução**: `gen.solution`, o caminho mais curto em letras `N`, `E`, `S`, `W`.
