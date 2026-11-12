---
sidebar_position: 4
title: Time, bônus e recursos
---

# Time, bônus e recursos

As três últimas seções são as mais pessoais: o texto delas é **seu**, não do tutorial. O
README de referência mostra o formato; troque cada frase pela sua experiência.

## Team and project management

O subject lista quatro perguntas, e a seção responde as quatro, um tópico para cada:

| Tópico | Pergunta do subject | O que escrever |
|---|---|---|
| **Team** | os papéis de cada membro | quem fez o quê; sozinho, diga que fez tudo |
| **Planning** | o planejamento previsto e como evoluiu | a ordem em que você construiu as peças e o que mudou no caminho |
| **What worked well** / **What could improve** | o que funcionou e o que melhoraria | decisões concretas, não adjetivos |
| **Tools** | ferramentas usadas | linguagem, ambiente, linters, controle de versão, scripts |

"What could improve" pede honestidade técnica. O README de referência aponta uma: a checagem do
3x3 percorre a grade inteira a cada parede aberta, e olhar só as janelas em volta da parede
seria mais rápido. Um ponto assim mostra que você conhece o próprio código melhor do que um
"poderia ter mais testes".

Se você seguiu este tutorial, a ordem das partes 3 a 15 é um planejamento válido para
descrever: esqueleto, value objects, entidade, algoritmos, gerador público, utilitários,
config, geração, desenho, menu e fechamento.

## Bonus

O subject pede que funcionalidades avançadas sejam descritas no README. O único bônus
implementado é o tabuleiro sem becos do modo Pac-Man (parte 16). A seção diz:

- o que é: o modo `PERFECT=False`, o padrão, sai sem nenhum beco real;
- por que: o braiding abre uma parede em cada beco, e sobram só os 2 cercados pelo "42", que o
  analisador não conta;
- como conferir, num bloco `sh`, com o `maze_analyzer.py` do subject e `--max-dead-ends 0`;
- o veredito esperado, exatamente como o analisador o imprime.

Se você não implementou nenhum bônus, a seção pode ser omitida. Se implementou outros, cada um
entra aqui, com o que faz e como ativar.

## Resources

Duas partes, ambas exigidas.

**Referências clássicas.** Livros, artigos e documentação sobre o assunto, cada um com título
e link. O critério é ajudar quem quer aprender mais: *Mazes for Programmers*, do Jamis Buck, o
artigo dele sobre o recursive backtracker, as páginas da Wikipedia sobre geração de labirintos,
busca em largura e códigos ANSI, a documentação do `random`, a PEP 257 e o guia de estilo do
Google (docstrings), o guia de empacotamento do Python e a PEP 639 (licença no
`pyproject.toml`), e o texto da licença MIT. Liste o que **você** leu.

**AI usage.** O subject pede que o README diga para quais tarefas a IA foi usada e quais
partes do projeto ela afetou. Uma tabela de duas colunas resolve:

```markdown
| Task | Files or parts affected |
|---|---|
| explaining `mypy --strict` messages | `mazegen/` and `amazeing/` type hints |
```

- Uma linha por tarefa, com o verbo do que a IA fez (revisar, sugerir, explicar, gerar).
- A coluna da direita nomeia arquivos ou partes, não "o projeto todo".
- Se você não usou IA, escreva isso numa frase.

O capítulo II do subject explica a regra por trás: a IA pode ajudar, mas só entra no projeto o
que você entende e consegue explicar. A frase final do README de referência diz exatamente
isso, e só deve ficar lá se for verdade.
