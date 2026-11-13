---
sidebar_position: 2
title: Variáveis de ambiente
---

# Variáveis de ambiente

Para tirar a configuração do código, o programa precisa recebê-la de fora. O jeito mais antigo e
universal são as **variáveis de ambiente**: pares nome e valor que o terminal entrega a todo
programa que ele inicia. Algumas já existem sempre: `HOME`, por exemplo, guarda o caminho da pasta
pessoal do usuário, e `PATH` é a lista de pastas de programas
([Ativar o ambiente](../02-ex0/03-ativar-o-ambiente.md#o-path)).

## No Python: os.environ

O módulo `os` traz `os.environ`, que funciona como um dicionário com todas as variáveis de
ambiente que o programa recebeu: as chaves são os nomes, e os valores são sempre textos.
`os.environ.get(nome)` devolve o valor, ou `None` se a variável não existe, sem lançar erro.

Crie `experimentos/ambiente.py`:

```python title="experimentos/ambiente.py"
import os

print(f"MATRIX_MODE: {os.environ.get('MATRIX_MODE')}")
print(f"HOME is set: {'HOME' in os.environ}")
```

`'HOME' in os.environ` pergunta se a chave existe, como num dicionário.

```bash
python3 experimentos/ambiente.py
```

```text
MATRIX_MODE: None
HOME is set: True
```

`MATRIX_MODE` não existe; `HOME` existe.

## Dar um valor só para um comando

Escrito antes do comando, `NOME=valor` cria a variável só para aquele programa:

```bash
MATRIX_MODE=production python3 experimentos/ambiente.py
python3 experimentos/ambiente.py
```

```text
MATRIX_MODE: production
HOME is set: True
MATRIX_MODE: None
HOME is set: True
```

Na segunda execução, a variável já não existe. É o jeito do roteiro do enunciado:
`MATRIX_MODE=production API_KEY=secret123 python3 ex1/oracle.py` passa duas variáveis ao
programa, só naquela execução.

## Dar um valor para o resto do terminal

`export` cria a variável no próprio terminal, e todo programa iniciado depois a recebe; `unset` a
apaga:

```bash
export MATRIX_MODE=development
python3 experimentos/ambiente.py
unset MATRIX_MODE
python3 experimentos/ambiente.py
```

```text
MATRIX_MODE: development
HOME is set: True
MATRIX_MODE: None
HOME is set: True
```

Cada programa recebe uma **cópia** das variáveis do terminal. Se o programa mudar `os.environ`, a
mudança vale só dentro dele e dos programas que ele iniciar; o terminal não fica sabendo.

## Por que a configuração vai aqui

- o mesmo código roda em lugares diferentes, cada um com os seus valores: o servidor de produção
  define as variáveis dele, e quem desenvolve define as suas;
- o segredo não fica escrito em nenhum arquivo do repositório.

A desvantagem: definir cinco variáveis à mão toda vez que se abre um terminal cansa. Para o
desenvolvimento, existe o arquivo `.env`, na [próxima página](./03-o-arquivo-env-e-o-python-dotenv.md).
