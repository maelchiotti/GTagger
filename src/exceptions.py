"""Exceptions."""


class DiscardLyrics(Exception):
    """Raised when the lyrics are probably wrong and should be discarded."""

    def __init__(self, error: str, title: str, length: int) -> None:
        """Init DiscardLyrics.

        Args:
            error (str): Name of the error.
            title (str): Title of the track on which the error occurred.
            length (int): Number of characters of the line that triggered the error.
        """
        message = f"Discarded the lyrics because {error} for the track '{title}': {length} characters"
        super().__init__(message)
