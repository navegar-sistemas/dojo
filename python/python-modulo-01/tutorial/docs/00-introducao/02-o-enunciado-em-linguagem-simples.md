---
sidebar_position: 2
title: O enunciado em linguagem simples
---

# O enunciado em linguagem simples

## Regras que valem para todos os exercícios

- **Python 3.10 ou mais novo.** Os programas são rodados com `python3`
  ([Ambiente](../01-ambiente/01-o-python.md)).
- **Estilo conferido pelo flake8.** O flake8 é um programa que lê o seu código e aponta o que
  foge do estilo padrão do Python: linha comprida demais, falta de linha em branco entre funções,
  variável criada e nunca usada. O código entregue não pode ter nenhum aviso dele.
- **Type hints em todas as funções e métodos, conferidos pelo mypy.** Um *type hint* é a anotação
  do tipo de cada parâmetro e do retorno, como em `def dobro(n: int) -> int:`. O mypy é o
  programa que confere se esses tipos batem com o uso
  ([Type hints, flake8 e mypy](../01-ambiente/04-type-hints-flake8-e-mypy.md)).
- **Um arquivo por exercício**, cada um na sua pasta (`ex0/` a `ex6/`).
- **Nomes no padrão do Python:** classes em `PascalCase` (cada palavra começando com maiúscula,
  sem separador: `Plant`, `GardenStats`) e funções e variáveis em `snake_case` (tudo minúsculo,
  palavras separadas por `_`: `show`, `age_days`).
- **O programa sempre roda sem erro.** Nenhum programa pode parar no meio com uma mensagem de erro
  do Python.
- **Sem validar o que não foi pedido.** Só o exercício 4 pede para recusar valores inválidos; nos
  outros, os valores usados são os do próprio programa.
- **Código só com o que o exercício pede**, escrito para deixar claro o conceito dele. O
  enunciado fala também em código "limpo e bem documentado". Nos exercícios, a documentação vem
  de nomes claros e dos type hints, sem comentários nem docstrings (textos de explicação entre
  aspas triplas no começo de uma função ou classe) que só repitam o nome; isso é escolha do
  projeto, e a alternativa seria uma docstring de uma linha em cada classe e método.
- **A partir do exercício 1, todo exercício usa classes.**

O enunciado também libera, em todos os exercícios, as palavras da linguagem (`class`, `def`,
`if`, `for`, `return`), o bloco `if __name__ == "__main__":` e o método `capitalize()` dos
textos, mesmo sem aparecerem nas listas abaixo.

## Funções autorizadas

Cada exercício tem uma lista de **funções autorizadas**: as únicas funções prontas do Python que o
código pode chamar. Funções, classes e métodos que você mesmo escreve no arquivo podem ser
chamados sempre.

| Exercício | Funções autorizadas |
|---|---|
| 0 e 1 | `print()` |
| 2, 3 e 4 | `print()`, `range()`, `round()` |
| 5 | `super()`, `print()`, `range()`, `round()` |
| 6 | `super()`, `print()`, `range()`, `round()`, `staticmethod()`, `classmethod()` |

Funções comuns como `int()`, `float()`, `len()` e `str()` **não** estão em nenhuma lista. Isso
pesa no exercício 2 ([O float e o round](../04-ex2/03-o-float-e-o-round.md)).

## Os sete exercícios

| Exercício | O que o programa precisa fazer |
|---|---|
| 0 | guardar nome, altura e idade de uma planta em três variáveis e imprimi-las, com o código dentro do bloco `if __name__ == "__main__":` ([Exercício 0](../02-ex0/01-o-problema.md)) |
| 1 | uma classe `Plant` com um método `show()` que imprime a planta, e pelo menos três plantas criadas a partir dela ([Exercício 1](../03-ex1/01-o-problema.md)) |
| 2 | a mesma classe, agora com os métodos `grow()` (crescer) e `age()` (envelhecer); o programa simula uma semana de uma planta, dia a dia, e no fim mostra quanto ela cresceu ([Exercício 2](../04-ex2/01-o-problema.md)) |
| 3 | plantas criadas já com os seus dados, numa linha só, e pelo menos cinco delas impressas com o mesmo `show()` ([Exercício 3](../05-ex3/01-o-problema.md)) |
| 4 | a classe protege os seus atributos, e a altura e a idade só podem ser lidas e mudadas por métodos (`get_height()`, `get_age()`, `set_height()`, `set_age()`), que recusam valores negativos com uma mensagem de erro ([Exercício 4](../06-ex4/01-o-problema.md)) |
| 5 | três tipos especiais de planta, `Flower` (flor), `Tree` (árvore) e `Vegetable` (hortaliça), que reaproveitam tudo de `Plant` e acrescentam os seus próprios dados e ações ([Exercício 5](../07-ex5/01-o-problema.md)) |
| 6 | um método que responde se uma idade passa de um ano, um jeito de criar uma planta "anônima", um tipo `Seed` (flor que dá sementes), e estatísticas de quantas vezes cada planta cresceu, envelheceu e foi mostrada ([Exercício 6](../08-ex6/01-o-problema.md)) |

Para cada exercício, o enunciado mostra a saída do programa
([as sete saídas](./04-o-resultado-final.md)). No exercício 0, o enunciado avisa que a saída não
será conferida letra por letra.

## Entrega

Só os sete arquivos `.py`, com esses nomes e nessas pastas, num repositório Git. Na avaliação,
quem avalia vai pedir que você transforme o programa do exercício 0 num executável direto, com a
linha *shebang*, e pode pedir que você explique os conceitos, mostre as relações de herança e
acrescente uma funcionalidade ao código ([Entregar](../09-fechamento/02-entregar.md)).

## O que o enunciado cita sem explicar

- **"Os fundamentos de Python da primeira atividade"**: um projeto anterior da mesma série, sobre
  o básico de Python. Tudo o que os exercícios usam dele está nos
  [pré-requisitos](./03-pre-requisitos.md).
- **"O conceito de imports, que fará parte de um projeto futuro"**: importar é usar, num arquivo,
  o código de outro arquivo. Um exemplo pequeno aparece no
  [exercício 0](../02-ex0/03-o-ponto-de-partida.md), porque é ele que explica o bloco
  `if __name__ == "__main__":`.
- **"Convenção protected" e "name mangling"**: dois jeitos de marcar um atributo como interno da
  classe. O exercício 4 usa o primeiro e explica por que não o segundo
  ([Encapsulamento](../06-ex4/02-encapsulamento.md)).
- **Instruções sobre IA**: o enunciado tem um capítulo pedindo que todo código vindo de uma
  ferramenta de IA seja entendido por completo e revisado com colegas.
