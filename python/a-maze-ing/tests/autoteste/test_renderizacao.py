"""Testes dos passos que conferem a renderização no terminal."""

from collections.abc import Callable

import pytest

from autoteste.desenho import (
    ANEL,
    ARQUIVO,
    AZUL,
    BRANCO,
    CIANO,
    CINZA,
    CONFIG,
    GRAFITE,
    LARANJA,
    MAGENTA,
    TEXTO_DO_MENU,
    VERDE,
    CAMINHO,
    com_fundo,
    com_simbolo,
    com_texto,
    desenhar,
    grade,
    saida,
    sgr,
    tela_com_menu,
    volta,
)
from autoteste.falso import programa_falso
from step_defs.interacao import envio_ao_menu, programa_iniciado
from step_defs.renderizacao import (
    caminho_do_arquivo_em_ciano,
    cantos_pelas_paredes,
    caracteres_da_largura,
    celulas_do_digito,
    cinco_cores,
    cor_so_no_elemento,
    cores_de_24_bits,
    diferente_do_anterior,
    espaco_fora_do_desenhado,
    elemento_tem_a_cor,
    fundo_branco,
    labirinto_atual,
    linhas_com_reset,
    linhas_da_altura,
    marcado_mais_curto,
    marcado_por_paredes_abertas,
    nenhuma_posicao_com_a_cor,
    nova_abaixo_da_anterior,
    paredes_do_arquivo,
    paredes_em_rodizio,
    pontas_do_rodape,
    seguidas_do_menu,
    sequencias_da_i02,
    sequencias_so_na_troca,
    so_caixa,
    tamanho_do_config,
    termina_com_reset,
)
from suporte.config import Config
from suporte.estado import Estado, Execucao
from suporte.render import PAR, RESET, Rgb, Tela
from suporte.sessao import PROMPT

PAREDE = "\x1b[38;2;31;41;55;48;2;255;255;255m┃\x1b[0m"
Passo = Callable[[Estado], None]
# Parede Sul da célula (1, 0), aberta no exemplo, desenhada fechada.
SUL_DE_1_0 = [(2, 5), (2, 6), (2, 7)]


def com_saida(
    cenario: Estado,
    saida_padrao: str,
    arquivo: str | None = ARQUIVO,
    config: list[str] | None = None,
) -> Estado:
    """Põe no cenário uma execução com a saída padrão e o arquivo dados.

    Args:
        cenario: Estado numa pasta temporária.
        saida_padrao: Texto do stdout.
        arquivo: Conteúdo do OUTPUT_FILE, ou None quando não existe.
        config: Linhas do config; o padrão é o do labirinto de exemplo.

    Returns:
        O cenário.
    """
    cenario.config = Config(list(CONFIG if config is None else config))
    cenario.resultados.append(
        Execucao("comando", 0, saida_padrao, "", False, None, arquivo)
    )
    return cenario


def test_linhas_coloridas_terminam_com_reset(cenario: Estado) -> None:
    """Linhas sem cor, como o menu, não precisam do reset.

    Args:
        cenario: Estado numa pasta temporária.
    """
    saida_padrao = f"{PAREDE}{PAREDE}\n{PAREDE}\n1. Regenerate\n{PROMPT}"
    linhas_com_reset(com_saida(cenario, saida_padrao))


@pytest.mark.parametrize(
    "linha",
    [
        "\x1b[38;2;31;41;55;48;2;255;255;255m┃",
        f"{PAREDE} ",
        f"{PAREDE}\x1b[38;2;31;41;55m┃",
    ],
    ids=["sem reset", "espaço depois do reset", "cor aberta no fim"],
)
def test_linha_colorida_sem_reset_no_fim(cenario: Estado, linha: str) -> None:
    """Uma única linha colorida que não termina no reset derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        linha: Linha renderizada com defeito.
    """
    with pytest.raises(pytest.fail.Exception, match="1 de 2 linhas"):
        linhas_com_reset(com_saida(cenario, f"{PAREDE}\n{linha}\n"))


def test_saida_sem_renderizacao(cenario: Estado) -> None:
    """Sem nenhuma linha colorida não houve renderização.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="nenhuma linha"):
        linhas_com_reset(com_saida(cenario, "teste\n"))


BONS: list[Passo] = [
    seguidas_do_menu,
    linhas_da_altura,
    caracteres_da_largura,
    so_caixa,
    cores_de_24_bits,
    fundo_branco,
    cantos_pelas_paredes,
    termina_com_reset,
    paredes_do_arquivo,
    pontas_do_rodape,
    caminho_do_arquivo_em_ciano,
    marcado_por_paredes_abertas,
    marcado_mais_curto,
    cinco_cores,
    sequencias_da_i02,
    sequencias_so_na_troca,
    espaco_fora_do_desenhado,
]


@pytest.mark.parametrize("passo", BONS, ids=lambda passo: passo.__name__)
def test_renderizacao_do_exemplo(cenario: Estado, passo: Passo) -> None:
    """A exibição do labirinto de exemplo cumpre cada propriedade.

    Args:
        cenario: Estado numa pasta temporária.
        passo: Propriedade conferida.
    """
    passo(com_saida(cenario, saida(grade(caminho=False), grade())))


def test_espaco_com_o_caminho_oculto(cenario: Estado) -> None:
    """Sem ciano, o caminho não conta, e o resto fora das paredes é espaço.

    Args:
        cenario: Estado numa pasta temporária.
    """
    espaco_fora_do_desenhado(
        com_saida(cenario, saida(grade(), grade(caminho=False)))
    )


def caminho_sem_ciano() -> Tela:
    """O exemplo com o caminho traçado na cor das paredes, sem ciano.

    Returns:
        A grade de caracteres.
    """
    desenho = grade()
    for linha, coluna in CAMINHO:
        desenho = com_texto(desenho, linha, coluna, GRAFITE)
    return desenho


def desenhar_com(desenho: Tela, antes: bool, depois: bool) -> str:
    """Escreve o desenho com sequência ou reset em volta de cada caractere.

    Args:
        desenho: Caracteres e cores.
        antes: Se cada caractere vem depois da sequência do seu par.
        depois: Se cada caractere vem seguido do reset.

    Returns:
        As linhas, cada uma terminada no reset.
    """
    linhas: list[str] = []
    for caracteres in desenho:
        partes = [
            (sgr(caractere.texto, caractere.fundo) if antes else "")
            + caractere.simbolo
            + (RESET if depois else "")
            for caractere in caracteres
        ]
        if not antes:
            primeiro = caracteres[0]
            partes.insert(0, sgr(primeiro.texto, primeiro.fundo))
        linhas.append("".join(partes) + ("" if depois else RESET))
    return "\n".join(linhas)


def com_texto_e_fundo_separados(texto: str) -> str:
    """Troca cada sequência de texto e fundo por duas, uma de cada.

    Args:
        texto: Saída padrão.

    Returns:
        A saída com a sequência do texto seguida da do fundo.
    """
    return PAR.sub(
        lambda casado: "\x1b[38;2;{};{};{}m\x1b[48;2;{};{};{}m".format(
            *casado.groups()
        ),
        texto,
    )


def exibicao(texto_do_desenho: str) -> str:
    """Saída de uma exibição com o desenho já escrito.

    Args:
        texto_do_desenho: Linhas desenhadas.

    Returns:
        A linha vazia, o desenho, o menu e o prompt.
    """
    return tela_com_menu(grade()).replace(desenhar(grade()), texto_do_desenho)


REPETIDA = "\x1b[38;2;1;2;3;48;2;4;5;6m"
SEM_MENU = "\n" + desenhar(grade()) + "\n"
OUTRA_ALTURA = ["WIDTH=3", "HEIGHT=3"]
OUTRA_LARGURA = ["WIDTH=4", "HEIGHT=2"]
TEXTO_GRAFITE = "38;2;31;41;55"
DEFEITOS: list[tuple[Passo, str, list[str], str]] = [
    (seguidas_do_menu, SEM_MENU, CONFIG, "sem o menu"),
    (seguidas_do_menu, TEXTO_DO_MENU, CONFIG, "nenhuma renderização"),
    (linhas_da_altura, saida(grade()), OUTRA_ALTURA, "esperadas 7"),
    (caracteres_da_largura, saida(grade()), OUTRA_LARGURA, "esperados 17"),
    (caracteres_da_largura, saida(grade()).replace("┓", "┓ ", 1), CONFIG,
     "tem 14 caracteres"),
    (so_caixa, saida(com_simbolo(grade(), [(0, 5)], "█")), CONFIG,
     "fora de"),
    (so_caixa, saida(com_simbolo(grade(), [(2, 4)], "┐")), CONFIG,
     "fora de"),
    (so_caixa, saida(com_simbolo(grade(), [(3, 6)], "#")), CONFIG,
     "fora de"),
    (cores_de_24_bits, saida(grade()).replace(TEXTO_GRAFITE, "37", 1),
     CONFIG, "'37' não é cor de 24 bits"),
    (cores_de_24_bits, saida(grade()).replace(TEXTO_GRAFITE, "38;5;236", 1),
     CONFIG, "'38' sem 2;R;G;B"),
    (cores_de_24_bits, saida(grade()).replace("m┏", "m\x1b[1m┏", 1), CONFIG,
     "'1' não é cor"),
    (cores_de_24_bits, saida(grade()).replace("m┏", "m\x1b[2J┏", 1), CONFIG,
     "não é SGR"),
    (cores_de_24_bits, saida(com_fundo(grade(), 0, 0, None)), CONFIG,
     "linha 0, coluna 0 não tem cor de texto e de fundo"),
    (cores_de_24_bits, saida(com_texto(grade(), 3, 6, None)), CONFIG,
     "linha 3, coluna 6 não tem cor"),
    (fundo_branco, saida(com_fundo(grade(), 3, 6, CINZA)), CONFIG,
     "1 caracteres fora da entrada"),
    (fundo_branco, saida(com_fundo(grade(), 1, 6, CIANO)), CONFIG,
     "linha 1, coluna 6"),
    (cantos_pelas_paredes, saida(com_simbolo(grade(), [(0, 0)], "╋")),
     CONFIG, "pedem '┏'"),
    (cantos_pelas_paredes, saida(com_simbolo(grade(), [(2, 4)], "━")),
     CONFIG, "linha 2, coluna 4 é '━'; as paredes ao redor pedem '┓'"),
    (cantos_pelas_paredes, saida(com_simbolo(grade(), SUL_DE_1_0, "━")),
     CONFIG, "coluna 4 é '┓'; as paredes ao redor pedem '┳'"),
    (termina_com_reset, saida(grade()) + "\x1b[38;2;1;2;3m", CONFIG,
     "'\\\\x1b\\[38;2;1;2;3m'"),
    (termina_com_reset, TEXTO_DO_MENU, CONFIG, "não tem sequência"),
    (paredes_do_arquivo, saida(com_simbolo(grade(), SUL_DE_1_0, "━")),
     CONFIG, "célula \\(1, 0\\) aparece com as paredes Norte, Sul e"),
    (paredes_do_arquivo, saida(com_simbolo(grade(), [(3, 4)], " ")),
     CONFIG, "célula \\(0, 1\\) aparece"),
    (paredes_do_arquivo, saida(com_simbolo(grade(), [(2, 6)], "━")),
     CONFIG, "só em parte"),
    (pontas_do_rodape, saida(com_fundo(grade(), 3, 6, MAGENTA)), CONFIG,
     "magenta deveria estar só"),
    (pontas_do_rodape, saida(com_fundo(grade(), 1, 3, BRANCO)), CONFIG,
     "magenta deveria estar só"),
    (caminho_do_arquivo_em_ciano, saida(grade(caminho=False)), CONFIG,
     "faltam 9"),
    (caminho_do_arquivo_em_ciano, saida(com_fundo(grade(), 3, 6, CIANO)),
     CONFIG, "sobram 1"),
    (caminho_do_arquivo_em_ciano, saida(com_texto(grade(), 2, 4, CIANO)),
     CONFIG, "sobram 1"),
    (caminho_do_arquivo_em_ciano,
     saida(com_simbolo(grade(), [(1, 2)], "━")), CONFIG,
     "caractere errado; a da linha 1, coluna 2 é '━', esperado '╺'"),
    (marcado_por_paredes_abertas, saida(grade(caminho=False)), CONFIG,
     "centro da entrada"),
    (marcado_mais_curto, saida(com_simbolo(grade(), [(1, 6)], "┳")), CONFIG,
     "pedem '━'"),
    (cinco_cores, saida(grade(caminho=False)), CONFIG,
     '"células do caminho" deveria ter uma única cor'),
    (cinco_cores, saida(com_fundo(grade(), 3, 1, BRANCO)), CONFIG,
     '"42" deveria ter uma única cor'),
    (cinco_cores, saida(com_texto(grade(), 1, 6, CINZA)), CONFIG,
     "cores repetidas"),
    (espaco_fora_do_desenhado, saida(caminho_sem_ciano()), CONFIG,
     "caracteres fora das paredes, dos cantos e do caminho visível"),
    (espaco_fora_do_desenhado,
     saida(com_simbolo(grade(), [(3, 1), (3, 2), (3, 3)], "━")), CONFIG,
     "3 caracteres fora"),
    (espaco_fora_do_desenhado,
     saida(com_simbolo(grade(caminho=False), [(3, 6)], "┃")), CONFIG,
     "linha 3, coluna 6: '┃'"),
    (sequencias_so_na_troca, exibicao(desenhar_com(grade(), True, False)),
     CONFIG, "repete o par de cores em vigor"),
    (sequencias_da_i02, exibicao(desenhar_com(grade(), False, True)),
     CONFIG, "no meio da linha não é texto e fundo"),
    (sequencias_da_i02, com_texto_e_fundo_separados(saida(grade())), CONFIG,
     "não abre com texto e fundo numa sequência só"),
    (sequencias_so_na_troca, com_texto_e_fundo_separados(saida(grade())),
     CONFIG, "sem caractere no meio"),
    (sequencias_da_i02, saida(grade()).replace("\n\x1b", "\n \x1b", 1),
     CONFIG, "não abre com texto e fundo"),
    (sequencias_da_i02, saida(grade()).replace("┓\x1b[0m", "\x1b[0m┓", 1),
     CONFIG, "não termina com o reset"),
    (sequencias_so_na_troca, saida(grade()).replace("\n", f"\n{REPETIDA}", 2),
     CONFIG, "sem caractere no meio"),
]


@pytest.mark.parametrize(
    ("passo", "texto", "config", "mensagem"),
    DEFEITOS,
    ids=[
        "menu ausente", "sem renderização", "altura", "largura",
        "caractere a mais", "bloco cheio", "caixa fina", "caractere ASCII",
        "16 cores", "256 cores", "negrito", "limpa a tela", "sem fundo",
        "sem texto", "fundo do 42 fora", "caminho no fundo",
        "canto errado", "canto sem braço", "canto sem parede nova",
        "termina colorido", "sem sequência", "parede a mais",
        "parede a menos", "parede em parte", "entrada a mais",
        "entrada a menos", "caminho oculto", "ciano no fundo",
        "canto ciano", "braço errado no caminho", "sem corrente",
        "centro do caminho errado", "caminho sem cor", "42 sem cor",
        "caminho na cor do 42", "caminho oculto traçado", "42 cheio de ━",
        "corredor com traço", "sequência a cada caractere",
        "reset a cada caractere", "texto e fundo separados",
        "texto e fundo separados sem caractere", "linha sem abrir",
        "reset antes do fim", "sequência sem caractere",
    ],
)
def test_renderizacao_com_defeito(
    cenario: Estado,
    passo: Passo,
    texto: str,
    config: list[str],
    mensagem: str,
) -> None:
    """Cada defeito derruba a propriedade que o cobre.

    Args:
        cenario: Estado numa pasta temporária.
        passo: Propriedade conferida.
        texto: Saída padrão.
        config: Linhas do config.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        passo(com_saida(cenario, texto, config=config))


def test_caminho_marcado_por_parede_fechada(cenario: Estado) -> None:
    """O ciano que atravessa uma parede fechada no arquivo é recusado.

    Args:
        cenario: Estado numa pasta temporária.
    """
    fechado = "dd7\nfc7\n\n0,0\n2,0\nEE\n"
    with pytest.raises(pytest.fail.Exception, match="parede fechada"):
        marcado_por_paredes_abertas(
            com_saida(cenario, saida(grade()), fechado)
        )


def test_caminho_marcado_mais_longo(cenario: Estado) -> None:
    """O ciano mais longo que a BFS é recusado, mas liga entrada e saída.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(volta()), ANEL, ["WIDTH=2", "HEIGHT=2"])
    marcado_por_paredes_abertas(cenario)
    with pytest.raises(pytest.fail.Exception, match="3 passos.*dá 1"):
        marcado_mais_curto(cenario)


def test_nova_renderizacao_abaixo(cenario: Estado) -> None:
    """Duas exibições seguidas do menu, sem limpar a tela, passam.

    Args:
        cenario: Estado numa pasta temporária.
    """
    nova_abaixo_da_anterior(com_saida(cenario, saida(grade(), grade())))


@pytest.mark.parametrize(
    ("texto", "mensagem"),
    [
        (saida(grade()), "1 renderização"),
        (saida(grade()) + saida(grade()).replace("\n", "\n\x1b[2J", 1),
         "limpar a tela"),
        (saida(grade()) + saida(grade()).replace("\n", "\n\x1bc", 1),
         "não são SGR.*x1bc"),
        (saida(grade()) + saida(grade()).replace("\n", "\n\x1b7", 1),
         "não são SGR.*x1b7"),
        (saida(grade()) + "\n" + desenhar(grade()), "não é seguida do menu"),
    ],
    ids=["uma só", "limpa a tela", "ESC c", "guarda o cursor",
         "sem menu no fim"],
)
def test_nova_renderizacao_com_defeito(
    cenario: Estado, texto: str, mensagem: str
) -> None:
    """Sem segunda exibição, com a tela limpa ou sem menu, falha.

    Args:
        cenario: Estado numa pasta temporária.
        texto: Saída padrão.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        nova_abaixo_da_anterior(com_saida(cenario, texto))


def test_labirinto_diferente(cenario: Estado) -> None:
    """Paredes diferentes entre as duas últimas exibições passam.

    Args:
        cenario: Estado numa pasta temporária.
    """
    outra = com_simbolo(grade(LARANJA), SUL_DE_1_0, "━")
    diferente_do_anterior(com_saida(cenario, saida(grade(), outra)))


FECHADA_EM_PARTE = com_simbolo(grade(), [(2, 6)], "━")


@pytest.mark.parametrize(
    ("texto", "mensagem"),
    [
        (saida(grade()), "1 renderização"),
        (saida(com_simbolo(grade(), SUL_DE_1_0, "━"), grade(caminho=False),
               grade(AZUL)), "mesmas paredes"),
        (saida(FECHADA_EM_PARTE, grade()), "penúltima renderização.*parte"),
    ],
    ids=["uma só", "mesmas paredes em outra cor", "parede em parte"],
)
def test_labirinto_igual(cenario: Estado, texto: str, mensagem: str) -> None:
    """A cor e o caminho não contam: só as paredes diferenciam.

    Args:
        cenario: Estado numa pasta temporária.
        texto: Saída padrão.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        diferente_do_anterior(com_saida(cenario, texto))


@pytest.mark.parametrize(
    ("elemento", "cor"),
    [
        ("entrada", "magenta"),
        ("saída", "vermelho"),
        ("células do caminho", "ciano"),
        ("passagens do caminho", "ciano"),
        ("42", "cinza"),
        ("paredes", "grafite"),
    ],
    ids=["entrada", "saída", "células", "passagens", "42", "paredes"],
)
def test_elemento_com_a_cor(cenario: Estado, elemento: str, cor: str) -> None:
    """Cada elemento do exemplo tem a cor da I02 e só ele tem essa cor.

    Args:
        cenario: Estado numa pasta temporária.
        elemento: Elemento conferido.
        cor: Cor esperada.
    """
    com_saida(cenario, saida(grade(caminho=False), grade()))
    elemento_tem_a_cor(cenario, elemento, cor)
    if elemento not in ("células do caminho", "passagens do caminho"):
        cor_so_no_elemento(cenario, cor, elemento)


@pytest.mark.parametrize(
    ("desenho", "elemento", "cor", "mensagem"),
    [
        (grade(), "paredes", "laranja", "não têm laranja no texto"),
        (grade(caminho=False), "células do caminho", "ciano",
         "não têm ciano no texto"),
        (com_fundo(grade(), 1, 7, GRAFITE), "passagens do caminho",
         "ciano", None),
        (com_texto(grade(), 1, 2, MAGENTA), "entrada", "magenta", None),
        (com_fundo(grade(), 1, 2, BRANCO), "entrada", "magenta",
         "1 de 3 posições de \"entrada\" não têm magenta no fundo"),
        (grade(), "corredor", "ciano", "não existe"),
        (grade(), "entrada", "roxo", "os válidos são: branco"),
    ],
    ids=["outra cor", "caminho oculto", "fundo não conta no caminho",
         "texto não conta na entrada", "entrada em parte",
         "elemento inválido", "cor inválida"],
)
def test_elemento_sem_a_cor(
    cenario: Estado,
    desenho: Tela,
    elemento: str,
    cor: str,
    mensagem: str | None,
) -> None:
    """Posição com outra cor na camada do elemento derruba o passo.

    A cor que só aparece na outra camada não muda o resultado: None diz
    que o passo passa.

    Args:
        cenario: Estado numa pasta temporária.
        desenho: Última exibição.
        elemento: Elemento conferido.
        cor: Cor esperada.
        mensagem: Trecho esperado na falha, ou None quando passa.
    """
    com_saida(cenario, saida(grade(), desenho))
    if mensagem is None:
        elemento_tem_a_cor(cenario, elemento, cor)
        return
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        elemento_tem_a_cor(cenario, elemento, cor)


def test_elemento_vazio(cenario: Estado) -> None:
    """Um labirinto sem células F não tem "42".

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(grade()), "d17\nec7\n\n0,0\n2,0\nEE\n")
    with pytest.raises(pytest.fail.Exception, match='não tem "42"'):
        elemento_tem_a_cor(cenario, "42", "cinza")


@pytest.mark.parametrize(
    ("desenho", "cor", "elemento", "mensagem"),
    [
        (grade(), "ciano", "células do caminho", "8 posições fora"),
        (grade(), "branco", "entrada", "fora de \"entrada\""),
        (com_texto(grade(), 0, 0, CINZA), "cinza", "42",
         "1 posições fora de \"42\": linha 0, coluna 0"),
        (com_texto(grade(), 3, 6, CINZA), "cinza", "42", None),
        (grade(), "azul", "lado", "não existe"),
    ],
    ids=["passagens fora", "cor em outro elemento", "texto conta fora",
         "texto de espaço não conta", "elemento inválido"],
)
def test_cor_fora_do_elemento(
    cenario: Estado,
    desenho: Tela,
    cor: str,
    elemento: str,
    mensagem: str | None,
) -> None:
    """A cor que aparece fora do elemento derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        desenho: Última exibição.
        cor: Cor conferida.
        elemento: Único elemento que pode ter a cor.
        mensagem: Trecho esperado na falha, ou None quando passa.
    """
    com_saida(cenario, saida(desenho))
    if mensagem is None:
        cor_so_no_elemento(cenario, cor, elemento)
        return
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        cor_so_no_elemento(cenario, cor, elemento)


def test_nenhuma_posicao_com_a_cor(cenario: Estado) -> None:
    """Sem ciano na última exibição, mesmo com ciano na anterior, passa.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(grade(), grade(caminho=False)), None)
    nenhuma_posicao_com_a_cor(cenario, "ciano")
    with pytest.raises(pytest.fail.Exception, match="magenta aparece em 3"):
        nenhuma_posicao_com_a_cor(cenario, "magenta")
    with pytest.raises(pytest.fail.Exception, match="não existe"):
        nenhuma_posicao_com_a_cor(cenario, "preto")


@pytest.mark.parametrize(
    ("digito", "paredes"),
    [
        ("f", "Norte, Leste, Sul e Oeste"),
        ("c", "Sul e Oeste"),
        ("1", "Norte"),
        ("D", "Norte, Sul e Oeste"),
    ],
    ids=["f", "c", "1", "maiúscula"],
)
def test_celulas_do_digito(cenario: Estado, digito: str, paredes: str) -> None:
    """Cada célula com o dígito mostra exatamente as paredes dele.

    Args:
        cenario: Estado numa pasta temporária.
        digito: Dígito do arquivo de saída.
        paredes: Paredes esperadas.
    """
    celulas_do_digito(com_saida(cenario, saida(grade())), digito, paredes)


@pytest.mark.parametrize(
    ("desenho", "digito", "paredes", "mensagem"),
    [
        (grade(), "f", "Norte e Sul", "esperadas Norte, Sul"),
        (com_simbolo(grade(), [(3, 4)], " "), "f",
         "Norte, Leste, Sul e Oeste",
         "aparece com as paredes Norte, Sul, Oeste"),
        (grade(), "5", "Norte e Sul", 'não tem célula de dígito "5"'),
        (grade(), "g", "nenhuma", "não é um dígito"),
        (grade(), "f", "Cima", "não existe"),
        (com_simbolo(grade(), [(4, 2)], " "), "f",
         "Norte, Leste, Sul e Oeste", "só em parte"),
    ],
    ids=["paredes erradas", "parede ausente no desenho", "dígito ausente",
         "dígito inválido", "direção inválida", "parede em parte"],
)
def test_celulas_do_digito_com_defeito(
    cenario: Estado, desenho: Tela, digito: str, paredes: str, mensagem: str
) -> None:
    """Paredes diferentes, dígito ausente ou valores inválidos falham.

    Args:
        cenario: Estado numa pasta temporária.
        desenho: Caracteres exibidos.
        digito: Dígito do arquivo de saída.
        paredes: Paredes esperadas.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        celulas_do_digito(com_saida(cenario, saida(desenho)), digito, paredes)


@pytest.mark.parametrize(
    ("arquivo", "mensagem"),
    [(None, "não existe ou não se lê"), ("xyz\n", "não se lê")],
    ids=["ausente", "ilegível"],
)
def test_sem_arquivo_de_saida(
    cenario: Estado, arquivo: str | None, mensagem: str
) -> None:
    """As propriedades que citam o arquivo falham sem ele.

    Args:
        cenario: Estado numa pasta temporária.
        arquivo: Conteúdo do OUTPUT_FILE.
        mensagem: Trecho esperado na falha.
    """
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        labirinto_atual(com_saida(cenario, saida(grade()), arquivo))


def test_tamanho_diferente_do_arquivo(cenario: Estado) -> None:
    """Desenho e arquivo de tamanhos diferentes derrubam o passo.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(grade()), ANEL)
    with pytest.raises(pytest.fail.Exception, match="3x2 células.*2x2"):
        paredes_do_arquivo(cenario)


@pytest.mark.parametrize(
    ("config", "mensagem"),
    [(None, "não tem config"), (["WIDTH=3"], "inteiros")],
    ids=["sem config", "sem HEIGHT"],
)
def test_tamanho_do_config(
    cenario: Estado, config: list[str] | None, mensagem: str
) -> None:
    """WIDTH e HEIGHT vêm do config do cenário.

    Args:
        cenario: Estado numa pasta temporária.
        config: Linhas do config, ou None.
        mensagem: Trecho esperado na falha.
    """
    cenario.config = None if config is None else Config(config)
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        tamanho_do_config(cenario)


def sessao_com_cores(
    cenario: Estado, cores: list[Rgb], envios: list[str]
) -> None:
    """Abre o programa falso, que exibe uma cor de paredes por exibição.

    Args:
        cenario: Estado numa pasta temporária.
        cores: Cor das paredes da primeira exibição e de cada resposta.
        envios: Linhas enviadas ao menu.
    """
    cenario.config = Config(list(CONFIG))
    exibicoes = [saida(grade(cor)) for cor in cores]
    programa_iniciado(cenario, programa_falso(cenario.cwd, exibicoes))
    envio_ao_menu(cenario, envios)


def test_paredes_em_rodizio(cenario: Estado) -> None:
    """Grafite, laranja, verde, azul e de volta ao grafite a cada opção 3.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cores = [GRAFITE, LARANJA, LARANJA, VERDE, AZUL, GRAFITE]
    sessao_com_cores(cenario, cores, ["3", "1", "3", "3", "3"])
    paredes_em_rodizio(cenario)


def test_paredes_fora_do_rodizio(cenario: Estado) -> None:
    """Uma regeneração que troca a cor quebra o rodízio.

    Args:
        cenario: Estado numa pasta temporária.
    """
    sessao_com_cores(cenario, [GRAFITE, LARANJA, VERDE], ["3", "1"])
    with pytest.raises(pytest.fail.Exception, match="depois de '1'"):
        paredes_em_rodizio(cenario)


def test_rodizio_sem_sessao(cenario: Estado) -> None:
    """Fora de uma sessão não há as opções enviadas para comparar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não há sessão"):
        paredes_em_rodizio(com_saida(cenario, saida(grade())))
