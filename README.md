# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track and its lyrics based on its title and artist.

To avoid any issue with your files, please backup them before using GTagger.

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

- Update source paths in .spec
- Add progression bar for saving
- Keep status color and lyrics color when changing mode
- Disable add buttons while adding files

**Future:**

- Support more file types (AAC and FLAC especially)
- Re-implement the [light theme](https://github.com/maelchiotti/GTagger/tree/light_theme)
