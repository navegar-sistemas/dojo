"""Entry point of A-Maze-ing: check the arguments and read the config file."""

import sys

if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
    sys.exit(1)

path = sys.argv[1]
try:
    with open(path, encoding="utf-8-sig") as f:
        texto = f.read()
except FileNotFoundError:
    print(f"Error: configuration file not found: {path}", file=sys.stderr)
    sys.exit(1)
except UnicodeDecodeError:
    print(f"Error: configuration file is not valid UTF-8: {path}",
          file=sys.stderr)
    sys.exit(1)
except OSError as e:
    print(f"Error: cannot read configuration file {path}: {e.strerror}",
          file=sys.stderr)
    sys.exit(1)
