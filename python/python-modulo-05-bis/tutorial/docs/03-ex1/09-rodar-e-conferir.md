---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## Estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
ex1/oracle.py:3: error: Cannot find implementation or library stub for module named "dotenv"  [import-not-found]
ex1/oracle.py:3: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 1 error in 1 file (checked 1 source file)
```

O flake8 não imprime nada, mas o mypy não acha o `dotenv`. Ele confere cada `import` procurando a
biblioteca no ambiente onde **ele** está instalado, o `.venv`, e o `python-dotenv` foi instalado
no `lab_env`. A opção `--python-executable` diz ao mypy de qual Python ele deve olhar as
bibliotecas:

```bash
.venv/bin/mypy --disallow-untyped-defs --python-executable lab_env/bin/python ex1
```

```text
Success: no issues found in 1 source file
```

Mais um efeito do isolamento: cada ambiente só enxerga as próprias bibliotecas, até para as
ferramentas.

Os comandos seguintes rodam o programa com o `lab_env` **ativado** (prompt com `(lab_env)`; se
não, `source lab_env/bin/activate`).

## Sem nenhuma configuração

O `ex1/.env` ainda não existe:

```bash
python3 ex1/oracle.py
```

```text

ORACLE STATUS: Consulting the configuration...

[WARNING] No .env file found, reading the environment only
[WARNING] MATRIX_MODE not set, using default: development
[WARNING] DATABASE_URL not set, using default: sqlite:///oracle.db
[WARNING] API_KEY not set and has no default
[WARNING] LOG_LEVEL not set, using default: INFO
[WARNING] ZION_ENDPOINT not set and has no default

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Anonymous (development only)
Log Level: INFO
Remote Network: Offline

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Production overrides available

The Oracle sees all configurations.
```

Os valores padrão e um aviso para cada coisa que falta, como o roteiro pede, e o programa termina
normalmente (código de saída `0`, que `echo $?` mostraria). Se alguma das cinco variáveis já
estiver definida no seu terminal (por um `export` antigo), a linha `Production overrides
available` vira `Environment overrides active`, com o nome dela; um terminal novo começa sem elas.

## Com o .env

Copie o modelo:

```bash
cp ex1/.env.example ex1/.env
python3 ex1/oracle.py
```

```text

ORACLE STATUS: Consulting the configuration...

[WARNING] API_KEY not set and has no default

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Anonymous (development only)
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Production overrides available

The Oracle sees all configurations.
```

Agora a configuração vem do `.env`: `Log Level: DEBUG` e `Remote Network: Online`. Falta a chave,
que o modelo deixa em branco. O roteiro manda editar o `ex1/.env` "com os seus valores": abra-o num
editor de texto e troque a linha `API_KEY=` por uma chave, como `API_KEY=dev-key-42` (qualquer
texto serve; o programa não a envia a lugar nenhum). O arquivo fica assim:

```bash
cat ex1/.env
```

```text
MATRIX_MODE=development
DATABASE_URL=sqlite:///oracle.db
API_KEY=dev-key-42
LOG_LEVEL=DEBUG
ZION_ENDPOINT=https://zion.example.com/api
```

`cat` imprime o conteúdo de um arquivo. Agora a saída é a do enunciado, e o `diff` confere:

```bash
diff <(python3 ex1/oracle.py) - <<'FIM'

ORACLE STATUS: Consulting the configuration...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Production overrides available

The Oracle sees all configurations.
FIM
```

Sem nenhuma linha impressa: igual, inclusive a linha vazia do começo. O `<(...)`, o `-` e o
`<<'FIM'` são explicados em [Rodar e conferir do exercício 0](../02-ex0/12-rodar-e-conferir.md).

## Sobrescrevendo pelo ambiente

O comando do roteiro, com o `.env` ainda no lugar:

```bash
MATRIX_MODE=production API_KEY=secret123 python3 ex1/oracle.py
```

```text

ORACLE STATUS: Consulting the configuration...

Configuration loaded:
Mode: production
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Environment overrides active: MATRIX_MODE, API_KEY
[WARNING] DEBUG logging enabled in production

The Oracle sees all configurations.
```

- `Mode: production`: o valor do terminal venceu o `development` do `.env`, e a linha
  `Environment overrides active` diz quais variáveis vieram do terminal;
- o resto (banco, nível de registro, rede) continua vindo do `.env`;
- o `DEBUG` do `.env`, aceitável em desenvolvimento, virou aviso em produção.

## Produção sem chave

Um `API_KEY=` vazio no terminal conta como variável existente para o `load_dotenv` (ele não a troca
pela do `.env`) e como chave faltando para o Oráculo:

```bash
MATRIX_MODE=production API_KEY= python3 ex1/oracle.py
```

```text

ORACLE STATUS: Consulting the configuration...

[WARNING] API_KEY not set and has no default

Configuration loaded:
Mode: production
Database: Connected to local instance
API Access: DENIED - API_KEY is required in production
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Environment overrides active: MATRIX_MODE
[WARNING] DEBUG logging enabled in production

The Oracle sees all configurations.
```

Em desenvolvimento, a mesma falta deu `Anonymous (development only)`; em produção, o acesso é
negado. As duas diferenças entre os modos aparecem na saída, como o enunciado pede.

## Um banco remoto

```bash
DATABASE_URL=postgresql://oracle:hunter2@db.zion.example.com/matrix python3 ex1/oracle.py | sed -n 4,6p
```

```text
Configuration loaded:
Mode: development
Database: Connected to remote instance
```

`sed -n 4,6p` imprime só as linhas 4 a 6 da saída. A URL não tem nenhum dos marcadores de banco
local. Repare que ela traz uma senha (`hunter2`), e que a saída não a mostra.

## Um segredo no código

A conferência de segredos procura o valor da `API_KEY` dentro do `oracle.py`. Uma chave que por
acaso é um texto escrito no código mostra o aviso; `localhost` está no código, em
`LOCAL_MARKERS`:

```bash
API_KEY=localhost python3 ex1/oracle.py | grep "source code"
```

```text
[WARNING] API_KEY value found in the source code
```

`grep` mostra só as linhas que contêm o texto procurado. Uma chave de verdade colada no código
cairia no mesmo aviso.

## O .gitignore funcionando

O `.gitignore` só tem efeito dentro de um repositório git. Um repositório de teste, numa pasta
`teste-git` criada só para isso, mostra o que o git veria da pasta `ex1`:

```bash
git init -q teste-git
cp -R ex1 teste-git/
git -C teste-git status --short --untracked-files=all
git -C teste-git check-ignore -v ex1/.env
rm -rf teste-git
```

```text
?? ex1/.env.example
?? ex1/.gitignore
?? ex1/oracle.py
?? ex1/requirements.txt
ex1/.gitignore:1:.env	ex1/.env
```

1. `git init -q teste-git` cria um repositório vazio na pasta `teste-git` (o `-q` cala a
   mensagem);
2. `cp -R` copia a pasta `ex1` inteira, com o `.env`, para dentro dele;
3. `git -C teste-git` roda o comando como se estivesse dentro da pasta. `status --short` lista os
   arquivos que o git encontrou, e `??` quer dizer "arquivo novo, ainda não registrado";
   `--untracked-files=all` lista os arquivos um a um, em vez de só a pasta. O `ex1/.env` não
   aparece;
4. `check-ignore -v` explica por que o arquivo é ignorado: a regra `.env`, da linha 1 do
   `ex1/.gitignore`;
5. `rm -rf` apaga o repositório de teste.
