from importlib.resources import path
import os
import sys
import re
import glob
import eyed3
import lyricsgenius


# Output colors
class colors:
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


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


def main():
    print(colors.PURPLE + colors.BOLD + "GeniusLyrics | Start\n" + colors.ENDC)

    # Check number of arguments
    if(len(sys.argv) < 3):
        print(colors.BOLD +
              "Usage:" + colors.ENDC + "\n\tpy geniuslyrics.py <Genius client ID> <tracks folder path> <options>")
        print(colors.BOLD + "Options:" + colors.ENDC +
              "\n\t-o\tOverwrite already existing lyrics")
        exit(-1)

    # Client ID and Genius instance
    clientID = sys.argv[1]
    search = re.search("[^a-zA-Z0-9_]", clientID)
    if(search != None):
        print("Incorrect client ID: ")
        print(search)
        exit(-1)
    genius = lyricsgenius.Genius(clientID)
    genius.verbose = False
    genius.remove_section_headers = True

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

        # Look for the track (while true to fix the timeout error)
        while True:
            try:
                track = genius.search_song(title, artist)
                break
            except:
                pass

        # Set the lyrics
        try:
            lyrics = format_lyrics(track.lyrics)
            audiofile.tag.lyrics.set(lyrics)
            lyrics_found += 1
            print(colors.GREEN + "Lyrics found for \"" +
                  title + "\" by " + artist + colors.ENDC)
        # AttributeError is raised if the track does not contain lyrics because they weren't found
        except AttributeError:
            audiofile.tag.lyrics.set("")
            print(colors.ORANGE + "No lyrics found for \"" +
                  title + "\" by " + artist + colors.ENDC)
        finally:
            # Save the lyrics
            try:
                audiofile.tag.save(
                    version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')
            # TagException is raised when an error while saving occurs
            except eyed3.id3.tag.TagException:
                lyrics_not_saved += 1
                print(colors.RED + "Lyrics could not be saved for \"" +
                      title + "\" by " + artist + colors.ENDC)
                continue

    # Statistics
    lyrics_found_perc = (lyrics_found - lyrics_not_saved) / lyrics_total * \
        100 if (lyrics_total > 0) else "-"
    lyrics_not_found_perc = (lyrics_total - lyrics_found) / \
        lyrics_total * 100 if (lyrics_total > 0) else "-"
    lyrics_not_saved_perc = lyrics_not_saved / \
        lyrics_total * 100 if (lyrics_total > 0) else "-"
    print(colors.PURPLE + colors.BOLD + "\nGeniusLyrics | End\n" + colors.ENDC)
    print(colors.BOLD + str(lyrics_total) + " lyrics searched" + colors.ENDC)
    print(colors.GREEN + "%.2f%% lyrics found and saved" %
          lyrics_found_perc + colors.ENDC)
    print(colors.ORANGE + "%.2f%% lyrics not found" %
          lyrics_not_found_perc + colors.ENDC)
    print(colors.RED + "%.2f%% lyrics found but not saved" %
          lyrics_not_saved_perc + colors.ENDC)


if __name__ == "__main__":
    main()
