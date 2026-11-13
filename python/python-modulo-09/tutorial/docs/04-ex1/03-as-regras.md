---
sidebar_position: 3
title: As regras
---

# As regras

As quatro regras de negócio entram num método do modelo, dentro da classe `AlienContact`, depois
do último campo (`is_verified`), com o mesmo recuo dos campos e separado dele por **uma** linha em
branco. Sem essa linha, o flake8 acusa `E301 expected 1 blank line, found 0`: o estilo padrão pede
uma linha em branco antes de cada método dentro de uma classe.

```python
    # Runs only after every field passed its own checks, so all the
    # attributes of self already hold valid values here.
    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")
        return self
```

O método segue o formato de [model_validator](../02-conceitos/06-model-validator.md): roda
depois que todos os campos passaram, lança `ValueError` na primeira regra que falha e devolve
`self` quando todas passam. O tipo de retorno é o nome da classe entre aspas, `"AlienContact"`.

## Regra a regra

1. **O ID começa com `AC`.** `startswith("AC")` é o método de texto que responde se o texto
   começa com `"AC"`. A mensagem tem aspas duplas dentro, e por isso o texto inteiro vai entre
   aspas simples.
2. **Contato físico verificado.** `self.contact_type is ContactType.PHYSICAL` compara o campo com
   o membro do Enum, e não com o texto `"physical"`
   ([Enum](../02-conceitos/05-enum.md#o-que-aconteceu)). A regra falha quando o contato é físico
   **e** não está verificado.
3. **Telepatia com 3 testemunhas.** Falha quando o contato é telepático e há menos de 3
   testemunhas. A condição não cabe numa linha de 79 caracteres: entre parênteses, o Python
   aceita continuar na linha de baixo, e o recuo maior da segunda linha separa a condição do
   corpo do `if`. A mensagem é a da saída do enunciado, letra por letra.
4. **Sinal forte com mensagem.** "Forte" é **acima** de 7.0 (`> 7.0`): um sinal de exatamente
   7.0 não precisa de mensagem. `not self.message_received` é verdadeiro quando o campo é `None`
   e também quando é o texto vazio `""`. Escolha do tutorial: uma mensagem vazia não conta como
   mensagem recebida.

As mensagens das regras 1, 2 e 4 não aparecem na saída do enunciado; o tutorial usa o próprio
texto de cada regra do enunciado, como na regra 3.

## Uma regra de cada vez

O método para no primeiro `raise`. Um relato que quebra duas regras recebe só a mensagem da
primeira, na ordem em que estão escritas, que é a ordem do enunciado. Para mostrar todas, o
método precisaria juntar as mensagens numa lista antes de lançar o erro; o enunciado só mostra
uma mensagem, e o tutorial fica com o mais simples.

## O comentário

O comentário em cima do decorador registra por que o método pode usar `self.witness_count` e os
outros campos sem conferir tipo nem limite: com `mode="after"`, ele só roda depois que todos os
campos passaram.
