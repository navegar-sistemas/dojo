#!/bin/sh
# Configura a suíte de testes do A-Maze-ing em a-maze-ing/tests/.
# Pode rodar de novo: arquivos que já existem não são sobrescritos.
set -eu

TESTS_DIR=$(cd "$(dirname "$0")" && pwd)
ANALYZER="$(dirname "$TESTS_DIR")/private/maze_analyzer.py"

cd "$TESTS_DIR"

if [ ! -f "$ANALYZER" ]; then
    echo "Erro: maze_analyzer.py não encontrado em $ANALYZER." >&2
    exit 1
fi

mkdir -p step_defs unit fixtures

if [ -f test_hello.py ] && [ ! -e unit/test_hello.py ]; then
    mv test_hello.py unit/test_hello.py
fi

if [ ! -f maze_analyzer.py ]; then
    cp "$ANALYZER" maze_analyzer.py
fi

if [ ! -f requirements.txt ]; then
    printf 'pytest==9.2.0\npytest-bdd==9.0.1\nflake8==7.4.1\nmypy==2.4.1\n' \
        > requirements.txt
fi

if [ ! -f .flake8 ]; then
    printf '[flake8]\nextend-exclude = .venv,maze_analyzer.py\n' > .flake8
fi

if [ ! -f mypy.ini ]; then
    cat > mypy.ini << 'EOF'
[mypy]
strict = True
exclude = ^(\.venv/|maze_analyzer\.py$)

[mypy-parse]
follow_untyped_imports = True
EOF
fi

if [ ! -f .gitignore ]; then
    printf '.venv/\n__pycache__/\n.pytest_cache/\n' > .gitignore
fi
# private/ é material do subject e fica fora do git; a cópia também.
if ! grep -qx 'maze_analyzer.py' .gitignore; then
    echo 'maze_analyzer.py' >> .gitignore
fi

if [ ! -f pytest.ini ]; then
    cat > pytest.ini << 'EOF'
[pytest]
bdd_features_base_dir = features
pythonpath = ../project
testpaths = step_defs unit
filterwarnings = error
markers =
    obrigatorio: requisito "must" do subject
    recomendado: requisito "should" do subject
    opcional: requisito "may" do subject
    bonus: bônus do Capítulo VIII
    informativo: contexto sem exigência própria
    derivado: consequência de requisito, exemplo ou figura
    automatizado: executado pela suíte
    manual: verificado por inspeção ou na defesa
EOF
fi

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
# O pip que vem com o venv grava o cache num formato que o pip atualizado não lê;
# sem cache neste passo, o pip novo não encontra entradas que não consegue ler.
.venv/bin/pip install --quiet --no-cache-dir --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

echo "Suíte configurada em $TESTS_DIR."
echo "Próximos passos (seção \"Primeiros passos\" de features/README.md):"
echo "  cd \"$TESTS_DIR\""
echo "  .venv/bin/pytest --generate-missing --feature features"
echo "  .venv/bin/pytest -m \"not manual\""
echo "  .venv/bin/flake8 . && .venv/bin/mypy ."
