import os
import sys
import re
import glob
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
    g, lg, pathname, options, lyrics_total, lyrics_found, lyrics_not_saved = init()
    print(colors.PURPLE + colors.BOLD + "GeniusLyrics | Start\n" + colors.ENDC)

    for filename in glob.glob(pathname + "*.mp3"):
        audiofile = eyed3.load(filename)

        # Check if lyrics must not be overwritten
        if(options["-o"] == False and len(audiofile.tag.lyrics) > 0):
            print(colors.ORANGE + "The file " + filename +
                  " was skipped: it already has lyrics and the overwrite option (-o) is not enabled" + colors.ENDC)
            continue

        title = audiofile.tag.title
        artist = audiofile.tag.artist
        if(title == None or artist == None):
            print(colors.RED + "The file " + filename +
                  " was skipped: it's missing its title or artist" + colors.ENDC)
            continue

        lyrics_total += 1

        # Split the artist name if it contains multiple artists, keeping only the first (and supposedly the main) one
        splitters = [" featuring ", " feat. ",
                     " feat ", " ft. ", " ft ", " & ", " / "]
        for splitter in splitters:
            if splitter in artist:
                artist = artist.split(splitter)[0]
                break

        # Search for the track and its lyrics
        ltrack = None
        searched_tracks = g.search(title + " " + artist)
        try:
            searched_track = next(searched_tracks)
            if(searched_track != None):
                track = g.get_song(searched_track.id)
                if(track != None):
                    ltrack = lg.search_song(
                        song_id=searched_track.id, get_full_info=False)
        except StopIteration:
            print(colors.RED + "The track \"" +
                  title + "\" by " + artist + " could not be found on Genius" + colors.ENDC)
            continue

        if(ltrack != None):
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

            # Set the lyrics
            lyrics = format_lyrics(ltrack.lyrics)
            audiofile.tag.lyrics.set(lyrics)
            lyrics_found += 1
            print(colors.GREEN + "Lyrics found for \"" +
                  title + "\" by " + artist + colors.ENDC)

            # Save the tags
            try:
                audiofile.tag.save(
                    version=eyed3.id3.ID3_V2_3, encoding='utf-8')

            # TagException is raised when an error while saving occurs
            except eyed3.id3.tag.TagException:
                lyrics_not_saved += 1
                print(colors.RED + "Lyrics could not be saved for \"" +
                      title + "\" by " + artist + colors.ENDC)
                pass

            # Rename the file
            try:
                audiofile.rename(audiofile.tag.title + " - " +
                                 audiofile.tag.artist, preserve_file_time=True)
            except IOError:
                pass

        else:
            audiofile.tag.lyrics.set("")
            print(colors.ORANGE + "No lyrics found for \"" +
                  title + "\" by " + artist + colors.ENDC)

    print_stats(lyrics_total, lyrics_found, lyrics_not_saved)


# Check arguments
def check_args():
    if(len(sys.argv) < 3):
        print_help()


# Print help message
def print_help():
    print(colors.BOLD +
          "Usage:" + colors.ENDC + "\n\tpy geniuslyrics.py <Genius access token> <tracks folder path> <options>")
    print(colors.BOLD + "Options:" + colors.ENDC +
          "\n\t-o : Overwrite already existing lyrics")
    print(colors.BOLD + "Tip:" + colors.ENDC +
          "\n\tGet your Genius access token at https://genius.com/api-clients")
    exit(-1)


# Initialize variables
def init():
    # Access token and
    access_token = sys.argv[1]
    search = re.search("[^a-zA-Z0-9_]", access_token)
    if(search != None):
        print("Incorrect access token")
        print_help()

    # genius and lyricsgenius instances
    g = genius.Genius(access_token=access_token)
    lg = lyricsgenius.Genius(
        access_token=access_token, verbose=False, remove_section_headers=True)

    # Path name
    pathname = sys.argv[2]
    if(not pathname.endswith("\\")):
        pathname = pathname + "\\"
    if(not os.path.isdir(pathname)):
        print("Incorrect path name: " + pathname)

    # Check for options
    options = {"-o": False}
    for option in options.keys():
        for i in range(3, len(sys.argv)):
            if option == sys.argv[i]:
                options[option] = True

    # Counters
    lyrics_total = 0
    lyrics_found = 0
    lyrics_not_saved = 0

    return g, lg, pathname, options, lyrics_total, lyrics_found, lyrics_not_saved


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
def print_stats(lyrics_total, lyrics_found, lyrics_not_saved):
    print(colors.PURPLE + colors.BOLD +
          "\nGeniusLyrics | End\n" + colors.ENDC)
    if(lyrics_total > 0):
        lyrics_found_perc = (
            lyrics_found - lyrics_not_saved) / lyrics_total * 100
        lyrics_not_found_perc = (
            lyrics_total - lyrics_found) / lyrics_total * 100
        lyrics_not_saved_perc = lyrics_not_saved / lyrics_total * 100
        print(colors.BOLD + str(lyrics_total) +
              " lyrics searched" + colors.ENDC)
        print(colors.GREEN + "%.2f%% lyrics found and saved" %
              lyrics_found_perc + colors.ENDC)
        print(colors.ORANGE + "%.2f%% lyrics not found" %
              lyrics_not_found_perc + colors.ENDC)
        print(colors.RED + "%.2f%% lyrics found but not saved" %
              lyrics_not_saved_perc + colors.ENDC)
    else:
        print(colors.BOLD + "No lyrics searched" + colors.ENDC)


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
