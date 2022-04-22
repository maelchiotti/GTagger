# GeniusLyrics

**GeniusLyrics** is a python utility that uses [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/index.html) to grab tracks lyrics from [Genius](https://genius.com/) and save them to `.mp3` files.

## Prerequesites

- Get a [Genius client ID](https://genius.com/api-clients) for lyricsgenius to work.
- Place all your tracks in a single folder.

## Usage

```bash
py geniuslyrics.py <Genius client ID> <tracks folder path> <options>
```

## Options

- `-o` : Overwrite already existing lyrics
