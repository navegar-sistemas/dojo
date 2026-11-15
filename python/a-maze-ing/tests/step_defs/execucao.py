"""Passos que executam comandos e conferem a saída."""

import re
from collections.abc import Callable

import pytest
from pytest_bdd import parsers, then, when

from suporte.estado import Estado, Execucao
from suporte.labirinto import FECHADA, Labirinto
from suporte.tipos import TIPOS

# Palavra-chave que a mensagem de erro traz para cada motivo (I21).
MOTIVOS = {
    "arquivo não encontrado": "not found",
    "arquivo não é UTF-8": "UTF-8",
    "chave obrigatória ausente": "missing",
    "entrada igual à saída": "differ",
    "tamanho sem tabuleiro Pac-Man": "Pac-Man",
    "coordenada no padrão 42": '"42"',
}
AVISO_DO_42 = 'Error: maze too small for the "42" pattern'


def conferir_mensagem_de_erro(execucao: Execucao, itens: list[str]) -> str:
    """Confere a mensagem de erro da D01 e os itens citados, na ordem.

    Args:
        execucao: Execução que deveria terminar em erro.
        itens: Textos que a mensagem cita, na ordem.

    Returns:
        A linha da mensagem.
    """
    linhas = execucao.saida_erro.strip().splitlines()
    if len(linhas) != 1 or not linhas[0].startswith("Error: "):
        pytest.fail(
            "a saída de erro deveria ser uma única linha começando com "
            f"'Error: ', mas foi:\n{execucao.saida_erro!r}"
        )
    mensagem = linhas[0]
    inicio = 0
    for item in itens:
        posicao = mensagem.find(item, inicio)
        if posicao < 0:
            pytest.fail(
                f"a mensagem não cita {item!r} depois de "
                f"{mensagem[:inicio]!r}: {mensagem!r}"
            )
        inicio = posicao + len(item)
    return mensagem


def conferir_motivo(mensagem: str, motivo: str) -> None:
    """Confere a palavra-chave do motivo (I21), sem diferenciar caixa.

    Args:
        mensagem: Linha da mensagem de erro.
        motivo: Uma das chaves de MOTIVOS.
    """
    chave = MOTIVOS.get(motivo)
    if chave is None:
        pytest.fail(
            f'motivo "{motivo}" não existe; os válidos são: '
            f"{', '.join(MOTIVOS)}"
        )
    if not re.search(re.escape(chave), mensagem, re.IGNORECASE):
        pytest.fail(f"a mensagem não contém {chave!r}: {mensagem!r}")


@when(parsers.parse("eu executo {comandos:L}", extra_types=TIPOS))
def eu_executo(estado: Estado, comandos: list[str]) -> None:
    """Grava o config e roda cada comando, com stdin vazio.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
    """
    estado.gravar_config()
    for comando in comandos:
        estado.executar(comando)


@when(
    parsers.parse(
        "eu executo {comandos:L} com a entrada {linhas:L}", extra_types=TIPOS
    )
)
def eu_executo_com_entrada(
    estado: Estado, comandos: list[str], linhas: list[str]
) -> None:
    """Grava o config e roda cada comando com as linhas no stdin.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
        linhas: Linhas enviadas ao stdin, cada uma terminada em "\\n".
    """
    entrada = "".join(f"{linha}\n" for linha in linhas)
    estado.gravar_config()
    for comando in comandos:
        estado.executar(comando, entrada)


@when(
    parsers.parse(
        "eu executo {comandos:L} {n:d} vezes com a entrada {linhas:L}",
        extra_types=TIPOS,
    )
)
def eu_executo_vezes(
    estado: Estado, comandos: list[str], n: int, linhas: list[str]
) -> None:
    """Repete a execução com entrada n vezes e troca a lista de execuções.

    Args:
        estado: Estado do cenário.
        comandos: Comandos na ordem em que aparecem no passo.
        n: Número de repetições.
        linhas: Linhas enviadas ao stdin, cada uma terminada em "\\n".
    """
    inicio = len(estado.resultados)
    for _ in range(n):
        eu_executo_com_entrada(estado, comandos, linhas)
    estado.execucoes = estado.resultados[inicio:]


@then(
    parsers.parse(
        "{fluxo:Fluxo} {verbo:Contem} {textos:L}", extra_types=TIPOS
    )
)
def saida_contem(
    estado: Estado, fluxo: str, verbo: str, textos: list[str]
) -> None:
    """Confere se o fluxo contém (ou não) cada texto.

    Args:
        estado: Estado do cenário.
        fluxo: "a saída", "a saída padrão" ou "a saída de erro".
        verbo: "contém" ou "não contém".
        textos: Textos procurados.
    """
    saida = estado.resultado.fluxo(fluxo)
    for texto in textos:
        if verbo == "contém":
            assert texto in saida, f"{fluxo} não contém {texto!r}:\n{saida}"
        else:
            assert texto not in saida, f"{fluxo} contém {texto!r}:\n{saida}"


@then(parsers.parse("o código de saída é {codigo:d}"))
def codigo_de_saida(estado: Estado, codigo: int) -> None:
    """Confere o código de saída do último comando.

    Numa sessão, espera o processo terminar antes de conferir.

    Args:
        estado: Estado do cenário.
        codigo: Código esperado.
    """
    sessao = estado.em_sessao()
    if sessao is not None and sessao.esperar_fim() is None:
        pytest.fail(f"'{sessao.comando}' não terminou dentro do tempo limite")
    resultado = estado.resultado
    assert resultado.codigo == codigo, (
        f"'{resultado.comando}' terminou com código {resultado.codigo}, "
        f"esperado {codigo}\n{resultado.saida_padrao}{resultado.saida_erro}"
    )


@then(
    parsers.parse(
        'o comando "{comando:Q}" termina com código {codigo:d}',
        extra_types=TIPOS,
    )
)
def comando_termina_com(estado: Estado, comando: str, codigo: int) -> None:
    """Roda o comando agora e confere o código de saída.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando.
        codigo: Código esperado.
    """
    resultado = estado.executar(comando)
    assert resultado.codigo == codigo, (
        f"'{comando}' terminou com código {resultado.codigo}, esperado "
        f"{codigo}\n{resultado.saida_padrao}{resultado.saida_erro}"
    )


@then(
    parsers.parse(
        'a saída de "{comando:Q}" é "{texto:Q}"', extra_types=TIPOS
    )
)
def saida_do_comando_igual(estado: Estado, comando: str, texto: str) -> None:
    """Compara a saída do comando, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando; usa a execução do cenário ou roda agora.
        texto: Saída esperada (stdout e stderr juntos).
    """
    saida = estado.resultado_de(comando).fluxo("a saída").strip()
    assert saida == texto, f"'{comando}' mostrou {saida!r}, esperado {texto!r}"


@then(
    parsers.parse(
        'a saída de "{comando:Q}" contém "{texto:Q}"', extra_types=TIPOS
    )
)
def saida_do_comando_contem(estado: Estado, comando: str, texto: str) -> None:
    """Confere que a saída do comando contém o texto.

    Args:
        estado: Estado do cenário.
        comando: Linha de comando; usa a execução do cenário ou roda agora.
        texto: Texto procurado (em stdout e stderr juntos).
    """
    saida = estado.resultado_de(comando).fluxo("a saída")
    assert texto in saida, f"'{comando}' não mostrou {texto!r}:\n{saida}"


@then(
    parsers.parse(
        'a linha da saída que contém "{a:Q}" também contém "{b:Q}"',
        extra_types=TIPOS,
    )
)
def linha_da_saida_contem(estado: Estado, a: str, b: str) -> None:
    """Toda linha da última saída que contém a também contém b.

    Args:
        estado: Estado do cenário.
        a: Texto que identifica a linha.
        b: Texto exigido nessa linha.
    """
    saida = estado.resultado.fluxo("a saída")
    linhas = [linha for linha in saida.splitlines() if a in linha]
    assert linhas, f"nenhuma linha da saída contém {a!r}:\n{saida}"
    sem_b = [linha for linha in linhas if b not in linha]
    assert not sem_b, f"linha com {a!r} sem {b!r}: {sem_b}"


@then(parsers.parse('{fluxo:Fluxo} é "{texto:Q}"', extra_types=TIPOS))
def saida_igual(estado: Estado, fluxo: str, texto: str) -> None:
    """Confere o fluxo inteiro, sem espaços nas pontas.

    Args:
        estado: Estado do cenário.
        fluxo: "a saída", "a saída padrão" ou "a saída de erro".
        texto: Texto esperado.
    """
    saida = estado.resultado.fluxo(fluxo).strip()
    assert saida == texto, f"{fluxo} é {saida!r}, esperado {texto!r}"


@then("o processo termina dentro do tempo limite")
def termina_no_tempo(estado: Estado) -> None:
    """Confere que o último comando não estourou o tempo limite.

    Args:
        estado: Estado do cenário.
    """
    resultado = estado.resultado
    if resultado.estourou:
        pytest.fail(f"'{resultado.comando}' estourou o tempo limite")


@then(
    parsers.parse(
        'o resultado da execução é "{resultado:Q}"', extra_types=TIPOS
    )
)
def resultado_da_execucao(estado: Estado, resultado: str) -> None:
    """Confere "sucesso" ou "erro citando A, B[; motivo: M]".

    Sucesso exige código 0, nenhuma linha com "Error:" no stderr além do
    aviso do "42" omitido (D06, I10) e o OUTPUT_FILE do config gravado com
    conteúdo; erro exige código 1 e a mensagem da D01.

    Args:
        estado: Estado do cenário.
        resultado: "sucesso" ou "erro citando A, B[; motivo: M]".
    """
    execucao = estado.resultado
    if execucao.estourou:
        pytest.fail(f"'{execucao.comando}' estourou o tempo limite")
    if resultado == "sucesso":
        erros = [
            linha for linha in execucao.saida_erro.splitlines()
            if "Error:" in linha and linha.strip() != AVISO_DO_42
        ]
        if execucao.codigo != 0 or erros:
            pytest.fail(
                f"esperado sucesso, mas terminou com código "
                f"{execucao.codigo}:\n{execucao.saida_erro}"
            )
        saida = execucao.arquivo_saida
        if saida is None:
            pytest.fail("o comando não passa um config com OUTPUT_FILE")
        if not saida.is_file() or saida.stat().st_size == 0:
            pytest.fail(f"o arquivo de saída {saida.name} não foi gravado")
        return
    prefixo = "erro citando "
    if not resultado.startswith(prefixo):
        pytest.fail(
            f'resultado "{resultado}" não é "sucesso" nem começa com '
            f'"{prefixo}"'
        )
    citados, _, motivo = resultado[len(prefixo):].partition("; motivo: ")
    if execucao.codigo != 1:
        pytest.fail(
            f"esperado erro com código 1, mas terminou com código "
            f"{execucao.codigo}:\n{execucao.saida_padrao}"
            f"{execucao.saida_erro}"
        )
    mensagem = conferir_mensagem_de_erro(execucao, citados.split(", "))
    if motivo:
        conferir_motivo(mensagem, motivo)


@then(parsers.parse("todos os comandos terminam com código {codigo:d}"))
def todos_terminam_com(estado: Estado, codigo: int) -> None:
    """Confere o código de saída de todos os comandos do cenário.

    Args:
        estado: Estado do cenário.
        codigo: Código esperado.
    """
    if not estado.resultados:
        pytest.fail("nenhum comando foi executado antes deste passo")
    errados = [
        f"'{execucao.comando}' terminou com código {execucao.codigo}\n"
        f"{execucao.saida_padrao}{execucao.saida_erro}"
        for execucao in estado.resultados
        if execucao.codigo != codigo
    ]
    if errados:
        pytest.fail(f"esperado código {codigo}:\n" + "\n".join(errados))


@then(parsers.parse("a mensagem de erro cita {itens:L}", extra_types=TIPOS))
def mensagem_cita(estado: Estado, itens: list[str]) -> None:
    """Confere a mensagem da D01 e os itens citados, na ordem.

    Args:
        estado: Estado do cenário.
        itens: Textos que a mensagem cita.
    """
    conferir_mensagem_de_erro(estado.resultado, itens)


@then(
    parsers.parse(
        'a mensagem de erro explica "{motivo:Q}"', extra_types=TIPOS
    )
)
def mensagem_explica(estado: Estado, motivo: str) -> None:
    """Confere a mensagem da D01 e a palavra-chave do motivo (I21).

    Args:
        estado: Estado do cenário.
        motivo: Uma das chaves de MOTIVOS.
    """
    conferir_motivo(conferir_mensagem_de_erro(estado.resultado, []), motivo)


def labirintos_do_cenario(estado: Estado) -> list[Labirinto]:
    """Labirintos produzidos no cenário, exigindo pelo menos um.

    Args:
        estado: Estado do cenário.

    Returns:
        Os labirintos, do primeiro ao atual.
    """
    if not estado.labirintos:
        pytest.fail("nenhum labirinto foi produzido antes deste passo")
    return estado.labirintos


def linhas_da_grade(labirinto: Labirinto) -> list[str]:
    """Linhas da grade como texto, sem a quebra de linha.

    Args:
        labirinto: Labirinto lido de arquivo ou gerado pela classe.

    Returns:
        As linhas do texto bruto até a linha vazia; para o labirinto da
        classe, a grade escrita em hexadecimal minúsculo.
    """
    if labirinto.texto is None:
        return [
            "".join(format(valor, "x") for valor in linha)
            for linha in labirinto.grade
        ]
    linhas = labirinto.texto.split("\n")
    return linhas[:linhas.index("")] if "" in linhas else linhas


def linhas_do_rodape(estado: Estado, inicio: int, fim: int) -> list[str]:
    """Linhas do rodapé de cada labirinto, da posição inicio até fim.

    Args:
        estado: Estado do cenário.
        inicio: Índice da primeira linha, a partir de 0.
        fim: Índice depois da última linha.

    Returns:
        As linhas pedidas de todos os labirintos do cenário.
    """
    linhas: list[str] = []
    for labirinto in labirintos_do_cenario(estado):
        if len(labirinto.rodape) < fim:
            pytest.fail(
                f"o rodapé tem {len(labirinto.rodape)} linha(s), esperadas "
                f"pelo menos {fim}: {labirinto.rodape!r}"
            )
        linhas += labirinto.rodape[inicio:fim]
    return linhas


def solucoes(estado: Estado) -> list[str]:
    """Solução de cada labirinto do cenário.

    Args:
        estado: Estado do cenário.

    Returns:
        O caminho de cada labirinto.
    """
    caminhos: list[str] = []
    for labirinto in labirintos_do_cenario(estado):
        if labirinto.caminho is None:
            pytest.fail("o labirinto não tem solução (linha do caminho)")
        caminhos.append(labirinto.caminho)
    return caminhos


def primeira_linha_do_readme(estado: Estado) -> list[str]:
    """Primeira linha do README.md do repositório, sem converter quebras.

    Args:
        estado: Estado do cenário.

    Returns:
        A linha, como item único.
    """
    readme = estado.cwd / "README.md"
    if not readme.is_file():
        pytest.fail(f"README.md não existe em {estado.cwd}")
    return [readme.read_bytes().decode("utf-8").split("\n")[0]]


def nomes_selecionados(estado: Estado) -> list[str]:
    """Nome de cada arquivo selecionado por "eu leio".

    Args:
        estado: Estado do cenário.

    Returns:
        Os nomes, sem a pasta.
    """
    if not estado.lido:
        pytest.fail("nenhum arquivo foi selecionado antes deste passo")
    return [caminho.name for caminho in estado.lido]


def ultima_linha_da_saida(estado: Estado) -> list[str]:
    """Última linha da saída padrão do último comando.

    Args:
        estado: Estado do cenário.

    Returns:
        A linha, como item único.
    """
    linhas = estado.resultado.saida_padrao.splitlines()
    if not linhas:
        pytest.fail(f"'{estado.resultado.comando}' não imprimiu nada")
    return [linhas[-1]]


# Itens a que cada alvo da V67 aplica a expressão; os de labirinto juntam
# os itens de todos os labirintos do cenário.
ALVOS: dict[str, Callable[[Estado], list[str]]] = {
    "a solução": solucoes,
    "cada linha da grade": lambda estado: [
        linha
        for labirinto in labirintos_do_cenario(estado)
        for linha in linhas_da_grade(labirinto)
    ],
    "cada linha de coordenadas do rodapé": (
        lambda estado: linhas_do_rodape(estado, 0, 2)
    ),
    "a linha 3 do rodapé": lambda estado: linhas_do_rodape(estado, 2, 3),
    "a primeira linha do README": primeira_linha_do_readme,
    "o nome de cada arquivo selecionado": nomes_selecionados,
    "a última linha da saída padrão": ultima_linha_da_saida,
}


@then(
    parsers.parse(
        '{alvo:Alvo} casa com a expressão "{regex:Q}"', extra_types=TIPOS
    )
)
def alvo_casa_com(estado: Estado, alvo: str, regex: str) -> None:
    """Aplica a expressão (``re.search``) a cada item do alvo.

    As expressões dos cenários trazem as âncoras ``^`` e ``$``; o passo
    não acrescenta nenhuma.

    Args:
        estado: Estado do cenário.
        alvo: Um dos ALVOS.
        regex: Expressão regular.
    """
    itens = ALVOS.get(alvo)
    if itens is None:
        pytest.fail(
            f'alvo "{alvo}" não existe; os válidos são: {", ".join(ALVOS)}'
        )
    try:
        padrao = re.compile(regex)
    except re.error as erro:
        pytest.fail(f"expressão {regex!r} inválida: {erro}")
    fora = [item for item in itens(estado) if not padrao.search(item)]
    if fora:
        pytest.fail(f"{alvo}: {fora!r} não casa com {regex!r}")


def labirinto_da(execucao: Execucao) -> Labirinto:
    """Labirinto de uma execução, exigindo que ela tenha produzido um.

    Args:
        execucao: Execução do cenário.

    Returns:
        O labirinto.
    """
    if execucao.labirinto is None:
        pytest.fail(
            f"'{execucao.comando}' não produziu labirinto (código "
            f"{execucao.codigo}):\n{execucao.saida_erro}"
        )
    return execucao.labirinto


def conteudo_da(execucao: Execucao) -> str:
    """Conteúdo do OUTPUT_FILE gravado por uma execução.

    Args:
        execucao: Execução do cenário.

    Returns:
        O texto do arquivo de saída.
    """
    if execucao.conteudo_saida is None:
        pytest.fail(f"'{execucao.comando}' não gravou arquivo de saída")
    return execucao.conteudo_saida


def solucao_da(execucao: Execucao) -> str:
    """Solução do labirinto de uma execução.

    Args:
        execucao: Execução do cenário.

    Returns:
        O caminho do labirinto.
    """
    caminho = labirinto_da(execucao).caminho
    if caminho is None:
        pytest.fail(f"o labirinto de '{execucao.comando}' não tem solução")
    return caminho


# O que a V71 compara em cada execução.
ASPECTOS: dict[str, Callable[[Execucao], object]] = {
    "arquivo de saída": conteudo_da,
    "grade": lambda execucao: labirinto_da(execucao).grade,
    "solução": solucao_da,
    "células de valor F": lambda execucao: {
        celula
        for celula in labirinto_da(execucao).celulas()
        if labirinto_da(execucao).valor(celula) == FECHADA
    },
    "saída exibida": lambda execucao: execucao.saida_padrao,
}


@then(
    parsers.parse(
        'os resultados são {relacao:Relacao} em "{aspecto:Q}"',
        extra_types=TIPOS,
    )
)
def resultados_comparados(estado: Estado, relacao: str, aspecto: str) -> None:
    """Compara as execuções da última repetição, duas a duas, no aspecto.

    "idênticos" exige todas iguais; "diferentes entre si" exige todas
    distintas entre si.

    Args:
        estado: Estado do cenário.
        relacao: "idênticos" ou "diferentes entre si".
        aspecto: Um dos ASPECTOS.
    """
    extrair = ASPECTOS.get(aspecto)
    if extrair is None:
        pytest.fail(
            f'aspecto "{aspecto}" não existe; os válidos são: '
            f'{", ".join(ASPECTOS)}'
        )
    if relacao not in ("idênticos", "diferentes entre si"):
        pytest.fail(
            f'relação "{relacao}" não existe; as válidas são: idênticos, '
            "diferentes entre si"
        )
    if len(estado.execucoes) < 2:
        pytest.fail(
            f"a comparação precisa de pelo menos 2 execuções, o cenário tem "
            f"{len(estado.execucoes)}"
        )
    valores = [extrair(execucao) for execucao in estado.execucoes]
    pares = [
        (i, j)
        for i in range(len(valores))
        for j in range(i + 1, len(valores))
        if (valores[i] == valores[j]) != (relacao == "idênticos")
    ]
    if pares:
        descricao = ", ".join(f"{i + 1} e {j + 1}" for i, j in pares)
        comandos = "\n".join(
            f"{numero}: {execucao.comando}"
            for numero, execucao in enumerate(estado.execucoes, start=1)
        )
        pytest.fail(
            f'esperados resultados {relacao} em "{aspecto}", mas as '
            f"execuções {descricao} "
            f"{'diferem' if relacao == 'idênticos' else 'são iguais'}:\n"
            f"{comandos}"
        )
