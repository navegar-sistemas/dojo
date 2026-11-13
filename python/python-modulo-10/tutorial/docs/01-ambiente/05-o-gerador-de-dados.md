---
sidebar_position: 5
title: O gerador de dados
---

# O gerador de dados

Testar uma função só com os dados do exemplo do enunciado prova pouco: os mesmos três magos
sempre dão o mesmo resultado. O enunciado vem com um anexo, `generator.tar.gz`, com um programa
que sorteia dados novos para cada exercício, o `data_generator.py`. O enunciado sugere usá-lo
para testar o código e também durante a avaliação.

## Extrair o anexo

O anexo é baixado da página do projeto, junto com o enunciado. Salve o `generator.tar.gz` na
pasta `funcmage`. Um arquivo `.tar.gz` é um pacote de arquivos comprimido; o comando `tar` lista
e extrai o que tem dentro:

```bash
tar -tzf generator.tar.gz
```

```text
data_generator.py
```

- `-t` lista o conteúdo sem extrair;
- `-z` descomprime (é o `.gz` do nome);
- `-f generator.tar.gz` diz qual arquivo ler.

O pacote tem um arquivo só. Extraia-o numa pasta própria, `gerador`, para não misturá-lo com os
exercícios:

```bash
mkdir gerador
tar -xzf generator.tar.gz -C gerador
ls gerador
```

```text
data_generator.py
```

`-x` extrai, e `-C gerador` extrai dentro da pasta `gerador`.

## Rodar

```bash
python3 gerador/data_generator.py
```

O programa mostra um menu e espera uma escolha digitada:

```text
🧙‍♀️ FuncMage Chronicles - Data Generator Helper 🧙‍♂️
==================================================

Choose an option:
0. Generate data for Exercise 0 (Lambda Sanctum)
1. Generate data for Exercise 1 (Higher Realm)
2. Generate data for Exercise 2 (Memory Depths)
3. Generate data for Exercise 3 (Ancient Library)
4. Generate data for Exercise 4 (Master's Tower)
5. Generate data for ALL exercises
6. Generate custom mage data
7. Generate custom artifact data
q. Quit

Enter your choice:
```

Digite o número da opção e Enter. As opções `0` a `4` geram os dados de um exercício, a `5` gera
os de todos, a `6` e a `7` perguntam quantos magos ou artefatos gerar (Enter sem número gera 5).
Depois de cada resposta, o menu volta; `q` encerra o programa.

## Sem digitar no menu

As respostas também podem ser mandadas de uma vez, pela entrada do programa:

```bash
printf '5\nq\n' | python3 gerador/data_generator.py
```

- `printf '5\nq\n'` imprime `5`, uma quebra de linha (`\n`), `q` e outra quebra: as duas
  respostas que seriam digitadas;
- o `|` (*pipe*) liga a saída do `printf` à entrada do programa, que lê cada linha como se
  tivesse sido digitada.

As respostas não aparecem na saída, porque não foram digitadas no terminal. Uma execução real:

```text
🧙‍♀️ FuncMage Chronicles - Data Generator Helper 🧙‍♂️
==================================================

Choose an option:
0. Generate data for Exercise 0 (Lambda Sanctum)
1. Generate data for Exercise 1 (Higher Realm)
2. Generate data for Exercise 2 (Memory Depths)
3. Generate data for Exercise 3 (Ancient Library)
4. Generate data for Exercise 4 (Master's Tower)
5. Generate data for ALL exercises
6. Generate custom mage data
7. Generate custom artifact data
q. Quit

Enter your choice: === Exercise 0 Test Data ===
# Lambda Sanctum Test Data
artifacts = [{'name': 'Crystal Orb', 'power': 120, 'type': 'weapon'}, {'name': 'Fire Staff', 'power': 115, 'type': 'accessory'}, {'name': 'Storm Crown', 'power': 64, 'type': 'relic'}, {'name': 'Earth Shield', 'power': 115, 'type': 'focus'}]
mages = [{'name': 'Morgan', 'power': 52, 'element': 'wind'}, {'name': 'Sage', 'power': 58, 'element': 'shadow'}, {'name': 'Storm', 'power': 97, 'element': 'wind'}, {'name': 'Sage', 'power': 88, 'element': 'fire'}, {'name': 'Jordan', 'power': 98, 'element': 'lightning'}]
spells = ['meteor', 'tornado', 'freeze', 'darkness']

=== Exercise 1 Test Data ===
# Higher Realm Test Data
# Use these in your test functions:
test_values = [5, 15, 14]
test_targets = ['Dragon', 'Goblin', 'Wizard', 'Knight']

=== Exercise 2 Test Data ===
# Memory Depths Test Data
initial_powers = [75, 72, 80]
power_additions = [19, 10, 6, 13, 13]
enchantment_types = ['Earthen', 'Shocking', 'Flaming']
items_to_enchant = ['Staff', 'Shield', 'Cloak', 'Amulet']

=== Exercise 3 Test Data ===
# Ancient Library Test Data
spell_powers = [17, 49, 12, 30, 21, 18]
operations = ['add', 'multiply', 'max', 'min']
fibonacci_tests = [13, 15, 11]

=== Exercise 4 Test Data ===
# Master's Tower Test Data
test_powers = [20, 10, 12, 18]
spell_names = ['freeze', 'fireball', 'flash', 'meteor']
mage_names = ['Ash', 'Casey', 'Phoenix', 'Rowan', 'Luna', 'Jordan']
invalid_names = ['Jo', 'A', 'Alex123', 'Test@Name']

Choose an option:
0. Generate data for Exercise 0 (Lambda Sanctum)
1. Generate data for Exercise 1 (Higher Realm)
2. Generate data for Exercise 2 (Memory Depths)
3. Generate data for Exercise 3 (Ancient Library)
4. Generate data for Exercise 4 (Master's Tower)
5. Generate data for ALL exercises
6. Generate custom mage data
7. Generate custom artifact data
q. Quit

Enter your choice: May your functions be pure and your closures be strong! 🌟
```

Os nomes e números são sorteados: cada execução dá outros. Algumas listas são fixas e saem
sempre iguais (`test_targets`, `operations` e `invalid_names`).

## O que cada exercício recebe

Cada linha de dados é código Python pronto para colar: um nome, `=`, e uma lista.

| Exercício | Dados | Como são sorteados |
|---|---|---|
| 0 | `artifacts`, `mages`, `spells` | 4 artefatos com poder de 60 a 120; 5 magos com poder de 50 a 100; 4 nomes de feitiço sem repetição. Nomes de magos e de artefatos podem se repetir |
| 1 | `test_values`, `test_targets` | 3 poderes de 5 a 25; 4 alvos fixos |
| 2 | `initial_powers`, `power_additions`, `enchantment_types`, `items_to_enchant` | 3 poderes iniciais de 20 a 80; 5 acréscimos de 5 a 20; 3 tipos de encantamento e 4 itens, sem repetição |
| 3 | `spell_powers`, `operations`, `fibonacci_tests` | 6 poderes de 10 a 50; as 4 operações de `spell_reducer`; 3 valores de `n` de 8 a 20 |
| 4 | `test_powers`, `spell_names`, `mage_names`, `invalid_names` | 4 poderes de 5 a 30; 4 feitiços e 6 nomes de mago válidos, sem repetição; 4 nomes inválidos fixos |

A página "Rodar e conferir" de cada exercício cola os dados desta execução num teste e mostra o
resultado. Com os seus dados, os números do resultado são outros, mas seguem as mesmas regras.

O gerador não é entregue e não segue as regras do projeto (duas das funções dele não têm type
hints de retorno); por isso as conferências do tutorial nunca incluem a pasta `gerador`.
