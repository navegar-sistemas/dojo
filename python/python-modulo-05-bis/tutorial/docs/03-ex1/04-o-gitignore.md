---
sidebar_position: 4
title: O .gitignore e o .env.example
---

# O .gitignore e o .env.example

O `.env` guarda a configuração de verdade, com a chave de API. Ele precisa ficar ao lado do
programa, mas nunca pode entrar no repositório. Dois arquivos resolvem isso: o `.gitignore`, que
esconde o `.env` do git, e o `.env.example`, que vai para o repositório no lugar dele.

## O que o git registra

O git registra os arquivos que alguém marca com `git add`, e um `git add` de uma pasta inteira (como
`git add ex1`) marca tudo o que há nela. Um arquivo registrado uma vez fica no **histórico** do
repositório para sempre: apagá-lo depois não o tira dos registros antigos, e qualquer pessoa com
acesso ao repositório consegue lê-lo. Com uma chave de API, isso quer dizer trocar a chave, porque
a antiga não é mais secreta.

## O .gitignore

O **`.gitignore`** é um arquivo de texto com nomes (ou padrões de nomes) que o git deve ignorar:
ele não aparece como arquivo novo no `git status`, e o `git add` de uma pasta o pula. Crie
`ex1/.gitignore`:

```text title="ex1/.gitignore"
.env
```

Uma linha só, com o nome do arquivo. Um `.gitignore` vale para a pasta onde está e para as pastas
dentro dela; este, em `ex1/`, faz o git ignorar o `ex1/.env`. O enunciado pede o `.gitignore`
dentro de `ex1/`, e não na raiz do repositório.

O `.gitignore` não apaga nem esconde o arquivo da pasta: o `.env` continua lá, e o programa o lê
normalmente. Só o git deixa de vê-lo. E ele só protege o que ainda não foi registrado: um arquivo
que já entrou no repositório continua registrado mesmo depois de entrar no `.gitignore`.

## O .env.example

Sem o `.env` no repositório, quem baixa o projeto não sabe quais variáveis o programa espera. O
**`.env.example`** é o modelo: as mesmas variáveis, com valores que podem ser públicos, e os
segredos em branco. Crie `ex1/.env.example`:

```ini title="ex1/.env.example"
MATRIX_MODE=development
DATABASE_URL=sqlite:///oracle.db
API_KEY=
LOG_LEVEL=DEBUG
ZION_ENDPOINT=https://zion.example.com/api
```

- `MATRIX_MODE=development`: o modo de desenvolvimento, para o qual o `.env` existe;
- `DATABASE_URL=sqlite:///oracle.db`: o endereço de um banco **SQLite**, um banco de dados que
  cabe num único arquivo, aqui o `oracle.db`. O formato `tipo://endereço` é o de uma URL; um banco
  num servidor teria algo como `postgresql://usuario:senha@servidor/banco`, e aí a URL também é um
  segredo;
- `API_KEY=`: em branco. O segredo nunca vai para o modelo; cada pessoa põe a sua chave no próprio
  `.env`;
- `LOG_LEVEL=DEBUG`: o nível de registro mais detalhado, útil para quem desenvolve;
- `ZION_ENDPOINT=https://zion.example.com/api`: o endereço da rede remota. O domínio
  `example.com` é reservado para exemplos e não pertence a ninguém.

Os valores são escolha do tutorial; o enunciado só fixa os nomes das variáveis. O programa não se
conecta a nada: ele só lê a configuração e mostra o que faria com ela.

## O ciclo

```mermaid
flowchart LR
    ex["ex1/.env.example<br/>(no repositório)"] -->|"cp"| env["ex1/.env<br/>(só na sua máquina)"]
    env -->|"você preenche API_KEY"| env
    env -->|"load_dotenv"| prog["oracle.py"]
    gi["ex1/.gitignore<br/>.env"] -.->|"o git ignora"| env
```

Quem baixa o projeto copia o modelo, preenche os segredos e roda. O roteiro do enunciado faz
exatamente isso, com `cp ex1/.env.example ex1/.env`
([Rodar e conferir](./09-rodar-e-conferir.md)).
