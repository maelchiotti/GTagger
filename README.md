# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track's Genius ID based on its title and artist, and [LyricsGenius](https://github.com/johnwmillr/LyricsGenius) to fetch the lyrics automatically.

## WIP

GTagger is a work in progress, so it lacks functionnalities and it may be buggy. To avoid any issue with your files, please backup them first.

## Usage

### On Windows

Download the executable `GTagger.exe` from the [Releases](https://github.com/maelchiotti/GTagger/releases) and execute it.

### From source

- Install the required dependencies:

  ```shell
  pip install -r requirements.txt
  ```

- Launch GTagger with the following command:

  ```shell
  py gtagger.py
  ```

## TODO

**v1.2.0:**

- ?

**Future:**

- Support more file types (AAC and FLAC especially)
- Re-implement the [light theme](https://github.com/maelchiotti/GTagger/tree/light_theme)
- Fix the width issue when lyrics contain a very, very long line (which should be very unusual though)
