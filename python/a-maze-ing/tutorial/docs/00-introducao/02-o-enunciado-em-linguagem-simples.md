---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

Esta página resume o que o enunciado do projeto (o *subject*) exige. Cada item diz a regra, o
que ela quer dizer na prática e onde o tutorial a constrói.

## 1. Como o programa é chamado

O programa se chama obrigatoriamente `a_maze_ing.py` e recebe **um** argumento: o caminho de um
arquivo de texto com as opções.

```bash
python3 a_maze_ing.py config.txt
```

Qualquer erro (arquivo que não existe, opção inválida, labirinto impossível) precisa terminar
com uma **mensagem clara**, nunca com o programa quebrando e mostrando um *traceback* do Python.
Construído na [parte 14](../14-menu-e-main/05-a-barreira-de-erros.md).

## 2. O arquivo de opções

Um arquivo de texto com uma opção por linha, no formato `CHAVE=valor`. Linhas que começam com
`#` são comentários. Seis opções são obrigatórias:

| Opção | O que define | Exemplo |
|---|---|---|
| `WIDTH` | largura do labirinto, em células | `WIDTH=20` |
| `HEIGHT` | altura do labirinto, em células | `HEIGHT=15` |
| `ENTRY` | a célula de entrada, como `x,y` | `ENTRY=0,0` |
| `EXIT` | a célula de saída, como `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | o nome do arquivo onde o labirinto é gravado | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | o tipo de labirinto (item 4) | `PERFECT=True` |

O enunciado deixa acrescentar opções; este projeto acrescenta `SEED` (item 3). O repositório
precisa ter um arquivo de opções pronto, o `config.txt`. Explicado em detalhe na
[parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md) e construído na
[parte 11](../11-configuracao/01-o-value-object-maze-config.md).

## 3. O labirinto

O labirinto é uma grade retangular de **células** (os quadradinhos). Cada célula tem quatro
lados, e cada lado tem ou não uma **parede**.

![Uma célula com os quatro lados nomeados](/img/problema/lados-da-celula.svg)

As regras:

- **Sorteado, mas repetível.** Cada execução gera um labirinto diferente, mas deve existir um
  jeito de repetir exatamente o mesmo labirinto. Isso se faz com uma **semente** (*seed*): um
  número que fixa o sorteio. Mesma semente, mesmo labirinto.
- **Entrada e saída** existem, são células diferentes e ficam dentro da grade.
- **Tudo conectado.** Dá para chegar a qualquer célula partindo da entrada. A única exceção são
  as células que desenham o "42".
- **Borda fechada.** A volta toda da grade tem parede. A entrada e a saída são células marcadas
  por dentro, não buracos na borda.
- **Paredes coerentes.** Duas células vizinhas dividem a mesma parede, então as duas precisam
  concordar: se uma diz que há parede à sua direita, a vizinha da direita diz que há parede à
  sua esquerda.
- **Sem salões.** Nenhum bloco de 3x3 células pode ficar totalmente aberto, sem nenhuma parede
  por dentro. Blocos de 2x3 ou 3x2 abertos são permitidos.
- **Um "42" visível**, desenhado por células com as quatro paredes fechadas. Se o labirinto
  for pequeno demais para caber o "42", ele é gerado sem o desenho e o programa avisa.

Explicado na [parte 1](../01-o-problema/01-a-grade-e-as-celulas.md).

## 4. Dois tipos de labirinto

A opção `PERFECT` escolhe o tipo:

- `PERFECT=True`: **labirinto perfeito**. Existe exatamente **um** caminho entre a entrada e a
  saída; o labirinto não tem nenhum ciclo (nenhum jeito de andar em círculo e voltar ao mesmo
  lugar).
- `PERFECT=False` (o padrão): **tabuleiro de Pac-Man**, o jogo em que um personagem foge de
  fantasmas por corredores. Para ser jogável:
  - todo corredor é alcançável;
  - os quatro cantos e o centro são corredores (é onde os fantasmas e o jogador começam);
  - há pelo menos **duas rotas independentes** (dois ciclos), para quem foge sempre ter outra
    saída;
  - **becos sem saída** (células com uma só abertura) são raros: no máximo um ou dois.

Explicado na [parte 1](../01-o-problema/05-perfeito-e-pac-man.md).

## 5. O arquivo de saída

O labirinto é gravado no arquivo de `OUTPUT_FILE`: um caractere por célula, uma linha do
arquivo por linha da grade. Cada caractere é um dígito **hexadecimal** (de `0` a `9` e de `a` a
`f`, ou seja, de 0 a 15) que diz quais das quatro paredes da célula estão fechadas. Depois da
grade vêm uma linha vazia, a entrada, a saída e o caminho mais curto, escrito com as letras
`N`, `E`, `S` e `W` (um passo para cima, para a direita, para baixo ou para a esquerda).

O enunciado fornece um programa, o `maze_analyzer.py`, que lê esse arquivo e confere se o
labirinto cumpre as regras. Explicado na [parte 1](../01-o-problema/04-o-arquivo-de-saida.md).

## 6. O desenho e o menu

O programa mostra o labirinto na tela, com as paredes, a entrada, a saída e o caminho bem
visíveis, no terminal (com caracteres e cores) ou numa janela gráfica. Enquanto ele roda, o
usuário precisa poder:

- gerar outro labirinto;
- mostrar ou esconder o caminho mais curto;
- trocar a cor das paredes.

Este projeto desenha no terminal. Explicado na
[parte 1](../01-o-problema/07-o-desenho-e-o-menu.md).

## 7. O gerador reutilizável

A geração do labirinto fica numa **única classe** (aqui, `MazeGenerator`), dentro de um módulo
que outro projeto consegue importar. Esse módulo é distribuído como um **pacote Python**: um
único arquivo, chamado `mazegen-...`, que se instala com `pip install`. O repositório precisa
ter tudo para reconstruir esse pacote, e a documentação de uso vai junto. Construído na
[parte 9](../09-gerador/01-a-fachada.md).

## 8. Qualidade de código

- Python 3.10 ou mais novo.
- O código segue o padrão de estilo **flake8** e passa no verificador de tipos **mypy**: toda
  função tem anotações de tipo.
- Toda função e classe tem uma **docstring** (o texto entre `"""` que documenta o que ela faz).
- Erros são tratados com `try`/`except`, e arquivos são abertos com `with`.
- Um `Makefile` com os atalhos `install`, `run`, `debug`, `clean`, `lint` e `lint-strict`.

Construído na [parte 3](../03-ambiente/01-o-ambiente-virtual.md).

## 9. O que mais entra no repositório

- `README.md`: a apresentação do projeto, com seções obrigatórias (descrição, instruções,
  formato do arquivo de opções, algoritmo escolhido e o porquê, o que é reutilizável, como a
  equipe trabalhou, como a IA foi usada). Construído na
  [parte 15](../15-fechamento/01-o-que-o-readme-precisa-ter.md).
- `LICENSE.md`: a licença que permite a outros projetos reutilizarem o gerador. Construído na
  [parte 9](../09-gerador/06-a-licenca.md).
- `.gitignore`: a lista de arquivos gerados que não entram no repositório.

## 10. Bônus

Itens opcionais que valem nota extra. O deste projeto é o tabuleiro de Pac-Man **sem nenhum**
beco sem saída. Explicado na [parte 16](../16-bonus/01-o-tabuleiro-sem-becos.md).
