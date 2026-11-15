"""Catálogo de casos de erro: um por cenário de erro de 03, 04, 05, 07, 08, 13.

Cada caso descreve, como dado, o que o cenário de origem prepara (config,
pares, linhas trocadas, caminho preparado, situação de erro), o comando e o
que a mensagem de erro precisa citar. Os passos de ``step_defs/catalogo.py``
montam e rodam cada caso. ``autoteste/test_catalogo.py`` confere que o
catálogo tem um caso para cada exemplo de cenário de erro dos .feature.
"""

from dataclasses import dataclass

COMANDO = "python3 a_maze_ing.py cfg.txt"
CHAVES = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")
TODAS_AUSENTES = (
    "erro citando WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT; motivo: "
    "chave obrigatória ausente"
)


@dataclass(frozen=True)
class Caso:
    """Um caso de erro e o cenário do .feature de onde ele vem.

    ``config`` é a origem do config gravado em cfg.txt ("base", "do
    repositório" ou None, sem config). Os ajustes são aplicados nesta ordem:
    ``pares``, ``sem``, ``linha``, ``linha_da_chave``, ``situacao`` e
    ``preparado``. ``uso`` marca o uso errado da linha de comando (I12), que
    tem mensagem própria e não segue a D01.
    """

    feature: str
    cenario: str
    exemplo: tuple[str, ...]
    comando: str
    cita: tuple[str, ...]
    config: str | None = "base"
    pares: tuple[str, ...] = ()
    sem: str | None = None
    linha: tuple[int, str] | None = None
    linha_da_chave: tuple[str, str] | None = None
    situacao: str | None = None
    preparado: tuple[str, str] | None = None
    uso: bool = False

    @property
    def nome(self) -> str:
        """Identificação do caso nas mensagens de falha.

        Returns:
            Número do .feature, título do cenário e a linha de exemplo.
        """
        if not self.exemplo:
            return f"{self.feature} {self.cenario}"
        return f"{self.feature} {self.cenario} | {' | '.join(self.exemplo)} |"


def _hostis() -> list[Caso]:
    """Exemplos de erro de "Entradas hostis não derrubam o programa".

    Returns:
        Um caso por exemplo que termina em erro.
    """
    exemplos = [
        (
            "bytes binários aleatórios",
            "erro citando cfg.txt; motivo: arquivo não é UTF-8",
            ("cfg.txt",),
        ),
        (
            "config base com WIDTH de 100000 dígitos",
            "erro citando WIDTH",
            ("WIDTH",),
        ),
        ("só WÍDTH=20 e HEÍGHT=15, com acento", TODAS_AUSENTES, CHAVES),
        ("só espaços e tabulações", TODAS_AUSENTES, CHAVES),
    ]
    return [
        Caso(
            "03",
            "Entradas hostis não derrubam o programa",
            (conteudo, resultado),
            COMANDO,
            cita,
            config=None,
            preparado=("cfg.txt", conteudo),
        )
        for conteudo, resultado, cita in exemplos
    ]


def _situacoes() -> list[Caso]:
    """Exemplos de "Nenhum caminho de erro termina em exceção não tratada".

    O cenário não diz o que a mensagem cita; vale a D01: o arquivo, a chave
    ou o caminho que causou o erro.

    Returns:
        Um caso por situação de erro.
    """
    exemplos = [
        ("arquivo de configuração inexistente", ("cfg.txt",)),
        ("arquivo de configuração sem permissão de leitura", ("cfg.txt",)),
        ("chave obrigatória ausente", ("WIDTH",)),
        ("valor inválido", ("WIDTH",)),
        ("parâmetros impossíveis", ("ENTRY", "EXIT")),
        (
            "OUTPUT_FILE num diretório inexistente",
            ("diretorio_inexistente/maze.txt",),
        ),
    ]
    return [
        Caso(
            "03",
            "Nenhum caminho de erro termina em exceção não tratada",
            (situacao,),
            COMANDO,
            cita,
            situacao=situacao,
        )
        for situacao, cita in exemplos
    ]


def _uso_cli() -> list[Caso]:
    """Cenários de erro de 04-uso-cli.feature.

    Returns:
        Os casos de argumentos errados e de arquivo que não se lê.
    """
    casos = [
        Caso(
            "04",
            "Quantidade de argumentos diferente de um é recusada",
            (argumentos,),
            f"python3 a_maze_ing.py {argumentos}",
            (),
            config=None,
            uso=True,
        )
        for argumentos in (
            "", "config.txt outro.txt", "config.txt a.txt b.txt"
        )
    ]
    casos.append(
        Caso(
            "04",
            "Arquivo de configuração inexistente",
            (),
            "python3 a_maze_ing.py nao_existe.txt",
            ("nao_existe.txt",),
            config=None,
            preparado=("nao_existe.txt", "inexistente"),
        )
    )
    casos += [
        Caso(
            "04",
            "Outros erros de leitura do arquivo de configuração",
            (tipo, argumento),
            f"python3 a_maze_ing.py {argumento}",
            (argumento,),
            config=None,
            preparado=(argumento, tipo),
        )
        for tipo, argumento in (
            ("diretório", "pasta"),
            ("sem permissão de leitura", "fechado.txt"),
            ("não UTF-8", "latin1.txt"),
        )
    ]
    return casos


def _valores_invalidos(chave: str, valores: tuple[str, ...]) -> list[Caso]:
    """Exemplos de um Esquema "<chave> inválido(a) gera erro" de 05.

    Args:
        chave: Chave cujo valor é trocado.
        valores: Valores da tabela de exemplos.

    Returns:
        Um caso por valor, citando a chave.
    """
    titulos = {
        "WIDTH": "WIDTH inválido gera erro",
        "HEIGHT": "HEIGHT inválido gera erro",
        "ENTRY": "ENTRY inválida gera erro",
        "EXIT": "EXIT inválida gera erro",
        "PERFECT": "PERFECT com valor que não é booleano gera erro",
    }
    return [
        Caso(
            "05",
            titulos[chave],
            (valor,),
            COMANDO,
            (chave,),
            pares=(f"{chave}={valor}",),
        )
        for valor in valores
    ]


def _configuracao() -> list[Caso]:
    """Cenários de erro de 05-configuracao.feature.

    Todos partem do Contexto, o config base salvo em cfg.txt.

    Returns:
        Os casos de sintaxe, chaves ausentes, valores e parâmetros.
    """
    casos = [
        Caso(
            "05",
            "Linha fora do formato KEY=VALUE é erro de sintaxe",
            (linha,),
            COMANDO,
            ("cfg.txt", "line 2", linha),
            linha=(2, linha),
        )
        for linha in ("HEIGHT 15", "HEIGHT", "=15")
    ]
    casos.append(
        Caso(
            "05",
            "Comentário no fim de uma linha de valor não é suportado",
            (),
            COMANDO,
            ("WIDTH",),
            linha=(1, "WIDTH=20 # largura"),
        )
    )
    casos += [
        Caso(
            "05",
            "Cada chave obrigatória ausente gera erro",
            (chave,),
            COMANDO,
            (chave,),
            sem=chave,
        )
        for chave in CHAVES
    ]
    casos.append(
        Caso(
            "05",
            "Arquivo sem nenhuma chave lista todas as chaves ausentes",
            (),
            COMANDO,
            CHAVES,
            preparado=("cfg.txt", "vazio"),
        )
    )
    casos += _valores_invalidos(
        "WIDTH",
        ("", "abc", "2.5", "0", "-3", "1e3", "20,0", "101", "1000000"),
    )
    casos += _valores_invalidos(
        "HEIGHT",
        (
            "", "quinze", "7.0", "0", "-1", "15 WIDTH=20", "15 # altura",
            "101", "99999999",
        ),
    )
    casos += _valores_invalidos(
        "ENTRY",
        ("", "0", "0,0,0", "a,b", "0;0", "(0,0)", "-1,0", "20,0", "0,15"),
    )
    casos += _valores_invalidos(
        "EXIT", ("", "19", "x,y", "19,-1", "20,14", "19,15")
    )
    casos += [
        Caso(
            "05",
            "ENTRY igual a EXIT é parâmetro impossível",
            (),
            COMANDO,
            ("ENTRY", "EXIT"),
            pares=("ENTRY=5,5", "EXIT=5,5"),
        ),
        Caso(
            "05",
            "OUTPUT_FILE vazio gera erro",
            (),
            COMANDO,
            ("OUTPUT_FILE",),
            pares=("OUTPUT_FILE=",),
        ),
    ]
    casos += _valores_invalidos("PERFECT", ("", "yes", "1", "sim", "Truee"))
    casos.append(
        Caso(
            "05",
            "Chave obrigatória com erro de digitação é acusada como ausente",
            (),
            COMANDO,
            ("WIDTH",),
            linha_da_chave=("WIDTH", "WIDHT=20"),
        )
    )
    casos += [
        Caso(
            "05",
            "Os cinco erros que o avaliador provoca no config",
            (chave, linha),
            COMANDO,
            (chave,),
            config="do repositório",
            linha_da_chave=(chave, linha),
        )
        for chave, linha in (
            ("WIDTH", ""),
            ("PERFECT", ""),
            ("HEIGHT", "HEIGHT 15"),
            ("WIDTH", "WIDTH=abc"),
            ("HEIGHT", "HEIGHT=xv"),
            ("PERFECT", "PERFECT=maybe"),
            ("ENTRY", "ENTRY=0;0"),
            ("EXIT", "EXIT=19"),
            ("ENTRY", "ENTRY=a,b"),
        )
    ]
    casos += [
        Caso(
            "05",
            "Grade onde o modo Pac-Man é impossível gera erro",
            (largura, altura, saida),
            COMANDO,
            ("PERFECT",),
            pares=(
                f"WIDTH={largura}",
                f"HEIGHT={altura}",
                f"EXIT={saida}",
                "PERFECT=False",
            ),
        )
        for largura, altura, saida in (
            ("1", "10", "0,9"),
            ("10", "1", "9,0"),
            ("2", "2", "1,1"),
        )
    ]
    return casos


def _seed_e_42_e_saida() -> list[Caso]:
    """Cenários de erro de 07, 08 e 13 que rodam o programa.

    O Esquema de 07 sobre a classe geradora (MazeError) não roda o programa
    e fica de fora: o catálogo é de execuções de ``a_maze_ing.py``.

    Returns:
        Os casos de SEED inválida, coordenada no "42" e erro de gravação.
    """
    casos = [
        Caso(
            "07",
            "SEED inválida gera erro",
            (valor,),
            COMANDO,
            ("SEED",),
            pares=(f"SEED={valor}",),
        )
        for valor in ("", "abc", "4.2")
    ]
    casos += [
        Caso(
            "08",
            'ENTRY ou EXIT sobre uma célula do "42" gera erro',
            (chave, coordenada),
            COMANDO,
            (chave,),
            pares=(f"{chave}={coordenada}",),
        )
        for chave, coordenada in (
            ("ENTRY", "6,5"),
            ("ENTRY", "8,7"),
            ("EXIT", "12,9"),
            ("EXIT", "10,5"),
        )
    ]
    casos += [
        Caso(
            "13",
            "Erro ao gravar o arquivo de saída vira mensagem clara",
            (caminho, diretorio, tipo),
            COMANDO,
            (caminho,),
            pares=(f"OUTPUT_FILE={caminho}",),
            preparado=(diretorio, tipo),
        )
        for caminho, diretorio, tipo in (
            ("nao_existe/maze.txt", "nao_existe", "inexistente"),
            (
                "trancado/maze.txt",
                "trancado",
                "diretório sem permissão de escrita",
            ),
            ("pasta", "pasta", "diretório"),
        )
    ]
    return casos


CATALOGO: tuple[Caso, ...] = (
    *_hostis(),
    *_situacoes(),
    *_uso_cli(),
    *_configuracao(),
    *_seed_e_42_e_saida(),
)
