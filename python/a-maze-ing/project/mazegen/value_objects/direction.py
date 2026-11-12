"""The four sides of a cell and the wall bit of each one."""

from enum import IntEnum


class Direction(IntEnum):
    """Side of a cell; the value is the wall bit in the output file.

    Iterating the enum yields NORTH, EAST, SOUTH and WEST, the neighbour
    order of the breadth-first search.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Side that faces this one across a shared wall.

        Returns:
            The opposite direction.
        """
        return _OPPOSITE[self.value]

    @property
    def dx(self) -> int:
        """Column offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][0]

    @property
    def dy(self) -> int:
        """Row offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][1]

    @property
    def letter(self) -> str:
        """Letter of this side in the shortest path.

        Returns:
            "N", "E", "S" or "W".
        """
        return _LETTER[self.value]


# Enum members cannot hold plain class attributes (each one would become a
# member), so the lookup tables live at module level.
_OPPOSITE: dict[int, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}
_DELTA: dict[int, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
_LETTER: dict[int, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W",
}
