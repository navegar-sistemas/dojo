"""Testes dos passos que conferem a renderização no terminal."""

from collections.abc import Callable

import pytest

from autoteste.desenho import (
    AMARELO,
    ARQUIVO,
    AZUL,
    BRANCO,
    CIANO,
    CINZA,
    CONFIG,
    MAGENTA,
    TEXTO_DO_MENU,
    VERDE,
    VERMELHO,
    desenhar,
    grade,
    saida,
)
from autoteste.falso import programa_falso
from step_defs.interacao import envio_ao_menu, programa_iniciado
from step_defs.renderizacao import (
    caminho_do_arquivo_em_ciano,
    celulas_do_digito,
    cinco_cores,
    cor_so_no_elemento,
    cores_de_fundo,
    diferente_do_anterior,
    elemento_tem_a_cor,
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
    posicoes_da_largura,
    seguidas_do_menu,
    so_ascii,
    tamanho_do_config,
    termina_com_reset,
)
from suporte.config import Config
from suporte.estado import Estado, Execucao
from suporte.render import Cor
from suporte.sessao import PROMPT

PAREDE = "\x1b[47m  \x1b[0m"
Passo = Callable[[Estado], None]
Grade = list[list[Cor]]

# Labirinto 2x2 em anel: a BFS liga (0,0) a (1,0) em 1 passo; o ciano dá a
# volta por baixo, em 3.
ANEL = "93\nc6\n\n0,0\n1,0\nE\n"
VOLTA: Grade = [
    [BRANCO] * 5,
    [BRANCO, MAGENTA, None, VERMELHO, BRANCO],
    [BRANCO, CIANO, BRANCO, CIANO, BRANCO],
    [BRANCO, CIANO, CIANO, CIANO, BRANCO],
    [BRANCO] * 5,
]


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


def trocar(fundos: Grade, linha: int, coluna: int, cor: Cor) -> Grade:
    """Cópia da grade de fundos com uma posição trocada.

    Args:
        fundos: Grade original.
        linha: Linha da posição.
        coluna: Coluna da posição.
        cor: Novo fundo.

    Returns:
        A grade nova.
    """
    copia = [list(linha_de_fundos) for linha_de_fundos in fundos]
    copia[linha][coluna] = cor
    return copia


def test_linhas_coloridas_terminam_com_reset(cenario: Estado) -> None:
    """Linhas sem cor, como o menu, não precisam do reset.

    Args:
        cenario: Estado numa pasta temporária.
    """
    saida_padrao = f"{PAREDE}{PAREDE}\n{PAREDE}\n1. Regenerate\n{PROMPT}"
    linhas_com_reset(com_saida(cenario, saida_padrao))


@pytest.mark.parametrize(
    "linha",
    ["\x1b[47m  ", f"{PAREDE} ", f"{PAREDE}\x1b[47m  "],
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
    posicoes_da_largura,
    so_ascii,
    cores_de_fundo,
    termina_com_reset,
    paredes_do_arquivo,
    pontas_do_rodape,
    caminho_do_arquivo_em_ciano,
    marcado_por_paredes_abertas,
    marcado_mais_curto,
    cinco_cores,
]


@pytest.mark.parametrize("passo", BONS, ids=lambda passo: passo.__name__)
def test_renderizacao_do_exemplo(cenario: Estado, passo: Passo) -> None:
    """A exibição do labirinto de exemplo cumpre cada propriedade.

    Args:
        cenario: Estado numa pasta temporária.
        passo: Propriedade conferida.
    """
    passo(com_saida(cenario, saida(grade(caminho=False), grade())))


SEM_MENU = "\n" + desenhar(grade()) + "\n"
OUTRA_ALTURA = ["WIDTH=3", "HEIGHT=3"]
OUTRA_LARGURA = ["WIDTH=4", "HEIGHT=2"]
DEFEITOS: list[tuple[Passo, str, list[str], str]] = [
    (seguidas_do_menu, SEM_MENU, CONFIG, "sem o menu"),
    (seguidas_do_menu, TEXTO_DO_MENU, CONFIG, "nenhuma renderização"),
    (linhas_da_altura, saida(grade()), OUTRA_ALTURA, "esperadas 7"),
    (posicoes_da_largura, saida(grade()), OUTRA_LARGURA, "esperadas 9"),
    (posicoes_da_largura, saida(grade()).replace("m  ", "m   ", 1), CONFIG,
     "número ímpar"),
    (so_ascii, saida(grade()).replace("  ", "\u2588\u2588", 1), CONFIG,
     "fora do ASCII"),
    (cores_de_fundo, saida(grade()).replace("[47m", "[37m", 1), CONFIG,
     "'37'"),
    (cores_de_fundo, saida(grade()).replace("m  ", "m##", 1), CONFIG,
     "não são espaço"),
    (cores_de_fundo, saida([[None] * 7] * 5), CONFIG,
     "nenhuma posição desenhada tem cor"),
    (termina_com_reset, saida(grade()) + "\x1b[47m", CONFIG,
     "'\\\\x1b\\[47m'"),
    (termina_com_reset, TEXTO_DO_MENU, CONFIG, "não tem sequência"),
    (paredes_do_arquivo, saida(trocar(grade(), 2, 3, BRANCO)), CONFIG,
     "célula \\(1, 0\\)"),
    (pontas_do_rodape, saida(trocar(grade(), 3, 3, MAGENTA)), CONFIG,
     "magenta deveria estar só"),
    (caminho_do_arquivo_em_ciano, saida(grade(caminho=False)), CONFIG,
     "faltam 3"),
    (caminho_do_arquivo_em_ciano, saida(trocar(grade(), 3, 3, CIANO)),
     CONFIG, "sobram 1"),
    (marcado_por_paredes_abertas, saida(grade(caminho=False)), CONFIG,
     "0 passagens ciano"),
    (cinco_cores, saida(grade(caminho=False)), CONFIG,
     '"células do caminho" deveria ter uma única cor'),
    (cinco_cores, saida(trocar(grade(), 3, 1, None)), CONFIG,
     '"células do 42" deveria ter uma única cor'),
    (cinco_cores, saida(trocar(grade(), 1, 3, CINZA)), CONFIG,
     "cores repetidas"),
]


@pytest.mark.parametrize(
    ("passo", "texto", "config", "mensagem"),
    DEFEITOS,
    ids=[
        "menu ausente", "sem renderização", "altura", "largura",
        "caractere ímpar", "não ASCII", "cor de frente", "caractere visível",
        "sem fundo", "termina colorido", "sem sequência", "parede a mais",
        "entrada em outro lugar", "caminho oculto", "ciano a mais",
        "sem corrente", "caminho sem cor", "42 sem cor",
        "caminho na cor do 42",
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
    com_saida(cenario, saida(VOLTA), ANEL, ["WIDTH=2", "HEIGHT=2"])
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
         "limpam a tela"),
        (saida(grade()) + "\n" + desenhar(grade()), "não é seguida do menu"),
    ],
    ids=["uma só", "limpa a tela", "sem menu no fim"],
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
    outra = trocar(grade(AMARELO), 2, 3, AMARELO)
    diferente_do_anterior(com_saida(cenario, saida(grade(), outra)))


@pytest.mark.parametrize(
    ("texto", "mensagem"),
    [
        (saida(grade()), "1 renderização"),
        (saida(trocar(grade(), 2, 3, BRANCO), grade(caminho=False),
               grade(AZUL)), "mesmas paredes"),
    ],
    ids=["uma só", "mesmas paredes em outra cor"],
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
        ("células do 42", "cinza"),
        ("paredes", "branco"),
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
    ("elemento", "cor", "mensagem"),
    [
        ("paredes", "amarelo", "não são amarelo"),
        ("células do caminho", "ciano", "não são ciano"),
        ("corredor", "ciano", "não existe"),
        ("entrada", "roxo", "os válidos são: branco"),
    ],
    ids=["outra cor", "caminho oculto", "elemento inválido", "cor inválida"],
)
def test_elemento_sem_a_cor(
    cenario: Estado, elemento: str, cor: str, mensagem: str
) -> None:
    """Posição com outra cor ou nome fora da lista derrubam o passo.

    Args:
        cenario: Estado numa pasta temporária.
        elemento: Elemento conferido.
        cor: Cor esperada.
        mensagem: Trecho esperado na falha.
    """
    com_saida(cenario, saida(grade(), grade(caminho=False)))
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        elemento_tem_a_cor(cenario, elemento, cor)


def test_elemento_vazio(cenario: Estado) -> None:
    """Um labirinto sem células F não tem "células do 42".

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(grade()), "d17\nec7\n\n0,0\n2,0\nEE\n")
    with pytest.raises(pytest.fail.Exception, match='não tem "células do 42"'):
        elemento_tem_a_cor(cenario, "células do 42", "cinza")


@pytest.mark.parametrize(
    ("cor", "elemento", "mensagem"),
    [
        ("ciano", "células do caminho", "2 posições fora"),
        ("branco", "entrada", "fora de \"entrada\""),
        ("azul", "lado", "não existe"),
    ],
    ids=["passagens fora", "cor em outro elemento", "elemento inválido"],
)
def test_cor_fora_do_elemento(
    cenario: Estado, cor: str, elemento: str, mensagem: str
) -> None:
    """A cor que aparece fora do elemento derruba o passo.

    Args:
        cenario: Estado numa pasta temporária.
        cor: Cor conferida.
        elemento: Único elemento que pode ter a cor.
        mensagem: Trecho esperado na falha.
    """
    com_saida(cenario, saida(grade()))
    with pytest.raises(pytest.fail.Exception, match=mensagem):
        cor_so_no_elemento(cenario, cor, elemento)


def test_nenhuma_posicao_com_a_cor(cenario: Estado) -> None:
    """Sem ciano na última exibição, mesmo com ciano na anterior, passa.

    Args:
        cenario: Estado numa pasta temporária.
    """
    com_saida(cenario, saida(grade(), grade(caminho=False)), None)
    nenhuma_posicao_com_a_cor(cenario, "ciano")
    with pytest.raises(pytest.fail.Exception, match="magenta aparece em 1"):
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
        (trocar(grade(), 3, 2, None), "f", "Norte, Leste, Sul e Oeste",
         "aparece com as paredes Norte, Sul, Oeste"),
        (grade(), "5", "Norte e Sul", 'não tem célula de dígito "5"'),
        (grade(), "g", "nenhuma", "não é um dígito"),
        (grade(), "f", "Cima", "não existe"),
        (trocar(grade(), 0, 0, None), "f", "nenhuma", "sem cor"),
    ],
    ids=["paredes erradas", "parede ausente no desenho", "dígito ausente",
         "dígito inválido", "direção inválida", "canto sem cor"],
)
def test_celulas_do_digito_com_defeito(
    cenario: Estado, desenho: Grade, digito: str, paredes: str, mensagem: str
) -> None:
    """Paredes diferentes, dígito ausente ou valores inválidos falham.

    Args:
        cenario: Estado numa pasta temporária.
        desenho: Grade de fundos exibida.
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
    cenario: Estado, cores: list[int], envios: list[str]
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
    """Branco, amarelo, verde, azul e de volta ao branco a cada opção 3.

    Args:
        cenario: Estado numa pasta temporária.
    """
    cores = [BRANCO, AMARELO, AMARELO, VERDE, AZUL, BRANCO]
    sessao_com_cores(cenario, cores, ["3", "1", "3", "3", "3"])
    paredes_em_rodizio(cenario)


def test_paredes_fora_do_rodizio(cenario: Estado) -> None:
    """Uma regeneração que troca a cor quebra o rodízio.

    Args:
        cenario: Estado numa pasta temporária.
    """
    sessao_com_cores(cenario, [BRANCO, AMARELO, VERDE], ["3", "1"])
    with pytest.raises(pytest.fail.Exception, match="depois de '1'"):
        paredes_em_rodizio(cenario)


def test_rodizio_sem_sessao(cenario: Estado) -> None:
    """Fora de uma sessão não há as opções enviadas para comparar.

    Args:
        cenario: Estado numa pasta temporária.
    """
    with pytest.raises(pytest.fail.Exception, match="não há sessão"):
        paredes_em_rodizio(com_saida(cenario, saida(grade())))
