"""Passos que conferem a renderização do labirinto no terminal."""

import pytest
from pytest_bdd import parsers, then

from suporte.config import chaves_das_linhas
from suporte.estado import Estado
from suporte.labirinto import Celula, Labirinto, ler_saida
from suporte.render import (
    CIANO,
    CORES,
    Cor,
    ELEMENTOS,
    ESCAPE,
    RESET,
    SEQUENCIA,
    Posicao,
    Renderizacao,
    Tela,
    caminho_marcado,
    conferir_rodizio,
    cor_das_paredes,
    da_celula,
    dimensoes,
    direcoes,
    distancia,
    grade_desenhada,
    nome_da_cor,
    nomes_das_direcoes,
    onde,
    paredes_desenhadas,
    posicoes_da_cor,
    posicoes_de,
    problemas_de_sgr,
    renderizacoes,
    seguida_do_menu,
    tela,
)
from suporte.tipos import TIPOS

ANSI = "\x1b["
AMOSTRA = 5


def tamanho_do_config(estado: Estado) -> tuple[int, int]:
    """WIDTH e HEIGHT do config do cenário.

    Args:
        estado: Estado do cenário.

    Returns:
        (largura, altura).
    """
    if estado.config is None:
        pytest.fail("o cenário não tem config para dar WIDTH e HEIGHT")
    chaves = chaves_das_linhas(estado.config.linhas)
    try:
        return int(chaves["WIDTH"]), int(chaves["HEIGHT"])
    except (KeyError, ValueError):
        pytest.fail(
            f"o config não tem WIDTH e HEIGHT inteiros: {estado.config.linhas}"
        )


def desenhos(estado: Estado) -> list[Renderizacao]:
    """Renderizações da saída padrão do último comando ou da sessão.

    Args:
        estado: Estado do cenário.

    Returns:
        Os blocos de 2 × HEIGHT + 1 linhas, pelo menos um.
    """
    _, altura = tamanho_do_config(estado)
    saida = estado.resultado.saida_padrao
    blocos = renderizacoes(saida, altura)
    if not blocos:
        pytest.fail(f"a saída padrão não tem nenhuma renderização:\n{saida}")
    return blocos


def tela_de(renderizacao: Renderizacao, numero: int) -> Tela:
    """Fundos das posições de uma renderização, ou a falha do passo.

    Args:
        renderizacao: Bloco desenhado.
        numero: Índice do bloco na saída, a partir de 0, para a mensagem.

    Returns:
        Os fundos, numa grade de 2n + 1 por 2m + 1 posições.
    """
    try:
        desenho = tela(renderizacao)
        dimensoes(desenho)
    except ValueError as erro:
        pytest.fail(f"renderização {numero}: {erro}")
    return desenho


def telas(estado: Estado) -> list[Tela]:
    """Fundos das posições de todas as renderizações.

    Args:
        estado: Estado do cenário.

    Returns:
        Uma grade de fundos por renderização, na ordem.
    """
    return [
        tela_de(bloco, numero)
        for numero, bloco in enumerate(desenhos(estado))
    ]


def ultima_tela(estado: Estado) -> Tela:
    """Fundos das posições da última renderização.

    Args:
        estado: Estado do cenário.

    Returns:
        A grade de fundos.
    """
    blocos = desenhos(estado)
    return tela_de(blocos[-1], len(blocos) - 1)


def labirinto_atual(estado: Estado) -> Labirinto:
    """Labirinto do OUTPUT_FILE atual do último comando ou da sessão.

    Args:
        estado: Estado do cenário.

    Returns:
        O labirinto lido do arquivo.
    """
    resultado = estado.resultado
    if resultado.conteudo_saida is None:
        pytest.fail(
            f"o arquivo de saída {resultado.arquivo_saida} de "
            f"'{resultado.comando}' não existe ou não se lê"
        )
    try:
        return ler_saida(resultado.conteudo_saida)
    except ValueError as erro:
        pytest.fail(f"o arquivo {resultado.arquivo_saida} não se lê: {erro}")


def tela_e_labirinto(estado: Estado) -> tuple[Tela, Labirinto]:
    """Última renderização e o labirinto do arquivo, do mesmo tamanho.

    Args:
        estado: Estado do cenário.

    Returns:
        (fundos da última renderização, labirinto do arquivo).
    """
    desenho = ultima_tela(estado)
    labirinto = labirinto_atual(estado)
    tamanho = dimensoes(desenho)
    if tamanho != (labirinto.largura, labirinto.altura):
        pytest.fail(
            f"a última renderização tem {tamanho[0]}x{tamanho[1]} células e "
            f"o arquivo de saída {labirinto.largura}x{labirinto.altura}"
        )
    return desenho, labirinto


def codigo_da_cor(cor: str) -> int:
    """Código SGR da cor nomeada no passo (I21).

    Args:
        cor: Nome da cor.

    Returns:
        O código do fundo.
    """
    if cor not in CORES:
        pytest.fail(f'"{cor}" não existe; os válidos são: {", ".join(CORES)}')
    return CORES[cor]


def posicoes_do_elemento(labirinto: Labirinto, nome: str) -> set[Posicao]:
    """Posições do elemento nomeado no passo, pelo menos uma.

    Args:
        labirinto: Labirinto do arquivo de saída.
        nome: Um dos ELEMENTOS.

    Returns:
        As posições do elemento no desenho.
    """
    try:
        posicoes = posicoes_de(labirinto, nome)
    except ValueError as erro:
        pytest.fail(str(erro))
    if not posicoes:
        pytest.fail(f'o labirinto do arquivo não tem "{nome}"')
    return posicoes


def descrever(desenho: Tela, posicoes: set[Posicao]) -> str:
    """Amostra de posições com a cor de cada uma, para as mensagens.

    Args:
        desenho: Fundos das posições.
        posicoes: Posições a descrever.

    Returns:
        Até AMOSTRA posições como "linha l, coluna c: cor".
    """
    amostra = sorted(posicoes)[:AMOSTRA]
    return "; ".join(
        f"{onde(posicao)}: {nome_da_cor(desenho[posicao[0]][posicao[1]])}"
        for posicao in amostra
    )


def marcado(estado: Estado) -> tuple[list[Celula], Labirinto]:
    """Caminho ciano da última renderização e o labirinto do arquivo.

    Args:
        estado: Estado do cenário.

    Returns:
        (células do caminho marcado, labirinto do arquivo).
    """
    desenho, labirinto = tela_e_labirinto(estado)
    if labirinto.entrada is None or labirinto.saida is None:
        pytest.fail(f"o rodapé não tem entrada e saída: {labirinto.rodape}")
    try:
        caminho = caminho_marcado(desenho, labirinto.entrada, labirinto.saida)
    except ValueError as erro:
        pytest.fail(f"na última renderização, {erro}")
    return caminho, labirinto


@then('a renderização confirma "cada linha termina com o reset ANSI"')
def linhas_com_reset(estado: Estado) -> None:
    """Toda linha colorida da saída padrão termina com o reset ANSI (I02).

    Sem nenhuma linha colorida não houve renderização, e o teste falha.

    Args:
        estado: Estado do cenário.
    """
    coloridas = [
        linha for linha in estado.resultado.saida_padrao.splitlines()
        if ANSI in linha
    ]
    if not coloridas:
        pytest.fail("a saída padrão não tem nenhuma linha renderizada")
    sem_reset = [
        numero for numero, linha in enumerate(coloridas, start=1)
        if not linha.endswith(RESET)
    ]
    if sem_reset:
        pytest.fail(
            f"{len(sem_reset)} de {len(coloridas)} linhas renderizadas sem "
            f"o reset no fim (primeira: {coloridas[sem_reset[0] - 1]!r})"
        )


@then('a renderização confirma "cada renderização seguida do menu"')
def seguidas_do_menu(estado: Estado) -> None:
    """Depois de cada renderização vêm as linhas do menu e o prompt (I03).

    Args:
        estado: Estado do cenário.
    """
    blocos = desenhos(estado)
    sem_menu = [
        numero for numero, bloco in enumerate(blocos)
        if not seguida_do_menu(bloco)
    ]
    if sem_menu:
        primeiro = blocos[sem_menu[0]]
        pytest.fail(
            f"{len(sem_menu)} de {len(blocos)} renderizações sem o menu logo "
            f"depois; a {sem_menu[0]} é seguida de {primeiro.seguinte[:6]!r}"
        )


@then(
    'a renderização confirma "nova renderização abaixo da anterior, seguida '
    'do menu"'
)
def nova_abaixo_da_anterior(estado: Estado) -> None:
    """A ação desenhou outra renderização depois do menu da anterior.

    O desenho anterior continua na saída: nenhuma sequência limpa a tela
    ou move o cursor (I02).

    Args:
        estado: Estado do cenário.
    """
    blocos = desenhos(estado)
    if len(blocos) < 2:
        pytest.fail(f"a saída tem {len(blocos)} renderização; esperadas 2")
    for numero in (len(blocos) - 2, len(blocos) - 1):
        if not seguida_do_menu(blocos[numero]):
            pytest.fail(
                f"a renderização {numero} não é seguida do menu: "
                f"{blocos[numero].seguinte[:6]!r}"
            )
    controles = [
        sequencia
        for sequencia in SEQUENCIA.findall(estado.resultado.saida_padrao)
        if not sequencia.endswith("m")
    ]
    if controles:
        pytest.fail(
            f"a saída tem sequências que limpam a tela ou movem o cursor: "
            f"{sorted(set(controles))}"
        )


@then('a renderização confirma "2 × HEIGHT + 1 linhas"')
def linhas_da_altura(estado: Estado) -> None:
    """Cada renderização tem 2 × HEIGHT + 1 linhas desenhadas.

    Args:
        estado: Estado do cenário.
    """
    _, altura = tamanho_do_config(estado)
    tamanhos = [len(bloco.linhas) for bloco in desenhos(estado)]
    errados = [tamanho for tamanho in tamanhos if tamanho != 2 * altura + 1]
    if errados:
        pytest.fail(
            f"renderizações com {tamanhos} linhas; com HEIGHT={altura}, "
            f"esperadas {2 * altura + 1} cada"
        )


@then(
    'a renderização confirma "2 × WIDTH + 1 posições de 2 caracteres por '
    'linha"'
)
def posicoes_da_largura(estado: Estado) -> None:
    """Cada linha desenhada tem 2 × WIDTH + 1 posições de 2 caracteres.

    Args:
        estado: Estado do cenário.
    """
    largura, _ = tamanho_do_config(estado)
    esperadas = 2 * largura + 1
    for numero, bloco in enumerate(desenhos(estado)):
        try:
            desenho = tela(bloco)
        except ValueError as erro:
            pytest.fail(f"renderização {numero}: {erro}")
        for linha, posicoes in enumerate(desenho):
            if len(posicoes) != esperadas:
                pytest.fail(
                    f"a linha {linha} da renderização {numero} tem "
                    f"{len(posicoes)} posições; com WIDTH={largura}, "
                    f"esperadas {esperadas}: {bloco.linhas[linha]!r}"
                )


@then('a renderização confirma "só caracteres ASCII"')
def so_ascii(estado: Estado) -> None:
    """As linhas desenhadas só têm caracteres ASCII (D18).

    Args:
        estado: Estado do cenário.
    """
    for numero, bloco in enumerate(desenhos(estado)):
        for linha in bloco.linhas:
            fora = sorted(set(linha) - set(map(chr, range(128))))
            if fora:
                pytest.fail(
                    f"a renderização {numero} tem caracteres fora do ASCII "
                    f"{fora}: {linha!r}"
                )


@then('a renderização confirma "cores por sequências ANSI de fundo"')
def cores_de_fundo(estado: Estado) -> None:
    """As cores vêm só de fundos SGR, sobre espaços (I02, I21).

    Toda sequência é um fundo, o 49 ou o reset; todo caractere desenhado é
    espaço; e o desenho usa pelo menos um fundo.

    Args:
        estado: Estado do cenário.
    """
    fundos: set[int] = set()
    for numero, bloco in enumerate(desenhos(estado)):
        for linha in bloco.linhas:
            problemas = problemas_de_sgr(linha)
            if problemas:
                pytest.fail(
                    f"renderização {numero}: {problemas[0]} em {linha!r}"
                )
            texto = SEQUENCIA.sub("", linha)
            if texto.strip(" "):
                pytest.fail(
                    f"a renderização {numero} desenha com caracteres que não "
                    f"são espaço ({sorted(set(texto) - {' '})}): {linha!r}"
                )
        for fundos_da_linha in tela_de(bloco, numero):
            fundos.update(
                fundo for fundo in fundos_da_linha if fundo is not None
            )
    if not fundos:
        pytest.fail("nenhuma posição desenhada tem cor de fundo")


@then('a renderização confirma "última sequência ANSI é o reset"')
def termina_com_reset(estado: Estado) -> None:
    """A última sequência ANSI da saída padrão é o reset (I02).

    Args:
        estado: Estado do cenário.
    """
    saida = estado.resultado.saida_padrao
    sequencias = SEQUENCIA.findall(saida)
    if not sequencias:
        pytest.fail(f"a saída padrão não tem sequência ANSI:\n{saida}")
    if sequencias[-1] != RESET:
        pytest.fail(
            f"a última sequência ANSI é {sequencias[-1]!r}, não o reset "
            f"{RESET!r}"
        )
    if ESCAPE in SEQUENCIA.sub("", saida):
        pytest.fail("a saída padrão tem um ESC fora de uma sequência CSI")


@then('a renderização confirma "paredes iguais às do arquivo de saída"')
def paredes_do_arquivo(estado: Estado) -> None:
    """As paredes da última renderização são as da grade do arquivo atual.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    desenhada = grade_desenhada(desenho)
    for celula in labirinto.celulas():
        x, y = celula
        if desenhada[y][x] != labirinto.valor(celula):
            pytest.fail(
                f"a célula {celula} aparece com as paredes "
                f"{nomes_das_direcoes(paredes_desenhadas(desenho, celula))} "
                f"e vale {labirinto.valor(celula):x} no arquivo de saída"
            )


@then('a renderização confirma "entrada e saída iguais às do rodapé"')
def pontas_do_rodape(estado: Estado) -> None:
    """Magenta e vermelho só nas células de entrada e saída do rodapé.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    if labirinto.entrada is None or labirinto.saida is None:
        pytest.fail(f"o rodapé não tem entrada e saída: {labirinto.rodape}")
    for nome, celula in (
        ("magenta", labirinto.entrada),
        ("vermelho", labirinto.saida),
    ):
        achadas = posicoes_da_cor(desenho, CORES[nome])
        if achadas != {da_celula(celula)}:
            pytest.fail(
                f"{nome} deveria estar só na célula {celula} do rodapé "
                f"({onde(da_celula(celula))}), mas está em "
                f"{[onde(posicao) for posicao in sorted(achadas)]}"
            )


@then('a renderização confirma "caminho do arquivo marcado em ciano"')
def caminho_do_arquivo_em_ciano(estado: Estado) -> None:
    """O ciano cobre exatamente o caminho do rodapé do arquivo atual (I02).

    Células intermediárias e passagens entre células consecutivas são
    ciano; entrada e saída ficam com as próprias cores.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    try:
        esperadas = posicoes_de(
            labirinto, "passagens do caminho"
        ) | posicoes_de(labirinto, "células do caminho")
    except ValueError as erro:
        pytest.fail(str(erro))
    achadas = posicoes_da_cor(desenho, CIANO)
    faltam = esperadas - achadas
    sobram = achadas - esperadas
    if faltam or sobram:
        pytest.fail(
            f"o ciano não é o caminho {labirinto.caminho!r} do arquivo: "
            f"faltam {len(faltam)} posições ({descrever(desenho, faltam)}) "
            f"e sobram {len(sobram)} "
            f"({[onde(posicao) for posicao in sorted(sobram)[:AMOSTRA]]})"
        )


@then(
    'a renderização confirma "caminho marcado liga entrada e saída por '
    'paredes abertas"'
)
def marcado_por_paredes_abertas(estado: Estado) -> None:
    """O ciano forma uma corrente da entrada à saída por paredes abertas.

    Cada passo da corrente atravessa uma parede aberta na grade do
    arquivo de saída atual.

    Args:
        estado: Estado do cenário.
    """
    caminho, labirinto = marcado(estado)
    for primeira, segunda in zip(caminho, caminho[1:]):
        if segunda not in labirinto.vizinhas(primeira):
            pytest.fail(
                f"o caminho marcado passa de {primeira} a {segunda} por uma "
                f"parede fechada no arquivo de saída"
            )


@then(
    'a renderização confirma "caminho marcado com o comprimento da busca em '
    'largura"'
)
def marcado_mais_curto(estado: Estado) -> None:
    """O caminho ciano tem o comprimento da BFS no arquivo atual (D15, I08).

    Args:
        estado: Estado do cenário.
    """
    caminho, labirinto = marcado(estado)
    try:
        mais_curto = distancia(labirinto, caminho[0], caminho[-1])
    except ValueError as erro:
        pytest.fail(f"no arquivo de saída, {erro}")
    if len(caminho) - 1 != mais_curto:
        pytest.fail(
            f"o caminho marcado tem {len(caminho) - 1} passos; a busca em "
            f"largura no arquivo de saída dá {mais_curto}"
        )


@then(
    'a renderização confirma "cinco cores distintas para entrada, saída, 42, '
    'caminho e paredes"'
)
def cinco_cores(estado: Estado) -> None:
    """Cada um dos cinco elementos tem uma cor só, e as cinco diferem.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    cores: dict[str, Cor] = {}
    for nome in ("entrada", "saída", "células do 42", "células do caminho",
                 "paredes"):
        achadas = {
            desenho[linha][coluna]
            for linha, coluna in posicoes_do_elemento(labirinto, nome)
        }
        if len(achadas) != 1 or None in achadas:
            pytest.fail(
                f'"{nome}" deveria ter uma única cor, mas tem '
                f"{sorted(nome_da_cor(cor) for cor in achadas)}"
            )
        cores[nome] = achadas.pop()
    if len(set(cores.values())) != len(cores):
        pytest.fail(
            "cores repetidas entre os elementos: "
            + ", ".join(
                f"{nome}={nome_da_cor(cor)}" for nome, cor in cores.items()
            )
        )


@then(
    'a renderização confirma "paredes em rodízio branco, amarelo, verde, '
    'azul"'
)
def paredes_em_rodizio(estado: Estado) -> None:
    """A cor das paredes segue o rodízio da I04 a cada opção 3 da sessão.

    Args:
        estado: Estado do cenário.
    """
    sessao = estado.em_sessao()
    if sessao is None:
        pytest.fail(
            "o rodízio confere as opções enviadas ao menu, e não há sessão "
            "aberta"
        )
    cores = [cor_das_paredes(desenho) for desenho in telas(estado)]
    try:
        conferir_rodizio(cores, sessao.enviados)
    except ValueError as erro:
        pytest.fail(str(erro))


@then(
    'a renderização confirma "labirinto diferente do da renderização '
    'anterior"'
)
def diferente_do_anterior(estado: Estado) -> None:
    """As paredes da última renderização diferem das da penúltima.

    Args:
        estado: Estado do cenário.
    """
    desenhos_da_saida = telas(estado)
    if len(desenhos_da_saida) < 2:
        pytest.fail(
            f"a saída tem {len(desenhos_da_saida)} renderização; esperadas 2"
        )
    anterior, ultima = desenhos_da_saida[-2], desenhos_da_saida[-1]
    if dimensoes(anterior) == dimensoes(ultima) and grade_desenhada(
        anterior
    ) == grade_desenhada(ultima):
        pytest.fail(
            "a última renderização mostra as mesmas paredes da anterior"
        )


@then(
    parsers.parse(
        'na última renderização, as posições de "{elemento:Q}" têm a cor '
        '"{cor:Q}"',
        extra_types=TIPOS,
    )
)
def elemento_tem_a_cor(estado: Estado, elemento: str, cor: str) -> None:
    """Todas as posições do elemento têm a cor na última renderização.

    Args:
        estado: Estado do cenário.
        elemento: Um dos ELEMENTOS.
        cor: Nome da cor (I21).
    """
    if elemento not in ELEMENTOS:
        pytest.fail(
            f'"{elemento}" não existe; os válidos são: {", ".join(ELEMENTOS)}'
        )
    codigo = codigo_da_cor(cor)
    desenho, labirinto = tela_e_labirinto(estado)
    posicoes = posicoes_do_elemento(labirinto, elemento)
    erradas = {
        posicao for posicao in posicoes
        if desenho[posicao[0]][posicao[1]] != codigo
    }
    if erradas:
        pytest.fail(
            f'{len(erradas)} de {len(posicoes)} posições de "{elemento}" não '
            f"são {cor}: {descrever(desenho, erradas)}"
        )


@then(
    parsers.parse(
        'na última renderização, a cor "{cor:Q}" só aparece em "{elemento:Q}"',
        extra_types=TIPOS,
    )
)
def cor_so_no_elemento(estado: Estado, cor: str, elemento: str) -> None:
    """A cor não aparece fora do elemento na última renderização.

    Args:
        estado: Estado do cenário.
        cor: Nome da cor (I21).
        elemento: Um dos ELEMENTOS.
    """
    if elemento not in ELEMENTOS:
        pytest.fail(
            f'"{elemento}" não existe; os válidos são: {", ".join(ELEMENTOS)}'
        )
    codigo = codigo_da_cor(cor)
    desenho, labirinto = tela_e_labirinto(estado)
    fora = posicoes_da_cor(desenho, codigo) - posicoes_do_elemento(
        labirinto, elemento
    )
    if fora:
        pytest.fail(
            f'{cor} aparece em {len(fora)} posições fora de "{elemento}": '
            f"{[onde(posicao) for posicao in sorted(fora)[:AMOSTRA]]}"
        )


@then(
    parsers.parse(
        'na última renderização, nenhuma posição tem a cor "{cor:Q}"',
        extra_types=TIPOS,
    )
)
def nenhuma_posicao_com_a_cor(estado: Estado, cor: str) -> None:
    """A cor não aparece na última renderização.

    Args:
        estado: Estado do cenário.
        cor: Nome da cor (I21).
    """
    codigo = codigo_da_cor(cor)
    achadas = posicoes_da_cor(ultima_tela(estado), codigo)
    if achadas:
        pytest.fail(
            f"{cor} aparece em {len(achadas)} posições: "
            f"{[onde(posicao) for posicao in sorted(achadas)[:AMOSTRA]]}"
        )


@then(
    parsers.parse(
        'na última renderização, as células de dígito "{digito:Q}" mostram '
        'exatamente as paredes "{paredes:Q}"',
        extra_types=TIPOS,
    )
)
def celulas_do_digito(estado: Estado, digito: str, paredes: str) -> None:
    """Cada célula com o dígito aparece com exatamente essas paredes.

    Args:
        estado: Estado do cenário.
        digito: Dígito hexadecimal do arquivo de saída.
        paredes: "nenhuma" ou direções em lista com vírgulas e "e".
    """
    try:
        esperadas = direcoes(paredes)
    except ValueError as erro:
        pytest.fail(str(erro))
    try:
        valor = int(digito, 16)
    except ValueError:
        pytest.fail(f'"{digito}" não é um dígito hexadecimal')
    desenho, labirinto = tela_e_labirinto(estado)
    if cor_das_paredes(desenho) is None:
        pytest.fail("o canto superior esquerdo do desenho está sem cor")
    celulas = [
        celula for celula in labirinto.celulas()
        if labirinto.valor(celula) == valor
    ]
    if not celulas:
        pytest.fail(f'o arquivo de saída não tem célula de dígito "{digito}"')
    for celula in celulas:
        mostradas = paredes_desenhadas(desenho, celula)
        if mostradas != esperadas:
            pytest.fail(
                f"a célula {celula}, de dígito {digito}, aparece com as "
                f"paredes {nomes_das_direcoes(mostradas)}; esperadas "
                f"{nomes_das_direcoes(esperadas)}"
            )


def tem_ciano(estado: Estado) -> bool:
    """Diz se a última renderização tem alguma posição ciano.

    Args:
        estado: Estado do cenário.

    Returns:
        True quando o caminho aparece.
    """
    return bool(posicoes_da_cor(ultima_tela(estado), CIANO))
