---
sidebar_position: 2
title: Encapsulamento
---

# Encapsulamento

**Encapsular** é esconder os dados de um objeto e só deixar mexer neles por métodos que a classe
controla. Quem está de fora não escreve `rose.height = -10`: pede `rose.set_height(-10.0)`, e a
classe decide se aceita. A regra de "altura não pode ser negativa" fica escrita num lugar só,
dentro da classe, em vez de espalhada por todo código que muda uma altura.

## A convenção protected

O Python não tem um jeito de proibir de verdade o acesso a um atributo. Ele tem uma
**convenção**: um atributo cujo nome começa com **um** `_`, como `_height`, é **protegido**
(*protected*), e o recado é "isto é interno da classe; de fora, use os métodos". O Python não
impede ninguém de escrever `rose._height`; quem escreve está quebrando o combinado, e qualquer
leitor do código vê isso pelo `_`.

"Interno" inclui as **classes filhas**, que o exercício 5 apresenta: classes construídas a partir
de `Plant` podem usar `self._height` normalmente.

## O name mangling, e por que não ele

Um atributo cujo nome começa com **dois** `_`, como `__age_days`, recebe um tratamento especial
chamado **name mangling** ("embaralhar o nome"): o Python troca o nome por dentro, juntando o
nome da classe na frente. Um experimento mostra a troca:

```python title="experimentos/protegido.py"
class Plant:
    def __init__(self) -> None:
        self.name = "Rose"
        self._height = 25.0
        self.__age_days = 30


rose = Plant()
print(rose.__dict__)
print(rose._height)
```

```bash
python3 experimentos/protegido.py
```

```text
{'name': 'Rose', '_height': 25.0, '_Plant__age_days': 30}
25.0
```

- `rose.__dict__` mostra os atributos que o objeto guarda, cada nome com o seu valor (todo objeto
  de uma classe escrita como esta tem esse `__dict__`);
- `name` e `_height` ficaram com o nome escrito; `__age_days` virou `_Plant__age_days`. De fora
  da classe, `rose.__age_days` nem existe;
- `rose._height` funciona: o `_` é só um aviso.

O mangling existe para evitar que uma classe filha, sem querer, use o mesmo nome de atributo da
classe a partir da qual foi construída (a **classe pai**, também apresentada no exercício 5) e,
ao guardar um valor nele, apague o valor que a classe pai guardava ali. O efeito colateral é que
a própria classe filha também não enxerga o atributo pelo nome escrito. O enunciado pede a
convenção protected, de um `_` só, para os atributos da classe, e por isso os **quatro**
atributos da planta passam a ser `_name`, `_height`, `_age_days` e `_growth_rate`: o nome e a
taxa também, mesmo sem regra de validação.
