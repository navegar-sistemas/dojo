import sys

MAX_SCORE = 2 ** 53


def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text


def parse_scores(arguments: list[str]) -> list[int]:
    """Convert the arguments to scores, reporting and skipping bad ones."""
    scores: list[int] = []
    for argument in arguments:
        try:
            score = int(argument)
        except ValueError:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        if not -MAX_SCORE <= score <= MAX_SCORE:
            print(f"Invalid parameter: '{printable(argument)}'")
            continue
        scores.append(score)
    return scores


def show_stats(scores: list[int]) -> None:
    """Print the statistics of a non-empty list of scores."""
    total = sum(scores)
    high = max(scores)
    low = min(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {total / len(scores)}")
    print(f"High score: {high}")
    print(f"Low score: {low}")
    print(f"Score range: {high - low}")


def main() -> None:
    """Read the scores from the command line and analyse them."""
    print("=== Player Score Analytics ===")
    scores = parse_scores(sys.argv[1:])
    if len(scores) == 0:
        print(f"No scores provided. Usage: python3 {printable(sys.argv[0])}"
              " <score1> <score2> ...")
    else:
        show_stats(scores)


if __name__ == "__main__":
    main()
