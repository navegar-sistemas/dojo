---
sidebar_position: 6
title: A conferência de segurança
---

# A conferência de segurança

O segundo bloco da saída do enunciado é uma conferência de segurança com três linhas `[OK]`:

```text
Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides available
```

O enunciado não diz o que cada linha confere. A **escolha do tutorial** é que cada uma seja uma
verificação de verdade, que pode falhar e trocar o `[OK]` por um `[WARNING]` (aviso). As funções
desta página entram no arquivo depois de `show_config`, nesta ordem.

## Nenhum segredo no código

Um segredo **hardcoded** ("escrito no código") é um valor secreto escrito direto no código, como
`API_KEY = "abc123"`. Ele vai para o repositório junto com o código, e qualquer pessoa com acesso
ao repositório passa a conhecê-lo. A conferência procura o valor da `API_KEY` em uso dentro do
próprio arquivo do programa:

```python
def secrets_check(api_key: str) -> str:
    with open(__file__, encoding="utf-8") as source:
        code = source.read()
    if f'"{api_key}"' in code or f"'{api_key}'" in code:
        return "[WARNING] API_KEY is hardcoded in the source code"
    return "[OK] No hardcoded secrets detected"
```

- `__file__` é uma variável que o Python preenche com o caminho do arquivo que está rodando: o
  próprio `oracle.py`;
- `with open(...) as source:` abre o arquivo e o fecha sozinho no fim do bloco; `read()` devolve
  o conteúdo inteiro num texto. `encoding="utf-8"` diz como os caracteres estão gravados;
- um valor escrito no código Python aparece sempre entre aspas, duplas ou simples. A função
  procura a chave com os dois tipos de aspas em volta: `f'"{api_key}"'` é o texto da chave entre
  aspas duplas.

No programa correto, a chave não está escrita em lugar nenhum: ela vem do ambiente. A conferência
só daria um aviso falso com uma chave igual a um dos textos que o próprio programa usa, como
`production` ou `DEBUG`, o que nenhuma chave de verdade é. A página
[Rodar e conferir](./10-rodar-e-conferir.md#os-avisos-de-segurança) prova o aviso com uma cópia do
programa que tem a chave escrita nele.

## O .env protegido

```python
def ignored_names() -> list[str]:
    if not os.path.isfile(IGNORE_FILE):
        return []
    with open(IGNORE_FILE, encoding="utf-8") as ignore:
        return ignore.read().splitlines()


def env_file_check() -> str:
    if not os.path.isfile(ENV_FILE):
        return "[OK] No .env file, using environment variables only"
    if ENV_FILE not in ignored_names():
        return "[WARNING] .env is not listed in .gitignore"
    return "[OK] .env file properly configured"
```

- `os.path.isfile(caminho)` responde se existe um arquivo com aquele caminho;
- `ignored_names` devolve as linhas do `.gitignore` (`splitlines()` divide um texto em linhas), ou
  uma lista vazia se não houver `.gitignore`;
- `env_file_check` tem três respostas. Sem `.env`, toda a configuração veio do ambiente, como num
  servidor de produção, e não há arquivo para proteger: `[OK]`. Com um `.env` que não está no
  `.gitignore`, o segredo corre o risco de ir para o repositório: `[WARNING]`. Com o `.env`
  listado: `[OK] .env file properly configured`, a linha do enunciado.

A conferência procura a linha exata `.env`, a que o `.gitignore` do exercício tem. O Git aceita
outros padrões que também cobririam o arquivo (como `/.env` ou `*.env`); o programa não os
reconhece, e avisaria. É uma conferência simples para um `.gitignore` conhecido.

## As variáveis que vieram do ambiente

```python
def overrides_check() -> str:
    file_values = dotenv_values(ENV_FILE)
    overridden = []
    for name in VARIABLES:
        if name in file_values and file_values[name] != os.environ[name]:
            overridden.append(name)
    if overridden:
        return f"[OK] Production overrides active: {', '.join(overridden)}"
    return "[OK] Production overrides available"
```

Um **override** ("sobreposição") é uma variável definida no ambiente que vale mais que o valor do
`.env` ([Quem vale mais](./02-o-arquivo-env.md#quem-vale-mais)). A função descobre quais variáveis
estão nessa situação:

- `dotenv_values(ENV_FILE)` lê o `.env` sem mexer no ambiente, e devolve o que o arquivo diz;
- uma variável do arquivo cujo valor no ambiente (`os.environ[name]`) é **diferente** do valor do
  arquivo só pode ter vindo de fora, porque o `load_dotenv` não substitui o que já existe;
- sem nenhuma sobreposição, a linha é a do enunciado, `[OK] Production overrides available`: o
  mecanismo está disponível. Com sobreposições, a linha lista quais estão ativas, como em
  `MATRIX_MODE=production API_KEY=secret123 python3 oracle.py`, que dá
  `[OK] Production overrides active: MATRIX_MODE, API_KEY`.

A linha fica `[OK]` nos dois casos: sobrepor variáveis é o jeito certo de configurar a produção.
O que ela informa é de onde veio cada valor.
