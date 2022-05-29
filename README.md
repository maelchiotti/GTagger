# GeniusLyrics

GeniusLyrics is a python tool that adds lyrics from [Genius](https://genius.com/) to `.mp3` files.

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the tracks' Genius ID based on its title and artist, and [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html) to fetch the lyrics automatically.

## Usage

- Install the required dependencies:

    ```shell
    pip install wrap-genius lyricsgenius eyed3
    ```

- Get a [Genius access token](https://genius.com/api-clients) (needed for the API)

- Use the following command (arguments ending with a `*` are mandatory):

    ```shell
    geniuslyrics.py <Genius access token*> <tracks folder path*> <options>
    ```

## Options

Options must be separated by a space.

- `-s` : Search for files recursively in sub-folders
- `-o` : Overwrite already existing lyrics
- `-h` : Show help

## WIP

`geniustagger.py` is a work in progress to automatically add tags to `.mp3` files (mainly artist, album, release date and cover art) and rename them (following the pattern *Title - Artist.mp3*).
