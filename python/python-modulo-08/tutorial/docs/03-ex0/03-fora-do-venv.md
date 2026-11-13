---
sidebar_position: 3
title: Fora do venv
---

# Fora do venv

Fora de um ambiente virtual, o programa avisa que está no Python global e ensina a criar e ativar
um venv. A função entra no fim do arquivo:

```python
def show_outside() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows")
    print()
    print("Then run this program again.")
```

- `print()` sem argumento imprime uma linha vazia, a que separa os blocos da saída;
- `sys.executable` é o caminho do Python que está rodando o programa: a única informação desta
  saída que muda de máquina para máquina;
- os textos seguem a saída do enunciado letra por letra. O `"You're"` tem um apóstrofo, e por isso
  o texto fica entre aspas duplas.

## A barra invertida

Dentro de um texto Python, a **barra invertida** `\` começa um código especial: `\n` é uma
quebra de linha, `\t` uma tabulação. Para imprimir a barra em si, escreve-se `\\`. Por isso
`"matrix_env\\Scripts\\activate"` imprime `matrix_env\Scripts\activate`. Com a barra simples, o
`\a` viraria um caractere invisível (o "sino" do terminal) e a palavra `activate` perderia o `a`;
o `\S`, que não é um código válido, sairia como está, mas com um aviso do flake8
(`W605 invalid escape sequence`) e, a partir do Python 3.12, outro do próprio Python
(`SyntaxWarning`).

A mesma linha tem dois espaços antes do `#`, como no enunciado.

## Os comandos sugeridos

As três linhas de comando são as que o enunciado mostra, inclusive o `python` (e não `python3`)
no primeiro: o programa repete o texto do enunciado. Num sistema que só tem `python3`, o primeiro
comando é `python3 -m venv matrix_env`
([Rodar e conferir](./07-rodar-e-conferir.md)).
