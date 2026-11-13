---
sidebar_position: 9
title: O arquivo completo
---

# O arquivo completo

```python title="ex2/oracle.py"
import os
import sys

try:
    from dotenv import dotenv_values, load_dotenv
except ImportError:
    print("ORACLE ERROR: python-dotenv is not installed.")
    print("Install it with: pip install -r requirements.txt")
    sys.exit(1)

ENV_FILE = ".env"
IGNORE_FILE = ".gitignore"
VARIABLES = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
SECRETS = ["API_KEY", "DATABASE_URL"]
MODES = ["development", "production"]
LOCAL_MARKERS = ["sqlite", "localhost", "127.0.0.1"]


def load_env_file() -> None:
    try:
        load_dotenv(ENV_FILE)
    except (OSError, UnicodeDecodeError) as error:
        print(f"ORACLE ERROR: cannot read {ENV_FILE}: {error}")
        sys.exit(1)


def find_problems() -> list[str]:
    problems = []
    for name in VARIABLES:
        if not os.getenv(name):
            problems.append(f"[MISSING] {name} is not set")
    mode = os.getenv("MATRIX_MODE")
    if mode and mode not in MODES:
        problems.append("[INVALID] MATRIX_MODE must be development "
                        f"or production, not '{mode}'")
    return problems


def read_config() -> dict[str, str]:
    config = {}
    for name in VARIABLES:
        config[name] = os.environ[name]
    return config


def is_local(url: str) -> bool:
    for marker in LOCAL_MARKERS:
        if marker in url:
            return True
    return False


def show_config(config: dict[str, str]) -> None:
    place = "local" if is_local(config["DATABASE_URL"]) else "remote"
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: Connected to {place} instance")
    print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print("Zion Network: Online")


def secrets_check(config: dict[str, str]) -> str:
    try:
        with open(__file__, encoding="utf-8") as source:
            code = source.read()
    except (OSError, UnicodeDecodeError):
        return "[WARNING] Cannot read the source code to look for secrets"
    found = []
    for name in SECRETS:
        value = config[name]
        if f'"{value}"' in code or f"'{value}'" in code:
            found.append(name)
    if found:
        return f"[WARNING] Hardcoded in the source code: {', '.join(found)}"
    return "[OK] No hardcoded secrets detected"


def ignored_names() -> list[str] | None:
    if not os.path.isfile(IGNORE_FILE):
        return []
    try:
        with open(IGNORE_FILE, encoding="utf-8") as ignore:
            return ignore.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None


def env_file_check() -> str:
    if not os.path.isfile(ENV_FILE):
        return "[OK] No .env file, using environment variables only"
    names = ignored_names()
    if names is None:
        return "[WARNING] Cannot read .gitignore"
    if ENV_FILE not in names:
        return "[WARNING] .env is not listed in .gitignore"
    return "[OK] .env file properly configured"


def overrides_check() -> str:
    try:
        file_values = dotenv_values(ENV_FILE)
    except (OSError, UnicodeDecodeError):
        return "[WARNING] Cannot read .env to compare overrides"
    overridden = []
    for name in VARIABLES:
        if name in file_values and file_values[name] != os.environ[name]:
            overridden.append(name)
    if overridden:
        return f"[OK] Production overrides active: {', '.join(overridden)}"
    return "[OK] Production overrides available"


def production_checks(config: dict[str, str]) -> list[str]:
    warnings = []
    if config["LOG_LEVEL"] == "DEBUG":
        warnings.append("[WARNING] DEBUG log level in production")
    if is_local(config["DATABASE_URL"]):
        warnings.append("[WARNING] Local database in production")
    if not warnings:
        return ["[OK] Production settings verified"]
    return warnings


def security_check(config: dict[str, str]) -> None:
    print("Environment security check:")
    print(secrets_check(config))
    print(env_file_check())
    print(overrides_check())
    if config["MATRIX_MODE"] == "production":
        for line in production_checks(config):
            print(line)


def main() -> None:
    print()
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    load_env_file()
    problems = find_problems()
    if problems:
        print("Configuration errors:")
        for problem in problems:
            print(problem)
        print()
        print("Copy .env.example to .env and fill in the values,")
        print("or set the variables in the environment.")
        sys.exit(1)
    config = read_config()
    show_config(config)
    print()
    security_check(config)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: os módulos `os` (`getenv`, `environ`, `path.isfile`) e
`sys` (`exit`), o `python-dotenv` (`load_dotenv` e `dotenv_values`) e as operações com arquivos
(`open`, `read`). Os outros três arquivos do exercício estão completos em
[Os arquivos de apoio](./03-os-arquivos-de-apoio.md).
