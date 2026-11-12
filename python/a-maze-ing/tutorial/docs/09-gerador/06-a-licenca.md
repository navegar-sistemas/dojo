---
sidebar_position: 6
title: A licença MIT
---

# A licença MIT

## O que o subject pede

O gerador vai ser reaproveitado num projeto seguinte. Por isso o capítulo VI exige um
`LICENSE.md` na raiz do repositório, com uma licença que **permita explicitamente a reutilização
e a distribuição** do código.

Sem licença nenhuma, vale o direito autoral padrão: o código é só do autor, e ninguém (nem um
colega, nem um projeto futuro) tem permissão de copiá-lo, modificá-lo ou redistribuí-lo.

## Por que MIT

A licença MIT cabe em três parágrafos e diz exatamente o que o subject pede:

| Trecho da MIT | O que concede ou exige |
|---|---|
| "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell" | uso, cópia, modificação e distribuição, com todas as letras |
| "The above copyright notice and this permission notice shall be included" | a única condição: manter o aviso de copyright e o texto da licença nas cópias |
| "THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND" | o autor não responde por defeitos |

As alternativas mais comuns:

| Licença | Por que não |
|---|---|
| GPL | é *copyleft*: todo projeto que incorpora o código e é distribuído tem de sair também sob a GPL. Isso impõe uma condição ao projeto seguinte, em vez de só liberar o uso |
| Apache 2.0 | também permissiva, com cláusulas extras sobre patentes e avisos de mudança; é mais longa e cobre casos que um gerador de labirintos não tem |
| nenhuma | ninguém pode reutilizar legalmente |

A MIT é a mais curta que cumpre a exigência, e uma das mais usadas em projetos abertos.

## A linha de copyright

```text
Copyright (c) 2026 macoelho
```

O ano e o titular dos direitos: o login da intra 42 de quem escreveu o código. Troque `macoelho`
pelo seu login; com mais de um autor, separe os logins por vírgula. O resto do texto é o da MIT,
sem nenhuma alteração.

## Como o pacote leva a licença

O `pyproject.toml` (parte 3) declara a licença em duas chaves:

```toml
license = "MIT"
license-files = ["LICENSE.md"]
```

- `license = "MIT"` é um identificador padrão (SPDX), gravado nos metadados do pacote como
  `License-Expression: MIT`;
- `license-files` aponta o arquivo, que o build copia para dentro do wheel, em
  `mazegen-1.0.0.dist-info/licenses/LICENSE.md`.

Assim, quem instala o wheel recebe a licença junto, como a própria MIT exige.

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
