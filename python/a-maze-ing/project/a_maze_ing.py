import sys

if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py <config>", file=sys.stderr)
    sys.exit(1)

path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as f:
        texto = f.read()
except FileNotFoundError:
    print(f"Error: configuration file not found: {path}", file=sys.stderr)
    sys.exit(1)
except (OSError, UnicodeDecodeError) as e:
    print(f"Error: cannot read configuration file: {path}: {e}",
          file=sys.stderr)
    sys.exit(1)
