"""Exceptions."""


class DiscardLyrics(Exception):
    """Raised when the lyrics are probably wrong and should be discarded."""

    def __init__(self, error: str, title: str, length: int) -> None:
        message = f"Discarded the lyrics because {error} for the track {title}: {length} characters"
        super().__init__(message)
