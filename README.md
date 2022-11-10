# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.flac` and `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track and its lyrics based on its title and artist.

To avoid any issue with your files, please back them up before using GTagger.

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
  python gtagger.py
  ```

## TODO

**Future:**

- Improve performance of the following actions when a lot of files are opened. When using `Ctrl+A`, This will allow to enable the reset button only if at least one track has new lyrics.
  - Changing mode
  - (De)selecting track layouts
- Re-implement the [light theme](https://github.com/maelchiotti/GTagger/tree/light_theme)
