---
sidebar_position: 3
title: output_pipeline
---

# output_pipeline

O **pipeline** é o caminho inteiro do dado: entra no fluxo por `process_stream`, fica guardado na
fila de um processador e sai exportado por um plugin. `output_pipeline` é a parte da saída.

```python
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            data: list[tuple[int, str]] = []
            while len(data) < nb and processor.remaining() > 0:
                data.append(processor.output())
            if data:
                plugin.process_output(data)
```

O método entra em `DataStream`, entre `print_processors_stats` e `_find_processor`.

## Passo a passo

Para cada processador registrado, na ordem do registro:

1. `data` começa como uma lista vazia de tuplas `(rank, texto)`. A anotação é obrigatória: o
   primeiro uso de `data` é o `len(data)` do `while`, e não um `append`
   ([O tipo de uma lista que começa vazia](../02-conceitos/05-a-fila.md#o-tipo-de-uma-lista-que-começa-vazia));
2. o `while` tira um item com `output` e o acrescenta em `data`, enquanto as **duas** condições
   valerem: ainda não juntou `nb` itens, e o processador ainda tem itens
   (`processor.remaining() > 0`, [Nome e contadores](../04-ex1/02-nome-e-contadores.md)). A
   segunda condição impede o `output` numa fila vazia, que lançaria `IndexError`;
3. se juntou algum item, entrega a lista inteira ao plugin com `plugin.process_output(data)`.

O plugin é chamado uma vez **por processador**: por isso a saída do enunciado tem três blocos
`CSV Output:`, um para números, um para textos e um para logs.

![O pipeline com nb igual a 3 e o plugin CSV: o Numeric Processor tem 4 itens e entrega os 3 mais antigos (ranks 0, 1 e 2), ficando com 1; o Text Processor entrega os seus 3 itens; o Log Processor tem só 2 e entrega os 2. Cada lista vai para process_output do plugin, que imprime um bloco CSV Output](/img/ex2/pipeline.svg)

## Quando um processador está vazio

O enunciado não diz o que fazer quando um processador não tem nada para exportar. A escolha do
tutorial é **não chamar o plugin**: um bloco `CSV Output:` sem nenhum dado não informa nada. O
`if data:` faz isso, porque uma lista vazia conta como falso. No cenário do enunciado, todo
processador tem pelo menos um item a cada exportação, e a escolha não aparece na saída.

## Polimorfismo dos dois lados

`output_pipeline` não sabe que tipo de processador está percorrendo (chama `remaining` e
`output`, que todos têm) nem que formato o plugin escreve (chama `process_output`, que todo
plugin tem). Um processador novo ou um formato novo entram no pipeline sem nenhuma mudança neste
método.
