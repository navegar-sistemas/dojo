"""Hello world test."""


def hello() -> str:
    """Return the greeting."""
    return "Hello, World!"


def test_hello() -> None:
    """Check the greeting."""
    assert hello() == "Hello, World!"
