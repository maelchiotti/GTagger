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


# Pretend to be a request form a normal web brower, otherwise Genius doesn't allow downloading of cover arts
HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
          'AppleWebKit/537.11 (KHTML, like Gecko) '
          'Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}


def main():
    check_args()
    g, lg, files, options, tag_lyrics_total, tag_lyrics_found, tag_lyrics_not_saved = init()
    print(colors.PURPLE + colors.BOLD + "GeniusLyrics | Start\n" + colors.ENDC)

    for filename in files:
        audiofile = eyed3.load(filename)
        title = audiofile.tag.title
        artist = split_artist(audiofile)
        if(title == None or artist == None):
            print(colors.RED + "File " + filename +
                  " skipped (title or artist missing)" + colors.ENDC)
            continue

        print(title + " - " + artist + " | ", end="")

        # If tag or lyrics options are enabled
        if(options["-a"] or options["-t"] or options["-l"]):
            tag_lyrics_total += 1

            # Search for the track to get infos
            searched_tracks = g.search(title + " " + artist)
            try:
                searched_track = next(searched_tracks)
                if(searched_track != None):
                    track = g.get_song(searched_track.id)
            except StopIteration:
                print(colors.RED + "Could not be found on Genius" + colors.ENDC)
                continue

            # Tag
            if(options["-a"] or options["-t"]):
                tags_confirmed = tag(options, audiofile, track)
                if(not tags_confirmed):
                    continue
                if(options["-a"] or options["-l"]):
                    print(" | ", end="")

            # Lyrics
            if(options["-a"] or options["-l"]):
                if(options["-o"] == True):
                    tag_lyrics_found = lyrics(
                        audiofile, lg, searched_track, tag_lyrics_found)
                else:
                    print(
                        colors.ORANGE + "Already existing lyrics skipped" + colors.ENDC, end="")

            save(audiofile)
            if(options["-a"] or options["-r"]):
                print(" | ", end="")

        if(options["-a"] or options["-r"]):
            rename(audiofile)

        print()

    print_stats(options, tag_lyrics_total,
                tag_lyrics_found, tag_lyrics_not_saved)


# Tag the audiofiles
def tag(options, audiofile, track):
    # Check if needs to ask for confirmation
    if(options["-c"]):
        # Old tags
        print(colors.RED + "\n\tOLD: " + colors.ENDC, end="")
        print((audiofile.tag.title if audiofile.tag.title !=
              None else "No title") + " | ", end="")
        print((audiofile.tag.artist if audiofile.tag.artist !=
              None else "No artist") + " | ", end="")
        print((audiofile.tag.album if audiofile.tag.album !=
              None else "No album") + " | ", end="")
        print(audiofile.tag.recording_date if audiofile.tag.recording_date !=
              None else "No recording date")
        # New tags
        print(colors.GREEN + "\tNEW: " + colors.ENDC, end="")
        print((track.title if track.title != None else "No title") + " | ", end="")
        print((track.artist.name if track.artist !=
              None else "No artist") + " | ", end="")
        print((track.album.name if track.album !=
              None else "[Single]") + " | ", end="")
        print(track.release_date.year if track.release_date !=
              None else "No recording date")
        # Confirmation
        print(colors.PURPLE + "\tSave new tags? " + colors.ENDC, end="")
        confirmation = input()
        while(confirmation != "y" and confirmation != "n"):
            print(colors.PURPLE +
                  "\tSave new tags? ('y' = yes, 'n' = no) " + colors.ENDC, end="")
            confirmation = input()
        if(confirmation == "n"):
            print(colors.ORANGE + "New tags discarded" + colors.ENDC)
            return False

    # Set the main tags
    audiofile.tag.title = track.title
    audiofile.tag.artist = track.artist.name
    if(track.release_date != None):
        audiofile.tag.recording_date = eyed3.core.Date(
            track.release_date.year)
    if(track.album != None):
        audiofile.tag.album = track.album.name
    else:
        audiofile.tag.album = track.title + " - Single"

    # Find the cover art URL (either the album one or otherwise the track one), download it and set it
    url = ""
    if(track.album != None):
        url = track.album.cover_art_url
    else:
        url = track.song_art_image_url
    request = urllib.request.Request(url=url, headers=HEADER)
    imagedata = urllib.request.urlopen(request).read()
    audiofile.tag.images.set(
        ImageFrame.FRONT_COVER, imagedata, "image/jpeg")

    print(colors.GREEN + "Tags set" + colors.ENDC, end="")
    return True


# Add lyrics to the audiofiles
def lyrics(audiofile, lg, searched_track, tag_lyrics_found):
    lyrics_track = None
    # Search for the track to get lyrics (while true fixes the timeout error)
    while True:
        try:
            lyrics_track = lg.search_song(
                song_id=searched_track.id, get_full_info=False)
            break
        except:
            pass

    # Set the lyrics
    if(lyrics_track != None):
        tag_lyrics_found += 1
        lyrics = format_lyrics(lyrics_track.lyrics)
        audiofile.tag.lyrics.set(lyrics)
        print(colors.GREEN + "Lyrics found" + colors.ENDC, end="")
    else:
        audiofile.tag.lyrics.set("")
        print(colors.RED + "No lyrics found" + colors.ENDC, end="")

    return tag_lyrics_found


# Rename the audiofiles
def rename(audiofile):
    # Rename the file
    try:
        audiofile.rename(audiofile.tag.title + " - " +
                         audiofile.tag.artist, preserve_file_time=True)
        print(colors.GREEN + "Renamed" + colors.ENDC, end="")
    except IOError:
        print(colors.ORANGE + "No need to rename" + colors.ENDC, end="")
        pass


# Save the tags
def save(audiofile):
    # Save the tags
    try:
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3, encoding='utf-8')
    # TagException is raised when an error while saving occurs
    except eyed3.id3.tag.TagException:
        tag_lyrics_not_saved += 1
        print(colors.RED + "Could not save lyrics" + colors.ENDC, end="")
        pass


# Check arguments
def check_args():
    if(len(sys.argv) == 1 or (len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"))):
        print_help()


# Print help message
def print_help():
    print(colors.BOLD +
          "Usage:" + colors.ENDC + "\n\tpy geniustagger.py <Genius access token> <tracks folder path> <options>")
    print(colors.BOLD + "Options:" + colors.ENDC +
          "\n\t-a : Apply all modifications: tags, lyrics, renaming" +
          "\n\t-t : Add tags" +
          "\n\t-l : Add lyrics" +
          "\n\t-r : Rename files" +
          "\n\t-o : Overwrite already existing lyrics" +
          "\n\t-s : Search for files recursively in sub-folders" +
          "\n\t-c : Ask for user confirmation before saving new tags" +
          "\n\t-h : Show help")
    print(colors.BOLD + "Tip:" + colors.ENDC +
          "\n\tGet your Genius access token at https://genius.com/api-clients")
    exit(1)


# Initialize variables
def init():
    # Access token and
    access_token = sys.argv[1]
    search = re.search("[^a-zA-Z0-9_-]", access_token)
    if(search != None):
        print("Incorrect access token")
        print_help()

    # genius and lyricsgenius instances
    g = genius.Genius(access_token=access_token)
    lg = lyricsgenius.Genius(access_token=access_token,
                             verbose=False, remove_section_headers=True)

    # Path name
    pathname = sys.argv[2]
    if(not pathname.endswith("\\")):
        pathname = pathname + "\\"
    if(not os.path.isdir(pathname)):
        print("Incorrect path name: " + pathname)

    # Check for options
    options = {"-a": False, "-o": False, "-t": False,
               "-l": False, "-r": False, "-s": False, "-c": False}
    for option in options.keys():
        for i in range(3, len(sys.argv)):
            if(sys.argv[i] == "-h" or sys.argv[i] == "-help"):
                print_help()
            if option == sys.argv[i]:
                options[option] = True

    # List of files
    if(options["-s"]):
        files = Path(pathname).rglob("*.mp3")
    else:
        files = Path(pathname).glob("*.mp3")

    # Counters
    tag_lyrics_total = 0
    tag_lyrics_found = 0
    tag_lyrics_not_saved = 0

    return g, lg, files, options, tag_lyrics_total, tag_lyrics_found, tag_lyrics_not_saved


# Split the artist name if it contains multiple artists, keeping only the first (and supposedly the main) one
def split_artist(audiofile):
    # Initialize the artist if it exists
    if(audiofile.tag.artist == None):
        return None
    else:
        artist = audiofile.tag.artist

    # Search for splitters and split
    splitters = [" featuring ", " feat. ",
                 " feat ", " ft. ", " ft ", " & ", " / "]
    for splitter in splitters:
        if splitter in audiofile.tag.artist:
            artist = audiofile.tag.artist.split(splitter)[0]
            break

    return artist


# Format the lyrics (remove unwanted text)
def format_lyrics(lyrics):
    lines = lyrics.split("\n")
    if(len(lines) > 0):
        lines.pop(0)
    if(len(lines) > 1):
        lines[len(lines) - 1] = re.sub("[0-9]+Embed",
                                       "", lines[len(lines) - 1])
    lyrics = "\n".join(lines)
    return lyrics


# Print statistics
def print_stats(options, tag_lyrics_total, tag_lyrics_found, tag_lyrics_not_saved):
    print(colors.PURPLE + colors.BOLD +
          "\nGeniusLyrics | End" + colors.ENDC)
    if(options["-l"] and tag_lyrics_total > 0):
        lyrics_found_perc = (tag_lyrics_found -
                             tag_lyrics_not_saved) / tag_lyrics_total * 100
        lyrics_not_found_perc = (
            tag_lyrics_total - tag_lyrics_found) / tag_lyrics_total * 100
        lyrics_not_saved_perc = tag_lyrics_not_saved / tag_lyrics_total * 100
        print(colors.BOLD + "\n" + str(tag_lyrics_total) +
              " lyrics searched" + colors.ENDC)
        print(colors.GREEN + "%.2f%% lyrics found and saved" %
              lyrics_found_perc + colors.ENDC)
        print(colors.ORANGE + "%.2f%% lyrics not found" %
              lyrics_not_found_perc + colors.ENDC)
        print(colors.RED + "%.2f%% lyrics found but not saved" %
              lyrics_not_saved_perc + colors.ENDC)


# Output colors
class colors:
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


if __name__ == "__main__":
    main()
