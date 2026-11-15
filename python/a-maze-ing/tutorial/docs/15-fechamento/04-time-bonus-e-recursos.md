---
sidebar_position: 4
title: Time, bônus e recursos
---

# Time, bônus e recursos

As três últimas seções do README contam como o projeto foi feito, o que ele tem a mais e onde
aprender sobre o assunto. São as mais pessoais: o texto delas é **seu**, não do tutorial. O
[README de referência](./05-o-readme-completo.md) mostra o formato; troque cada frase pela sua
experiência.

## Team and project management

O enunciado pede quatro respostas sobre a equipe e a gestão do projeto, e a seção dá um tópico
para cada:

| Tópico | O que o enunciado pede | O que escrever |
|---|---|---|
| **Team** | o papel de cada membro da equipe | quem fez o quê; se fez sozinho, diga que fez tudo |
| **Planning** | o planejamento previsto e como ele mudou até o fim | a ordem em que você construiu as peças e o que mudou no caminho |
| **What worked well** / **What could improve** | o que funcionou bem e o que poderia melhorar | decisões concretas, não adjetivos |
| **Tools** | as ferramentas usadas | linguagem, ambiente, verificadores de código, controle de versão, scripts |

"What could improve" pede honestidade técnica. O README de referência aponta uma melhoria
concreta: depois de cada parede aberta no modo Pac-Man, a conferência da regra do 3x3 olha a
grade inteira, quando bastaria olhar os blocos 3x3 em volta da parede aberta. Um ponto assim
mostra que você conhece o próprio código; uma frase genérica ("o código poderia ser melhor") não
mostra nada.

Se você seguiu este tutorial, a ordem das partes 3 a 15 é um planejamento real para descrever:
ambiente, valores básicos (coordenada, direção, "42"), a grade de paredes, os três algoritmos
(cavar, achar o caminho, trançar), o gerador público, os utilitários, a configuração, a geração
com o arquivo de saída, o desenho, o menu e o fechamento.

## Bonus

O enunciado diz que, se o projeto tem funcionalidades além da parte obrigatória, o README as
descreve. Ele sugere três bônus: um tabuleiro de Pac-Man sem nenhum beco sem saída, vários
algoritmos de geração e uma animação da geração. Este projeto fez só o primeiro
([parte 16](../16-bonus/01-o-tabuleiro-sem-becos.md)). A seção diz:

- **o que é**: nos labirintos medidos, o modo `PERFECT=False` (o modo que o enunciado chama de
  padrão) sai sem nenhum beco real. Não é uma garantia: o código garante no máximo 2, porque a
  regra obrigatória do 3x3 (nenhum bloco de 3x3 células todo aberto) pode impedir uma abertura
  ([parte 16, página 2](../16-bonus/02-por-que-nao-e-garantido.md));
- **por que sai assim**: o *braiding* abre uma parede em cada beco, e sobram só os 2 becos
  cercados pelo "42", que não podem ser abertos e que o analisador do enunciado não conta
  ([parte 16, página 3](../16-bonus/03-conferir-com-o-analyzer.md));
- **como conferir**: o comando do `maze_analyzer.py`, o programa que vem com o enunciado e
  confere o arquivo de saída, com a opção `--max-dead-ends 0` ("no máximo 0 becos");
- **o resultado esperado**, exatamente como o analisador o imprime.

Se você não fez nenhum bônus, a seção pode ser omitida. Se fez outros, cada um entra aqui, com o
que faz e como ativar. O mesmo vale para a interação opcional do menu que o enunciado sugere,
escolher cores específicas para o "42": este projeto não a tem (o "42" é sempre cinza), e por
isso o README não a cita.

## Resources

O enunciado pede duas coisas nesta seção.

**Referências clássicas.** Livros, artigos e documentação sobre o assunto, cada um com título e
link. O critério é ajudar quem quer aprender mais. O README de referência lista:

- o livro *Mazes for Programmers*, de Jamis Buck, e o artigo dele sobre o *recursive
  backtracker*;
- as páginas da Wikipedia sobre algoritmos de geração de labirintos, busca em largura, códigos
  ANSI (as sequências de cor do terminal) e caracteres de caixa (os que desenham as paredes);
- a documentação do módulo `random` do Python;
- a PEP 257 (a convenção das docstrings) e o guia de estilo do Google, que define o formato das
  docstrings do projeto;
- o guia oficial de empacotamento do Python e a PEP 639 (como declarar a licença no
  `pyproject.toml`);
- o texto da licença MIT.

Liste o que **você** leu.

**Uso de IA.** O enunciado pede que o README diga para quais tarefas a inteligência artificial
foi usada e quais partes do projeto ela afetou. Uma subseção `### AI usage` com uma tabela de
duas colunas resolve:

```markdown
| Task | Files or parts affected |
|---|---|
| explaining `mypy --strict` messages | `mazegen/` and `amazeing/` type hints |
```

- Uma linha por tarefa, começando pelo verbo do que a IA fez: revisar, sugerir, explicar, gerar.
- A coluna da direita nomeia arquivos ou partes do projeto, e não "o projeto todo".
- Se você não usou IA, escreva isso numa frase.

A regra por trás está no capítulo do enunciado sobre IA: ela pode ajudar, mas só entra no projeto
o que você entende por completo e pelo que pode responder. Os exemplos do próprio enunciado
mostram um aluno que reprova por não conseguir explicar, na avaliação, um código que a IA
escreveu. A frase final do README de referência ("Every line of
the project was reviewed and can be explained by its author", "cada linha foi revisada e pode
ser explicada pelo autor") diz exatamente isso, e só deve ficar lá se for verdade.
