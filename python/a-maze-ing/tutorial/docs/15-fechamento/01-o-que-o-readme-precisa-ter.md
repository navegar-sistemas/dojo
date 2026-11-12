---
sidebar_position: 1
title: O que o README precisa ter
---

# O que o README precisa ter

Com o programa pronto, falta o `README.md` final. Ele conta na avaliação: cada seção exigida
pelo subject é conferida, e o avaliador lê o arquivo antes de rodar qualquer coisa. Ele também
é a descrição longa do pacote `mazegen` (o `pyproject.toml` declara `readme = "README.md"`),
então vai dentro do wheel.

O objetivo, nas palavras do subject: alguém que não conhece o projeto (colega, staff,
recrutador) entende rapidamente do que se trata, como executá-lo e onde aprender mais sobre o
assunto.

## A primeira linha

A primeiríssima linha do arquivo, em itálico, é fixa:

```markdown
*This project has been created as part of the 42 curriculum by macoelho.*
```

- Troque `macoelho` pelo **seu** login da intra 42. Com mais de um autor, separe por vírgula e
  espaço: `by login1, login2.`
- Os asteriscos de abertura e fechamento fazem o itálico; o ponto final fica **dentro** deles.
- Nada antes dela: nem título, nem linha em branco, nem comentário.

O mesmo login vai no `authors` do `pyproject.toml` (parte 3) e na linha `Copyright` do
`LICENSE.md` (parte 9). Os três arquivos precisam dizer a mesma coisa.

## Idioma

O subject recomenda inglês e aceita o idioma principal do campus. O README do projeto é em
inglês, como o código e as mensagens do programa.

## As seções

O subject exige três seções com nome fixo (`Description`, `Instructions` e `Resources`) e,
para este projeto, mais cinco assuntos. O README tem oito seções, nesta ordem:

| Seção | O que o subject pede |
|---|---|
| `Description` | o objetivo do projeto e uma visão geral |
| `Instructions` | como instalar e executar |
| `Configuration file` | a estrutura e o formato completos do arquivo de configuração |
| `Algorithm` | o algoritmo de geração escolhido e **por que** foi escolhido |
| `Reusable module` | qual parte do código é reutilizável e como reutilizá-la, com a documentação curta do módulo |
| `Team and project management` | papéis, planejamento e como ele evoluiu, o que funcionou e o que melhoraria, ferramentas |
| `Bonus` | as funcionalidades além da parte obrigatória |
| `Resources` | referências clássicas e **como a IA foi usada** |

Os títulos são `##`, abaixo de um único `# A-Maze-ing`. A ordem segue o caminho de quem chega
ao projeto: o que é, como roda, como configura, como funciona por dentro, como reutiliza, quem
fez e onde aprender mais.

## O que vale para todas as seções

- **Só o que existe.** Uma funcionalidade descrita no README e ausente no programa é a primeira
  coisa que o avaliador testa. Animação, múltiplos algoritmos e cor própria para o "42" não
  foram implementados, então não aparecem.
- **Valores reais.** Comandos que funcionam se colados no terminal, o `config.txt` exatamente
  como está no repositório, mensagens exatamente como o programa as imprime.
- **Você explica tudo.** O capítulo de IA do subject vale também para o README: o que estiver
  escrito ali, você defende na avaliação.
