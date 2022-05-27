"""
Add lyrics to audio files.
"""

import os
import sys
import re
from pathlib import Path
import eyed3
import lyricsgenius
import genius


def main():
    """
    Main function.
    """
    check_args()
    genius_instance, lyricsgenius_instance, options, files, counters = init()
    print(Colors.PURPLE + Colors.BOLD + "GeniusLyrics | Start\n" + Colors.ENDC)

    for filename in files:
        counters["lyrics_total"] += 1

        audiofile = eyed3.load(filename)
        title = audiofile.tag.title
        artist = split_artist(audiofile)
        if title is None or artist is None:
            print(Colors.RED + "File " + filename +
                  " skipped (title or artist missing)" + Colors.ENDC)
            continue

        print(title + " - " + artist + " | ", end="")

        # Search for the track to get infos
        searched_tracks = genius_instance.search(title + " " + artist)
        try:
            searched_track = next(searched_tracks)
        except StopIteration:
            print(Colors.RED + "Could not be found on Genius" + Colors.ENDC)
            continue

        # Find lyrics
        counters, wrote = lyrics(options, counters, lyricsgenius_instance,
                                 audiofile, searched_track)

        # Skip if no lyrics were written
        if not wrote:
            print()
            continue

        # Save lyrics
        print(" | ", end="")
        counters = save(counters, audiofile)

        print()

    print_stats(counters)


def lyrics(options, counters, lyricsgenius_instance, audiofile, searched_track):
    """
    Add lyrics to the audiofiles.
    """
    # Check if the files already has lyrics
    # and they should not be overwritten
    if not options["-o"] and len(audiofile.tag.lyrics) > 0:
        counters["lyrics_skipped"] += 1
        print(Colors.ORANGE + "Skipped already existing lyrics" + Colors.ENDC, end="")
        return counters, False

    # Search for the track to get lyrics (while true fixes the timeout error)
    lyrics_track = None
    while True:
        try:
            lyrics_track = lyricsgenius_instance.search_song(
                song_id=searched_track.id, get_full_info=False)
            break
        except Exception as excpetion:
            print("Unexpected exception: " + str(excpetion.with_traceback()))
            return counters, False

    # Skip if no lyrics were found
    if lyrics_track is None:
        counters["lyrics_not_found"] += 1
        print(Colors.RED + "No lyrics found" + Colors.ENDC, end="")
        return counters, False

    # Set the lyrics
    audiofile.tag.lyrics.set(format_lyrics(lyrics_track.lyrics))
    counters["lyrics_found_saved"] += 1
    print(Colors.GREEN + "Lyrics found" + Colors.ENDC, end="")
    return counters, True


def save(counters, audiofile):
    """
    Save the lyrics.
    """
    # Save the lyrics
    try:
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3, encoding='utf-8')
        print(Colors.GREEN + "Lyrics saved" + Colors.ENDC, end="")
    # TagException is raised when an error while saving occurs
    except eyed3.id3.tag.TagException:
        counters["lyrics_found_not_saved"] += 1
        print(Colors.RED + "Could not save lyrics" + Colors.ENDC, end="")

    return counters


def check_args():
    """
    Check the number of arguments.
    """
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and (
            sys.argv[1] == "-h" or sys.argv[1] == "--help")):
        print_help()


def print_help():
    """
    Print help message.
    """
    print(
        Colors.BOLD + "Usage:" + Colors.ENDC +
        "\n\tpython3 geniustagger.py <Genius access token> <tracks folder path> <options>")
    print(Colors.BOLD + "Options:" + Colors.ENDC +
          "\n\t-r\tSearch for files recursively in sub-folders" +
          "\n\t-o\tOverwrite already existing lyrics" +
          "\n\t-h\tShow help")
    print(Colors.BOLD + "Tips:" + Colors.ENDC +
          "\n\tGet your Genius access token at https://genius.com/api-clients")
    sys.exit()


def init():
    """
    Initialize variables.
    """
    # Access token and
    access_token = sys.argv[1]
    search = re.search("[^a-zA-Z0-9_-]", access_token)
    if search is not None:
        print("Incorrect access token")
        print_help()

    # genius and lyricsgenius instances
    genius_instance = genius.Genius(access_token=access_token)
    geniuslyrics_instance = lyricsgenius.Genius(access_token=access_token,
                                                verbose=False, remove_section_headers=True)

    # Path name
    pathname = sys.argv[2]
    if not pathname.endswith("\\"):
        pathname = pathname + "\\"
    if not os.path.isdir(pathname):
        print("Incorrect path name: " + pathname)

    # Check for options
    options = {"-r": False, "-o": False, }
    for option in dict(options):
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "-h" or sys.argv[i] == "-help":
                print_help()
            if option == sys.argv[i]:
                options[option] = True

    # List files
    if options["-r"]:
        files = Path(pathname).rglob("*.mp3")
    else:
        files = Path(pathname).glob("*.mp3")

    # Counters
    counters = {"lyrics_total": 0,
                "lyrics_found_saved": 0,
                "lyrics_skipped": 0,
                "lyrics_not_found": 0,
                "lyrics_found_not_saved": 0}

    return genius_instance, geniuslyrics_instance, options, files, counters


def split_artist(audiofile):
    """
    Split the artist name if it contains multiple artists, keeping only the
    first (and supposedly the main) one.
    """
    # Initialize the artist if it exists
    if audiofile.tag.artist is None:
        return None

    artist = audiofile.tag.artist

    # Search for splitters and split
    splitters = [" featuring ", " feat. ",
                 " feat ", " ft. ", " ft ", " & ", " / "]
    for splitter in splitters:
        if splitter in audiofile.tag.artist:
            artist = audiofile.tag.artist.split(splitter)[0]
            break

    return artist


def format_lyrics(unformatted_lyrics):
    """
    Format the lyrics (remove unwanted text).
    """
    lines = unformatted_lyrics.split("\n")
    if len(lines) > 0:
        lines.pop(0)
    if len(lines) > 1:
        lines[len(lines) - 1] = re.sub("[0-9]+Embed",
                                       "", lines[len(lines) - 1])
    return "\n".join(lines)


def print_stats(counters):
    """
    Print statistics.
    """
    print(Colors.PURPLE + Colors.BOLD + "\nGeniusLyrics | End" + Colors.ENDC)

    if counters["lyrics_total"] == 0:
        return

    lyrics_found_saved_perc = (
        counters["lyrics_found_saved"] - counters["lyrics_found_not_saved"]) / counters["lyrics_total"] * 100
    lyrics_skipped_perc = counters["lyrics_skipped"] / \
        counters["lyrics_total"] * 100
    lyrics_not_found_perc = counters["lyrics_not_found"] / \
        counters["lyrics_total"] * 100
    lyrics_found_not_saved_perc = counters["lyrics_found_not_saved"] / \
        counters["lyrics_total"] * 100

    print(Colors.BOLD + "\n" + str(counters["lyrics_total"]) +
          " lyrics searched" + Colors.ENDC)
    print(Colors.GREEN +
          f"{lyrics_found_saved_perc:.2f}% lyrics found and saved" + Colors.ENDC)
    print(Colors.ORANGE +
          f"{lyrics_skipped_perc:.2f}% lyrics skipped" + Colors.ENDC)
    print(Colors.ORANGE +
          f"{lyrics_not_found_perc:.2f}% lyrics not found" + Colors.ENDC)
    print(Colors.RED +
          f"{lyrics_found_not_saved_perc:.2f}% lyrics found but not saved" + Colors.ENDC)


class Colors:
    """
    Output colors.
    """
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


if __name__ == "__main__":
    main()
