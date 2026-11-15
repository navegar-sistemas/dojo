"""Passos que conferem a renderização do labirinto no terminal."""

import pytest
from pytest_bdd import parsers, then

from suporte.config import chaves_das_linhas
from suporte.estado import Estado
from suporte.labirinto import Celula, Labirinto, ler_saida
from suporte.render import (
    BRANCO,
    CAMADAS,
    CIANO,
    CORES,
    ELEMENTOS,
    ESCAPE,
    GLIFOS,
    PERMITIDOS,
    RESET,
    SEQUENCIA,
    TEXTO,
    Cor,
    Posicao,
    Renderizacao,
    Rgb,
    Tela,
    bracos,
    caminho_do_arquivo,
    caminho_marcado,
    cantos,
    conferir_rodizio,
    cor_das_paredes,
    cor_em,
    da_celula,
    descrever,
    desenho_do_caminho,
    dimensoes,
    direcoes,
    distancia,
    grade_desenhada,
    interior,
    nome_da_cor,
    nomes_das_direcoes,
    onde,
    paredes_desenhadas,
    paredes_na_tela,
    posicoes_da_cor,
    posicoes_de,
    problemas_de_sgr,
    problemas_do_formato,
    renderizacoes,
    seguida_do_menu,
    sequencias_que_nao_sao_sgr,
    tela,
    trocas_sem_mudanca,
    visiveis,
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
    """Caracteres e cores de uma renderização, ou a falha do passo.

    Args:
        renderizacao: Bloco desenhado.
        numero: Índice do bloco na saída, a partir de 0, para a mensagem.

    Returns:
        Os caracteres, numa grade de 2n + 1 linhas por 4m + 1 colunas.
    """
    try:
        desenho = tela(renderizacao)
        dimensoes(desenho)
    except ValueError as erro:
        pytest.fail(f"renderização {numero}: {erro}")
    return desenho


def telas(estado: Estado) -> list[Tela]:
    """Caracteres e cores de todas as renderizações.

    Args:
        estado: Estado do cenário.

    Returns:
        Uma grade de caracteres por renderização, na ordem.
    """
    return [
        tela_de(bloco, numero)
        for numero, bloco in enumerate(desenhos(estado))
    ]


def ultima_tela(estado: Estado) -> Tela:
    """Caracteres e cores da última renderização.

    Args:
        estado: Estado do cenário.

    Returns:
        A grade de caracteres.
    """
    blocos = desenhos(estado)
    return tela_de(blocos[-1], len(blocos) - 1)


def grade_da_tela(desenho: Tela, qual: str) -> list[list[int]]:
    """Bits de parede que o desenho mostra, ou a falha do passo.

    Args:
        desenho: Caracteres de uma renderização.
        qual: Nome da renderização, para a mensagem.

    Returns:
        Uma linha de valores de 0 a 15 por linha de células.
    """
    try:
        return grade_desenhada(desenho)
    except ValueError as erro:
        pytest.fail(f"na {qual}, {erro}")


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
        (caracteres da última renderização, labirinto do arquivo).
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


def rgb_da_cor(cor: str) -> Rgb:
    """RGB da cor nomeada no passo (I21).

    Args:
        cor: Nome da cor.

    Returns:
        O RGB.
    """
    if cor not in CORES:
        pytest.fail(f'"{cor}" não existe; os válidos são: {", ".join(CORES)}')
    return CORES[cor]


def conferir_elemento(elemento: str) -> None:
    """Derruba o passo quando o elemento não é da lista fechada.

    Args:
        elemento: Nome escrito no passo.
    """
    if elemento not in ELEMENTOS:
        pytest.fail(
            f'"{elemento}" não existe; os válidos são: {", ".join(ELEMENTOS)}'
        )


def posicoes_ou_falha(labirinto: Labirinto, nome: str) -> set[Posicao]:
    """Posições do elemento, ou a falha do passo quando o rodapé não as dá.

    Args:
        labirinto: Labirinto do arquivo de saída.
        nome: Um dos ELEMENTOS.

    Returns:
        As posições do elemento no desenho, possivelmente nenhuma.
    """
    try:
        return posicoes_de(labirinto, nome)
    except ValueError as erro:
        pytest.fail(str(erro))


def posicoes_do_elemento(labirinto: Labirinto, nome: str) -> set[Posicao]:
    """Posições do elemento nomeado no passo, pelo menos uma.

    Args:
        labirinto: Labirinto do arquivo de saída.
        nome: Um dos ELEMENTOS.

    Returns:
        As posições do elemento no desenho.
    """
    posicoes = posicoes_ou_falha(labirinto, nome)
    if not posicoes:
        pytest.fail(f'o labirinto do arquivo não tem "{nome}"')
    return posicoes


def amostra(desenho: Tela, posicoes: set[Posicao]) -> str:
    """Amostra de posições com o caractere e as cores, para as mensagens.

    Args:
        desenho: Caracteres da renderização.
        posicoes: Posições a descrever.

    Returns:
        Até AMOSTRA posições como "linha l, coluna c: 'x' texto t, fundo f".
    """
    return "; ".join(
        f"{onde(posicao)}: {descrever(desenho[posicao[0]][posicao[1]])}"
        for posicao in sorted(posicoes)[:AMOSTRA]
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

    O desenho anterior continua na saída: nenhuma sequência ESC além das
    SGR, CSI ou não (como ``ESC c``), limpa a tela ou move o cursor (I02).

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
    controles = sequencias_que_nao_sao_sgr(estado.resultado.saida_padrao)
    if controles:
        pytest.fail(
            f"a saída tem sequências ESC que não são SGR, e podem limpar a "
            f"tela ou mover o cursor: {controles}"
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


@then('a renderização confirma "4 × WIDTH + 1 caracteres por linha"')
def caracteres_da_largura(estado: Estado) -> None:
    """Cada linha desenhada tem 4 × WIDTH + 1 caracteres visíveis (I02).

    Args:
        estado: Estado do cenário.
    """
    largura, _ = tamanho_do_config(estado)
    esperados = 4 * largura + 1
    for numero, bloco in enumerate(desenhos(estado)):
        for indice, linha in enumerate(bloco.linhas):
            achados = len(visiveis(linha))
            if achados != esperados:
                pytest.fail(
                    f"a linha {indice} da renderização {numero} tem "
                    f"{achados} caracteres; com WIDTH={largura}, esperados "
                    f"{esperados}: {linha!r}"
                )


@then('a renderização confirma "só espaços e caracteres de caixa"')
def so_caixa(estado: Estado) -> None:
    """As linhas desenhadas só têm espaços e os caracteres da I02 (D18).

    Args:
        estado: Estado do cenário.
    """
    for numero, bloco in enumerate(desenhos(estado)):
        for linha in bloco.linhas:
            fora = sorted(
                {caractere.simbolo for caractere in visiveis(linha)}
                - PERMITIDOS
            )
            if fora:
                pytest.fail(
                    f"a renderização {numero} tem caracteres fora de "
                    f"{''.join(sorted(PERMITIDOS))!r} {fora}: {linha!r}"
                )


@then('a renderização confirma "cores por sequências ANSI de 24 bits"')
def cores_de_24_bits(estado: Estado) -> None:
    """As cores vêm de SGR 38;2 e 48;2, e todo caractere tem as duas (I02).

    Toda sequência é uma cor de texto ou de fundo de 24 bits ou o reset;
    todo caractere desenhado tem cor de texto e de fundo em vigor.

    Args:
        estado: Estado do cenário.
    """
    for numero, bloco in enumerate(desenhos(estado)):
        for indice, linha in enumerate(bloco.linhas):
            problemas = problemas_de_sgr(linha)
            if problemas:
                pytest.fail(
                    f"renderização {numero}: {problemas[0]} em {linha!r}"
                )
            for coluna, caractere in enumerate(visiveis(linha)):
                if caractere.texto is None or caractere.fundo is None:
                    pytest.fail(
                        f"na renderização {numero}, o caractere da "
                        f"{onde((indice, coluna))} não tem cor de texto e de "
                        f"fundo: {descrever(caractere)}"
                    )


def linhas_desenhadas(estado: Estado) -> list[tuple[int, str]]:
    """Linhas de todas as renderizações, com o número da renderização.

    Args:
        estado: Estado do cenário.

    Returns:
        Pares (renderização, linha), na ordem da saída.
    """
    return [
        (numero, linha)
        for numero, bloco in enumerate(desenhos(estado))
        for linha in bloco.linhas
    ]


@then(
    'a renderização confirma "texto e fundo na mesma sequência e um reset no '
    'fim de cada linha"'
)
def sequencias_da_i02(estado: Estado) -> None:
    """Cada linha abre com texto e fundo juntos e só tem o reset no fim.

    Toda sequência antes do fim é ``ESC[38;2;R;G;B;48;2;R;G;Bm``; a
    primeira abre a linha e a última é o único reset (I02).

    Args:
        estado: Estado do cenário.
    """
    for numero, linha in linhas_desenhadas(estado):
        problemas = problemas_do_formato(linha)
        if problemas:
            pytest.fail(f"renderização {numero}: {problemas[0]}")


@then(
    'a renderização confirma "sequência só quando o par de cores muda"'
)
def sequencias_so_na_troca(estado: Estado) -> None:
    """Nenhuma sequência repete o par em vigor ou fica sem caractere (I02).

    Args:
        estado: Estado do cenário.
    """
    for numero, linha in linhas_desenhadas(estado):
        sobrando = trocas_sem_mudanca(linha)
        if sobrando:
            pytest.fail(
                f"renderização {numero}: {len(sobrando)} sequências sem "
                f"troca de cor; a primeira: {sobrando[0]}"
            )


@then(
    'a renderização confirma "espaço fora das paredes, dos cantos e do '
    'caminho"'
)
def espaco_fora_do_desenhado(estado: Estado) -> None:
    """Só paredes fechadas, cantos com braço e o caminho visível têm traço.

    As paredes vêm do OUTPUT_FILE atual; o caminho do rodapé conta só
    quando a última renderização tem algum ciano.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    tracadas = posicoes_ou_falha(labirinto, "paredes")
    if posicoes_da_cor(desenho, CIANO):
        try:
            tracadas |= set(
                desenho_do_caminho(caminho_do_arquivo(labirinto))
            )
        except ValueError as erro:
            pytest.fail(str(erro))
    sobram = {
        (linha, coluna)
        for linha, caracteres in enumerate(desenho)
        for coluna, caractere in enumerate(caracteres)
        if (linha, coluna) not in tracadas and caractere.simbolo != " "
    }
    if sobram:
        pytest.fail(
            f"{len(sobram)} caracteres fora das paredes, dos cantos e do "
            f"caminho visível não são espaço: {amostra(desenho, sobram)}"
        )


@then(
    'a renderização confirma "fundo branco fora da entrada, da saída e do '
    '42"'
)
def fundo_branco(estado: Estado) -> None:
    """Todo caractere fora da entrada, da saída e do 42 tem fundo branco.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    destacadas: set[Posicao] = set()
    for nome in ("entrada", "saída", "42"):
        destacadas |= posicoes_ou_falha(labirinto, nome)
    erradas = {
        (linha, coluna)
        for linha, caracteres in enumerate(desenho)
        for coluna, caractere in enumerate(caracteres)
        if (linha, coluna) not in destacadas and caractere.fundo != BRANCO
    }
    if erradas:
        pytest.fail(
            f"{len(erradas)} caracteres fora da entrada, da saída e do 42 "
            f"sem fundo branco: {amostra(desenho, erradas)}"
        )


@then(
    'a renderização confirma "cada canto com o caractere das suas paredes"'
)
def cantos_pelas_paredes(estado: Estado) -> None:
    """Cada canto tem o caractere dos braços das paredes ao redor (I02).

    Args:
        estado: Estado do cenário.
    """
    for numero, desenho in enumerate(telas(estado)):
        largura, altura = dimensoes(desenho)
        fechadas = paredes_na_tela(desenho)
        for canto in sorted(cantos(largura, altura)):
            esperado = GLIFOS[bracos(fechadas, canto)]
            achado = desenho[canto[0]][canto[1]].simbolo
            if achado != esperado:
                pytest.fail(
                    f"na renderização {numero}, o canto da {onde(canto)} é "
                    f"{achado!r}; as paredes ao redor pedem {esperado!r}"
                )


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
    desenhada = grade_da_tela(desenho, "última renderização")
    for celula in labirinto.celulas():
        x, y = celula
        if desenhada[y][x] != labirinto.valor(celula):
            mostradas = paredes_desenhadas(desenho, celula)
            pytest.fail(
                f"a célula {celula} aparece com as paredes "
                f"{nomes_das_direcoes(mostradas)} e vale "
                f"{labirinto.valor(celula):x} no arquivo de saída"
            )


@then('a renderização confirma "entrada e saída iguais às do rodapé"')
def pontas_do_rodape(estado: Estado) -> None:
    """Magenta e vermelho só no interior da entrada e da saída do rodapé.

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
        if achadas != interior(celula):
            pytest.fail(
                f"{nome} deveria estar só no interior da célula {celula} do "
                f"rodapé ({onde(da_celula(celula))} e as vizinhas), mas está "
                f"em {[onde(posicao) for posicao in sorted(achadas)]}"
            )


@then('a renderização confirma "caminho do arquivo marcado em ciano"')
def caminho_do_arquivo_em_ciano(estado: Estado) -> None:
    """O ciano desenha exatamente o caminho do rodapé do arquivo (I02).

    O centro de cada célula do caminho, entrada e saída inclusive, tem o
    caractere dos braços para a anterior e a seguinte; cada passagem entre
    células consecutivas, ``━`` ou ``┃``; nada mais é ciano.

    Args:
        estado: Estado do cenário.
    """
    desenho, labirinto = tela_e_labirinto(estado)
    try:
        esperado = desenho_do_caminho(caminho_do_arquivo(labirinto))
    except ValueError as erro:
        pytest.fail(str(erro))
    achadas = posicoes_da_cor(desenho, CIANO)
    faltam = {
        posicao for posicao in esperado
        if cor_em(desenho[posicao[0]][posicao[1]], TEXTO) != CIANO
    }
    sobram = achadas - set(esperado)
    if faltam or sobram:
        pytest.fail(
            f"o ciano não é o caminho {labirinto.caminho!r} do arquivo: "
            f"faltam {len(faltam)} posições ({amostra(desenho, faltam)}) "
            f"e sobram {len(sobram)} ({amostra(desenho, sobram)})"
        )
    trocados = {
        posicao for posicao, simbolo in esperado.items()
        if desenho[posicao[0]][posicao[1]].simbolo != simbolo
    }
    if trocados:
        primeiro = min(trocados)
        pytest.fail(
            f"{len(trocados)} posições do caminho com o caractere errado; a "
            f"da {onde(primeiro)} é "
            f"{desenho[primeiro[0]][primeiro[1]].simbolo!r}, esperado "
            f"{esperado[primeiro]!r}"
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
    for nome in ("entrada", "saída", "42", "células do caminho", "paredes"):
        achadas = {
            cor_em(desenho[linha][coluna], CAMADAS[nome])
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
    'a renderização confirma "paredes em rodízio grafite, laranja, verde, '
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
    if dimensoes(anterior) == dimensoes(ultima) and grade_da_tela(
        anterior, "penúltima renderização"
    ) == grade_da_tela(ultima, "última renderização"):
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

    A cor das paredes e do caminho é a do texto; a da entrada, da saída e
    do 42, a do fundo.

    Args:
        estado: Estado do cenário.
        elemento: Um dos ELEMENTOS.
        cor: Nome da cor (I21).
    """
    conferir_elemento(elemento)
    rgb = rgb_da_cor(cor)
    desenho, labirinto = tela_e_labirinto(estado)
    posicoes = posicoes_do_elemento(labirinto, elemento)
    erradas = {
        posicao for posicao in posicoes
        if cor_em(desenho[posicao[0]][posicao[1]], CAMADAS[elemento]) != rgb
    }
    if erradas:
        pytest.fail(
            f'{len(erradas)} de {len(posicoes)} posições de "{elemento}" não '
            f"têm {cor} no {CAMADAS[elemento]}: {amostra(desenho, erradas)}"
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
    conferir_elemento(elemento)
    rgb = rgb_da_cor(cor)
    desenho, labirinto = tela_e_labirinto(estado)
    fora = posicoes_da_cor(desenho, rgb) - posicoes_do_elemento(
        labirinto, elemento
    )
    if fora:
        pytest.fail(
            f'{cor} aparece em {len(fora)} posições fora de "{elemento}": '
            f"{amostra(desenho, fora)}"
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
    rgb = rgb_da_cor(cor)
    desenho = ultima_tela(estado)
    achadas = posicoes_da_cor(desenho, rgb)
    if achadas:
        pytest.fail(
            f"{cor} aparece em {len(achadas)} posições: "
            f"{amostra(desenho, achadas)}"
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
    celulas = [
        celula for celula in labirinto.celulas()
        if labirinto.valor(celula) == valor
    ]
    if not celulas:
        pytest.fail(f'o arquivo de saída não tem célula de dígito "{digito}"')
    for celula in celulas:
        try:
            mostradas = paredes_desenhadas(desenho, celula)
        except ValueError as erro:
            pytest.fail(f"na última renderização, {erro}")
        if mostradas != esperadas:
            pytest.fail(
                f"a célula {celula}, de dígito {digito}, aparece com as "
                f"paredes {nomes_das_direcoes(mostradas)}; esperadas "
                f"{nomes_das_direcoes(esperadas)}"
            )


def tem_ciano(estado: Estado) -> bool:
    """Diz se a última renderização tem algum caractere ciano.

    Args:
        estado: Estado do cenário.

    Returns:
        True quando o caminho aparece.
    """
    return bool(posicoes_da_cor(ultima_tela(estado), CIANO))
