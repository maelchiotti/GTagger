<div align="center">
  <img src="src/img/logo_large_white.png" height="100px" style="margin:10px 10px 0px 0px" alt="Logo Python">
  <br /><br />
</div>

GTagger is a python tool that adds lyrics from [Genius](https://genius.com/) to `.flac` and `.mp3` files.

![Screenshot of the main window](docs/gtagger.png)

It uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) to find the track and its lyrics based on its title and artist.

To avoid any issue with your files, please back them up before using GTagger.

## Use

All downloads are available in the [Releases](https://github.com/maelchiotti/GTagger/releases).

### On Windows

- Portable : download and run `GTagger.portable.exe`.
- Install : download and run `GTagger.setup.exe`.

### On Linux

- Portable : download and run `GTagger.portable`.
- Install : not yet available.

### From source

- Install the required dependencies:

  ```shell
  pip3 install -r requirements.txt -U
  ```

- Launch GTagger:

  ```shell
  python gtagger.py
  ```

### Contribute

Pull requests are welcome. Please make sure you follow the guidelines from [QUALITY.md](QUALITY.md).
