---
sidebar_position: 3
title: Os getters
---

# Os getters

Um **getter** ("pegador") é um método que devolve o valor de um atributo protegido. É a forma
segura de **ler** um dado: quem está de fora recebe o valor, mas não ganha acesso ao atributo.

```python
    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age_days
```

- os nomes `get_height` e `get_age` são os que o enunciado pede;
- cada um devolve o valor do atributo, com o tipo anotado depois da seta.

Quem lê a altura da rosa escreve `rose.get_height()`. Hoje o getter só devolve o atributo, mas,
como toda leitura passa por ele, a classe pode mudar o jeito de guardar a altura (em milímetros,
por exemplo) sem que nenhum código de fora precise mudar.
