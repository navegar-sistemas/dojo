---
sidebar_position: 8
title: Os arquivos completos
---

# Os arquivos completos

```python title="ex1/oracle.py"
import os

from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
VARIABLES = ["MATRIX_MODE", "DATABASE_URL", "API_KEY", "LOG_LEVEL",
             "ZION_ENDPOINT"]
DEFAULTS = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///oracle.db",
    "LOG_LEVEL": "INFO",
}
MODES = ["development", "production"]
LOCAL_MARKERS = ["sqlite:", "localhost", "127.0.0.1"]


def load_config() -> tuple[dict[str, str], list[str]]:
    warnings: list[str] = []
    env_file = os.path.join(HERE, ".env")
    if os.path.isfile(env_file):
        load_dotenv(env_file)
    else:
        warnings.append("No .env file found, reading the environment only")
    config: dict[str, str] = {}
    for name in VARIABLES:
        value = os.environ.get(name)
        if value:
            config[name] = value
        elif name in DEFAULTS:
            config[name] = DEFAULTS[name]
            warnings.append(f"{name} not set, using default: "
                            f"{DEFAULTS[name]}")
        else:
            config[name] = ""
            warnings.append(f"{name} not set and has no default")
    if config["MATRIX_MODE"] not in MODES:
        warnings.append(f"MATRIX_MODE '{config['MATRIX_MODE']}' is unknown, "
                        "using development")
        config["MATRIX_MODE"] = "development"
    return config, warnings


def database_status(url: str) -> str:
    for marker in LOCAL_MARKERS:
        if marker in url:
            return "Connected to local instance"
    return "Connected to remote instance"


def api_status(config: dict[str, str]) -> str:
    if config["API_KEY"]:
        return "Authenticated"
    if config["MATRIX_MODE"] == "production":
        return "DENIED - API_KEY is required in production"
    return "Anonymous (development only)"


def show_config(config: dict[str, str]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {database_status(config['DATABASE_URL'])}")
    print(f"API Access: {api_status(config)}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    network = "Online" if config["ZION_ENDPOINT"] else "Offline"
    print(f"Remote Network: {network}")


def read_file(name: str) -> str:
    path = os.path.join(HERE, name)
    if not os.path.isfile(path):
        return ""
    with open(path) as file:
        return file.read()


def security_check(config: dict[str, str], overrides: list[str]) -> None:
    print("Configuration security check:")
    secret = config["API_KEY"]
    source = read_file(os.path.basename(__file__))
    if secret and secret in source:
        print("[WARNING] API_KEY value found in the source code")
    else:
        print("[OK] No hardcoded secrets detected")
    if ".env" in read_file(".gitignore").splitlines():
        print("[OK] .env file properly ignored by git")
    else:
        print("[WARNING] .env file is not listed in .gitignore")
    if overrides:
        print(f"[OK] Production overrides active: {', '.join(overrides)}")
    else:
        print("[OK] Production overrides available")
    production = config["MATRIX_MODE"] == "production"
    if production and config["LOG_LEVEL"] == "DEBUG":
        print("[WARNING] DEBUG logging enabled in production")


def main() -> None:
    print()
    print("ORACLE STATUS: Consulting the configuration...")
    print()
    overrides = [name for name in VARIABLES if os.environ.get(name)]
    config, warnings = load_config()
    for warning in warnings:
        print(f"[WARNING] {warning}")
    if warnings:
        print()
    show_config(config)
    print()
    security_check(config, overrides)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
```

O que o arquivo usa: o módulo `os` (`os.environ`, `os.path`), a função `load_dotenv` da
biblioteca `python-dotenv`, a função embutida `open` para ler arquivos, e `print`. Tudo dentro do
permitido no exercício 1.

```text title="ex1/requirements.txt"
python-dotenv>=1.0
```

```ini title="ex1/.env.example"
MATRIX_MODE=development
DATABASE_URL=sqlite:///oracle.db
API_KEY=
LOG_LEVEL=DEBUG
ZION_ENDPOINT=https://zion.example.com/api
```

```text title="ex1/.gitignore"
.env
```

Os quatro arquivos do enunciado ficam na pasta `ex1`. O `-a` do `ls` mostra também os arquivos que
começam com ponto:

```bash
ls -1a ex1
```

```text
.
..
.env.example
.gitignore
oracle.py
requirements.txt
```

`.` e `..` não são arquivos: são os nomes que toda pasta tem para ela mesma e para a pasta de
cima. O `.env` ainda não existe; ele nasce na [próxima página](./09-rodar-e-conferir.md).
