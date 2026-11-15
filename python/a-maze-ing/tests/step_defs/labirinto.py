"""Passos sobre o labirinto, a célula isolada e o validador da suíte."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from step_defs.geracao import gerar_pelo_programa
from suporte.config import CONFIG_BASE, Config, chaves_das_linhas
from suporte.estado import Estado
from suporte.labirinto import (
    CONTAGENS,
    DESLOCAMENTOS,
    DIRECOES,
    FECHADA,
    FIXTURES,
    MODELOS,
    NOMES,
    PROPRIEDADES,
    RELATOS,
    Celula,
    Chaves,
    Labirinto,
    bits_em_paredes,
    celulas_f,
    contagem,
    coordenada,
    intervalos,
    ler_saida,
    paredes_em_bits,
    regiao,
    relatar,
    texto_do_arquivo,
    violacoes,
    xy,
)
from suporte.tipos import TIPOS

ARQUIVO_DE_TESTE = "labirinto_de_teste.txt"
CONFIG_DE_REFERENCIA = "cfg_base.txt"
DIRECAO_POR_NOME = {nome: letra for letra, nome in NOMES.items()}
BORDAS: dict[str, Callable[[Labirinto], list[Celula]]] = {
    "primeira linha": lambda lab: [(x, 0) for x in range(lab.largura)],
    "última coluna": lambda lab: [
        (lab.largura - 1, y) for y in range(lab.altura)
    ],
    "última linha": lambda lab: [
        (x, lab.altura - 1) for x in range(lab.largura)
    ],
    "primeira coluna": lambda lab: [(0, y) for y in range(lab.altura)],
}


def todos_os_labirintos(estado: Estado) -> list[Labirinto]:
    """Labirintos do cenário: os registrados e os das gerações repetidas.

    Args:
        estado: Estado do cenário.

    Returns:
        Cada labirinto uma vez, na ordem em que foi produzido.
    """
    achados = list(estado.labirintos)
    for execucao in estado.execucoes:
        if execucao.labirinto is not None and not any(
            execucao.labirinto is labirinto for labirinto in achados
        ):
            achados.append(execucao.labirinto)
    if not achados:
        pytest.fail("nenhum labirinto foi produzido antes deste passo")
    return achados


def chaves_do_cenario(estado: Estado) -> Chaves:
    """Chaves do config atual, para as propriedades que dependem dele.

    Args:
        estado: Estado do cenário.

    Returns:
        Chave em maiúsculas para valor, ou None sem config.
    """
    if estado.config is None:
        return None
    return chaves_das_linhas(estado.config.linhas)


def falhar_por_labirinto(
    estado: Estado, conferir: Callable[[Labirinto], list[str]], o_que: str
) -> None:
    """Aplica a conferência a cada labirinto e falha com as violações.

    Args:
        estado: Estado do cenário.
        conferir: Função que devolve as violações de um labirinto.
        o_que: O que se esperava, para a mensagem de falha.
    """
    labirintos = todos_os_labirintos(estado)
    falhas: list[str] = []
    for numero, labirinto in enumerate(labirintos, start=1):
        achadas = conferir(labirinto)
        if achadas:
            detalhes = "; ".join(achadas[:10])
            sobra = len(achadas) - 10
            if sobra > 0:
                detalhes += f"; e mais {sobra}"
            falhas.append(
                f"labirinto {numero} de {len(labirintos)} "
                f"({labirinto.largura}x{labirinto.altura}): {detalhes}"
            )
    if falhas:
        pytest.fail(f"esperava {o_que}:\n" + "\n".join(falhas))


def confirmar(estado: Estado, propriedade: str) -> None:
    """Confere uma propriedade de V72 em todos os labirintos do cenário.

    Args:
        estado: Estado do cenário.
        propriedade: Nome da lista fechada de V72.
    """
    if propriedade not in PROPRIEDADES:
        pytest.fail(
            f'propriedade "{propriedade}" não existe; as válidas são: '
            f"{', '.join(PROPRIEDADES)}"
        )
    chaves = chaves_do_cenario(estado)
    falhar_por_labirinto(
        estado,
        lambda labirinto: violacoes(labirinto, propriedade, chaves),
        f'"{propriedade}"',
    )


def gravar_labirinto_de_teste(estado: Estado, texto: str) -> Labirinto:
    """Grava o arquivo de um labirinto de teste e o registra.

    O arquivo fica na pasta do cenário e some no fim do teste.

    Args:
        estado: Estado do cenário.
        texto: Conteúdo do arquivo de saída.

    Returns:
        O labirinto lido do texto, já em ``labirintos``.
    """
    destino = estado.cwd / ARQUIVO_DE_TESTE
    if not estado.reservado(destino):
        estado.proteger(destino)
    destino.write_bytes(texto.encode("utf-8"))
    try:
        labirinto = ler_saida(texto)
    except ValueError as erro:
        pytest.fail(f"o labirinto de teste não se lê: {erro}")
    labirinto.arquivo = destino
    estado.labirintos.append(labirinto)
    return labirinto


def celula_do_cenario(estado: Estado) -> int:
    """Valor da célula isolada do cenário.

    Args:
        estado: Estado do cenário.

    Returns:
        Os bits de 0 a 15.
    """
    if estado.celula is None:
        pytest.fail("nenhuma célula foi dada antes deste passo")
    return estado.celula


def celula_dada(texto: str) -> Celula:
    """Converte a célula "x,y" de um passo.

    Args:
        texto: Coordenada como escrita no passo.

    Returns:
        A coordenada.
    """
    celula = coordenada(texto)
    if celula is None:
        pytest.fail(f'célula "{texto}" não é x,y')
    return celula


@given(
    parsers.parse(
        'o labirinto de teste com a grade "{grade:Q}", entrada '
        '"{entrada:Q}" e saída "{saida:Q}"',
        extra_types=TIPOS,
    )
)
def labirinto_de_teste_com_grade(
    estado: Estado, grade: str, entrada: str, saida: str
) -> None:
    """Grava o arquivo de saída de uma grade dada à mão.

    Args:
        estado: Estado do cenário.
        grade: Linhas hexadecimais separadas por " / ".
        entrada: Coordenada "x,y" da entrada.
        saida: Coordenada "x,y" da saída.
    """
    try:
        texto = texto_do_arquivo(grade.split(" / "), entrada, saida)
    except ValueError as erro:
        pytest.fail(f'a grade "{grade}" não serve de labirinto: {erro}')
    gravar_labirinto_de_teste(estado, texto)


@given(
    parsers.parse('o labirinto de teste "{modelo:Q}"', extra_types=TIPOS)
)
def labirinto_de_teste_modelo(estado: Estado, modelo: str) -> None:
    """Grava um dos modelos de ``tests/fixtures/`` como arquivo atual.

    Args:
        estado: Estado do cenário.
        modelo: Nome da lista fechada de V23.
    """
    arquivo = MODELOS.get(modelo)
    if arquivo is None:
        pytest.fail(
            f'modelo "{modelo}" não existe; os válidos são: '
            f"{', '.join(MODELOS)}"
        )
    with (FIXTURES / arquivo).open(encoding="utf-8", newline="") as fonte:
        gravar_labirinto_de_teste(estado, fonte.read())


@given(
    parsers.parse('a célula de dígito "{digito:Q}"', extra_types=TIPOS)
)
def celula_de_digito(estado: Estado, digito: str) -> None:
    """Guarda a célula dada por um dígito hexadecimal.

    Args:
        estado: Estado do cenário.
        digito: Um dígito de 0 a F, em qualquer caixa.
    """
    if len(digito) != 1 or digito not in "0123456789abcdefABCDEF":
        pytest.fail(f'"{digito}" não é um dígito hexadecimal')
    estado.celula = int(digito, 16)


@given(
    parsers.parse(
        'a célula com as paredes fechadas "{paredes:Q}"', extra_types=TIPOS
    )
)
def celula_com_paredes(estado: Estado, paredes: str) -> None:
    """Guarda a célula dada pelas paredes fechadas.

    Args:
        estado: Estado do cenário.
        paredes: "nenhuma" ou direções como "Norte e Sul".
    """
    try:
        estado.celula = paredes_em_bits(paredes)
    except ValueError as erro:
        pytest.fail(str(erro))


@when("o validador da suíte lê o labirinto")
def validador_le_o_labirinto(estado: Estado) -> None:
    """Lê o labirinto atual; numa sessão, relê o OUTPUT_FILE regravado.

    Args:
        estado: Estado do cenário.
    """
    if estado.em_sessao() is not None:
        saida = estado.saida_da_sessao()
        texto = Estado.ler_saida_de(saida)
        if saida is None or texto is None:
            pytest.fail(
                f"a sessão não deixou arquivo de saída legível: {saida}"
            )
        try:
            labirinto = ler_saida(texto)
        except ValueError as erro:
            pytest.fail(f"o arquivo {saida} não se lê como labirinto: {erro}")
        labirinto.arquivo = saida
        estado.labirintos.append(labirinto)
        return
    if estado.labirintos or estado.execucoes:
        todos_os_labirintos(estado)
        return
    if estado.resultados and estado.resultado.conteudo_saida is not None:
        try:
            ler_saida(estado.resultado.conteudo_saida)
        except ValueError as erro:
            pytest.fail(
                f"o arquivo {estado.resultado.arquivo_saida} não se lê como "
                f"labirinto: {erro}"
            )
    todos_os_labirintos(estado)


@when("o validador da suíte converte a célula")
def validador_converte_a_celula(estado: Estado) -> None:
    """Converte o valor em paredes e de volta, exigindo o mesmo valor.

    Args:
        estado: Estado do cenário.
    """
    valor = celula_do_cenario(estado)
    if not 0 <= valor <= FECHADA:
        pytest.fail(f"a célula vale {valor}, fora de 0 a 15")
    paredes = bits_em_paredes(valor)
    if paredes_em_bits(paredes) != valor:
        pytest.fail(f"o valor {valor} vira {paredes!r} e não volta")


@then(
    parsers.parse(
        "a grade do labirinto tem {largura:d} colunas e {altura:d} linhas"
    )
)
def grade_tem_dimensoes(estado: Estado, largura: int, altura: int) -> None:
    """Confere as dimensões de cada labirinto do cenário.

    Args:
        estado: Estado do cenário.
        largura: Colunas esperadas.
        altura: Linhas esperadas.
    """
    falhar_por_labirinto(
        estado,
        lambda lab: [] if (lab.largura, lab.altura) == (largura, altura)
        else [f"a grade tem {lab.largura} colunas e {lab.altura} linhas"],
        f"{largura} colunas e {altura} linhas",
    )


@then(
    parsers.parse(
        'a linha {n:d} do rodapé é "{texto:Q}"', extra_types=TIPOS
    )
)
def linha_do_rodape(estado: Estado, n: int, texto: str) -> None:
    """Confere uma das 3 linhas do rodapé de cada labirinto.

    Args:
        estado: Estado do cenário.
        n: Número da linha, de 1 a 3.
        texto: Conteúdo esperado, exato.
    """
    if not 1 <= n <= 3:
        pytest.fail(f"o rodapé tem as linhas 1 a 3, não a {n}")

    def conferir(labirinto: Labirinto) -> list[str]:
        """Compara a linha n do rodapé.

        Args:
            labirinto: Labirinto conferido.

        Returns:
            A violação, se houver.
        """
        if labirinto.texto is None:
            return ["o labirinto veio de generate(), sem rodapé"]
        if len(labirinto.rodape) < n:
            return [f"o rodapé só tem {labirinto.rodape!r}"]
        if labirinto.rodape[n - 1] != texto:
            return [f"a linha {n} do rodapé é {labirinto.rodape[n - 1]!r}"]
        return []

    falhar_por_labirinto(estado, conferir, f"a linha {n} {texto!r}")


@then("o arquivo de saída é idêntico byte a byte ao gerado com o config base")
def identico_ao_config_base(estado: Estado) -> None:
    """Compara o arquivo do labirinto atual com o gerado pelo config base.

    O arquivo atual é lido antes da nova geração, que pode regravar o mesmo
    caminho; o config base vai para um destino próprio.

    Args:
        estado: Estado do cenário.
    """
    atual = (estado.labirintos or todos_os_labirintos(estado))[-1]
    execucao = next(
        (
            execucao
            for execucao in reversed([*estado.resultados, *estado.execucoes])
            if execucao.labirinto is atual
        ),
        None,
    )
    if execucao is None or execucao.arquivo_saida is None:
        pytest.fail("o labirinto atual não veio de um arquivo de saída")
    arquivo: Path = execucao.arquivo_saida
    antes = arquivo.read_bytes()
    original = estado.config
    estado.config = Config(list(CONFIG_BASE), CONFIG_DE_REFERENCIA)
    try:
        referencia = gerar_pelo_programa(estado)
    finally:
        estado.config = original
    if referencia.codigo != 0 or referencia.arquivo_saida is None:
        pytest.fail(
            f"o config base não gerou labirinto (código {referencia.codigo})"
            f":\n{referencia.saida_erro}"
        )
    depois = referencia.arquivo_saida.read_bytes()
    if antes != depois:
        pytest.fail(
            f"{arquivo} difere do gerado com o config base:\n"
            f"{antes!r}\n!=\n{depois!r}"
        )


@then(
    parsers.parse(
        'o validador da suíte relata "{relato:Q}" em '
        '"{verificacao:Q}"',
        extra_types=TIPOS,
    )
)
def validador_relata(
    estado: Estado, relato: str, verificacao: str
) -> None:
    """Compara o relato do validador numa verificação.

    Args:
        estado: Estado do cenário.
        relato: Texto que o validador deveria devolver.
        verificacao: Nome da lista fechada de V73.
    """
    if verificacao not in RELATOS:
        pytest.fail(
            f'verificação "{verificacao}" não existe; as válidas são: '
            f"{', '.join(RELATOS)}"
        )
    falhar_por_labirinto(
        estado,
        lambda lab: [] if relatar(lab, verificacao) == relato
        else [f"o validador relata {relatar(lab, verificacao)!r}"],
        f"o relato {relato!r} em {verificacao!r}",
    )


@then(
    parsers.parse(
        'o validador da suíte conta {n:d} "{item:Q}"', extra_types=TIPOS
    )
)
def validador_conta(estado: Estado, n: int, item: str) -> None:
    """Conta um item em cada labirinto.

    Args:
        estado: Estado do cenário.
        n: Quantidade esperada.
        item: Nome da lista fechada de V74.
    """
    if item not in CONTAGENS:
        pytest.fail(
            f'item "{item}" não existe; os válidos são: '
            f"{', '.join(CONTAGENS)}"
        )
    falhar_por_labirinto(
        estado,
        lambda lab: [] if contagem(lab, item) == n
        else [f"o validador conta {contagem(lab, item)}"],
        f"{n} {item!r}",
    )


def _sem_valor_f(labirinto: Labirinto, celula: Celula) -> list[str]:
    """A célula não é F.

    Args:
        labirinto: Labirinto conferido.
        celula: Célula dentro da grade.

    Returns:
        A violação, se houver.
    """
    if labirinto.valor(celula) == FECHADA:
        return [f"a célula {xy(celula)} tem valor F"]
    return []


def _alcancavel(labirinto: Labirinto, celula: Celula) -> list[str]:
    """A célula está na região da entrada.

    Args:
        labirinto: Labirinto conferido.
        celula: Célula dentro da grade.

    Returns:
        A violação, se houver.
    """
    if celula not in regiao(labirinto):
        return [
            f"a célula {xy(celula)} não é alcançável a partir da entrada "
            f"{labirinto.entrada}"
        ]
    return []


def _externas_fechadas(labirinto: Labirinto, celula: Celula) -> list[str]:
    """As paredes da célula voltadas para fora da grade estão fechadas.

    Args:
        labirinto: Labirinto conferido.
        celula: Célula dentro da grade.

    Returns:
        A violação, se houver.
    """
    externas = [
        direcao for direcao, (dx, dy) in DESLOCAMENTOS.items()
        if not labirinto.dentro((celula[0] + dx, celula[1] + dy))
    ]
    if not externas:
        return [f"a célula {xy(celula)} não fica na borda"]
    return [
        f"a célula {xy(celula)} tem a parede externa {NOMES[direcao]} aberta"
        for direcao in externas
        if labirinto.aberta(celula, direcao)
    ]


SITUACOES_DA_CELULA: dict[str, Callable[[Labirinto, Celula], list[str]]] = {
    "não tem valor F": _sem_valor_f,
    "é alcançável a partir da entrada": _alcancavel,
    "tem as paredes externas fechadas": _externas_fechadas,
}


@then(
    parsers.parse(
        'a célula "{celula:Q}" {situacao:EstadoCelula}', extra_types=TIPOS
    )
)
def celula_na_situacao(estado: Estado, celula: str, situacao: str) -> None:
    """Confere uma célula "x,y" em cada labirinto.

    Args:
        estado: Estado do cenário.
        celula: Coordenada "x,y".
        situacao: Valor da lista fechada EstadoCelula.
    """
    conferir = SITUACOES_DA_CELULA.get(situacao)
    if conferir is None:
        pytest.fail(
            f'situação "{situacao}" não existe; as válidas são: '
            f"{', '.join(SITUACOES_DA_CELULA)}"
        )
    alvo = celula_dada(celula)
    falhar_por_labirinto(
        estado,
        lambda lab: conferir(lab, alvo) if lab.dentro(alvo)
        else [f"a célula {xy(alvo)} fica fora da grade"],
        f"a célula {celula} {situacao}",
    )


@then(
    parsers.parse(
        "pelo menos uma das células {celulas:L} é alcançável a partir da "
        "entrada",
        extra_types=TIPOS,
    )
)
def alguma_alcancavel(estado: Estado, celulas: list[str]) -> None:
    """Exige, em cada labirinto, uma das células alcançável e sem F.

    Args:
        estado: Estado do cenário.
        celulas: Coordenadas "x,y".
    """
    alvos = [celula_dada(celula) for celula in celulas]

    def conferir(labirinto: Labirinto) -> list[str]:
        """Procura uma célula alcançável e sem F.

        Args:
            labirinto: Labirinto conferido.

        Returns:
            A violação, se nenhuma serve.
        """
        alcancadas = regiao(labirinto)
        if any(
            labirinto.dentro(alvo)
            and labirinto.valor(alvo) != FECHADA
            and alvo in alcancadas
            for alvo in alvos
        ):
            return []
        return ["nenhuma delas é corredor alcançável"]

    falhar_por_labirinto(
        estado, conferir, f"uma de {', '.join(celulas)} alcançável"
    )


@then(
    parsers.parse(
        'todas as células da "{borda:Q}" têm a parede "{direcao:Q}" fechada',
        extra_types=TIPOS,
    )
)
def borda_com_parede(estado: Estado, borda: str, direcao: str) -> None:
    """Percorre uma borda e confere a parede pedida.

    Args:
        estado: Estado do cenário.
        borda: Nome da lista fechada de V77.
        direcao: "Norte", "Leste", "Sul" ou "Oeste".
    """
    celulas_da = BORDAS.get(borda)
    if celulas_da is None:
        pytest.fail(
            f'borda "{borda}" não existe; as válidas são: '
            f"{', '.join(BORDAS)}"
        )
    letra = DIRECAO_POR_NOME.get(direcao)
    if letra is None:
        pytest.fail(
            f'direção "{direcao}" não existe; as válidas são: '
            f"{', '.join(DIRECAO_POR_NOME)}"
        )
    falhar_por_labirinto(
        estado,
        lambda lab: [
            f"a célula {xy(celula)} tem a parede {direcao} aberta"
            for celula in celulas_da(lab)
            if lab.aberta(celula, letra)
        ],
        f"a parede {direcao} fechada em toda a {borda}",
    )


@then(
    parsers.parse(
        'as células de valor F ocupam as colunas "{colunas:Q}" e as linhas '
        '"{linhas:Q}"',
        extra_types=TIPOS,
    )
)
def celulas_f_ocupam(estado: Estado, colunas: str, linhas: str) -> None:
    """Confere as colunas e as linhas onde há células F.

    Args:
        estado: Estado do cenário.
        colunas: Intervalos como "6 a 8 e 10 a 12".
        linhas: Intervalos como "5 a 9".
    """
    try:
        xs, ys = intervalos(colunas), intervalos(linhas)
    except ValueError as erro:
        pytest.fail(str(erro))

    def conferir(labirinto: Labirinto) -> list[str]:
        """Compara as colunas e as linhas das células F.

        Args:
            labirinto: Labirinto conferido.

        Returns:
            As violações.
        """
        celulas = celulas_f(labirinto)
        achadas_x = {x for x, _ in celulas}
        achadas_y = {y for _, y in celulas}
        problemas: list[str] = []
        if achadas_x != xs:
            problemas.append(
                f"as células F estão nas colunas {sorted(achadas_x)}"
            )
        if achadas_y != ys:
            problemas.append(
                f"as células F estão nas linhas {sorted(achadas_y)}"
            )
        return problemas

    falhar_por_labirinto(
        estado,
        conferir,
        f"células F nas colunas {sorted(xs)} e nas linhas {sorted(ys)}",
    )


@then(
    parsers.parse('o dígito da célula é "{digito:Q}"', extra_types=TIPOS)
)
def digito_da_celula(estado: Estado, digito: str) -> None:
    """Compara o dígito hexadecimal da célula, sem diferenciar caixa.

    Args:
        estado: Estado do cenário.
        digito: Dígito esperado.
    """
    valor = celula_do_cenario(estado)
    if format(valor, "x") != digito.lower():
        pytest.fail(f"a célula tem o dígito {valor:x}, não {digito}")


@then(
    parsers.parse(
        'as paredes {situacao:FA} da célula são "{paredes:Q}"',
        extra_types=TIPOS,
    )
)
def paredes_da_celula(estado: Estado, situacao: str, paredes: str) -> None:
    """Compara as paredes fechadas ou abertas da célula.

    Args:
        estado: Estado do cenário.
        situacao: "fechadas" ou "abertas".
        paredes: "nenhuma" ou direções como "Norte e Sul".
    """
    valor = celula_do_cenario(estado)
    try:
        esperado = paredes_em_bits(paredes)
    except ValueError as erro:
        pytest.fail(str(erro))
    fechadas = situacao == "fechadas"
    achado = valor if fechadas else FECHADA - valor
    if achado != esperado:
        pytest.fail(
            f"as paredes {situacao} da célula {valor:x} são "
            f"{bits_em_paredes(valor, fechadas)!r}, não {paredes!r}"
        )


@then(parsers.parse("a célula tem {n:d} paredes fechadas"))
def celula_tem_paredes(estado: Estado, n: int) -> None:
    """Conta as paredes fechadas da célula.

    Args:
        estado: Estado do cenário.
        n: Quantidade esperada.
    """
    valor = celula_do_cenario(estado)
    fechadas = sum(1 for bit in DIRECOES.values() if valor & bit)
    if fechadas != n:
        pytest.fail(f"a célula {valor:x} tem {fechadas} paredes fechadas")


@then(parsers.parse("o bit {bit:d} da célula está ligado"))
def bit_ligado(estado: Estado, bit: int) -> None:
    """Confere um bit da célula, de 0 (Norte) a 3 (Oeste).

    Args:
        estado: Estado do cenário.
        bit: Posição do bit.
    """
    valor = celula_do_cenario(estado)
    if not 0 <= bit <= 3:
        pytest.fail(f"a célula tem os bits 0 a 3, não o {bit}")
    if not valor >> bit & 1:
        pytest.fail(f"o bit {bit} da célula {valor:04b} está desligado")


@then('o validador da suíte confirma "valores de 0 a 15"')
def confirma_valores(estado: Estado) -> None:
    """Todo valor da grade vai de 0 a 15.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "valores de 0 a 15")


@then('o validador da suíte confirma "bits na convenção N=1, E=2, S=4, W=8"')
def confirma_convencao(estado: Estado) -> None:
    """Lida com N=1, E=2, S=4, W=8, a grade fecha a borda e é coerente.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "bits na convenção N=1, E=2, S=4, W=8")


@then('o validador da suíte confirma "x é a coluna e y é a linha"')
def confirma_x_coluna(estado: Estado) -> None:
    """Colunas = WIDTH, linhas = HEIGHT e a solução lê x como coluna.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "x é a coluna e y é a linha")


@then('o validador da suíte confirma "entrada e saída válidas"')
def confirma_entrada_e_saida(estado: Estado) -> None:
    """Entrada e saída na grade, fora do F, ligadas e iguais ao config.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "entrada e saída válidas")


@then('o validador da suíte confirma "entrada diferente da saída"')
def confirma_entrada_diferente(estado: Estado) -> None:
    """Entrada e saída são células diferentes.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "entrada diferente da saída")


@then(
    'o validador da suíte confirma "x de entrada e saída dentro da largura"'
)
def confirma_x_na_largura(estado: Estado) -> None:
    """O x da entrada e da saída fica dentro da largura.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "x de entrada e saída dentro da largura")


@then('o validador da suíte confirma "y de entrada e saída dentro da altura"')
def confirma_y_na_altura(estado: Estado) -> None:
    """O y da entrada e da saída fica dentro da altura.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "y de entrada e saída dentro da altura")


@then('o validador da suíte confirma "toda célula fora do 42 alcançável"')
def confirma_conectividade(estado: Estado) -> None:
    """Toda célula fora do "42" é alcançável a partir da entrada.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "toda célula fora do 42 alcançável")


@then('o validador da suíte confirma "borda fechada"')
def confirma_borda(estado: Estado) -> None:
    """Toda parede voltada para fora da grade está fechada.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "borda fechada")


@then('o validador da suíte confirma "paredes coerentes"')
def confirma_coerencia(estado: Estado) -> None:
    """Toda parede compartilhada é codificada igual pelas duas células.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "paredes coerentes")


@then('o validador da suíte confirma "vizinhas leste-oeste coerentes"')
def confirma_leste_oeste(estado: Estado) -> None:
    """O bit E de (x, y) é igual ao bit W de (x+1, y).

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "vizinhas leste-oeste coerentes")


@then('o validador da suíte confirma "vizinhas norte-sul coerentes"')
def confirma_norte_sul(estado: Estado) -> None:
    """O bit S de (x, y) é igual ao bit N de (x, y+1).

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "vizinhas norte-sul coerentes")


@then('o validador da suíte confirma "inalcançáveis são as células do 42"')
def confirma_inalcancaveis(estado: Estado) -> None:
    """As células que a entrada não alcança são exatamente as do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "inalcançáveis são as células do 42")


@then(
    'o validador da suíte confirma "células F em dois componentes 4-conexos"'
)
def confirma_dois_componentes(estado: Estado) -> None:
    """As células F formam dois componentes 4-conexos.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "células F em dois componentes 4-conexos")


@then(
    'o validador da suíte confirma "componente da esquerda com a forma do 4"'
)
def confirma_forma_do_4(estado: Estado) -> None:
    """O componente F da esquerda desenha o 4.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "componente da esquerda com a forma do 4")


@then(
    'o validador da suíte confirma "componente da direita com a forma do 2"'
)
def confirma_forma_do_2(estado: Estado) -> None:
    """O componente F da direita desenha o 2.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "componente da direita com a forma do 2")


@then('o validador da suíte confirma "células F iguais ao padrão 42"')
def confirma_f_igual_ao_padrao(estado: Estado) -> None:
    """As células F são exatamente as do "42" da D07.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "células F iguais ao padrão 42")


@then('o validador da suíte confirma "nenhuma célula F fora do padrão"')
def confirma_nenhuma_f_fora(estado: Estado) -> None:
    """Nenhuma célula F fica fora do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "nenhuma célula F fora do padrão")


@then('o validador da suíte confirma "42 sem passagem aberta"')
def confirma_42_fechado(estado: Estado) -> None:
    """Nenhuma passagem entra nas células do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "42 sem passagem aberta")


@then(
    'o validador da suíte confirma "glifos 3x5 com uma coluna livre entre os '
    'dígitos"'
)
def confirma_glifos(estado: Estado) -> None:
    """As células F desenham o 4 e o 2 3x5 com uma coluna livre no meio.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "glifos 3x5 com uma coluna livre entre os dígitos")


@then(
    parsers.parse(
        'o validador da suíte confirma "42 {presenca:Presenca}"',
        extra_types=TIPOS,
    )
)
def confirma_presenca_do_42(estado: Estado, presenca: str) -> None:
    """O "42" está desenhado ("presente") ou não há célula F ("ausente").

    Args:
        estado: Estado do cenário.
        presenca: "presente" ou "ausente".
    """
    confirmar(estado, f"42 {presenca}")


@then('o validador da suíte confirma "42 com margem de corredor"')
def confirma_margem(estado: Estado) -> None:
    """Há um anel de corredores alcançáveis em volta do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "42 com margem de corredor")


@then('o validador da suíte confirma "42 fora dos cantos"')
def confirma_42_fora_dos_cantos(estado: Estado) -> None:
    """Nenhum canto é célula do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "42 fora dos cantos")


@then('o validador da suíte confirma "centro livre do 42"')
def confirma_centro_livre(estado: Estado) -> None:
    """Uma célula do centro (D08) é corredor alcançável fora do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "centro livre do 42")


@then('o validador da suíte confirma "árvore geradora fora do 42"')
def confirma_arvore(estado: Estado) -> None:
    """As células fora do "42" formam uma árvore geradora.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "árvore geradora fora do 42")


@then('o validador da suíte confirma "caminho único entre entrada e saída"')
def confirma_caminho_unico(estado: Estado) -> None:
    """Há um único caminho simples entre a entrada e a saída.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "caminho único entre entrada e saída")


@then(
    'o validador da suíte confirma "ramos fora da solução terminam em beco"'
)
def confirma_ramos(estado: Estado) -> None:
    """Todo corredor que sai da solução acaba num beco sem saída.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "ramos fora da solução terminam em beco")


@then('o validador da suíte confirma "solução atravessa só paredes abertas"')
def confirma_solucao_por_passagens(estado: Estado) -> None:
    """Cada passo da solução passa por uma parede aberta.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução atravessa só paredes abertas")


@then('o validador da suíte confirma "solução não sai da grade"')
def confirma_solucao_na_grade(estado: Estado) -> None:
    """Nenhum passo da solução sai da grade.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução não sai da grade")


@then('o validador da suíte confirma "solução não entra no 42"')
def confirma_solucao_fora_do_42(estado: Estado) -> None:
    """A solução não visita célula do "42".

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução não entra no 42")


@then('o validador da suíte confirma "solução termina na saída"')
def confirma_solucao_na_saida(estado: Estado) -> None:
    """A solução para na saída.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução termina na saída")


@then('o validador da suíte confirma "solução mais curta"')
def confirma_solucao_curta(estado: Estado) -> None:
    """A solução tem o comprimento da busca em largura.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução mais curta")


@then('o validador da suíte confirma "solução sem célula repetida"')
def confirma_solucao_sem_repeticao(estado: Estado) -> None:
    """A solução não visita a mesma célula duas vezes.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução sem célula repetida")


@then('o validador da suíte confirma "solução válida e mais curta"')
def confirma_solucao_valida(estado: Estado) -> None:
    """A solução é válida passo a passo e tem o comprimento mínimo.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "solução válida e mais curta")


@then('o validador da suíte confirma "pelo menos 2 rotas independentes"')
def confirma_rotas(estado: Estado) -> None:
    """A região alcançável tem pelo menos 2 ciclos independentes.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "pelo menos 2 rotas independentes")


@then('o validador da suíte confirma "no máximo 2 becos reais"')
def confirma_poucos_becos(estado: Estado) -> None:
    """Há no máximo 2 becos reais.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "no máximo 2 becos reais")


@then('o validador da suíte confirma "zero becos reais"')
def confirma_zero_becos(estado: Estado) -> None:
    """Não há beco real.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "zero becos reais")


@then('o validador da suíte confirma "sem área aberta 3x3"')
def confirma_sem_3x3(estado: Estado) -> None:
    """Nenhum bloco 3x3 tem as 12 paredes internas abertas.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "sem área aberta 3x3")


@then(
    'o validador da suíte confirma "blocos 2x2, 2x3 e 3x2 abertos aceitos"'
)
def confirma_blocos_aceitos(estado: Estado) -> None:
    """O validador aceita as áreas abertas e há um bloco 2x2 aberto.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "blocos 2x2, 2x3 e 3x2 abertos aceitos")


@then('o validador da suíte confirma "modo igual ao PERFECT do config"')
def confirma_modo(estado: Estado) -> None:
    """O labirinto é perfeito ou Pac-Man conforme o PERFECT do config.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "modo igual ao PERFECT do config")


@then(
    'o validador da suíte confirma "rodapé com ENTRY, EXIT e caminho válido"'
)
def confirma_rodape(estado: Estado) -> None:
    """O rodapé traz ENTRY, EXIT e uma solução válida e mais curta.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "rodapé com ENTRY, EXIT e caminho válido")


@then('o validador da suíte confirma "labirinto válido conforme o config"')
def confirma_valido(estado: Estado) -> None:
    """O labirinto cumpre todas as regras do config.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "labirinto válido conforme o config")


@then('o validador da suíte confirma "uma linha vazia logo após a grade"')
def confirma_linha_vazia(estado: Estado) -> None:
    """A linha seguinte à grade é vazia.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "uma linha vazia logo após a grade")


@then(
    'o validador da suíte confirma "exatamente 3 linhas após a linha vazia"'
)
def confirma_tres_linhas(estado: Estado) -> None:
    """Depois da linha vazia há exatamente 3 linhas.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "exatamente 3 linhas após a linha vazia")


@then('o validador da suíte confirma "arquivo termina com quebra de linha"')
def confirma_quebra_final(estado: Estado) -> None:
    """O arquivo termina com quebra de linha.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "arquivo termina com quebra de linha")


@then(
    'o validador da suíte confirma "linha vazia contém só a quebra de linha"'
)
def confirma_vazia_pura(estado: Estado) -> None:
    """A linha vazia tem só a quebra de linha.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "linha vazia contém só a quebra de linha")


@then('o validador da suíte confirma "nenhuma linha com espaço no fim"')
def confirma_sem_espaco(estado: Estado) -> None:
    """Nenhuma linha do arquivo termina com espaço.

    Args:
        estado: Estado do cenário.
    """
    confirmar(estado, "nenhuma linha com espaço no fim")
