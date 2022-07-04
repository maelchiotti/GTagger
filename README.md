# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track's Genius ID based on its title and artist, and [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html) to fetch the lyrics automatically.

## WIP

GTagger is a work in progress, so it lacks functionnalities and it may be buggy. To avoid any issue with your files, please backup them first.

## Usage

### On Windows

Download the executable `gtagger.exe` from the [Releases](https://github.com/maelchiotti/GTagger/releases) and execute it.

### From source

- Install the required dependencies:

    ```shell
    pip install wrap-genius lyricsgenius eyed3 qtawesome PySide6
    ```

- Launch GTagger with the following command:

    ```shell
    py main.py
    ```

## TODO

- Use a GridLayout and QFrames to display the songs in a prettier way

- Toggle the save lyrics button automatically

- Improve the settings window to be a `QtCore.Qt.Tool` so that it keeps focus

- Add options:
  - Ignore files with lyrics
