---
sidebar_position: 5
title: A seed e o random.Random único
---

# A seed e o random.Random único

O enunciado pede duas coisas que parecem opostas: o labirinto deve ser **sorteado** (cada
execução gera um diferente), mas também **reproduzível** (deve existir um jeito de gerar de novo
exatamente o mesmo labirinto, por exemplo para mostrá-lo na avaliação). Esta página mostra como
a **semente** (*seed*) resolve as duas e por que o pacote inteiro sorteia com um único objeto.

## Como um computador sorteia

Um computador não joga dados de verdade. O sorteio sai de uma **conta**: um gerador de números
parte de um número inicial, a **semente**, e a cada pedido calcula o próximo número a partir do
anterior. A sequência parece aleatória, mas é sempre a mesma para a mesma semente.

Em Python, `random.Random(semente)` cria um desses geradores, um objeto com o próprio estado:

```python
import random

a = random.Random(7)
b = random.Random(7)
c = random.Random(8)
print([a.randint(1, 6) for _ in range(8)])
print([b.randint(1, 6) for _ in range(8)])
print([c.randint(1, 6) for _ in range(8)])
```

```text
[3, 2, 4, 6, 1, 1, 5, 1]
[3, 2, 4, 6, 1, 1, 5, 1]
[2, 3, 4, 2, 2, 6, 1, 1]
```

`randint(1, 6)` sorteia um inteiro de 1 a 6, como um dado. `a` e `b` têm a mesma semente e dão
os mesmos "dados"; `c` tem outra semente e dá outra sequência.

Com labirintos acontece o mesmo. Abaixo, três labirintos 8x5 cavados pelo `Carver` (a classe da
[página 7](./05-o-codigo-do-carver.md)) com `Random(1)`, `Random(2)` e de novo `Random(1)`: o
primeiro e o terceiro são idênticos, e o do meio é outro. A célula magenta é a entrada, `0,0`.

![Três labirintos 8 por 5: Random(1), Random(2) e de novo Random(1), o primeiro e o terceiro iguais](/img/carver/seeds.svg)

Sem semente, `random.Random()` (ou `random.Random(None)`) pega um valor imprevisível do sistema
operacional, e cada execução sai diferente. É assim que o programa funciona quando a opção `SEED`
não está no arquivo de configuração ([parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md));
com `SEED=42`, toda execução gera o mesmo labirinto. O nome `SEED` e o fato de ela ser opcional
são escolhas do projeto: o enunciado só exige que a reprodução seja possível.

Os dois métodos de sorteio que o `mazegen` usa:

| Método | O que faz |
|---|---|
| `rng.choice(lista)` | devolve um item sorteado da lista |
| `rng.shuffle(lista)` | embaralha a própria lista, sem criar outra |

No código, o gerador se chama `rng`, abreviação de *random number generator* (gerador de números
aleatórios).

## Um único `random.Random` para tudo

O módulo `random` também tem funções soltas, como `random.choice` e `random.shuffle`. Elas usam um
gerador **global**, compartilhado com qualquer outro código do programa. Se uma outra biblioteca
sorteia alguma coisa no meio da geração, a sequência muda e o labirinto sai diferente, mesmo com a
mesma semente. Por isso o `mazegen` nunca usa as funções soltas.

O `mazegen` usa um único objeto `random.Random`:

1. o `MazeGenerator`, a classe que coordena a geração, cria esse objeto uma vez, com a semente
   recebida ([parte 9](../09-gerador/02-validar-os-parametros.md));
2. ele é passado como parâmetro `rng` ao `Carver` e, no modo Pac-Man, ao `Braider`, a classe que
   abre as paredes extras ([parte 8](../08-braider/01-becos-sem-saida.md));
3. nenhum outro lugar do pacote sorteia nada nem cria outro `Random`.

O `Carver` não cria o próprio gerador: recebe por parâmetro. Se cada classe criasse o seu
`random.Random(semente)` a cada uso, dois problemas apareceriam:

- o `Carver` e o `Braider` tirariam os mesmos números, cada um do começo da sua própria
  sequência, em vez de o `Braider` continuar de onde o `Carver` parou;
- o programa tem um menu, e uma das opções pede **outro** labirinto
  ([parte 14](../14-menu-e-main/01-o-laco-do-menu.md)). Para atender, o `MazeGenerator` gera de
  novo. Se a cada geração o `Carver` recriasse `random.Random(semente)`, a sequência recomeçaria
  do zero, e o "outro" labirinto sairia igual ao primeiro
  ([parte 9](../09-gerador/03-generate.md)).

Com um único gerador passado de mão em mão, a semente controla a geração inteira, do começo ao
fim, e cada geração nova continua a sequência de onde a anterior parou.

## O que mais precisa ser fixo

A semente garante a mesma sequência de números. Para o labirinto sair igual, cada número também
precisa ser usado do mesmo jeito em toda execução:

- **A lista sorteada vem sempre na mesma ordem.** `rng.choice(options)` sorteia uma **posição**
  da lista. `options` é montada percorrendo `Direction`, sempre na ordem Norte, Leste, Sul, Oeste.
  Se a ordem mudasse, o mesmo número sorteado escolheria outro lado.
- **O conjunto de visitadas só é consultado.** `visited` é um `set`, e um `set` não promete
  nenhuma ordem quando é percorrido. O `Carver` só pergunta `nxt not in visited` ("essa célula
  ainda não foi visitada?") e nunca percorre o conjunto, então essa ordem não decide nada.
- **Cada sorteio acontece no mesmo ponto do laço**: um por avanço.

As [páginas 6](./07-a-assinatura-do-carver.md) e [7](./05-o-codigo-do-carver.md) escrevem o
`Carver`. O fim da página 7 confere com um exemplo que a mesma semente dá o mesmo labirinto.
