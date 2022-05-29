"""
[WIP] Add tags to audio files and rename them.
"""

import os
import sys
import re
from pathlib import Path
import urllib
import eyed3
from eyed3.id3.frames import ImageFrame
import eyed3.core
import lyricsgenius
import genius


# Pretend to be a request form a normal web brower,
# otherwise Genius doesn't allow downloading of cover arts
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
    'AppleWebKit/537.11 (KHTML, like Gecko) '
    'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


def main():
    """
    Main function.
    """
    check_args()
    g, lg, files, options, tag_lyrics_total, tag_lyrics_found, tag_lyrics_not_saved = init()
    print(Colors.PURPLE + Colors.BOLD + "GeniusLyrics | Start\n" + Colors.ENDC)

    for filename in files:
        audiofile = eyed3.load(filename)
        title = audiofile.tag.title
        artist = split_artist(audiofile)
        if title is None or artist is None:
            print(Colors.RED + "File " + filename +
                  " skipped (title or artist missing)" + Colors.ENDC)
            continue

        print(title + " - " + artist + " | ", end="")

        # If tag or lyrics options are enabled
        if options["-a"] or options["-t"] or options["-l"]:
            tag_lyrics_total += 1

            # Search for the track to get infos
            searched_tracks = g.search(title + " " + artist)
            try:
                searched_track = next(searched_tracks)
                if searched_track is not None:
                    track = g.get_song(searched_track.id)
            except StopIteration:
                print(
                    Colors.RED +
                    "Could not be found on Genius" +
                    Colors.ENDC)
                continue

            # Tag
            if options["-a"] or options["-t"]:
                tags_confirmed = tag(options, audiofile, track)
                if not tags_confirmed:
                    continue
                if options["-a"] or options["-l"]:
                    print(" | ", end="")

            # Lyrics
            if options["-a"] or options["-l"]:
                if options["-o"]:
                    tag_lyrics_found = lyrics(
                        audiofile, lg, searched_track, tag_lyrics_found)
                else:
                    print(
                        Colors.ORANGE +
                        "Already existing lyrics skipped" +
                        Colors.ENDC,
                        end="")

            tag_lyrics_not_saved = save(audiofile, tag_lyrics_not_saved)
            if options["-a"] or options["-r"]:
                print(" | ", end="")

        if options["-a"] or options["-r"]:
            rename(audiofile)

        print()

    print_stats(options, tag_lyrics_total,
                tag_lyrics_found, tag_lyrics_not_saved)


def tag(options, audiofile, track):
    """
    Tag the audiofile.
    """
    # Check if needs to ask for confirmation
    if options["-c"]:
        # Old tags
        print(Colors.RED + "\n\tOLD: " + Colors.ENDC, end="")
        print((audiofile.tag.title if audiofile.tag.title is not None else "No title") + " | ", end="")
        print((audiofile.tag.artist if audiofile.tag.artist is not None else "No artist") + " | ", end="")
        print((audiofile.tag.album if audiofile.tag.album is not None else "No album") + " | ", end="")
        print(audiofile.tag.recording_date if audiofile.tag.recording_date is not None else "No recording date")
        # New tags
        print(Colors.GREEN + "\tNEW: " + Colors.ENDC, end="")
        print((track.title if track.title is not None else "No title") + " | ", end="")
        print(
            (track.artist.name if track.artist is not None else "No artist") + " | ", end="")
        print(
            (track.album.name if track.album is not None else "[Single]") + " | ", end="")
        print(
            track.release_date.year if track.release_date is not None else "No recording date")
        # Confirmation
        print(Colors.PURPLE + "\tSave new tags? " + Colors.ENDC, end="")
        confirmation = input()
        while(confirmation not in ["y", "n"]):
            print(
                Colors.PURPLE +
                "\tSave new tags? ('y' = yes, 'n' = no) " +
                Colors.ENDC,
                end="")
            confirmation = input()
        if confirmation == "n":
            print(Colors.ORANGE + "New tags discarded" + Colors.ENDC)
            return False

    # Set the main tags
    audiofile.tag.title = track.title
    audiofile.tag.artist = track.artist.name
    if track.release_date is not None:
        audiofile.tag.recording_date = eyed3.core.Date(
            track.release_date.year)
    if track.album is not None:
        audiofile.tag.album = track.album.name
    else:
        audiofile.tag.album = track.title + " - Single"

    # Find the cover art URL (either the album one or otherwise the track
    # one), download it and set it
    url = ""
    if track.album is not None:
        url = track.album.cover_art_url
    else:
        url = track.song_art_image_url
    request = urllib.request.Request(url=url, headers=HEADER)
    with urllib.request.urlopen(request).read() as imagedata:
        audiofile.tag.images.set(
            ImageFrame.FRONT_COVER, imagedata, "image/jpeg")

    print(Colors.GREEN + "Tags set" + Colors.ENDC, end="")
    return True


def lyrics(audiofile, lg, searched_track, tag_lyrics_found):
    """
    Add lyrics to the audiofiles.
    """
    lyrics_track = None
    # Search for the track to get lyrics (while true fixes the timeout error)
    while True:
        try:
            lyrics_track = lg.search_song(
                song_id=searched_track.id, get_full_info=False)
            break
        except BaseException:
            pass

    # Set the lyrics
    if lyrics_track is not None:
        tag_lyrics_found += 1
        lyrics = format_lyrics(lyrics_track.lyrics)
        audiofile.tag.lyrics.set(lyrics)
        print(Colors.GREEN + "Lyrics found" + Colors.ENDC, end="")
    else:
        audiofile.tag.lyrics.set("")
        print(Colors.RED + "No lyrics found" + Colors.ENDC, end="")

    return tag_lyrics_found


def rename(audiofile):
    """
    Rename the audiofiles.
    """
    # Rename the file
    try:
        audiofile.rename(audiofile.tag.title + " - " +
                         audiofile.tag.artist, preserve_file_time=True)
        print(Colors.GREEN + "Renamed" + Colors.ENDC, end="")
    except IOError:
        print(Colors.ORANGE + "No need to rename" + Colors.ENDC, end="")


def save(audiofile, tag_lyrics_not_saved):
    """
    Save the tags.
    """
    # Save the tags
    try:
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3, encoding='utf-8')
    # TagException is raised when an error while saving occurs
    except eyed3.id3.tag.TagException:
        tag_lyrics_not_saved += 1
        print(Colors.RED + "Could not save lyrics" + Colors.ENDC, end="")

    return tag_lyrics_not_saved


def check_args():
    """
    Check arguments.
    """
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and (
            sys.argv[1] == "-h" or sys.argv[1] == "-help")):
        print_help()


def print_help():
    """
    Print help message.
    """
    print(
        Colors.BOLD +
        "Usage:" +
        Colors.ENDC +
        "\n\tpy geniustagger.py <Genius access token> <tracks folder path> <options>")
    print(Colors.BOLD + "Options:" + Colors.ENDC +
          "\n\t-a : Apply all modifications: tags, lyrics, renaming" +
          "\n\t-t : Add tags" +
          "\n\t-l : Add lyrics" +
          "\n\t-r : Rename files" +
          "\n\t-o : Overwrite already existing lyrics" +
          "\n\t-s : Search for files recursively in sub-folders" +
          "\n\t-c : Ask for user confirmation before saving new tags" +
          "\n\t-h : Show help")
    print(Colors.BOLD + "Tip:" + Colors.ENDC +
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
    g = genius.Genius(access_token=access_token)
    lg = lyricsgenius.Genius(access_token=access_token,
                             verbose=False, remove_section_headers=True)

    # Path name
    pathname = sys.argv[2]
    if not pathname.endswith("\\"):
        pathname = pathname + "\\"
    if not os.path.isdir(pathname):
        print("Incorrect path name: " + pathname)

    # Check for options
    options = {"-a": False, "-o": False, "-t": False,
               "-l": False, "-r": False, "-s": False, "-c": False}
    for option in dict(options):
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "-h" or sys.argv[i] == "-help":
                print_help()
            if option == sys.argv[i]:
                options[option] = True

    # List of files
    if options["-s"]:
        files = Path(pathname).rglob("*.mp3")
    else:
        files = Path(pathname).glob("*.mp3")

    # Counters
    tag_lyrics_total = 0
    tag_lyrics_found = 0
    tag_lyrics_not_saved = 0

    return g, lg, files, options, tag_lyrics_total, tag_lyrics_found, tag_lyrics_not_saved


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


def format_lyrics(lyrics):
    """
    Format the lyrics (remove unwanted text).
    """
    lines = lyrics.split("\n")
    if len(lines) > 0:
        lines.pop(0)
    if len(lines) > 1:
        lines[len(lines) - 1] = re.sub("[0-9]+Embed",
                                       "", lines[len(lines) - 1])
    lyrics = "\n".join(lines)
    return lyrics


def print_stats(
        options,
        tag_lyrics_total,
        tag_lyrics_found,
        tag_lyrics_not_saved):
    """
    Print statistics.
    """
    print(Colors.PURPLE + Colors.BOLD +
          "\nGeniusLyrics | End" + Colors.ENDC)
    if options["-l"] and tag_lyrics_total > 0:
        lyrics_found_perc = (tag_lyrics_found -
                             tag_lyrics_not_saved) / tag_lyrics_total * 100
        lyrics_not_found_perc = (
            tag_lyrics_total - tag_lyrics_found) / tag_lyrics_total * 100
        lyrics_not_saved_perc = tag_lyrics_not_saved / tag_lyrics_total * 100
        print(Colors.BOLD + "\n" + str(tag_lyrics_total) +
              " lyrics searched" + Colors.ENDC)
        print(Colors.GREEN +
              f"{lyrics_found_perc:.2f} lyrics found and saved" + Colors.ENDC)
        print(Colors.ORANGE +
              f"{lyrics_not_found_perc:.2f} lyrics not found" + Colors.ENDC)
        print(
            Colors.RED +
            f"{lyrics_not_saved_perc:.2f} lyrics found but not saved" +
            Colors.ENDC)


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
