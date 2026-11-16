import sys


def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text


def main() -> None:
    """Show the program name and every command-line argument."""
    print("=== Command Quest ===")
    print(f"Program name: {printable(sys.argv[0])}")
    arguments = sys.argv[1:]
    if len(arguments) == 0:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(arguments)}")
        number = 1
        for argument in arguments:
            print(f"Argument {number}: {printable(argument)}")
            number += 1
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
