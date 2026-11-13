---
sidebar_position: 4
title: O prefixo Created
---

# O prefixo Created

Cada linha da saída começa com `Created: ` e continua com a linha do `show()`. O `show()` não
pode mudar, então o prefixo é impresso **antes** dele, na mesma linha.

## O parâmetro end do print

Todo `print()` termina o que imprime com uma quebra de linha. O parâmetro `end` troca esse final.
Ele é passado **pelo nome**, no formato `nome=valor`, depois dos textos a imprimir:
`print("Created: ", end="")` imprime o texto e termina com nada (`""`), e o próximo `print`
continua na mesma linha.

```python title="experimentos/end.py"
print("Created: ", end="")
print("Rose")
print("Next line")
```

```bash
python3 experimentos/end.py
```

```text
Created: Rose
Next line
```

O primeiro `print` não quebrou a linha, e o segundo escreveu `Rose` logo depois de `Created: `;
o segundo, sem `end`, quebrou a linha normalmente.

## No laço

```python
    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created: ", end="")
        plant.show()
```

O espaço depois dos dois-pontos fica no texto do prefixo, porque o `show()` começa direto pelo
nome. `end` é um parâmetro do próprio `print`, a função autorizada, e não uma função nova.
