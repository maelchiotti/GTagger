# GeniusTagger

**GeniusTagger** is a python tool that searches for tracks information on [Genius](https://genius.com/) and saves them to `.mp3` files.

## Features

- **Add main tags** (artist, album, release date, cover art) thanks to [wrap-genius](https://github.com/fedecalendino/wrap-genius)
- **Add lyrics** thanks to [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html)
- **Rename files** following the pattern `Title - Artist.mp3`

## Usage

- Get a [Genius access token](https://genius.com/api-clients) (needed for the API)
- Use the following command (arguments ending with a `*` are mandatory)

```bash
py geniustagger.py <Genius access token*> <tracks folder path*> <options>
```

## Options

Options must be separated by a space.

- `-a` : Apply <u>a</u>ll modifications: tags, lyrics, renaming
- `-t` : Add <u>t</u>ags
- `-l` : Add <u>l</u>yrics
- `-r` : <u>R</u>ename files
- `-o` : <u>O</u>verwrite already existing lyrics
- `-s` : Search for files recursively in <u>s</u>ub-folders
- `-c` : Ask for user <u>c</u>onfirmation before saving new tags
- `-h` : Show <u>h</u>elp

## TODO

- Allow theuser to only add cover arts
- Allow the user to choose a custom renaming pattern
- Add a confirmation step so the user can also check the lyrics and the renaming
