---
sidebar_position: 9
title: O arquivo completo
---

# O arquivo completo

```python title="ex1/loading.py"
import importlib
import sys

OUTPUT = "matrix_analysis.png"
DATA_POINTS = 1000
DEPENDENCIES = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
    ("matplotlib", "Visualization"),
]


def check_dependencies() -> list[str]:
    missing = []
    for name, role in DEPENDENCIES:
        try:
            module = importlib.import_module(name)
        except ImportError:
            print(f"[MISSING] {name} - {role} not available")
            missing.append(name)
        else:
            print(f"[OK] {name} ({module.__version__}) - {role} ready")
    return missing


def show_install_help(missing: list[str]) -> None:
    print(f"Missing dependencies: {', '.join(missing)}")
    print()
    print("With pip: installs the packages listed in requirements.txt")
    print("into the active environment (activate a venv first)")
    print("  pip install -r requirements.txt")
    print("  python3 loading.py")
    print()
    print("With Poetry: reads pyproject.toml, creates its own virtual")
    print("environment and records the exact versions in poetry.lock")
    print("  poetry install")
    print("  poetry run python loading.py")


def run_analysis() -> None:
    np = importlib.import_module("numpy")
    pd = importlib.import_module("pandas")
    matplotlib = importlib.import_module("matplotlib")
    matplotlib.use("Agg")
    plt = importlib.import_module("matplotlib.pyplot")

    print("Analyzing Matrix data...")
    rng = np.random.default_rng(1999)
    steps = rng.normal(0.0, 1.0, DATA_POINTS)
    data = pd.DataFrame({"signal": np.cumsum(steps)})
    data["trend"] = data["signal"].rolling(window=50).mean()
    print(f"Processing {len(data)} data points...")

    print("Generating visualization...")
    figure, axes = plt.subplots(figsize=(10, 5))
    axes.plot(data.index, data["signal"], color="#2a78d6",
              linewidth=1.5, label="signal")
    axes.plot(data.index, data["trend"], color="#eb6834",
              linewidth=2, label="trend (50-point mean)")
    axes.set_title("Matrix data")
    axes.set_xlabel("data point")
    axes.set_ylabel("signal")
    axes.grid(color="#e5e5e5")
    axes.legend()
    figure.savefig(OUTPUT)
    plt.close(figure)


def main() -> None:
    print()
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")
    missing = check_dependencies()
    print()
    if missing:
        show_install_help(missing)
        sys.exit(1)
    try:
        run_analysis()
    except OSError as error:
        print(f"Analysis failed: {error}")
        sys.exit(1)
    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: os módulos `importlib` (`import_module`) e `sys`
(`exit`), e, por meio do `importlib`, as bibliotecas `numpy`, `pandas` e `matplotlib`. Os outros
dois arquivos do exercício estão completos nas suas páginas:
[O requirements.txt](./03-o-requirements-txt.md) e [O pyproject.toml](./04-o-pyproject-toml.md).
