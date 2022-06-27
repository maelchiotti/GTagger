# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.mp3` files.

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track's Genius ID based on its title and artist, and [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html) to fetch the lyrics automatically.

## WIP

GTagger is a work in progress, so it lacks functionnalities and it may be buggy. To avoid any issue with your files, please backup them first.

## Usage

- Install the required dependencies:

    ```shell
    pip install wrap-genius lyricsgenius eyed3 qtawesome PySide6
    ```

- Launch GTagger with the following command:

    ```shell
    py main.py
    ```

**TODO:**

- Save the lyrics
- Option to ignore files with lyrics
- When using cancel, only remove lyrics if it's added lyrics and not original lyrics
