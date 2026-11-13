---
sidebar_position: 6
title: O shebang
---

# O shebang

Até aqui, o programa roda com `python3 ex0/ft_garden_intro.py`: quem digita escolhe o programa
(`python3`) que vai ler o arquivo. Um programa comum do sistema, como `ls`, roda só pelo nome. O
**shebang** dá isso a um arquivo `.py`: com ele, o arquivo roda com `./ft_garden_intro.py`, sem
digitar `python3`.

Na avaliação, quem avalia pede que você acrescente o shebang ao programa, ao vivo. O arquivo
entregue fica sem shebang; o treino é feito numa cópia, em `experimentos/`.

## A linha

O shebang é a **primeira linha** do arquivo, começando com `#!` (o nome vem de *hash*, `#`, e
*bang*, `!`):

```text
#!/usr/bin/env python3
```

- para o Python, a linha é só um comentário (começa com `#`) e é ignorada;
- para o sistema, ela diz qual programa deve ler o arquivo: `/usr/bin/env python3`;
- `/usr/bin/env` é um programa que existe em todo Linux e macOS e que procura `python3` nas
  pastas de programas do sistema. Escrever o caminho do Python direto (como `/usr/bin/python3`)
  também funciona, mas só nas máquinas em que o Python está exatamente ali; o `env` acha o
  `python3` em qualquer pasta da lista de pastas de programas do sistema (o `PATH`).

## Treinar numa cópia

Copie o programa para a pasta de experimentos:

```bash
cp ex0/ft_garden_intro.py experimentos/semente.py
```

Abra `experimentos/semente.py` e acrescente o shebang como **primeira linha**, antes de tudo:

```python title="experimentos/semente.py"
#!/usr/bin/env python3
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

## A permissão de execução

Tentar rodar agora com `./experimentos/semente.py` termina num erro com `permission denied`
("permissão negada"; o resto da mensagem muda conforme o shell): o sistema só roda como programa um
arquivo marcado como **executável**. O comando `chmod +x` dá essa marca:

```bash
chmod +x experimentos/semente.py
```

- `chmod` muda as permissões de um arquivo;
- `+x` acrescenta a permissão de execução (*execute*).

Agora o arquivo roda pelo caminho, sem `python3`:

```bash
./experimentos/semente.py
```

```text
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days

=== End of Program ===
```

O `./` no começo quer dizer "a pasta atual". Um nome de comando **sem** nenhuma barra, como
`semente.py`, é procurado só nas pastas de programas do sistema, e não na pasta atual; por isso,
de dentro da pasta `experimentos`, o comando seria `./semente.py`. Com uma barra no nome, como
`experimentos/semente.py`, o caminho já é seguido a partir da pasta atual, e o `./` só deixa isso
explícito.

## Na avaliação

São os mesmos dois passos, no arquivo de verdade: acrescentar `#!/usr/bin/env python3` como
primeira linha de `ex0/ft_garden_intro.py` e rodar `chmod +x ex0/ft_garden_intro.py`. Depois,
`./ex0/ft_garden_intro.py` roda o programa. O shebang não muda nada para o flake8, para o mypy
nem para `python3 ex0/ft_garden_intro.py`, que continua funcionando.
