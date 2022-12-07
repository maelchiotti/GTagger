# GTagger

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.flac` and `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track and its lyrics based on its title and artist.

To avoid any issue with your files, please back them up before using GTagger.

## Use

### On Windows

Download the latest version of the executable `GTagger.exe` from the [Releases](https://github.com/maelchiotti/GTagger/releases) and execute it.

### From source

- Install the required dependencies:

  ```shell
  pip install -r requirements.txt
  ```

- Launch GTagger:

  ```shell
  python gtagger.py
  ```

### Contribute

Pull requests are welcome. A list of planned improvements is available in [TODO.md](TODO.md). Please make sure you follow the guidelines in [QUALITY.md](QUALITY.md).
