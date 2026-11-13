---
sidebar_position: 7
title: A licença MIT
---

# A licença MIT

O gerador vai ser reaproveitado num projeto seguinte, talvez por outras pessoas. Para
alguém poder usar legalmente um código que não escreveu, o autor precisa dar essa permissão por
escrito. Esta página explica o que é uma licença de software, o que o enunciado exige dela e por
que este projeto usa a licença MIT.

## O que é uma licença

Quem escreve um código tem, automaticamente, o **direito autoral** (*copyright*) sobre ele, como o
autor de um livro. Sem nenhuma autorização escrita, ninguém além do autor pode copiar, modificar
ou redistribuir esse código, nem um colega, nem um projeto futuro.

Uma **licença** é o texto em que o autor diz o que os outros **podem** fazer com o código e em
que condições. Existem licenças prontas, de texto padronizado, que qualquer pessoa pode adotar:
basta copiar o texto para o projeto e pôr o próprio nome.

## O que o enunciado exige

- um arquivo `LICENSE.md` na raiz do repositório, declarando a licença do código;
- uma licença que **permita explicitamente a reutilização e a distribuição** do gerador pelos
  projetos que vierem depois.

O enunciado deixa a escolha da licença para o aluno e diz que escolhê-la faz parte da tarefa: é o
primeiro contato com licenciamento de software.

## Por que MIT

A escolha da MIT é do projeto. Ela cabe em três parágrafos e diz exatamente o que o enunciado
pede:

| Trecho da MIT | O que concede ou exige |
|---|---|
| "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell" | usar, copiar, modificar, juntar a outro código, publicar, distribuir e até vender, com todas as letras |
| "The above copyright notice and this permission notice shall be included" | a única condição: manter o aviso de copyright e o texto da licença nas cópias |
| "THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND" | o código vem "como está": o autor não responde por defeitos |

As alternativas mais comuns:

| Licença | Por que não |
|---|---|
| GPL | é *copyleft*: todo projeto que incorpora o código e é distribuído tem de sair também sob a GPL. Isso impõe uma condição ao projeto seguinte, em vez de só liberar o uso |
| Apache 2.0 | também libera o uso, mas tem cláusulas extras sobre patentes e sobre avisar mudanças; é mais longa e cobre casos que um gerador de labirintos não tem |
| BSD de 3 cláusulas | quase igual à MIT, com uma cláusula a mais (proíbe usar o nome do autor para promover o projeto derivado); a MIT é mais curta |
| nenhuma | ninguém pode reutilizar legalmente, e o enunciado não é cumprido |

A MIT é a mais curta que cumpre a exigência, e uma das licenças mais usadas em projetos abertos.

## A linha de copyright

```text
Copyright (c) 2026 macoelho
```

O ano e o dono dos direitos: aqui, o login (o nome de usuário) de quem escreveu o código. Troque `macoelho` pelo seu login; com mais de um autor, separe os logins por vírgula. O
resto do texto é o da MIT, sem nenhuma alteração.

## Como o pacote leva a licença

O `pyproject.toml`, o arquivo de configuração do pacote Python
([parte 3](../03-ambiente/04-pyproject.md)), declara a licença em duas chaves:

```toml
license = "MIT"
license-files = ["LICENSE.md"]
```

- `license = "MIT"` usa o identificador padrão da licença. Os nomes de licença seguem uma lista
  oficial chamada SPDX, para qualquer ferramenta reconhecê-los; o nome vai para os dados do pacote
  como `License-Expression: MIT`;
- `license-files` aponta o arquivo com o texto, que o empacotamento copia para dentro do pacote
  instalável, em `mazegen-1.0.0.dist-info/licenses/LICENSE.md`
  ([página 10](./09-instalar-o-pacote.md)).

Assim, quem instala o pacote recebe a licença junto, como a própria MIT exige.

## O arquivo completo

Na raiz do projeto:

```markdown title="LICENSE.md"
MIT License

Copyright (c) 2026 macoelho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
