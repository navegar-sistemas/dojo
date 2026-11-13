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
ao repositório passa a conhecê-lo. A conferência procura os valores em uso das variáveis de
`SECRETS`, a `API_KEY` e a `DATABASE_URL`, dentro do próprio arquivo do programa:

```python
def secrets_check(config: dict[str, str]) -> str:
    try:
        with open(__file__, encoding="utf-8") as source:
            code = source.read()
    except (OSError, UnicodeDecodeError):
        return "[WARNING] Cannot read the source code to look for secrets"
    found = []
    for name in SECRETS:
        value = config[name]
        if f'"{value}"' in code or f"'{value}'" in code:
            found.append(name)
    if found:
        return f"[WARNING] Hardcoded in the source code: {', '.join(found)}"
    return "[OK] No hardcoded secrets detected"
```

- `__file__` é uma variável que o Python preenche com o caminho do arquivo que está rodando: o
  próprio `oracle.py`;
- `with open(...) as source:` abre o arquivo e o fecha sozinho no fim do bloco; `read()` devolve
  o conteúdo inteiro num texto. `encoding="utf-8"` diz como os caracteres estão gravados;
- se o arquivo não puder ser lido (`OSError`, como falta de permissão, ou `UnicodeDecodeError`,
  um arquivo que não é UTF-8 válido), a conferência não acontece, e a linha diz isso com um
  `[WARNING]` em vez de derrubar o programa;
- um valor escrito no código Python aparece sempre entre aspas, duplas ou simples. Para cada
  variável de `SECRETS`, a função procura o valor com os dois tipos de aspas em volta:
  `f'"{value}"'` é o texto do valor entre aspas duplas;
- a linha de aviso diz quais variáveis foram achadas, como
  `[WARNING] Hardcoded in the source code: API_KEY, DATABASE_URL`.

No programa correto, nenhum desses valores está escrito em lugar nenhum: eles vêm do ambiente. A conferência
só daria um aviso falso com um valor igual a um dos textos que o próprio programa usa, como
`production` ou `DEBUG`, o que nenhuma chave nem endereço de banco de verdade é. A página
[Rodar e conferir](./10-rodar-e-conferir.md#os-avisos-de-segurança) prova o aviso com uma cópia do
programa que tem a chave e o endereço escritos nele.

## O .env protegido

```python
def ignored_names() -> list[str] | None:
    if not os.path.isfile(IGNORE_FILE):
        return []
    try:
        with open(IGNORE_FILE, encoding="utf-8") as ignore:
            return ignore.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None


def env_file_check() -> str:
    if not os.path.isfile(ENV_FILE):
        return "[OK] No .env file, using environment variables only"
    names = ignored_names()
    if names is None:
        return "[WARNING] Cannot read .gitignore"
    if ENV_FILE not in names:
        return "[WARNING] .env is not listed in .gitignore"
    return "[OK] .env file properly configured"
```

- `os.path.isfile(caminho)` responde se existe um arquivo com aquele caminho;
- `ignored_names` devolve as linhas do `.gitignore` (`splitlines()` divide um texto em linhas),
  uma lista vazia se não houver `.gitignore`, ou `None` se ele existe mas não pôde ser lido. O tipo
  de retorno `list[str] | None` diz exatamente isso: uma lista de textos ou nada;
- com `None`, `env_file_check` avisa `[WARNING] Cannot read .gitignore`: sem ler o arquivo, não há
  como saber se o `.env` está protegido;
- fora isso, `env_file_check` tem três respostas. Sem `.env`, toda a configuração veio do ambiente, como num
  servidor de produção, e não há arquivo para proteger: `[OK]`. Com um `.env` que não está no
  `.gitignore`, o segredo corre o risco de ir para o repositório: `[WARNING]`. Com o `.env`
  listado: `[OK] .env file properly configured`, a linha do enunciado.

A conferência procura a linha exata `.env`, a que o `.gitignore` do exercício tem. O Git aceita
outros padrões que também cobririam o arquivo (como `/.env` ou `*.env`); o programa não os
reconhece, e avisaria. É uma conferência simples para um `.gitignore` conhecido.

## As variáveis que vieram do ambiente

```python
def overrides_check() -> str:
    try:
        file_values = dotenv_values(ENV_FILE)
    except (OSError, UnicodeDecodeError):
        return "[WARNING] Cannot read .env to compare overrides"
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

- `dotenv_values(ENV_FILE)` lê o `.env` sem mexer no ambiente, e devolve o que o arquivo diz. O
  `main` já leu o mesmo arquivo com o `load_dotenv`, mas ele pode ter mudado entre uma leitura e
  outra; se esta falhar, a linha avisa, como as outras conferências;
- uma variável do arquivo cujo valor no ambiente (`os.environ[name]`) é **diferente** do valor do
  arquivo só pode ter vindo de fora, porque o `load_dotenv` não substitui o que já existe;
- sem nenhuma sobreposição, a linha é a do enunciado, `[OK] Production overrides available`: o
  mecanismo está disponível. Com sobreposições, a linha lista quais estão ativas, como em
  `MATRIX_MODE=production API_KEY=secret123 python3 oracle.py`, que dá
  `[OK] Production overrides active: MATRIX_MODE, API_KEY`.

A linha fica `[OK]` nos dois casos: sobrepor variáveis é o jeito certo de configurar a produção.
O que ela informa é de onde veio cada valor.
