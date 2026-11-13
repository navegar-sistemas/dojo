---
sidebar_position: 8
title: Enviar e conferir
---

# Enviar e conferir

Com os arquivos certos na raiz ([página anterior](./07-o-que-entregar.md)), falta registrar a
versão final no Git, enviá-la ao servidor de entrega e conferir que o que foi enviado funciona
sozinho. Antes disso, nenhum arquivo de experiência pode ter sobrado na pasta.

## Limpar os arquivos de experiência

Os blocos Experimente do tutorial criam arquivos e pastas na raiz do projeto
(`solto_config.txt`, `pasta_saida/`, `trancado/`, `pequeno.txt`, `troca_porta.py`,
`sem_barreira.py` e outros) e os apagam no fim do próprio bloco. Um bloco interrompido no meio,
porém, pode deixar algum para trás.

`git status --porcelain` lista, uma por linha, as mudanças que o Git ainda não registrou num
*commit* (um registro de versão do Git). Cada linha começa com um código de duas letras e
termina com o caminho do arquivo:

| Código | Quer dizer |
|---|---|
| `??` | arquivo novo, que o Git ainda não acompanha |
| ` M` | arquivo acompanhado, modificado desde o último commit |
| ` D` | arquivo acompanhado, apagado desde o último commit |

```bash
git status --porcelain
```

Os arquivos que o `.gitignore` ignora (`.venv/`, `__pycache__/`, `maze.txt`...) nunca aparecem.
Toda linha `??` com um nome que não faz parte da entrega ([página anterior](./07-o-que-entregar.md))
é sobra de um exemplo: apague-a com `rm` (ou `rm -r`, se for uma pasta). Uma pasta sem
permissão de escrita, como a `trancado/` da [parte 12](../12-geracao-e-saida/05-gravando-o-arquivo.md),
precisa antes de `chmod 755 trancado`, que devolve a permissão de apagar o que tem dentro.

## Registrar e enviar

Três comandos, na raiz do projeto:

```bash
git add -A
git commit -m "Finish A-Maze-ing"
git push
```

- `git add -A` marca para o próximo commit todas as mudanças da pasta: arquivos novos,
  modificados e apagados, menos os ignorados pelo `.gitignore`. Por isso a limpeza vem antes.
- `git commit -m "..."` cria o commit com essas mudanças; o texto depois do `-m` é a descrição
  dele, que aparece no histórico. Escreva o que mudou, com as suas palavras.
- `git push` envia os commits novos ao servidor de onde o repositório foi clonado, o de entrega
  ([parte 3](../03-ambiente/01-o-ambiente-virtual.md)). Num repositório criado com `git init`,
  o primeiro envio precisa do endereço: `git remote add origin <url-do-repositório>` e depois
  `git push -u origin HEAD`.
  Antes dele, o commit só existe no seu computador.

Depois disso, `git status --porcelain` não pode imprimir nada: não sobrou mudança sem registro
nem arquivo esquecido.

## Rodar a entrega num clone novo

O último passo é fazer o que o avaliador vai fazer, numa pasta nova, fora da pasta do projeto
(por exemplo, na pasta acima dela). `git clone` baixa uma cópia nova do repositório, só com o
que está nele; o endereço é o mesmo do clone da [parte 3](../03-ambiente/01-o-ambiente-virtual.md):

```bash
git clone <url-do-repositório> entrega
cd entrega
make install
make lint
printf '4\n' | make run
```

- `make install` cria o `.venv` do zero e instala as ferramentas.
- `make lint` roda o flake8 (estilo) e o mypy (tipos) e precisa terminar sem nenhuma linha do
  flake8 e com `Success: no issues found` do mypy.
- `printf '4\n' | make run` desenha o labirinto e responde `4` ao menu, que sai com código 0.

Se algum desses passos depende de algo que só existe na sua máquina (um arquivo que o
`.gitignore` deixou de fora, uma ferramenta instalada fora do `.venv`), é no clone novo que isso
aparece. Não apague a pasta `entrega` ainda: a [próxima página](./08-o-roteiro-da-avaliacao.md)
usa esse mesmo clone para reconstruir o pacote como na avaliação.
