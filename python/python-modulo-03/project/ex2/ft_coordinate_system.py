import math

PROMPT = "Enter new coordinates as floats in format 'x,y,z': "
LIMIT = 1e150


def get_player_pos() -> tuple[float, float, float]:
    """Ask for coordinates until the user types three valid floats."""
    while True:
        try:
            x_text, y_text, z_text = input(PROMPT).split(",")
        except ValueError:
            print("Invalid syntax")
            continue
        values: list[float] = []
        for text in (x_text, y_text, z_text):
            parameter = text.strip()
            try:
                value = float(parameter)
            except ValueError as error:
                print(f"Error on parameter '{parameter}': {error}")
                break
            if not -LIMIT <= value <= LIMIT:
                print(f"Error on parameter '{parameter}': out of range")
                break
            values.append(value)
        else:
            return (values[0], values[1], values[2])


def distance(first: tuple[float, float, float],
             second: tuple[float, float, float]) -> float:
    """Return the Euclidean distance between two 3D points."""
    x1, y1, z1 = first
    x2, y2, z2 = second
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def main() -> None:
    """Read two positions and show the distances between them."""
    print("=== Game Coordinate System ===")
    print("\nGet a first set of coordinates")
    first = get_player_pos()
    print(f"Got a first tuple: {first}")
    x, y, z = first
    print(f"It includes: X={x}, Y={y}, Z={z}")
    to_center = distance((0.0, 0.0, 0.0), first)
    print(f"Distance to center: {round(to_center, 4)}")
    print("\nGet a second set of coordinates")
    second = get_player_pos()
    between = distance(first, second)
    print(f"Distance between the 2 sets of coordinates: {round(between, 4)}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted - leaving the coordinate system")
