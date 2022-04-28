# GeniusTagger

**GeniusTagger** is a python tool that searches for tracks information on [Genius](https://genius.com/) and saves them to `.mp3` files.

## Features

- **Add main tags** (artist, album, release date, cover art) thanks to [wrap-genius](https://github.com/fedecalendino/wrap-genius)
- **Add lyrics** thanks to [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html)
- **Rename files** following the pattern `Title - Artist.mp3`

## Prerequesites

- Get a [Genius access token](https://genius.com/api-clients) (needed for the API calls)
- Place all your files in a single folder (it does not look for files in sub-folders)

## Usage

Arguments ending with a `*` or mandatory.

```bash
py geniustagger.py <Genius access token*> <tracks folder path*> <options>
```

## Options

Options must be separated by a space.

- `-t` : Add tags
- `-l` : Add lyrics
- `-r` : Rename files
- `-o` : Overwrite already existing lyrics
- `-h` : Show help

## TODO

- Add an option to search for files in sub-folders
- Allow user to choose a custom renaming pattern
- Add a confirmation step so the user can chek informations
