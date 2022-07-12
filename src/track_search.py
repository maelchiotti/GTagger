"""Searches a track on Genius."""

import re
import logging as log
import genius

from src.track import Track


class TrackSearch:
    """Allows to search a track on Genius.

    Attributes:
        token (str): Genius client access token.
        genius (genius.Genius): `genius` instance.
    """

    def __init__(self, token: str) -> None:
        search = re.search("[^a-zA-Z0-9_-]", token)
        if search is not None:
            log.error("Incorrect access token: %s", search)
            self.token: str = None
            self.genius: genius.Genius = None
        else:
            self.token: str = token
            self.genius: genius.Genius = genius.Genius(access_token=self.token)

    def search_track(self, track: Track) -> bool:
        """Searches for a track on Genius using the `track.title` and the `track.artist`.

        The tags found are added to the `genius_tags` attribute of `track`.

        Args:
            track (Track): Track to search.

        Returns:
            bool: `True` is the track was found.
        """
        if track.title is None or track.main_artist is None:
            return False
        search = f"{track.title} {track.main_artist}"
        searched_tracks = self.genius.search(search)
        try:
            searched_track = next(searched_tracks)
        except StopIteration:
            log.warning(
                "Track '%s' by %s not found on Genius", track.title, track.main_artist
            )
            return False
        track.genius_tags = searched_track
        return True
