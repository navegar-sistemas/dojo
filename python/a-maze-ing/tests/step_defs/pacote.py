"""Passos dos virtualenvs, do pacote mazegen-* e dos arquivos de texto."""

import ast
import csv
import io
import re
import shlex
from collections.abc import Callable
from email.parser import Parser
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when

from step_defs.repositorio import casar, git, git_ou_falha
from suporte.estado import TIMEOUT, Estado, Execucao
from suporte.modulo import CLASSE, MODULO
from suporte.pacote import (
    Pacote,
    abrir_pacote,
    bin_do,
    criar_virtualenv,
    nome_e_versao,
    rodar_no_virtualenv,
    secao_markdown,
    versao_do_pyproject,
)
from suporte.tipos import TIPOS

CAMPOS = ("Name", "Version", "License-Expression")
README = "README.md"
LICENCA = "LICENSE.md"
PYPROJECT = "pyproject.toml"
INIT = f"{MODULO}/__init__.py"
ARQUIVOS_DO_DIST_INFO = ("METADATA", "WHEEL", "RECORD")
CAMPOS_DO_WHEEL = ("Wheel-Version", "Root-Is-Purelib")
ARQUIVOS_DO_SDIST = ("PKG-INFO", PYPROJECT)
PASTA_DOS_VENVS = "virtualenvs"
PASTA_DAS_INSTALACOES = "instalacoes"

Propriedade = Callable[[Estado, list[Pacote], Path], None]


def exigir_sucesso(execucao: Execucao) -> None:
    """Falha o teste se o comando estourou o tempo ou terminou com erro.

    Args:
        execucao: Execução de um comando de preparação.
    """
    if execucao.estourou:
        pytest.fail(
            f"'{execucao.comando}' estourou o tempo limite de {TIMEOUT} s\n"
            f"{execucao.saida_padrao}{execucao.saida_erro}"
        )
    if execucao.codigo != 0:
        pytest.fail(
            f"'{execucao.comando}' terminou com código {execucao.codigo}\n"
            f"{execucao.saida_padrao}{execucao.saida_erro}"
        )


def novo_virtualenv(estado: Estado, destino: Path) -> None:
    """Cria o virtualenv e falha o teste se a criação der errado.

    Args:
        estado: Estado do cenário, cujo PATH dá o python3.
        destino: Pasta do virtualenv, que ainda não existe.
    """
    destino.parent.mkdir(parents=True, exist_ok=True)
    exigir_sucesso(criar_virtualenv(destino, estado.caminhos_extras))


@given(
    parsers.parse(
        'um virtualenv novo "{venv:Q}" em que rodou {comandos:L}',
        extra_types=TIPOS,
    )
)
def virtualenv_novo(
    estado: Estado, tmp_path: Path, venv: str, comandos: list[str]
) -> None:
    """Cria um virtualenv fora do repositório e roda os comandos nele.

    Os comandos rodam na raiz do repositório do cenário, com o bin do
    virtualenv na frente do PATH, e precisam terminar com código 0.

    Args:
        estado: Estado do cenário.
        tmp_path: Pasta temporária do cenário, que recebe o virtualenv.
        venv: Nome do virtualenv no cenário.
        comandos: Comandos, na ordem do passo.
    """
    if venv in estado.venvs:
        pytest.fail(f'o virtualenv "{venv}" já foi criado neste cenário')
    destino = tmp_path / PASTA_DOS_VENVS / venv
    novo_virtualenv(estado, destino)
    for comando in comandos:
        exigir_sucesso(rodar_no_virtualenv(destino, estado.cwd, comando))
    estado.venvs[venv] = destino


@given(
    parsers.parse(
        'o ambiente de execução é o virtualenv "{venv:Q}" na pasta '
        '"{pasta:Q}"',
        extra_types=TIPOS,
    )
)
@when(
    parsers.parse(
        'o ambiente de execução é o virtualenv "{venv:Q}" na pasta '
        '"{pasta:Q}"',
        extra_types=TIPOS,
    )
)
def ambiente_do_virtualenv(estado: Estado, venv: str, pasta: str) -> None:
    """Troca o PATH e a pasta dos próximos comandos.

    A pasta é relativa à raiz do repositório do cenário, que é a pasta
    do cenário até este passo; por isso ele só vale uma vez por cenário.

    Args:
        estado: Estado do cenário.
        venv: Nome de um virtualenv criado no cenário.
        pasta: Pasta relativa à raiz do repositório; "." é a raiz.
    """
    if venv not in estado.venvs:
        pytest.fail(
            f'o virtualenv "{venv}" não foi criado neste cenário; os '
            f"criados são: {', '.join(estado.venvs) or 'nenhum'}"
        )
    executaveis = {bin_do(destino) for destino in estado.venvs.values()}
    if executaveis.intersection(estado.caminhos_extras):
        pytest.fail(
            "o ambiente de execução já é um virtualenv neste cenário; a "
            "pasta do passo é relativa à raiz do repositório, que não é "
            f"mais a pasta do cenário ({estado.cwd})"
        )
    alvo = estado.cwd / pasta
    if not alvo.is_dir():
        pytest.fail(f'a pasta "{pasta}" não existe em {estado.cwd}')
    estado.caminhos_extras = [bin_do(estado.venvs[venv])]
    estado.cwd = alvo


def conferir_textos(
    texto: str, verbo: str, textos: list[str], onde: str
) -> None:
    """Exige todos os textos ("contém") ou nenhum deles ("não contém").

    Args:
        texto: Texto onde procurar.
        verbo: "contém" ou "não contém".
        textos: Textos procurados.
        onde: Descrição do texto, para a mensagem.
    """
    if verbo == "contém":
        faltando = [item for item in textos if item not in texto]
        if faltando:
            pytest.fail(f"{onde} não contém {faltando}")
        return
    presentes = [item for item in textos if item in texto]
    if presentes:
        pytest.fail(f"{onde} contém {presentes}")


def ler_texto(estado: Estado, arquivo: str) -> str:
    """Lê um arquivo do repositório sem converter as quebras de linha.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório.

    Returns:
        O texto, com ``\\r`` preservado.
    """
    caminho = estado.cwd / arquivo
    if not caminho.is_file():
        pytest.fail(f'"{arquivo}" não existe em {estado.cwd}')
    with caminho.open(encoding="utf-8", newline="") as entrada:
        return entrada.read()


@then(
    parsers.parse(
        'o arquivo "{arquivo:Q}" {verbo:Contem} {textos:L}',
        extra_types=TIPOS,
    )
)
def arquivo_contem(
    estado: Estado, arquivo: str, verbo: str, textos: list[str]
) -> None:
    """Procura os textos no arquivo lido com ``newline=""``.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório.
        verbo: "contém" ou "não contém".
        textos: Textos procurados.
    """
    conferir_textos(ler_texto(estado, arquivo), verbo, textos, f'"{arquivo}"')


@then(
    parsers.parse(
        'a seção "{secao:Q}" do README contém {textos:L}', extra_types=TIPOS
    )
)
def secao_do_readme_contem(
    estado: Estado, secao: str, textos: list[str]
) -> None:
    """Procura os textos na seção do README.md.

    Args:
        estado: Estado do cenário.
        secao: Texto do título da seção, sem os ``#``.
        textos: Textos que a seção precisa conter.
    """
    corpo = secao_markdown(ler_texto(estado, README), secao)
    if corpo is None:
        pytest.fail(f'{README} não tem um título "#… {secao}"')
    conferir_textos(corpo, "contém", textos, f'a seção "{secao}" do {README}')


def pacotes(estado: Estado, arquivo: str) -> list[Pacote]:
    """Abre os pacotes que casam com o caminho.

    Args:
        estado: Estado do cenário.
        arquivo: Caminho relativo à raiz do repositório; aceita glob.

    Returns:
        Os pacotes, em ordem de nome.
    """
    caminhos = [caminho for caminho in casar(estado, arquivo)
                if caminho.is_file()]
    if not caminhos:
        pytest.fail(f'nenhum arquivo casa com "{arquivo}" em {estado.cwd}')
    abertos: list[Pacote] = []
    for caminho in caminhos:
        try:
            abertos.append(abrir_pacote(caminho))
        except ValueError as erro:
            pytest.fail(str(erro))
    return abertos


def falhar_se_houver(problemas: list[str], regra: str) -> None:
    """Falha o teste listando os problemas encontrados.

    Args:
        problemas: Uma linha por problema.
        regra: O que se esperava, para o título da mensagem.
    """
    if problemas:
        lista = "\n".join(f"  {item}" for item in problemas)
        pytest.fail(f"{regra}:\n{lista}")


@then(
    parsers.parse(
        'o metadado "{campo:Q}" do pacote "{arquivo:Q}" é "{valor:Q}"',
        extra_types=TIPOS,
    )
)
def metadado_do_pacote(
    estado: Estado, campo: str, arquivo: str, valor: str
) -> None:
    """Confere o campo do METADATA (wheel) ou do PKG-INFO (sdist).

    Args:
        estado: Estado do cenário.
        campo: "Name", "Version" ou "License-Expression".
        arquivo: Caminho relativo à raiz do repositório; aceita glob.
        valor: Valor esperado, único no campo.
    """
    if campo not in CAMPOS:
        pytest.fail(
            f'campo "{campo}" não existe; os válidos são: {", ".join(CAMPOS)}'
        )
    problemas: list[str] = []
    for pacote in pacotes(estado, arquivo):
        valores = pacote.metadados().get_all(campo) or []
        if valores != [valor]:
            problemas.append(f"{pacote.caminho.name}: {campo} é {valores}")
    falhar_se_houver(problemas, f'o metadado {campo} deveria ser "{valor}"')


def do_modulo(pacote: Pacote) -> dict[str, bytes]:
    """Arquivos .py do módulo que o pacote carrega.

    Args:
        pacote: Pacote aberto.

    Returns:
        Caminho no repositório para os bytes.
    """
    return {
        relativo: pacote.arquivos[nome]
        for nome, relativo in pacote.fontes().items()
        if relativo.startswith(f"{MODULO}/") and relativo.endswith(".py")
    }


def contem_codigo_do_modulo(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Cada pacote tem os .py de mazegen/ do repositório, idênticos.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    raiz = estado.cwd / MODULO
    repositorio = {
        caminho.relative_to(estado.cwd).as_posix(): caminho.read_bytes()
        for caminho in raiz.rglob("*.py")
        if "__pycache__" not in caminho.parts
    }
    if not repositorio:
        pytest.fail(f"{raiz} não tem arquivos .py")
    problemas: list[str] = []
    for pacote in abertos:
        nome = pacote.caminho.name
        carregados = do_modulo(pacote)
        problemas += [
            f"{nome}: falta {caminho}"
            for caminho in sorted(repositorio.keys() - carregados.keys())
        ]
        problemas += [
            f"{nome}: tem {caminho}, que não existe no repositório"
            for caminho in sorted(carregados.keys() - repositorio.keys())
        ]
        problemas += [
            f"{nome}: {caminho} difere do repositório"
            for caminho in sorted(repositorio.keys() & carregados.keys())
            if repositorio[caminho] != carregados[caminho]
        ]
    falhar_se_houver(problemas, f"o pacote deveria ter o código de {MODULO}/")


def docstring_de(fonte: bytes | str, onde: str) -> str:
    """Docstring de módulo de um código-fonte.

    Args:
        fonte: Código Python.
        onde: Arquivo de origem, para a mensagem.

    Returns:
        A docstring, que precisa existir e não ser vazia.
    """
    try:
        docstring = ast.get_docstring(ast.parse(fonte))
    except SyntaxError as erro:
        pytest.fail(f"{onde} não é Python válido: {erro}")
    if not docstring:
        pytest.fail(f"{onde} não tem docstring de módulo")
    return docstring


def contem_docstring_do_init(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """O mazegen/__init__.py de cada pacote tem a docstring do repositório.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    caminho = estado.cwd / INIT
    if not caminho.is_file():
        pytest.fail(f"{INIT} não existe em {estado.cwd}")
    esperada = docstring_de(caminho.read_bytes(), INIT)
    problemas: list[str] = []
    for pacote in abertos:
        nome = f"{pacote.caminho.name}:{pacote.raiz}{INIT}"
        conteudo = pacote.arquivos.get(pacote.raiz + INIT)
        if conteudo is None:
            problemas.append(f"{nome} não existe")
        elif docstring_de(conteudo, nome) != esperada:
            problemas.append(f"{nome} tem outra docstring")
    falhar_se_houver(problemas, f"o pacote deveria ter a docstring de {INIT}")


def primeira_diferenca(esperado: str, achado: str) -> str:
    """Descreve a primeira linha em que dois textos diferem.

    Args:
        esperado: Texto de referência.
        achado: Texto conferido.

    Returns:
        O número da linha e as duas versões dela.
    """
    linhas_esperadas = esperado.splitlines()
    linhas_achadas = achado.splitlines()
    for indice in range(max(len(linhas_esperadas), len(linhas_achadas))):
        a = linhas_esperadas[indice] if indice < len(linhas_esperadas) else ""
        b = linhas_achadas[indice] if indice < len(linhas_achadas) else ""
        if a != b:
            return f"linha {indice + 1}: esperado {a!r}, veio {b!r}"
    return "diferem só nas quebras de linha do fim"


def readme_como_descricao(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """O corpo dos metadados de cada pacote é o README.md do repositório.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    readme = (estado.cwd / README).read_text(encoding="utf-8")
    problemas: list[str] = []
    for pacote in abertos:
        corpo = pacote.metadados().get_payload()
        if not isinstance(corpo, str):
            problemas.append(f"{pacote.caminho.name}: metadados sem corpo")
        elif corpo.rstrip("\n") != readme.rstrip("\n"):
            problemas.append(
                f"{pacote.caminho.name}: {primeira_diferenca(readme, corpo)}"
            )
    falhar_se_houver(
        problemas, f"a descrição longa do pacote deveria ser o {README}"
    )


def instala_e_importa(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Cada pacote instala num virtualenv novo e o import vem dele.

    O import roda numa pasta vazia, para não achar o mazegen do
    repositório, e o ``__file__`` do módulo precisa estar no virtualenv.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário, que recebe os virtualenvs.
    """
    importar = (
        f"python -c 'import {MODULO}; from {MODULO} import {CLASSE}; "
        f"print({MODULO}.__file__)'"
    )
    for indice, pacote in enumerate(abertos):
        base = pasta / PASTA_DAS_INSTALACOES / str(indice)
        venv = base / "venv"
        vazia = base / "vazia"
        novo_virtualenv(estado, venv)
        vazia.mkdir()
        exigir_sucesso(
            rodar_no_virtualenv(
                venv, vazia, f"pip install {shlex.quote(str(pacote.caminho))}"
            )
        )
        execucao = rodar_no_virtualenv(venv, vazia, importar)
        exigir_sucesso(execucao)
        origem = Path(execucao.saida_padrao.strip()).resolve()
        if not origem.is_relative_to(venv.resolve()):
            pytest.fail(
                f"{pacote.caminho.name}: o {MODULO} importado veio de "
                f"{origem}, fora do virtualenv {venv}"
            )


def normalizado(nome: str) -> str:
    """Nome da distribuição como aparece no nome dos arquivos do build.

    Args:
        nome: Campo Name dos metadados.

    Returns:
        O nome em minúsculas, com ``-``, ``_`` e ``.`` trocados por ``_``.
    """
    return re.sub(r"[-_.]+", "_", nome).lower()


def problemas_do_formato(pacote: Pacote) -> list[str]:
    """Diferenças entre o pacote e o que o ``python -m build`` produz.

    Args:
        pacote: Pacote aberto.

    Returns:
        Uma linha por problema; vazia quando o formato confere.
    """
    nome = pacote.caminho.name
    declarado = nome_e_versao(nome)
    if declarado is None:
        return [f"{nome}: o nome não segue o formato do wheel nem do sdist"]
    distribuicao, versao = declarado
    metadados = pacote.metadados()
    problemas: list[str] = []
    if normalizado(str(metadados["Name"])) != distribuicao:
        problemas.append(f"{nome}: Name é {metadados['Name']}")
    if metadados["Version"] != versao:
        problemas.append(f"{nome}: Version é {metadados['Version']}")
    if pacote.wheel:
        return problemas + problemas_do_wheel(pacote, distribuicao, versao)
    return problemas + problemas_do_sdist(pacote, distribuicao, versao)


def problemas_do_wheel(
    pacote: Pacote, distribuicao: str, versao: str
) -> list[str]:
    """Confere o .dist-info, o WHEEL e o RECORD de um wheel.

    Args:
        pacote: Wheel aberto.
        distribuicao: Nome da distribuição no nome do arquivo.
        versao: Versão no nome do arquivo.

    Returns:
        Uma linha por problema.
    """
    nome = pacote.caminho.name
    info = f"{distribuicao}-{versao}.dist-info"
    problemas = [
        f"{nome}: falta {info}/{arquivo}"
        for arquivo in ARQUIVOS_DO_DIST_INFO
        if f"{info}/{arquivo}" not in pacote.arquivos
    ]
    if problemas:
        return problemas
    wheel = pacote.arquivos[f"{info}/WHEEL"].decode("utf-8")
    campos = Parser().parsestr(wheel)
    problemas += [
        f"{nome}: {info}/WHEEL sem {campo}"
        for campo in CAMPOS_DO_WHEEL
        if campo not in campos
    ]
    registro = pacote.arquivos[f"{info}/RECORD"].decode("utf-8")
    listados = {linha[0] for linha in csv.reader(io.StringIO(registro))
                if linha}
    if listados != set(pacote.arquivos):
        problemas.append(
            f"{nome}: o RECORD não lista exatamente os arquivos do wheel "
            f"(fora dele: {sorted(set(pacote.arquivos) - listados)}; sem "
            f"arquivo: {sorted(listados - set(pacote.arquivos))})"
        )
    return problemas


def problemas_do_sdist(
    pacote: Pacote, distribuicao: str, versao: str
) -> list[str]:
    """Confere a pasta de topo e os arquivos obrigatórios de um sdist.

    Args:
        pacote: Sdist aberto.
        distribuicao: Nome da distribuição no nome do arquivo.
        versao: Versão no nome do arquivo.

    Returns:
        Uma linha por problema.
    """
    nome = pacote.caminho.name
    topo = f"{distribuicao}-{versao}/"
    if pacote.raiz != topo:
        return [f"{nome}: a pasta de topo é {pacote.raiz}, não {topo}"]
    problemas = [
        f"{nome}: {arquivo} fora de {topo}"
        for arquivo in pacote.arquivos if not arquivo.startswith(topo)
    ]
    return problemas + [
        f"{nome}: falta {topo}{arquivo}"
        for arquivo in ARQUIVOS_DO_SDIST
        if topo + arquivo not in pacote.arquivos
    ]


def formato_do_build(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Cada pacote tem a estrutura de wheel ou de sdist do ``python -m build``.

    Args:
        estado: Estado do cenário (não usado).
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    falhar_se_houver(
        [problema for pacote in abertos
         for problema in problemas_do_formato(pacote)],
        "o pacote deveria ter o formato produzido por python -m build",
    )


def versoes_dos_nomes(abertos: list[Pacote]) -> dict[str, str]:
    """Versão que o nome de cada pacote declara.

    Args:
        abertos: Pacotes selecionados.

    Returns:
        Nome do arquivo para a versão.
    """
    versoes: dict[str, str] = {}
    for pacote in abertos:
        declarado = nome_e_versao(pacote.caminho.name)
        if declarado is None:
            pytest.fail(
                f"{pacote.caminho.name}: o nome não segue o formato do wheel "
                "nem do sdist"
            )
        versoes[pacote.caminho.name] = declarado[1]
    return versoes


def mesma_versao_nos_nomes(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Todos os pacotes selecionados declaram a mesma versão no nome.

    Args:
        estado: Estado do cenário (não usado).
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    versoes = versoes_dos_nomes(abertos)
    if len(set(versoes.values())) != 1:
        pytest.fail(f"os nomes dos pacotes declaram versões diferentes: "
                    f"{versoes}")


def versao_do_pyproject_confere(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Version dos metadados e versão do nome iguais às do pyproject.toml.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    caminho = estado.cwd / PYPROJECT
    if not caminho.is_file():
        pytest.fail(f"{PYPROJECT} não existe em {estado.cwd}")
    esperada = versao_do_pyproject(caminho.read_text(encoding="utf-8"))
    if esperada is None:
        pytest.fail(
            f'{PYPROJECT} de {estado.cwd} não declara version = "..." na '
            "tabela [project]"
        )
    versoes = versoes_dos_nomes(abertos)
    problemas: list[str] = []
    for pacote in abertos:
        nome = pacote.caminho.name
        if versoes[nome] != esperada:
            problemas.append(f"{nome}: o nome declara {versoes[nome]}")
        declarada = pacote.metadados().get_all("Version") or []
        if declarada != [esperada]:
            problemas.append(f"{nome}: Version é {declarada}")
    falhar_se_houver(
        problemas, f"a versão deveria ser a do {PYPROJECT}, {esperada}"
    )


def licenca_incluida(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """Cada pacote leva o LICENSE.md do repositório e o declara.

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    caminho = estado.cwd / LICENCA
    if not caminho.is_file():
        pytest.fail(f"{LICENCA} não existe em {estado.cwd}")
    licenca = caminho.read_bytes()
    problemas: list[str] = []
    for pacote in abertos:
        nome = pacote.caminho.name
        levados = [
            arquivo for arquivo, relativo in pacote.fontes().items()
            if relativo == LICENCA
        ]
        if not levados:
            problemas.append(f"{nome}: não leva {LICENCA}")
        problemas += [
            f"{nome}: {arquivo} difere do {LICENCA} do repositório"
            for arquivo in levados if pacote.arquivos[arquivo] != licenca
        ]
        declarados = pacote.metadados().get_all("License-File") or []
        if LICENCA not in declarados:
            problemas.append(f"{nome}: License-File é {declarados}")
    falhar_se_houver(problemas, f"o pacote deveria incluir o {LICENCA}")


def nada_ignorado(
    estado: Estado, abertos: list[Pacote], pasta: Path
) -> None:
    """O pacote e cada arquivo que ele leva do repositório estão no git.

    Cada caminho precisa estar versionado (``git ls-files``) e não ser
    ignorado (``git check-ignore``).

    Args:
        estado: Estado do cenário.
        abertos: Pacotes selecionados.
        pasta: Pasta temporária do cenário (não usada).
    """
    versionados = set(
        git_ou_falha(["ls-files", "-z"], estado.cwd).split("\0")
    )
    caminhos = sorted(
        {
            pacote.caminho.relative_to(estado.cwd).as_posix()
            for pacote in abertos
        }
        | {
            relativo for pacote in abertos
            for relativo in pacote.fontes().values()
        }
    )
    verificacao = git(["check-ignore", "--", *caminhos], estado.cwd)
    if verificacao.returncode not in (0, 1):
        pytest.fail(f"git check-ignore falhou:\n{verificacao.stderr}")
    problemas = [
        f"{caminho} é ignorado pelo git"
        for caminho in verificacao.stdout.splitlines()
    ]
    problemas += [
        f"{caminho} não está versionado no git"
        for caminho in caminhos if caminho not in versionados
    ]
    falhar_se_houver(
        problemas, "nada do que o build usa pode ficar fora do git"
    )


PROPRIEDADES: dict[str, Propriedade] = {
    "contém o código do módulo": contem_codigo_do_modulo,
    "contém a docstring de mazegen/__init__.py": contem_docstring_do_init,
    "README como descrição longa": readme_como_descricao,
    "instala e importa MazeGenerator num virtualenv novo": instala_e_importa,
    "formato produzido por python -m build": formato_do_build,
    "mesma versão no nome dos arquivos": mesma_versao_nos_nomes,
    "versão igual à do pyproject.toml": versao_do_pyproject_confere,
    "LICENSE.md incluído": licenca_incluida,
    "nada do build ignorado pelo git": nada_ignorado,
}


@then(
    parsers.parse(
        'o pacote "{arquivo:Q}" confirma "{propriedade:Q}"', extra_types=TIPOS
    )
)
def pacote_confirma(
    estado: Estado, tmp_path: Path, arquivo: str, propriedade: str
) -> None:
    """Confere a propriedade em cada pacote que casa com o caminho.

    Args:
        estado: Estado do cenário.
        tmp_path: Pasta temporária do cenário, para os virtualenvs.
        arquivo: Caminho relativo à raiz do repositório; aceita glob.
        propriedade: Uma das chaves de PROPRIEDADES.
    """
    conferir = PROPRIEDADES.get(propriedade)
    if conferir is None:
        pytest.fail(
            f'propriedade "{propriedade}" não existe; as válidas são: '
            f"{', '.join(PROPRIEDADES)}"
        )
    conferir(estado, pacotes(estado, arquivo), tmp_path)
