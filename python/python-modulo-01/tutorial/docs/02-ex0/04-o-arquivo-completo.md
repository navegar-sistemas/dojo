---
sidebar_position: 4
title: O arquivo completo
---

# O arquivo completo

As variáveis e os `print` vão dentro do bloco `if __name__ == "__main__":`, com quatro espaços
de recuo:

```python title="ex0/ft_garden_intro.py"
if __name__ == "__main__":
    name: str = "Rose"
    height: int = 25
    age: int = 30
    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days")
    print()
    print("=== End of Program ===")
```

O arquivo termina com **uma** quebra de linha logo depois da última linha,
`print("=== End of Program ===")`, e nada depois dela. O botão de copiar, no canto do bloco, não
leva essa quebra final: se, depois de colar, o cursor ficar no fim dessa última linha, aperte
Enter uma vez antes de salvar. Alguns editores já acrescentam a quebra ao salvar. Sem a quebra, o
flake8 acusa `W292 no newline at end of file` ("sem quebra de linha no fim do arquivo"); com mais de uma, ele
acusa `W391 blank line at end of file` ("linha em branco no fim do arquivo"), e a correção é
apagar as linhas vazias do fim. Se o Enter deixar espaços de recuo na linha nova, o flake8 acusa
`W293 blank line contains whitespace` ("linha em branco com espaços") junto com o `W292`: apague
esses espaços, deixando a linha vazia. O mesmo vale para os arquivos dos outros exercícios.

O arquivo só chama `print()`, a única função autorizada.
