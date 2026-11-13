---
sidebar_position: 4
title: As regras da missão
---

# As regras da missão

As quatro regras de segurança entram num método dentro de `SpaceMission`, depois do último campo
(`budget_millions`), separado dele por uma linha em branco, no mesmo formato das regras do
exercício 1 ([As regras](../04-ex1/03-as-regras.md)):

```python
    @model_validator(mode="after")
    def check_safety_requirements(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        leaders = 0
        experienced = 0
        inactive = 0
        for member in self.crew:
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                leaders += 1
            if member.years_experience >= 5:
                experienced += 1
            if not member.is_active:
                inactive += 1
        if leaders == 0:
            raise ValueError(
                "Mission must have at least one Commander or Captain")
        # "At least half the crew", in integers: experienced / size >= 0.5.
        if self.duration_days > 365 and experienced * 2 < len(self.crew):
            raise ValueError("Long missions (> 365 days) need 50% "
                             "experienced crew (5+ years)")
        if inactive > 0:
            raise ValueError("All crew members must be active")
        return self
```

## Uma volta pela tripulação

As regras 2, 3 e 4 olham todos os tripulantes. Um único `for` percorre a lista e conta três
coisas:

- `leaders`: quantos têm patente `commander` ou `captain`. `member.rank in (Rank.COMMANDER,
  Rank.CAPTAIN)` pergunta se a patente é um dos dois membros da tupla;
- `experienced`: quantos têm 5 anos ou mais de experiência (`>= 5`, porque o enunciado diz
  *5+ years*, "5 anos ou mais");
- `inactive`: quantos não estão na ativa.

Quando o método roda, cada `member` já é um `CrewMember` validado: `member.rank` é um membro de
`Rank`, e `member.years_experience` é um inteiro de 0 a 50.

## Regra a regra

1. **O ID começa com `M`.** Conferida antes do laço, porque não depende da tripulação.
2. **Alguém no comando.** Falha quando nenhum tripulante é `commander` nem `captain`. A mensagem é
   a da saída do enunciado, com `Mission` na frente ([O problema](./01-o-problema.md#a-saída-esperada)).
3. **Experiência nas missões longas.** Só vale quando `duration_days` passa de 365. Escolha do
   tutorial: "50% de tripulação experiente" é lido como **pelo menos metade**. Com 3 tripulantes,
   2 experientes bastam (66%) e 1 não basta (33%); com 4, bastam 2 (exatamente 50%); com 5, são
   precisos 3. O gerador de dados do enunciado usa outra conta, `len(crew) // 2`, e com 5
   tripulantes se contenta com 2 ([Validar os dados](../06-dados-do-gerador/03-validar-os-dados.md)). A conta
   `experienced * 2 < len(self.crew)` é `experienced / len(self.crew) < 0.5` sem divisão: os dois
   lados ficam inteiros, e não há arredondamento de `float` no caminho. O comentário em inglês
   registra essa troca.
4. **Todos na ativa.** Falha se algum tripulante tem `is_active` falso.

A ordem dos `if` é a ordem do enunciado. Como no exercício 1, o método para na primeira regra que
falha.

## A mensagem do erro

O erro de uma regra tem o mesmo `Value error, ` na frente do `msg`, e a demonstração usa a mesma
função do exercício 1. Ela entra depois de `SpaceMission`:

```python
def validation_message(error: ValidationError) -> str:
    detail = error.errors()[0]
    # A ValueError raised by a validator shows up in msg as
    # "Value error, <text>"; ctx keeps the original exception.
    if detail["type"] == "value_error":
        return str(detail["ctx"]["error"])
    return detail["msg"]
```

Cada exercício é um programa independente. O Python procura os módulos importados na pasta do
arquivo rodado: rodando `ex2/space_crew.py`, a procura é na pasta `ex2`, e não na `ex1`, e um
`import alien_contact` falharia. Por isso a função é copiada, e não importada do exercício 1
([A mensagem do erro](../04-ex1/04-a-mensagem-do-erro.md)).
