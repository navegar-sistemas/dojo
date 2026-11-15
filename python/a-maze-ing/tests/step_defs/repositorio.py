"""Passos que preparam e conferem o repositório de entrega (project/)."""

import os
import random
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from suporte.config import CONFIG_BASE, VARIACOES, Config
from suporte.estado import PROJECT_DIR, TIMEOUT, Estado, Execucao
from suporte.tipos import TIPOS

# O clone e as consultas ao git não podem herdar a configuração de quem roda
# a suíte: o ignore global (inclusive o padrão em ~/.config/git/ignore, lido
# mesmo sem config) mascararia um .gitignore incompleto, um templateDir com
# info/exclude faria o mesmo no git init, e hooks ou assinatura obrigatória
# quebrariam o commit da cópia.
GIT = [
    "git",
    "-c", "core.excludesFile=/dev/null",
    "-c", "core.hooksPath=/dev/null",
    "-c", "commit.gpgsign=false",
    "-c", "user.name=suite",
    "-c", "user.email=suite@localhost",
]
VARIAVEIS_DO_GIT = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_TEMPLATE_DIR",
    "GIT_CONFIG",
    "GIT_CONFIG_PARAMETERS",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_SYSTEM",
)
REMOTO = "AMAZEING_REMOTE"
COPIADOS = ("a_maze_ing.py", "amazeing", "config.txt")
DEPENDEM_DE_PERMISSAO = {
    "sem permissão de leitura",
    "diretório sem permissão de escrita",
}
ESPECIAIS = {
    "inexistente",
    "diretório",
    "diretório pai criado",
    "diretório sem permissão de escrita",
    "pasta com a_maze_ing.py, amazeing/ e config.txt",
}


def ambiente_do_git() -> dict[str, str]:
    """Ambiente do processo sem a configuração global e de sistema do git.

    Returns:
        Cópia de os.environ sem as variáveis que redirecionam o git e com
        GIT_CONFIG_GLOBAL=/dev/null e GIT_CONFIG_NOSYSTEM=1.
    """
    ambiente = {
        chave: valor for chave, valor in os.environ.items()
        if chave not in VARIAVEIS_DO_GIT
        and not chave.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))
    }
    ambiente["GIT_CONFIG_GLOBAL"] = "/dev/null"
    ambiente["GIT_CONFIG_NOSYSTEM"] = "1"
    return ambiente


@dataclass
class Instalacao:
    """Resultado do ``make install``, feito uma vez por sessão de testes."""

    execucao: Execucao | None = None

    def garantir(self) -> Execucao:
        """Roda ``make install`` na primeira chamada e reaproveita depois.

        Returns:
            A execução do ``make install``.
        """
        if self.execucao is None:
            self.execucao = Estado().executar("make install")
        return self.execucao


@pytest.fixture(scope="session")
def instalacao() -> Instalacao:
    """Instalação compartilhada por todos os cenários da sessão.

    Returns:
        A instalação, ainda sem o ``make install`` executado.
    """
    return Instalacao()


def git(
    argumentos: list[str], pasta: Path
) -> subprocess.CompletedProcess[str]:
    """Roda o git com a configuração isolada da suíte.

    Args:
        argumentos: Subcomando e argumentos, sem o "git".
        pasta: Pasta onde o comando roda.

    Returns:
        O processo terminado, com stdout e stderr capturados.
    """
    return subprocess.run(
        [*GIT, *argumentos],
        cwd=pasta,
        env=ambiente_do_git(),
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def git_ou_falha(argumentos: list[str], pasta: Path) -> str:
    """Roda o git e falha o teste se ele terminar com erro.

    Args:
        argumentos: Subcomando e argumentos, sem o "git".
        pasta: Pasta onde o comando roda.

    Returns:
        A saída padrão do comando.
    """
    processo = git(argumentos, pasta)
    if processo.returncode != 0:
        pytest.fail(
            f"'git {' '.join(argumentos)}' terminou com código "
            f"{processo.returncode}\n{processo.stdout}{processo.stderr}"
        )
    return processo.stdout


def falhar_se_terminou_mal(
    processo: subprocess.CompletedProcess[bytes], comando: str
) -> None:
    """Falha o teste se o processo terminou com código diferente de 0.

    Args:
        processo: Processo terminado, com stderr capturado.
        comando: Comando para a mensagem.
    """
    if processo.returncode != 0:
        pytest.fail(
            f"'{comando}' terminou com código {processo.returncode}\n"
            + processo.stderr.decode("utf-8", errors="replace")
        )


def clonar_limpo(destino: Path) -> None:
    """Recria em destino o repositório de entrega com o que está commitado.

    A raiz do git é o monorepo dojo; ``git archive HEAD`` rodado em
    project/ extrai só essa pasta, como está no último commit (mudanças
    não commitadas ficam de fora), e o git próprio da cópia reproduz o
    clone do repositório da instituição.

    Args:
        destino: Pasta vazia que recebe a cópia.
    """
    arquivo = subprocess.run(
        [*GIT, "archive", "--format=tar", "HEAD"],
        cwd=PROJECT_DIR,
        env=ambiente_do_git(),
        capture_output=True,
        timeout=TIMEOUT,
    )
    falhar_se_terminou_mal(arquivo, f"git archive HEAD em {PROJECT_DIR}")
    extracao = subprocess.run(
        ["tar", "-x", "-C", str(destino)],
        input=arquivo.stdout,
        capture_output=True,
        timeout=TIMEOUT,
    )
    falhar_se_terminou_mal(extracao, f"tar -x -C {destino}")
    git_ou_falha(["init", "-q"], destino)
    git_ou_falha(["add", "-A"], destino)
    git_ou_falha(
        ["commit", "-q", "--allow-empty", "-m", "clone limpo"], destino
    )


def casar(estado: Estado, padrao: str) -> list[Path]:
    """Caminhos do repositório que casam com o padrão (aceita glob).

    Args:
        estado: Estado do cenário; o padrão é relativo a ``estado.cwd``.
        padrao: Caminho ou glob, com ou sem "/" no fim.

    Returns:
        Os caminhos existentes que casam.
    """
    return sorted(estado.cwd.glob(padrao.rstrip("/")))


@given(parsers.parse('o repositório no estado "{nome:Q}"', extra_types=TIPOS))
def repositorio_no_estado(
    estado: Estado, instalacao: Instalacao, tmp_path: Path, nome: str
) -> None:
    """Prepara o repositório no estado pedido.

    Args:
        estado: Estado do cenário.
        instalacao: Instalação da sessão.
        tmp_path: Pasta temporária do cenário.
        nome: "atual", "instalado", "clone limpo" ou "clone do remoto".
    """
    estado.cwd = PROJECT_DIR
    if nome == "atual":
        return
    if nome == "instalado":
        execucao = instalacao.garantir()
        if execucao.codigo != 0:
            pytest.fail(
                f"'{execucao.comando}' terminou com código {execucao.codigo}"
                f"\n{execucao.saida_padrao}{execucao.saida_erro}"
            )
        estado.caminhos_extras = [PROJECT_DIR / ".venv" / "bin"]
        return
    if nome == "clone limpo":
        clone = tmp_path / "clone"
        clone.mkdir()
        clonar_limpo(clone)
    elif nome == "clone do remoto":
        clone = tmp_path / "remoto"
        clonar_remoto(clone)
    else:
        pytest.fail(f'estado "{nome}" ainda não implementado')
    estado.cwd = clone
    estado.caminhos_extras = [clone / ".venv" / "bin"]


def clonar_remoto(destino: Path) -> None:
    """Clona em destino o repositório da URL em AMAZEING_REMOTE.

    Args:
        destino: Pasta que ainda não existe.
    """
    url = os.environ.get(REMOTO)
    if not url:
        pytest.skip(
            f"a variável de ambiente {REMOTO} não está definida ou está "
            "vazia; ela leva a URL do repositório de entrega"
        )
    git_ou_falha(
        ["clone", "-q", "--depth", "1", url, str(destino)], destino.parent
    )


@given(
    parsers.parse(
        'o arquivo "{arquivo:Q}" na raiz do repositório', extra_types=TIPOS
    )
)
def arquivo_na_raiz(estado: Estado, arquivo: str) -> None:
    """Confere que o arquivo existe no repositório.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório; aceita glob.
    """
    if not casar(estado, arquivo):
        pytest.fail(f'"{arquivo}" não existe em {estado.cwd}')


@when(parsers.parse('eu leio "{arquivo:Q}"', extra_types=TIPOS))
def eu_leio(estado: Estado, arquivo: str) -> None:
    """Seleciona os arquivos que os passos Então vão conferir.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório; aceita glob.
    """
    selecionados = [caminho for caminho in casar(estado, arquivo)
                    if caminho.is_file()]
    if not selecionados:
        pytest.fail(f'nenhum arquivo casa com "{arquivo}" em {estado.cwd}')
    estado.lido = selecionados


@given(
    parsers.parse(
        'o arquivo "{arquivo:Q}" {tem:TemLinha} que casa com a expressão '
        '"{regex:Q}"',
        extra_types=TIPOS,
    )
)
@then(
    parsers.parse(
        'o arquivo "{arquivo:Q}" {tem:TemLinha} que casa com a expressão '
        '"{regex:Q}"',
        extra_types=TIPOS,
    )
)
def arquivo_tem_linha(
    estado: Estado, arquivo: str, tem: str, regex: str
) -> None:
    """Procura a expressão nas linhas do arquivo (``re.search`` com ``re.M``).

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório.
        tem: "tem uma linha" ou "não tem nenhuma linha".
        regex: Expressão regular procurada.
    """
    caminho = estado.cwd / arquivo
    if not caminho.is_file():
        pytest.fail(f'"{arquivo}" não existe em {estado.cwd}')
    texto = caminho.read_text(encoding="utf-8")
    achado = re.search(regex, texto, re.M)
    if tem == "tem uma linha":
        assert achado, f'nenhuma linha de "{arquivo}" casa com {regex!r}'
    else:
        assert achado is None, (
            f'"{arquivo}" tem a linha {achado.group(0)!r}, que casa com '
            f"{regex!r}"
        )


@given(
    parsers.parse(
        'o caminho "{caminho:Q}" preparado como "{tipo:Q}"', extra_types=TIPOS
    )
)
def caminho_preparado(estado: Estado, caminho: str, tipo: str) -> None:
    """Prepara o caminho; a fixture estado desfaz tudo no fim.

    Args:
        estado: Estado do cenário.
        caminho: Caminho relativo ao repositório.
        tipo: Uma das chaves de ESPECIAIS ou de CONTEUDOS.
    """
    preparar(estado, estado.cwd / caminho, tipo)


def _texto(linhas: list[str]) -> bytes:
    """Linhas de config como bytes UTF-8, uma por linha.

    Args:
        linhas: Linhas do config, sem a quebra de linha.

    Returns:
        O conteúdo do arquivo.
    """
    return ("\n".join(linhas) + "\n").encode("utf-8")


# Conteúdo de cada tipo de arquivo preparado. O primeiro byte 0xFF nunca
# aparece em UTF-8, então os bytes aleatórios são sempre inválidos.
CONTEUDOS: dict[str, Callable[[], bytes]] = {
    "vazio": lambda: b"",
    "bytes binários aleatórios": (
        lambda: b"\xff" + random.Random(0).randbytes(255)
    ),
    "só espaços e tabulações": lambda: b"  \t \n\t\t  \n \n",
    "BOM UTF-8 + config base": lambda: b"\xef\xbb\xbf" + _texto(CONFIG_BASE),
    "config base com WIDTH de 100000 dígitos": lambda: _texto(
        ["WIDTH=" + "9" * 100000, *CONFIG_BASE[1:]]
    ),
    "só WÍDTH=20 e HEÍGHT=15, com acento": (
        lambda: _texto(["WÍDTH=20", "HEÍGHT=15"])
    ),
    "sem permissão de leitura": lambda: _texto(CONFIG_BASE),
    "não UTF-8": lambda: (
        "# configuração\n" + "\n".join(CONFIG_BASE) + "\n"
    ).encode("latin-1"),
}


def copiar_do_repositorio(origem: Path, alvo: Path) -> None:
    """Copia a_maze_ing.py, amazeing/ e config.txt para a pasta alvo.

    Args:
        origem: Raiz do repositório do cenário.
        alvo: Pasta já criada.
    """
    for nome in COPIADOS:
        if (origem / nome).is_dir():
            shutil.copytree(
                origem / nome,
                alvo / nome,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
        else:
            shutil.copy2(origem / nome, alvo / nome)


def preparar(estado: Estado, alvo: Path, tipo: str) -> None:
    """Prepara o alvo conforme o tipo.

    O original vai para a reserva, as pastas pai que faltam são criadas
    (menos em "inexistente") e o alvo deixa de receber o config automático
    do cenário e a proteção do OUTPUT_FILE antes de rodar o programa.

    Args:
        estado: Estado do cenário.
        alvo: Caminho absoluto.
        tipo: Uma das chaves de ESPECIAIS ou de CONTEUDOS.
    """
    if tipo not in ESPECIAIS and tipo not in CONTEUDOS:
        pytest.fail(f'tipo "{tipo}" ainda não implementado')
    if tipo in DEPENDEM_DE_PERMISSAO and os.geteuid() == 0:
        pytest.skip(
            f'o tipo "{tipo}" depende de chmod, que não barra o root; rode '
            "a suíte com um usuário comum"
        )
    if tipo == "pasta com a_maze_ing.py, amazeing/ e config.txt":
        faltando = [
            nome for nome in COPIADOS if not (estado.cwd / nome).exists()
        ]
        if faltando:
            pytest.fail(f"faltam em {estado.cwd}: {', '.join(faltando)}")
    if tipo != "inexistente":
        estado.criar_pastas(alvo.parent)
    estado.proteger(alvo)
    estado.sem_gravacao.add(alvo)
    if tipo in ("inexistente", "diretório pai criado"):
        return
    if tipo in CONTEUDOS:
        alvo.write_bytes(CONTEUDOS[tipo]())
        if tipo == "sem permissão de leitura":
            alvo.chmod(0)
        return
    alvo.mkdir()
    if tipo == "diretório sem permissão de escrita":
        alvo.chmod(0o500)
    elif tipo != "diretório":
        copiar_do_repositorio(estado.cwd, alvo)


@given(parsers.parse("o config {origem:Origem}", extra_types=TIPOS))
def config_de(estado: Estado, origem: str) -> None:
    """Carrega o config base ou o config.txt do repositório.

    Args:
        estado: Estado do cenário.
        origem: "base" ou "do repositório".
    """
    if origem == "base":
        estado.config = Config(list(CONFIG_BASE))
        return
    repositorio = estado.cwd / "config.txt"
    if not repositorio.is_file():
        pytest.fail(f"config.txt não existe em {estado.cwd}")
    estado.config = Config(
        repositorio.read_text(encoding="utf-8").splitlines()
    )


@given(
    parsers.parse('o config {origem:Origem} salvo em "{arquivo:Q}"',
                  extra_types=TIPOS)
)
def config_salvo_em(estado: Estado, origem: str, arquivo: str) -> None:
    """Carrega o config como em ``config_de`` e troca o destino.

    A gravação, num passo Quando, cria as pastas pai que faltam.

    Args:
        estado: Estado do cenário.
        origem: "base" ou "do repositório".
        arquivo: Destino relativo à pasta do cenário.
    """
    config_de(estado, origem)
    if estado.config is not None:
        estado.config.destino = arquivo


# O que cada situação de erro faz com o config e com o seu destino.
SITUACOES: dict[str, Callable[[Estado, Config], None]] = {
    "arquivo de configuração inexistente": lambda estado, config: preparar(
        estado, estado.cwd / config.destino, "inexistente"
    ),
    "arquivo de configuração sem permissão de leitura": (
        lambda estado, config: preparar(
            estado, estado.cwd / config.destino, "sem permissão de leitura"
        )
    ),
    "chave obrigatória ausente": lambda estado, config: config.sem("WIDTH"),
    "valor inválido": lambda estado, config: config.definir("WIDTH", "abc"),
    "parâmetros impossíveis": (
        lambda estado, config: config.definir("EXIT", "0,0")
    ),
    "OUTPUT_FILE num diretório inexistente": (
        lambda estado, config: config.definir(
            "OUTPUT_FILE", "diretorio_inexistente/maze.txt"
        )
    ),
}


@given(parsers.parse('a situação de erro "{situacao:Q}"', extra_types=TIPOS))
@when(parsers.parse('a situação de erro "{situacao:Q}"', extra_types=TIPOS))
def situacao_de_erro(estado: Estado, situacao: str) -> None:
    """Aplica a situação de erro ao config atual e ao seu destino.

    Args:
        estado: Estado do cenário.
        situacao: Uma das chaves de SITUACOES.
    """
    if estado.config is None:
        pytest.fail("a situação de erro precisa de um config antes")
    aplicar = SITUACOES.get(situacao)
    if aplicar is None:
        pytest.fail(
            f'situação "{situacao}" não existe; as válidas são: '
            f"{', '.join(SITUACOES)}"
        )
    aplicar(estado, estado.config)


@then(
    parsers.parse(
        'o caminho "{caminho:Q}" {situacao:EstadoCaminho}', extra_types=TIPOS
    )
)
def caminho_na_situacao(estado: Estado, caminho: str, situacao: str) -> None:
    """Confere a existência, o conteúdo ou a situação no git.

    Args:
        estado: Estado do cenário.
        caminho: Caminho relativo ao repositório; aceita glob nas
            situações de existência e conteúdo.
        situacao: Valor do tipo EstadoCaminho.
    """
    if situacao == "existe":
        if not casar(estado, caminho):
            pytest.fail(f'"{caminho}" não existe')
    elif situacao == "não existe":
        if casar(estado, caminho):
            pytest.fail(f'"{caminho}" existe')
    elif situacao == "não está vazio":
        if not any(
            (item.is_file() and item.stat().st_size > 0)
            or (item.is_dir() and any(item.iterdir()))
            for item in casar(estado, caminho)
        ):
            pytest.fail(f'"{caminho}" não existe ou está vazio')
    elif situacao == "está versionado no git":
        processo = git(["ls-files", "--error-unmatch", caminho], estado.cwd)
        if processo.returncode != 0:
            pytest.fail(f'"{caminho}" não está versionado no git')
    else:
        processo = git(["check-ignore", "-q", caminho], estado.cwd)
        if processo.returncode not in (0, 1):
            pytest.fail(f"git check-ignore falhou:\n{processo.stderr}")
        ignorado = processo.returncode == 0
        if ignorado != (situacao == "é ignorado pelo git"):
            pytest.fail(
                f'"{caminho}" {"é" if ignorado else "não é"} ignorado pelo '
                f"git em {estado.cwd}"
            )


def config_atual(estado: Estado) -> Config:
    """Config que um passo anterior carregou.

    Args:
        estado: Estado do cenário.

    Returns:
        O config do cenário.
    """
    if estado.config is None:
        pytest.fail("este passo precisa de um config carregado antes")
    return estado.config


def aplicar_pares(config: Config, pares: list[str]) -> None:
    """Aplica cada "CHAVE=valor" ao config, trocando ou acrescentando.

    Args:
        config: Config a alterar.
        pares: Itens no formato CHAVE=valor; o valor pode ser vazio.
    """
    for par in pares:
        chave, igual, valor = par.partition("=")
        if not igual or not chave:
            pytest.fail(f'"{par}" não está no formato CHAVE=valor')
        config.definir(chave, valor)


@given(parsers.parse("o config base com {pares:L}", extra_types=TIPOS))
def config_base_com(estado: Estado, pares: list[str]) -> None:
    """Parte do config base e aplica os pares.

    Args:
        estado: Estado do cenário.
        pares: Itens CHAVE=valor.
    """
    estado.config = Config(list(CONFIG_BASE))
    aplicar_pares(estado.config, pares)


@given(parsers.parse("o config com {pares:L}", extra_types=TIPOS))
def config_com(estado: Estado, pares: list[str]) -> None:
    """Aplica os pares ao config atual, depois de um Contexto.

    Args:
        estado: Estado do cenário.
        pares: Itens CHAVE=valor.
    """
    aplicar_pares(config_atual(estado), pares)


@given(parsers.parse('o config sem a chave "{chave:Q}"', extra_types=TIPOS))
def config_sem_chave(estado: Estado, chave: str) -> None:
    """Remove as linhas da chave.

    Args:
        estado: Estado do cenário.
        chave: Nome da chave, sem diferenciar maiúsculas.
    """
    config_atual(estado).sem(chave)


@given(
    parsers.parse(
        'o config com a linha {n:d} trocada por "{linha:Q}"',
        extra_types=TIPOS,
    )
)
def config_com_linha_trocada(estado: Estado, n: int, linha: str) -> None:
    """Troca a linha número n, contada a partir de 1.

    Args:
        estado: Estado do cenário.
        n: Número da linha.
        linha: Linha nova.
    """
    try:
        config_atual(estado).trocar_linha(n, linha)
    except ValueError as erro:
        pytest.fail(str(erro))


@given(
    parsers.parse(
        'o config com a linha da chave "{chave:Q}" trocada por "{linha:Q}"',
        extra_types=TIPOS,
    )
)
def config_com_linha_da_chave(
    estado: Estado, chave: str, linha: str
) -> None:
    """Troca a linha da chave; texto vazio remove a linha.

    Args:
        estado: Estado do cenário.
        chave: Nome da chave.
        linha: Linha nova, ou "".
    """
    try:
        config_atual(estado).trocar_linha_da_chave(chave, linha)
    except ValueError as erro:
        pytest.fail(str(erro))


@given(
    parsers.parse(
        'o config com a linha "{linha:Q}" {posicao:Pos}', extra_types=TIPOS
    )
)
def config_com_linha(estado: Estado, linha: str, posicao: str) -> None:
    """Insere a linha no início ou acrescenta no fim.

    Args:
        estado: Estado do cenário.
        linha: Linha nova.
        posicao: "inserida no início" ou "acrescentada no fim".
    """
    config_atual(estado).inserir(linha, posicao == "inserida no início")


@given(
    parsers.parse(
        'o config escrito com a variação "{variacao:Q}"', extra_types=TIPOS
    )
)
def config_com_variacao(estado: Estado, variacao: str) -> None:
    """Marca a variação que a gravação aplica ao texto do config.

    Args:
        estado: Estado do cenário.
        variacao: Uma das variações de VARIACOES.
    """
    if variacao not in VARIACOES:
        pytest.fail(
            f'variação "{variacao}" não existe; as válidas são: '
            f"{', '.join(VARIACOES)}"
        )
    config_atual(estado).variacao = variacao
