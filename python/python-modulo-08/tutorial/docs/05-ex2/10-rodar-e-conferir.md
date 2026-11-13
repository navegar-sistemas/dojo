---
sidebar_position: 10
title: Rodar e conferir
---

# Rodar e conferir

Os comandos desta página são rodados dentro da pasta `ex2`, começando sem nenhum ambiente
ativado:

```bash
cd ex2
```

## Sem o python-dotenv

Com o Python global, que não tem o python-dotenv:

```bash
python3 oracle.py
echo $?
```

```text
ORACLE ERROR: python-dotenv is not installed.
Install it with: pip install -r requirements.txt
1
```

O `import` falhou dentro do `try`, e o programa terminou com a instrução de instalação e o código
`1` ([Ler a configuração](./04-ler-a-configuracao.md#o-import-do-python-dotenv)).

## O ambiente do exercício

```bash
python3 -m venv matrix_env
source matrix_env/bin/activate
pip install -r requirements.txt
```

A saída termina com:

```text
Installing collected packages: python-dotenv
Successfully installed python-dotenv-1.2.4

[notice] A new release of pip is available: 26.1.1 -> 26.3
[notice] To update, run: pip install --upgrade pip
```

A versão pode ser outra. As linhas `[notice]` são o aviso de pip mais novo, o mesmo do
[exercício 1](../04-ex1/10-rodar-com-pip.md#uma-biblioteca-só), e podem não aparecer.

## Sem configuração

Ainda não há `.env`, e nenhuma das cinco variáveis existe no terminal:

```bash
python3 oracle.py
echo $?
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration errors:
[MISSING] MATRIX_MODE is not set
[MISSING] DATABASE_URL is not set
[MISSING] API_KEY is not set
[MISSING] LOG_LEVEL is not set
[MISSING] ZION_ENDPOINT is not set

Copy .env.example to .env and fill in the values,
or set the variables in the environment.
1
```

## O .env copiado do modelo

```bash
cp .env.example .env
python3 oracle.py
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration errors:
[MISSING] API_KEY is not set

Copy .env.example to .env and fill in the values,
or set the variables in the environment.
```

As outras quatro variáveis vieram do `.env`; a `API_KEY` está vazia no modelo, de propósito
([Os arquivos de apoio](./03-os-arquivos-de-apoio.md#envexample)).

## O .env preenchido

Abra o `.env` num editor de texto (por exemplo, `nano .env` no terminal: `Ctrl+O` grava e
`Ctrl+X` sai) e preencha a `API_KEY`. Num projeto de verdade, a chave é a que o serviço fornece;
aqui, qualquer texto serve. O arquivo fica assim:

```ini title="ex2/.env"
# Copy to .env and fill in the values. Never commit .env.
MATRIX_MODE=development
DATABASE_URL=sqlite:///matrix.db
API_KEY=dev-key-zion-0042
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:8080/zion
```

```bash
python3 oracle.py
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides available

The Oracle sees all configurations.
```

### Comparar com o enunciado

O `diff` compara a saída do programa com a do enunciado
([como o diff funciona](../03-ex0/07-rodar-e-conferir.md#comparar-com-o-enunciado)):

```bash
diff <(python3 oracle.py) - <<'FIM'

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides available

The Oracle sees all configurations.
FIM
```

Sem nenhuma linha impressa, a saída é igual à do enunciado, linha por linha.

## Produção

O exemplo do enunciado sobrepõe duas variáveis na linha de comando:

```bash
MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: production
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides active: MATRIX_MODE, API_KEY
[WARNING] DEBUG log level in production
[WARNING] Local database in production

The Oracle sees all configurations.
```

- `Mode: production`: o valor da linha de comando venceu o do `.env`;
- a linha de sobreposições lista as duas variáveis que vieram de fora do arquivo;
- o modo de produção acrescentou a sua conferência, e ela reprova o nível de log e o banco de
  dados, que continuam os de desenvolvimento, vindos do `.env`.

Com o nível de log e o banco de produção também sobrepostos (a `\` no fim da linha continua o
comando na linha de baixo):

```bash
MATRIX_MODE=production LOG_LEVEL=WARNING \
DATABASE_URL=postgresql://db.zion.net:5432/matrix python3 oracle.py
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: production
Database: Connected to remote instance
API Access: Authenticated
Log Level: WARNING
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly configured
[OK] Production overrides active: MATRIX_MODE, DATABASE_URL, LOG_LEVEL
[OK] Production settings verified

The Oracle sees all configurations.
```

O banco agora é remoto, e a conferência de produção passa. A chave é a do `.env`.

Num servidor de produção de verdade, não há `.env`: toda a configuração vem do ambiente. Para
simular isso, uma pasta `teste` só com o programa, criada e apagada no mesmo bloco:

```bash
mkdir teste
cp oracle.py teste/
cd teste
MATRIX_MODE=production \
DATABASE_URL=postgresql://db.zion.net:5432/matrix \
API_KEY=secret123 \
LOG_LEVEL=WARNING \
ZION_ENDPOINT=https://zion.net/api \
python3 oracle.py
cd ..
rm -r teste
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: production
Database: Connected to remote instance
API Access: Authenticated
Log Level: WARNING
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] No .env file, using environment variables only
[OK] Production overrides available
[OK] Production settings verified

The Oracle sees all configurations.
```

Sem `.env`, não há arquivo para proteger nem valor do arquivo para sobrepor. `rm -r teste` apaga
a pasta e o que está nela.

## Um modo que não existe

```bash
MATRIX_MODE=staging python3 oracle.py
echo $?
```

```text

ORACLE STATUS: Reading the Matrix...

Configuration errors:
[INVALID] MATRIX_MODE must be development or production, not 'staging'

Copy .env.example to .env and fill in the values,
or set the variables in the environment.
1
```

## Os avisos de segurança

Um segredo escrito no código: uma cópia do programa, `leaky.py` ("vazado"), com a chave do `.env`
escrita numa linha a mais no fim. `>>` acrescenta a saída do `echo` no fim do arquivo, e
`grep hardcoded` mostra só as linhas da saída que têm a palavra `hardcoded`:

```bash
cp oracle.py leaky.py
echo 'BACKUP_KEY = "dev-key-zion-0042"' >> leaky.py
python3 leaky.py | grep hardcoded
rm leaky.py
```

```text
[WARNING] API_KEY is hardcoded in the source code
```

Um `.env` sem `.gitignore`: o programa e o `.env` copiados para uma pasta sem `.gitignore`:

```bash
mkdir teste
cp oracle.py .env teste/
cd teste
python3 oracle.py | grep env
cd ..
rm -r teste
```

```text
[WARNING] .env is not listed in .gitignore
```

As duas conferências reagem quando o problema existe ([A conferência de
segurança](./06-a-conferencia-de-seguranca.md)).

## Conferir estilo e tipos

```bash
../.venv/bin/flake8 oracle.py
```

O flake8 não imprime nada. O mypy, rodado do jeito de sempre, reclama:

```bash
../.venv/bin/mypy --disallow-untyped-defs oracle.py
```

```text
oracle.py:5: error: Cannot find implementation or library stub for module named "dotenv"  [import-not-found]
oracle.py:5: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
Found 1 error in 1 file (checked 1 source file)
```

O mypy está instalado no `.venv` das ferramentas e procura o `dotenv` lá, onde ele não está. A
opção `--python-executable` diz ao mypy para procurar as bibliotecas no Python de outro ambiente,
o `matrix_env`, onde o python-dotenv foi instalado:

```bash
../.venv/bin/mypy --disallow-untyped-defs --python-executable matrix_env/bin/python oracle.py
```

```text
Success: no issues found in 1 source file
```

Agora o mypy encontra a biblioteca e confere o uso dela com os type hints que ela traz.

## No Python 3.10

Com o Python 3.10, todas as saídas desta página são as mesmas, menos o aviso `[notice]` do
`pip install`, que cita o pip que veio com o 3.10 (`23.0.1 -> 26.3`).

Desative o ambiente e volte para a pasta do projeto:

```bash
deactivate
cd ..
```
