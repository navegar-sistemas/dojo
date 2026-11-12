"""Exception raised by the maze generator."""


class MazeError(Exception):
    """Impossible parameter or broken invariant inside the maze generator.

    Messages that start with ``internal:`` point to a bug, not to a user
    error.
    """
